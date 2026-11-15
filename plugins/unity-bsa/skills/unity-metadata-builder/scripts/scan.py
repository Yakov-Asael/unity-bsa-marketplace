"""Static scan of a metadata payload (Metadata API XML or Tooling/Headless JSON) before it is built.

Usage: python3 scan.py <file> [--metadata-type TYPE]
Prints one line per finding (BLOCK/WARN), then a summary. Exit 2 when anything blocks.
"""

import re
import sys
import json
import argparse
import xml.etree.ElementTree as ET

from common import load_policy

BLOCK = "BLOCK"
WARN = "WARN"

DML_ELEMENTS = ("recordcreates", "recordupdates", "recorddeletes")
SKIP_ID_KEYS = {"id", "attributes", "url", "fullname", "developername"}
ID_TOKEN = re.compile(r"(?<![A-Za-z0-9])[A-Za-z0-9]{15}(?:[A-Za-z0-9]{3})?(?![A-Za-z0-9])")
FLOW_LABEL = re.compile(r"^[^-]+ - [^-]+ - .+$")
FIELD_API_NAME = re.compile(r"^[A-Z][A-Za-z0-9]*(?:_[A-Z0-9][A-Za-z0-9]*)*__c$")
FIELD_TYPES = {
    "autonumber", "checkbox", "currency", "date", "datetime", "email", "encryptedtext", "html",
    "location", "longtextarea", "lookup", "masterdetail", "multiselectpicklist", "number",
    "percent", "phone", "picklist", "summary", "text", "textarea", "time", "url",
}


class Finding:
    def __init__(self, level, rule, message):
        self.level = level
        self.rule = rule
        self.message = message

    def __str__(self):
        return f"{self.level} {self.rule} {self.message}"


def xml_to_tree(element):
    """
    Converts an XML element to nested dicts with lower-case local tag names.
    @param element An ElementTree element
    @returns dict | str The converted value
    """
    children = list(element)
    if not children:
        return (element.text or "").strip()
    tree = {}
    for child in children:
        key = child.tag.rsplit("}", 1)[-1].lower()
        value = xml_to_tree(child)
        if key not in tree:
            tree[key] = value
            continue
        if not isinstance(tree[key], list):
            tree[key] = [tree[key]]
        tree[key].append(value)
    return tree


def parse_xml(text):
    root = ET.fromstring(text)
    return {root.tag.rsplit("}", 1)[-1].lower(): xml_to_tree(root)}


def normalize(value):
    """
    Lower-cases dict keys, parses embedded JSON and XML strings.
    @param value Any JSON-like value
    @returns The normalized value
    """
    if isinstance(value, dict):
        return {str(key).lower(): normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if not isinstance(value, str):
        return value
    stripped = value.strip()
    if stripped.startswith("<"):
        try:
            return normalize(parse_xml(stripped))
        except ET.ParseError:
            return value
    if stripped[:1] in ("{", "["):
        try:
            return normalize(json.loads(stripped))
        except ValueError:
            return value
    return value


def load_payload(text):
    """
    Parses payload text as XML or JSON into a normalized tree.
    @param text The raw payload
    @returns The normalized tree, or the raw string when it is neither
    """
    return normalize(text)


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def walk(value, parent=None, key=None):
    """
    Yields (key, value, parent) for every node in the tree.
    @param value The tree
    @returns Iterator of (key, value, parent)
    """
    stack = [(key, value, parent)]
    while stack:
        current_key, current, current_parent = stack.pop()
        yield current_key, current, current_parent
        if isinstance(current, dict):
            stack.extend((child_key, child, current) for child_key, child in current.items())
            continue
        if isinstance(current, list):
            stack.extend((current_key, child, current_parent) for child in current)


def scalar(value):
    return value if isinstance(value, str) else ""


def check_forbidden_types(tree, policy, metadata_type, url):
    forbidden = {name.lower(): name for name in policy["forbidden_metadata_types"]}
    hits = set()
    if metadata_type and metadata_type.lower() in forbidden:
        hits.add(forbidden[metadata_type.lower()])
    for name in forbidden.values():
        if url and re.search(rf"/{name}(?:/|$|\?)", url):
            hits.add(name)
    for key, value, _ in walk(tree):
        if key in forbidden and isinstance(value, dict):
            hits.add(forbidden[key])
        if key in ("metadatatype", "type") and scalar(value).lower() in forbidden:
            hits.add(forbidden[scalar(value).lower()])
    return [Finding(BLOCK, "B19", f"{name} is not allowed here: Apex, profiles and workflow rules are out of scope. "
                    "Use a Flow and permission sets; logic too complex for Flow is a dev ticket.") for name in sorted(hits)]


def check_hardcoded_ids(tree, policy):
    prefixes = tuple(policy["id_key_prefixes"])
    found = set()
    for key, value, _ in walk(tree):
        if key in SKIP_ID_KEYS or not isinstance(value, str):
            continue
        for token in ID_TOKEN.findall(value):
            if token.startswith(prefixes) and sum(ch.isdigit() for ch in token) >= 3:
                found.add(token)
    return [Finding(BLOCK, "B4", f"Hardcoded record ID {token}. Look it up by DeveloperName, or use Custom Metadata, "
                    "a Custom Label or a Custom Setting.") for token in sorted(found)]


def find_flows(tree):
    return [value for key, value, _ in walk(tree)
            if isinstance(value, dict) and "processtype" in value]


def check_flow(flow, policy):
    findings = []
    error_flow = policy["error_subflow"]["name"]
    label = scalar(flow.get("label"))
    name = label or scalar(flow.get("fullname")) or "flow"

    status = scalar(flow.get("status"))
    if status and status.lower() not in ("draft", "inactive", "invaliddraft"):
        findings.append(Finding(BLOCK, "B8", f"{name}: status is {status}. Build it as Draft; you activate it yourself after checking it."))

    process_type = scalar(flow.get("processtype"))
    if process_type in policy["forbidden_process_types"]:
        findings.append(Finding(BLOCK, "B21", f"{name}: processType {process_type} is Process Builder/workflow. Build a record-triggered flow instead."))

    if not scalar(flow.get("description")):
        findings.append(Finding(BLOCK, "A4", f"{name}: no flow description. Add one line on what it does and why."))

    if label and not FLOW_LABEL.match(label):
        findings.append(Finding(WARN, "A5", f"{name}: label should follow the Flow Standards pattern '[Object] - [Trigger Type] - [Description]'."))

    error_calls = {scalar(sub.get("name")): sub for sub in as_list(flow.get("subflows"))
                   if isinstance(sub, dict) and scalar(sub.get("flowname")) == error_flow}
    findings.extend(check_error_calls(name, error_calls.values(), policy))

    for kind in DML_ELEMENTS:
        for element in as_list(flow.get(kind)):
            if not isinstance(element, dict):
                continue
            findings.extend(check_fault_path(name, kind, element, error_calls, error_flow))

    for action in as_list(flow.get("actioncalls")):
        if isinstance(action, dict) and not action.get("faultconnector"):
            findings.append(Finding(WARN, "B22", f"{name}: action '{scalar(action.get('name'))}' has no fault path. Consider routing it to {error_flow}."))
    return findings


def check_fault_path(flow_name, kind, element, error_calls, error_flow):
    element_name = scalar(element.get("name")) or kind
    connector = element.get("faultconnector")
    if not isinstance(connector, dict):
        return [Finding(BLOCK, "ZT2", f"{flow_name}: {element_name} has no fault path. Every DML element needs one, routed to {error_flow}.")]
    target = scalar(connector.get("targetreference"))
    if target in error_calls:
        return []
    return [Finding(BLOCK, "B22", f"{flow_name}: {element_name} fault path goes to '{target}', not a {error_flow} subflow call.")]


def check_error_calls(flow_name, calls, policy):
    required = set(policy["error_subflow"]["inputs"])
    findings = []
    for call in calls:
        assigned = {scalar(item.get("name")) for item in as_list(call.get("inputassignments")) if isinstance(item, dict)}
        missing = sorted(required - assigned)
        if missing:
            findings.append(Finding(WARN, "B22", f"{flow_name}: error subflow call '{scalar(call.get('name'))}' doesn't pass {', '.join(missing)}. "
                                    "Pass {!$Flow.FaultMessage}, the flow API name and the record ID."))
    return findings


def find_fields(tree):
    for _, value, parent in walk(tree):
        if not isinstance(value, dict) or "label" not in value:
            continue
        if scalar(value.get("type")).lower() not in FIELD_TYPES:
            continue
        name = scalar(value.get("fullname")) or (scalar(parent.get("fullname")) if isinstance(parent, dict) else "")
        yield name, value


def check_field(name, field):
    findings = []
    display = name or scalar(field.get("label")) or "field"
    api_name = name.rsplit(".", 1)[-1]
    if not scalar(field.get("description")):
        findings.append(Finding(BLOCK, "A4", f"{display}: no description. Say what it stores and who uses it."))
    if not scalar(field.get("inlinehelptext")):
        findings.append(Finding(WARN, "A4", f"{display}: no help text. Users see it as the (i) tooltip; one plain sentence."))
    if api_name.endswith("__c") and not FIELD_API_NAME.match(api_name):
        findings.append(Finding(WARN, "A5", f"{display}: API name should be Snake_Case_Words__c (integration prefixes like WD_ or NS_ only)."))
    return findings


def scan(text, policy, metadata_type=None, url=None):
    """
    Scans one payload.
    @param text The payload text (XML or JSON)
    @param policy The loaded policy
    @param metadata_type Optional metadata type named by the call
    @param url Optional API path named by the call
    @returns list[Finding] Blocks first, then warnings
    """
    tree = load_payload(text) if isinstance(text, str) else normalize(text)
    findings = check_forbidden_types(tree, policy, metadata_type, url)
    findings += check_hardcoded_ids(tree, policy)
    for flow in find_flows(tree):
        findings += check_flow(flow, policy)
    for name, field in find_fields(tree):
        findings += check_field(name, field)
    return sorted(findings, key=lambda finding: finding.level != BLOCK)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file")
    parser.add_argument("--metadata-type")
    args = parser.parse_args(argv)

    with open(args.file, encoding="utf-8") as handle:
        findings = scan(handle.read(), load_policy(), args.metadata_type)

    for finding in findings:
        print(finding)
    blocks = sum(finding.level == BLOCK for finding in findings)
    print(f"{'FAIL' if blocks else 'PASS'} {blocks} block, {len(findings) - blocks} warn")
    return 2 if blocks else 0


if __name__ == "__main__":
    sys.exit(main())
