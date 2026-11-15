import io
import os
import sys
import json
import tempfile
import unittest
import subprocess
from unittest import mock
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(__file__))
import guard  # noqa: E402

UAT = "00DQI00000J4hjN2AR"
PROD = "00Db0000000JqmVEAS"
BETA = "mcp__e1f02b1b__"
SESSION = "test-session"


def org_response(org_id, is_sandbox):
    record = {"attributes": {"type": "Organization", "url": f"/services/data/v66.0/sobjects/Organization/{org_id}"},
              "Id": org_id, "IsSandbox": is_sandbox}
    return [{"type": "text", "text": json.dumps({"status_code": 200, "body": {"records": [record]}})}]


def run(mode, event):
    out = io.StringIO()
    with mock.patch("sys.stdin", io.StringIO(json.dumps({"session_id": SESSION, **event}))), redirect_stdout(out):
        guard.main(["guard.py", mode])
    text = out.getvalue().strip()
    return json.loads(text)["hookSpecificOutput"]["permissionDecisionReason"] if text else None


def record_org(server, org_id, is_sandbox=True):
    run("post", {"tool_name": f"{server}dispatch_readonly", "tool_response": org_response(org_id, is_sandbox)})


class GuardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"CLAUDE_PLUGIN_DATA": self.tmp.name})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def dispatch(self, body, method="POST", url="/services/data/v66.0/tooling/sobjects/Flow"):
        return run("pre", {"tool_name": f"{BETA}dispatch", "tool_input": {"method": method, "url": url, "body": body}})

    def test_write_before_org_check_is_denied(self):
        self.assertIn("SELECT Id, Name, IsSandbox FROM Organization", self.dispatch({}))

    def test_write_on_uat_is_allowed(self):
        record_org(BETA, UAT)
        self.assertIsNone(self.dispatch({"Metadata": {"processType": "AutoLaunchedFlow", "status": "Draft",
                                                      "description": "x", "label": "A - B - C"}}))

    def test_write_on_production_is_denied(self):
        record_org(BETA, PROD, is_sandbox=False)
        self.assertIn("production", self.dispatch({}))

    def test_write_on_other_sandbox_is_denied(self):
        record_org(BETA, "00D000000000001AAA")
        self.assertIn("isn't a build org", self.dispatch({}))

    def test_scan_block_is_denied(self):
        record_org(BETA, UAT)
        reason = self.dispatch({"Metadata": {"processType": "AutoLaunchedFlow", "status": "Active",
                                             "description": "x", "label": "A - B - C"}})
        self.assertIn("B8", reason)

    def test_apex_via_url_is_denied(self):
        record_org(BETA, UAT)
        self.assertIn("B19", self.dispatch({"Body": "x"}, url="/services/data/v66.0/tooling/sobjects/ApexClass"))

    def test_read_dispatch_is_not_checked(self):
        self.assertIsNone(self.dispatch({}, method="GET"))

    def test_execute_metadata_action_apex_is_denied(self):
        server = "mcp__f82f87ad__"
        record_org(server, UAT)
        reason = run("pre", {"tool_name": f"{server}executeMetadataActionplatform_metadata_experts",
                             "tool_input": {"metadataType": "ApexClass", "actionName": "create", "parameters": {}}})
        self.assertIn("B19", reason)

    def test_record_write_outside_skill_is_allowed(self):
        record_org("mcp__prod__", PROD, is_sandbox=False)
        self.assertIsNone(run("pre", {"tool_name": "mcp__prod__updateSobjectRecordplatform_sobject_mutations", "tool_input": {}}))

    def test_record_write_on_production_during_skill_is_denied(self):
        run("post", {"tool_name": "Skill", "tool_input": {"skill": "unity-bsa:unity-metadata-builder"}})
        record_org("mcp__prod__", PROD, is_sandbox=False)
        reason = run("pre", {"tool_name": "mcp__prod__updateSobjectRecordplatform_sobject_mutations", "tool_input": {}})
        self.assertIn("production", reason)

    def test_other_skill_does_not_activate(self):
        run("post", {"tool_name": "Skill", "tool_input": {"skill": "unity-bsa:unity-qa-debug"}})
        self.assertIsNone(run("pre", {"tool_name": "mcp__x__createSobjectRecordplatform_sobject_all", "tool_input": {}}))

    def test_sf_deploy_is_denied(self):
        reason = run("pre", {"tool_name": "Bash", "tool_input": {"command": "sf project deploy start -o grow-uat"}})
        self.assertIn("Gearset", reason)

    def test_sf_query_is_allowed(self):
        self.assertIsNone(run("pre", {"tool_name": "Bash", "tool_input": {"command": "sf data query -q 'SELECT Id FROM Account'"}}))

    def test_git_commit_in_sfdc_repo_is_denied(self):
        repo = os.path.join(self.tmp.name, "repo")
        os.makedirs(repo)
        subprocess.run(["git", "init", "-q", repo], check=True)
        subprocess.run(["git", "-C", repo, "remote", "add", "origin", "git@github.com:unity/SFDC-IS.git"], check=True)
        reason = run("pre", {"tool_name": "Bash", "cwd": repo, "tool_input": {"command": "git commit -m x"}})
        self.assertIn("Gearset", reason)

    def test_git_commit_elsewhere_is_allowed(self):
        self.assertIsNone(run("pre", {"tool_name": "Bash", "cwd": self.tmp.name, "tool_input": {"command": "git commit -m x"}}))

    def test_editing_plugin_rules_is_denied(self):
        root = os.path.join(self.tmp.name, "plugin")
        with mock.patch.dict(os.environ, {"CLAUDE_PLUGIN_ROOT": root}):
            path = os.path.join(root, "skills", "unity-metadata-builder", "config", "policy.json")
            self.assertIn("PR", run("pre", {"tool_name": "Edit", "tool_input": {"file_path": path}}))
            other = os.path.join(root, "skills", "unity-metadata-builder", "SKILL.md")
            self.assertIsNone(run("pre", {"tool_name": "Edit", "tool_input": {"file_path": other}}))


if __name__ == "__main__":
    unittest.main()
