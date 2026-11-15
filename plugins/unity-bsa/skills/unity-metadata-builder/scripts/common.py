"""Shared helpers for the unity-metadata-builder scripts. Python 3 stdlib only."""

import os
import json
import tempfile

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POLICY_PATH = os.path.join(SKILL_DIR, "config", "policy.json")


def load_policy(path=POLICY_PATH):
    """
    Loads the skill policy.
    @param path Path to policy.json
    @returns dict The policy
    """
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def org_key(org_id):
    """
    Normalizes a Salesforce org ID to its case-sensitive 15-char form.
    @param org_id A 15- or 18-char org ID
    @returns str The 15-char ID, or "" when missing
    """
    return (org_id or "")[:15]


def build_org(policy, org_id):
    """
    Finds the build org entry for an org ID.
    @param policy The loaded policy
    @param org_id The org ID to look up
    @returns dict | None The matching build org
    """
    key = org_key(org_id)
    if not key:
        return None
    return next((org for org in policy["build_orgs"] if org_key(org["id"]) == key), None)


def state_dir():
    """
    Resolves the writable state directory for hook session state.
    @returns str An existing directory path
    """
    base = os.environ.get("CLAUDE_PLUGIN_DATA") or os.path.join(tempfile.gettempdir(), "unity-bsa-plugin-data")
    path = os.path.join(base, "metadata-builder-state")
    os.makedirs(path, exist_ok=True)
    return path


def state_path(session_id):
    safe = "".join(ch for ch in (session_id or "no-session") if ch.isalnum() or ch in "-_")
    return os.path.join(state_dir(), f"{safe or 'no-session'}.json")


def load_state(session_id):
    """
    Loads one session's hook state.
    @param session_id The Claude Code session ID
    @returns dict The state, with `servers` and `skill_active` keys
    """
    try:
        with open(state_path(session_id), encoding="utf-8") as handle:
            state = json.load(handle)
    except (OSError, ValueError):
        state = {}
    state.setdefault("servers", {})
    state.setdefault("skill_active", False)
    return state


def save_state(session_id, state):
    path = state_path(session_id)
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(state, handle)
    os.replace(tmp, path)


def decode_nested(value):
    """
    Recursively decodes JSON that MCP servers wrap inside strings.
    @param value Any JSON-like value
    @returns The value with JSON-looking strings parsed
    """
    if isinstance(value, dict):
        return {key: decode_nested(item) for key, item in value.items()}
    if isinstance(value, list):
        return [decode_nested(item) for item in value]
    if not isinstance(value, str):
        return value
    stripped = value.strip()
    if not stripped or stripped[0] not in "{[":
        return value
    try:
        return decode_nested(json.loads(stripped))
    except ValueError:
        return value


def iter_dicts(value):
    """
    Yields every dict inside a nested JSON-like value, depth first.
    @param value Any JSON-like value
    @returns Iterator of dicts
    """
    stack = [value]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            yield current
            stack.extend(current.values())
            continue
        if isinstance(current, list):
            stack.extend(current)


def find_organization(response):
    """
    Finds an Organization record in a tool response.
    @param response The raw MCP tool response
    @returns dict | None {"org_id", "is_sandbox"} when an Organization record with IsSandbox is present
    """
    for record in iter_dicts(decode_nested(response)):
        attributes = record.get("attributes")
        if not isinstance(attributes, dict) or attributes.get("type") != "Organization":
            continue
        if "IsSandbox" not in record:
            continue
        org_id = record.get("Id") or attributes.get("url", "").rsplit("/", 1)[-1]
        return {"org_id": org_id, "is_sandbox": record["IsSandbox"] is True}
    return None


def split_mcp_tool(tool_name):
    """
    Splits an MCP tool name into server and tool.
    @param tool_name e.g. mcp__<server>__<tool>
    @returns tuple (server, tool), or (None, None) when not an MCP tool
    """
    parts = (tool_name or "").split("__", 2)
    if len(parts) != 3 or parts[0] != "mcp":
        return None, None
    return parts[1], parts[2]
