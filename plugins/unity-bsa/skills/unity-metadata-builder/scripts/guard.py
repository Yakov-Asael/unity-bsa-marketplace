"""Claude Code hook for the unity-bsa plugin (metadata guardrails).

Usage: python3 guard.py pre|post   (hook input JSON on stdin)
pre  denies a tool call by printing a PreToolUse permissionDecision; silence allows it.
post records connector orgs and whether the metadata-builder skill is active in the session.
"""

import os
import re
import sys
import json
import subprocess

from common import load_policy, build_org, load_state, save_state, find_organization, split_mcp_tool
from scan import BLOCK, scan

READ_METHODS = {"GET", "HEAD"}
RECORD_WRITE = re.compile(r"^(create|update|delete)\w*Record")
PROTECTED_DIRS = (os.path.join("skills", "unity-metadata-builder", "config"),
                  os.path.join("skills", "unity-metadata-builder", "scripts"),
                  "hooks")
SF_DEPLOY = re.compile(r"\b(?:sf|sfdx)\s+(?:project\s+(?:deploy|delete)|deploy\b|org\s+delete|force:(?:source|mdapi):deploy)")
GIT_WRITE = re.compile(r"\bgit\b(?:\s+-C\s+(\S+))?\s+(?:checkout\s+-b|switch\s+-c|branch\s+(?!-)\S|commit|push)\b")

GEARSET = "Branches and deploys to the org go through Gearset, not Claude. Build in UAT, then promote with Gearset."


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))
    return 0


def is_sfdc_repo(path, policy):
    """
    Checks whether a directory is a checkout of the Salesforce org repo.
    @param path The directory
    @param policy The loaded policy
    @returns bool True when its remotes match a configured marker
    """
    if not path or not os.path.isdir(path):
        return False
    try:
        remotes = subprocess.run(["git", "-C", path, "remote", "-v"], capture_output=True, text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return False
    return any(marker in remotes for marker in policy["sfdc_repo_markers"])


def check_bash(command, cwd, policy):
    if SF_DEPLOY.search(command):
        return f"Blocked: sf CLI deploy/delete. {GEARSET}"
    match = GIT_WRITE.search(command)
    if not match:
        return None
    repo = os.path.join(cwd or "", match.group(1)) if match.group(1) else cwd
    if is_sfdc_repo(repo, policy):
        return f"Blocked: git branch/commit/push in the Salesforce org repo. {GEARSET}"
    return None


def check_edit(file_path):
    root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if not root or not file_path:
        return None
    target = os.path.realpath(file_path)
    for protected in PROTECTED_DIRS:
        guarded = os.path.realpath(os.path.join(root, protected))
        if target == guarded or target.startswith(guarded + os.sep):
            return ("Blocked: the metadata-builder rules and hooks can't be edited from a session. "
                    "Changes go through a PR to the unity-bsa marketplace repo, reviewed by the maintainer.")
    return None


def org_problem(server, state, policy):
    """
    Explains why a connector may not change the org, or returns None when it may.
    @param server The MCP server ID
    @param state The session state
    @param policy The loaded policy
    @returns str | None The reason to deny
    """
    org = state["servers"].get(server)
    if not org:
        return ("First confirm which org this connector points at: run "
                "SELECT Id, Name, IsSandbox FROM Organization through this same connector, then retry.")
    if not org.get("is_sandbox"):
        return "Blocked: this connector points at a production org. Metadata is built in UAT only; production goes through Gearset."
    if not build_org(policy, org.get("org_id")):
        allowed = ", ".join(org["label"] for org in policy["build_orgs"])
        return f"Blocked: this connector's org ({org.get('org_id')}) isn't a build org. Allowed: {allowed}."
    return None


def check_metadata_write(server, tool, tool_input, state, policy):
    problem = org_problem(server, state, policy)
    if problem:
        return problem
    if tool == "dispatch":
        payload, metadata_type, url = tool_input.get("body"), None, tool_input.get("url")
    else:
        payload, metadata_type, url = tool_input.get("parameters"), tool_input.get("metadataType"), None
    findings = [finding for finding in scan(payload or {}, policy, metadata_type, url) if finding.level == BLOCK]
    if not findings:
        return None
    lines = "\n".join(f"- {finding.rule}: {finding.message}" for finding in findings)
    return f"Blocked by the metadata-builder scan:\n{lines}"


def check_mcp(tool_name, tool_input, state, policy):
    server, tool = split_mcp_tool(tool_name)
    if not server:
        return None
    if tool == "dispatch" and str(tool_input.get("method", "GET")).upper() not in READ_METHODS:
        return check_metadata_write(server, tool, tool_input, state, policy)
    if tool.startswith("executeMetadataAction"):
        return check_metadata_write(server, tool, tool_input, state, policy)
    if RECORD_WRITE.match(tool) and state["skill_active"]:
        return org_problem(server, state, policy)
    return None


def pre(event, policy):
    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input") or {}
    if tool_name == "Bash":
        reason = check_bash(tool_input.get("command", ""), event.get("cwd"), policy)
    elif tool_name in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        reason = check_edit(tool_input.get("file_path") or tool_input.get("notebook_path"))
    else:
        reason = check_mcp(tool_name, tool_input, load_state(event.get("session_id")), policy)
    return deny(reason) if reason else 0


def post(event, policy):
    session_id = event.get("session_id")
    tool_name = event.get("tool_name", "")
    state = load_state(session_id)
    if tool_name == "Skill":
        if policy["skill_name"] not in str((event.get("tool_input") or {}).get("skill", "")):
            return 0
        state["skill_active"] = True
        save_state(session_id, state)
        return 0
    server, _ = split_mcp_tool(tool_name)
    org = find_organization(event.get("tool_response")) if server else None
    if not org:
        return 0
    state["servers"][server] = org
    save_state(session_id, state)
    return 0


def main(argv):
    mode = argv[1] if len(argv) > 1 else ""
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return 0
    policy = load_policy()
    if mode == "pre":
        return pre(event, policy)
    if mode == "post":
        return post(event, policy)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
