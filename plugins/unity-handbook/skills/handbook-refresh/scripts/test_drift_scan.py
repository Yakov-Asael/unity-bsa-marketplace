import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import drift_scan  # noqa: E402

ROOT = "unpackaged/main/default"
OLD_DATE = "2026-08-01T12:00:00"
NEW_DATE = "2026-09-01T12:00:00"


def git(repo, *args, date=OLD_DATE):
    env = {**os.environ, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
    subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, env=env)


def write(repo, relative, text):
    path = os.path.join(repo, ROOT, relative)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def claim(**overrides):
    base = {"id": "c1", "tab": "dispute", "type": "flow", "name": "Dispute_Flow", "verified_on": "2026-08-10"}
    return {**base, **overrides}


class DriftScanTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = self.tmp.name
        git(self.repo, "init", "-q", "-b", "Production")
        git(self.repo, "config", "user.email", "t@example.com")
        git(self.repo, "config", "user.name", "t")
        write(self.repo, "flows/Dispute_Flow.flow-meta.xml", "<status>Active</status><value>50000</value>")
        write(self.repo, "customPermissions/Fraud_Approver.customPermission-meta.xml", "<label>x</label>")
        write(self.repo, "workflows/Account.workflow-meta.xml", "<alerts><fullName>Credit_Alert</fullName></alerts>")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "snapshot")
        self.scanner = drift_scan.Repo(self.repo, "Production")

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, **overrides):
        return drift_scan.check_claim(self.scanner, claim(**overrides), ROOT)

    def test_unchanged_claim_has_no_findings(self):
        self.assertEqual(self.check(active=True, contains=[r"<value>50000</value>"]), [])

    def test_inactive_flow_is_state_changed(self):
        kinds = [f.kind for f in self.check(active=False)]
        self.assertEqual(kinds, ["STATE_CHANGED"])

    def test_missing_threshold_is_value_changed(self):
        kinds = [f.kind for f in self.check(contains=[r"<value>25000</value>"])]
        self.assertEqual(kinds, ["VALUE_CHANGED"])

    def test_edit_after_verified_date_is_changed_since(self):
        write(self.repo, "flows/Dispute_Flow.flow-meta.xml", "<status>Active</status><value>60000</value>")
        git(self.repo, "commit", "-q", "-am", "raise threshold", date=NEW_DATE)
        findings = self.check()
        self.assertEqual([f.kind for f in findings], ["CHANGED_SINCE"])
        self.assertIn("raise threshold", findings[0].commits[0])
        self.assertTrue(any("60000" in value for value in findings[0].added))

    def test_version_only_edit_is_not_reported(self):
        write(self.repo, "flows/Dispute_Flow.flow-meta.xml", "<apiVersion>62.0</apiVersion>\n<status>Active</status><value>50000</value>")
        git(self.repo, "commit", "-q", "-am", "bump api version", date=NEW_DATE)
        self.assertEqual(self.check(), [])

    def test_reordered_elements_are_not_reported(self):
        flow = "<Flow><decisions><name>A</name></decisions><decisions><name>B</name></decisions><status>Active</status></Flow>"
        swapped = "<Flow><decisions><name>B</name></decisions><decisions><name>A</name></decisions><status>Active</status></Flow>"
        write(self.repo, "flows/Dispute_Flow.flow-meta.xml", flow)
        git(self.repo, "commit", "-q", "-am", "xml form")
        write(self.repo, "flows/Dispute_Flow.flow-meta.xml", swapped)
        git(self.repo, "commit", "-q", "-am", "reorder", date=NEW_DATE)
        self.assertEqual(self.check(), [])

    def test_permission_set_found_as_custom_permission(self):
        findings = self.check(type="permissionSet", name="Fraud_Approver")
        self.assertEqual(findings[0].kind, "FOUND_ELSEWHERE")
        self.assertIn("customPermission", findings[0].detail)

    def test_absent_metadata_is_missing(self):
        self.assertEqual(self.check(name="Gone_Flow")[0].kind, "MISSING")

    def test_email_alert_checked_inside_workflow_file(self):
        self.assertEqual(self.check(type="emailAlert", name="Credit_Alert", object="Account"), [])
        self.assertEqual(self.check(type="emailAlert", name="Old_Alert", object="Account")[0].kind, "MISSING")

    def test_live_claims_are_not_checked_in_repo(self):
        findings, live = drift_scan.scan(self.scanner, [claim(type="user", name="Someone")], ROOT)
        self.assertEqual((findings, len(live)), ([], 1))

    def test_live_claims_become_one_batched_query_per_kind(self):
        live = [claim(type="user", name="O'Neil"), claim(type="user", name="O'Neil"), claim(type="cronJob", name="Nightly")]
        queries = drift_scan.live_queries(live)
        self.assertEqual(len(queries), 2)
        self.assertIn("IN ('O\\'Neil')", queries[0])

    def test_unknown_type_is_reported(self):
        self.assertEqual(self.check(type="layout")[0].kind, "UNSUPPORTED")


if __name__ == "__main__":
    unittest.main()
