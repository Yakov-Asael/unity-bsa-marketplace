import os
import sys
import json
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from common import load_policy  # noqa: E402
from scan import BLOCK, WARN, scan  # noqa: E402

POLICY = load_policy()

GOOD_FLOW = """<?xml version="1.0" encoding="UTF-8"?>
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">
    <description>Sets the credit status when the credit limit changes.</description>
    <label>Account - After Update - Set Credit Status</label>
    <processType>AutoLaunchedFlow</processType>
    <status>Draft</status>
    <recordUpdates>
        <name>Update_Account</name>
        <faultConnector><targetReference>Log_Error</targetReference></faultConnector>
    </recordUpdates>
    <subflows>
        <name>Log_Error</name>
        <flowName>Subflow_Log_Error</flowName>
        <inputAssignments><name>txtErrorMessage</name></inputAssignments>
        <inputAssignments><name>txtFlowName</name></inputAssignments>
        <inputAssignments><name>txtRecordId</name></inputAssignments>
    </subflows>
</Flow>"""

GOOD_FIELD = """<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Credit_Check_Status__c</fullName>
    <description>Latest credit check outcome, set by the credit flow.</description>
    <inlineHelpText>Result of the most recent credit check.</inlineHelpText>
    <label>Credit Check Status</label>
    <type>Picklist</type>
</CustomField>"""


def rules(findings, level=None):
    return sorted(finding.rule for finding in findings if level is None or finding.level == level)


class FlowScanTest(unittest.TestCase):
    def test_good_flow_passes_clean(self):
        self.assertEqual(scan(GOOD_FLOW, POLICY), [])

    def test_active_flow_blocks(self):
        findings = scan(GOOD_FLOW.replace("<status>Draft</status>", "<status>Active</status>"), POLICY)
        self.assertEqual(rules(findings, BLOCK), ["B8"])

    def test_missing_fault_path_blocks(self):
        xml = GOOD_FLOW.replace("<faultConnector><targetReference>Log_Error</targetReference></faultConnector>", "")
        self.assertIn("ZT2", rules(scan(xml, POLICY), BLOCK))

    def test_fault_path_to_other_element_blocks(self):
        xml = GOOD_FLOW.replace("<targetReference>Log_Error</targetReference>", "<targetReference>Send_Email</targetReference>")
        self.assertIn("B22", rules(scan(xml, POLICY), BLOCK))

    def test_error_call_missing_inputs_warns(self):
        xml = GOOD_FLOW.replace("<inputAssignments><name>txtRecordId</name></inputAssignments>", "")
        self.assertEqual(rules(scan(xml, POLICY), WARN), ["B22"])

    def test_missing_description_blocks(self):
        xml = GOOD_FLOW.replace("<description>Sets the credit status when the credit limit changes.</description>", "")
        self.assertEqual(rules(scan(xml, POLICY), BLOCK), ["A4"])

    def test_label_off_pattern_warns(self):
        xml = GOOD_FLOW.replace("Account - After Update - Set Credit Status", "Set credit status")
        self.assertEqual(rules(scan(xml, POLICY), WARN), ["A5"])

    def test_workflow_process_type_blocks(self):
        xml = GOOD_FLOW.replace("AutoLaunchedFlow", "Workflow")
        self.assertIn("B21", rules(scan(xml, POLICY), BLOCK))

    def test_hardcoded_id_blocks(self):
        xml = GOOD_FLOW.replace("</description>", " Owner 00G1a000003AbCdEAF.</description>")
        self.assertEqual(rules(scan(xml, POLICY), BLOCK), ["B4"])

    def test_tooling_json_flow_is_scanned(self):
        payload = {"FullName": "Account_Credit", "Metadata": {
            "processType": "AutoLaunchedFlow", "status": "Active", "description": "x",
            "label": "Account - After Update - Credit"}}
        self.assertEqual(rules(scan(json.dumps(payload), POLICY), BLOCK), ["B8"])

    def test_record_id_key_is_not_a_hardcoded_id(self):
        payload = {"Id": "3011a000000AbCdEAF", "Metadata": {"processType": "AutoLaunchedFlow", "status": "Draft",
                                                            "description": "x", "label": "A - B - C"}}
        self.assertEqual(scan(payload, POLICY), [])


class FieldScanTest(unittest.TestCase):
    def test_good_field_passes_clean(self):
        self.assertEqual(scan(GOOD_FIELD, POLICY), [])

    def test_missing_description_blocks_and_help_text_warns(self):
        xml = GOOD_FIELD.replace("<description>Latest credit check outcome, set by the credit flow.</description>", "")
        xml = xml.replace("<inlineHelpText>Result of the most recent credit check.</inlineHelpText>", "")
        findings = scan(xml, POLICY)
        self.assertEqual(rules(findings, BLOCK), ["A4"])
        self.assertEqual(rules(findings, WARN), ["A4"])

    def test_non_snake_case_api_name_warns(self):
        xml = GOOD_FIELD.replace("Credit_Check_Status__c", "creditcheckstatus__c")
        self.assertEqual(rules(scan(xml, POLICY), WARN), ["A5"])

    def test_tooling_json_field_uses_parent_full_name(self):
        payload = {"FullName": "Account.Credit_Check_Status__c",
                   "Metadata": {"type": "Picklist", "label": "Credit Check Status", "description": "x", "inlineHelpText": "y"}}
        self.assertEqual(scan(payload, POLICY), [])


class ForbiddenTypeTest(unittest.TestCase):
    def test_apex_class_blocks(self):
        self.assertEqual(rules(scan("<ApexClass><apiVersion>65.0</apiVersion></ApexClass>", POLICY), BLOCK), ["B19"])

    def test_metadata_type_argument_blocks(self):
        self.assertEqual(rules(scan({}, POLICY, metadata_type="ApexTrigger"), BLOCK), ["B19"])

    def test_tooling_url_blocks(self):
        self.assertEqual(rules(scan({}, POLICY, url="/services/data/v66.0/tooling/sobjects/ApexClass"), BLOCK), ["B19"])

    def test_headless_body_type_blocks(self):
        body = {"type": "ApexClass", "fullName": "Foo", "xmlRep": "<ApexClass><apiVersion>66.0</apiVersion></ApexClass>"}
        self.assertEqual(rules(scan(body, POLICY), BLOCK), ["B19"])

    def test_headless_field_envelope_is_scanned(self):
        xml_rep = GOOD_FIELD.replace("CustomField", "fields").replace("<description>Latest credit check outcome, set by the credit flow.</description>", "")
        body = {"type": "CustomField", "fullName": "Account.Credit_Check_Status__c",
                "xmlRep": f'<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">{xml_rep}</CustomObject>'}
        self.assertEqual(rules(scan(body, POLICY), BLOCK), ["A4"])

    def test_before_save_update_needs_no_fault_path(self):
        xml = GOOD_FLOW.replace("<faultConnector><targetReference>Log_Error</targetReference></faultConnector>", "")
        xml = xml.replace("<status>Draft</status>", "<status>Draft</status><start><triggerType>RecordBeforeSave</triggerType></start>")
        self.assertEqual(scan(xml, POLICY), [])

    def test_profile_layout_assignment_only_is_allowed(self):
        body = {"type": "Profile", "fullName": "Custom Sales",
                "xmlRep": "<Profile><layoutAssignments><layout>Account-Account Layout</layout></layoutAssignments></Profile>"}
        self.assertEqual(scan(body, POLICY), [])

    def test_profile_with_permissions_blocks(self):
        body = {"type": "Profile", "fullName": "Custom Sales",
                "xmlRep": "<Profile><layoutAssignments><layout>A-B</layout></layoutAssignments>"
                          "<fieldPermissions><field>Account.X__c</field></fieldPermissions></Profile>"}
        self.assertEqual(rules(scan(body, POLICY), BLOCK), ["B19"])

    def test_profile_blocks(self):
        self.assertEqual(rules(scan("<Profile><custom>true</custom></Profile>", POLICY), BLOCK), ["B19"])


if __name__ == "__main__":
    unittest.main()
