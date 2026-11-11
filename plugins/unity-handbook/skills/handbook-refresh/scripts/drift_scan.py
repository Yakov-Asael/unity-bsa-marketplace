#!/usr/bin/env python3
"""Compare handbook claims against an SFDC-IS metadata ref and print only what changed.

Reads metadata straight from a git ref (default origin/Production) with `git show`, so the
working copy and its checked-out branch are never touched. Claims that only the live org can
answer (users, cron jobs) are listed for the connector instead of being checked here.

Usage:
  drift_scan.py <claims.json> <sfdc-is-repo> [--ref origin/Production] [--meta-root unpackaged/main/default]
                [--fetch] [--json]
Exit code: 0 nothing changed, 1 findings, 2 usage or repo error.
"""
import argparse
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import asdict, dataclass, field

FETCH_TIMEOUT_SECONDS = 45
LIVE_TYPES = {"user", "cronJob", "customMetadataRow"}
SIBLING_TYPES = {
    "permissionSet": "customPermission",
    "customPermission": "permissionSet",
    "flow": "approvalProcess",
    "approvalProcess": "flow",
}
ACTIVE_PATTERNS = {
    "flow": r"<status>(\w+)</status>",
    "approvalProcess": r"<active>(\w+)</active>",
    "validationRule": r"<active>(\w+)</active>",
    "recordType": r"<active>(\w+)</active>",
}
ACTIVE_VALUES = {"Active", "true"}
NOISE_TAGS = {"locationX", "locationY", "apiVersion", "processMetadataValues", "environments", "interviewLabel"}
DELTA_SAMPLE = 12


def xml_leaves(text):
    """Returns the multiset of (parent/tag, value) leaves, ignoring layout and builder noise."""
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return None
    leaves = Counter()

    def walk(node, parent):
        tag = node.tag.split("}")[-1]
        if tag in NOISE_TAGS:
            return
        children = list(node)
        if not children:
            value = (node.text or "").strip()
            if value:
                leaves[f"{parent}/{tag}={value}"] += 1
            return
        for child in children:
            walk(child, tag)

    walk(root, "")
    return leaves


def line_set(text):
    lines = (line.strip() for line in text.splitlines())
    return Counter(line for line in lines if line and not any(f"<{tag}>" in line for tag in NOISE_TAGS))


@dataclass
class Finding:
    claim_id: str
    tab: str
    kind: str
    detail: str
    commits: list = field(default_factory=list)
    added: list = field(default_factory=list)
    removed: list = field(default_factory=list)


def metadata_path(claim_type, name, obj, root):
    """Maps a claim to its repo path, or None for types read from a parent file."""
    paths = {
        "flow": f"flows/{name}.flow-meta.xml",
        "approvalProcess": f"approvalProcesses/{obj}.{name}.approvalProcess-meta.xml",
        "validationRule": f"objects/{obj}/validationRules/{name}.validationRule-meta.xml",
        "field": f"objects/{obj}/fields/{name}.field-meta.xml",
        "recordType": f"objects/{obj}/recordTypes/{name}.recordType-meta.xml",
        "object": f"objects/{name}/{name}.object-meta.xml",
        "permissionSet": f"permissionsets/{name}.permissionset-meta.xml",
        "customPermission": f"customPermissions/{name}.customPermission-meta.xml",
        "apexClass": f"classes/{name}.cls",
        "apexTrigger": f"triggers/{name}.trigger",
        "emailAlert": f"workflows/{obj}.workflow-meta.xml",
    }
    relative = paths.get(claim_type)
    if relative is None:
        return None
    return f"{root}/{relative}"


class Repo:
    def __init__(self, path, ref):
        self.path = path
        self.ref = ref
        self._tree = None

    def git(self, *args):
        result = subprocess.run(["git", "-C", self.path, *args], capture_output=True, text=True)
        if result.returncode != 0:
            return None
        return result.stdout

    def read(self, path):
        return self.git("show", f"{self.ref}:{path}")

    def tree(self):
        if self._tree is None:
            self._tree = (self.git("ls-tree", "-r", "--name-only", self.ref) or "").splitlines()
        return self._tree

    def commits_since(self, path, since):
        out = self.git("log", self.ref, f"--since={since}", "--format=%h %ad %s", "--date=short", "--", path)
        return [line for line in (out or "").splitlines() if line]

    def baseline(self, path, since):
        """Returns the file as it stood on `since`, or None when the repo did not hold it then."""
        candidates = self.git("log", self.ref, f"--before={since}", "--format=%H", "-n", "20", "--", path) or ""
        snapshot = (self.git("rev-list", "-1", f"--before={since}", self.ref) or "").strip()
        for commit in [snapshot, *candidates.split()]:
            content = self.git("show", f"{commit}:{path}") if commit else None
            if content is not None:
                return content
        return None

    def delta_since(self, path, since):
        """Returns (added, removed) values between the file on `since` and the ref; reorders count as nothing."""
        before = self.baseline(path, since)
        if before is None:
            return None
        after = self.read(path) or ""
        old, new = xml_leaves(before), xml_leaves(after)
        if old is None or new is None:
            old, new = line_set(before), line_set(after)
        return sorted((new - old).elements()), sorted((old - new).elements())

    def ref_date(self):
        return (self.git("log", "-1", "--format=%cd", "--date=iso", self.ref) or "unknown").strip()


def fetch(repo):
    """Tries a bounded fetch of the ref's branch; returns an error line or None."""
    remote, _, branch = repo.ref.partition("/")
    if not branch:
        return f"ref {repo.ref} is not a remote ref; nothing to fetch"
    try:
        result = subprocess.run(
            ["git", "-C", repo.path, "fetch", remote, branch],
            capture_output=True, text=True, timeout=FETCH_TIMEOUT_SECONDS,
            env={"GIT_TERMINAL_PROMPT": "0", "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"},
        )
    except subprocess.TimeoutExpired:
        return f"fetch timed out after {FETCH_TIMEOUT_SECONDS}s"
    if result.returncode != 0:
        return f"fetch failed: {result.stderr.strip().splitlines()[-1] if result.stderr.strip() else 'unknown error'}"
    return None


def find_elsewhere(repo, claim, root):
    """Applies the false-drift trap: sibling type first, then a name search across the tree."""
    sibling = SIBLING_TYPES.get(claim["type"])
    if sibling:
        path = metadata_path(sibling, claim["name"], claim.get("object"), root)
        if path and repo.read(path) is not None:
            return f"exists as {sibling}: {path}"
    stem = claim["name"].lower()
    matches = [p for p in repo.tree() if stem in p.lower()]
    if matches:
        return "name found at: " + ", ".join(matches[:3])
    return None


def check_alert(content, claim):
    if f"<fullName>{claim['name']}</fullName>" in content:
        return None
    return Finding(claim["id"], claim["tab"], "MISSING", f"email alert {claim['name']} not in {claim['object']} workflow")


def check_state(content, claim):
    pattern = ACTIVE_PATTERNS.get(claim["type"])
    if pattern is None or "active" not in claim:
        return None
    match = re.search(pattern, content)
    if not match:
        return None
    is_active = match.group(1) in ACTIVE_VALUES
    if is_active == claim["active"]:
        return None
    return Finding(claim["id"], claim["tab"], "STATE_CHANGED", f"expected active={claim['active']}, repo says {match.group(1)}")


def check_contains(content, claim):
    missing = [p for p in claim.get("contains", []) if not re.search(p, content)]
    if not missing:
        return None
    return Finding(claim["id"], claim["tab"], "VALUE_CHANGED", "pattern not found: " + "; ".join(missing))


def check_claim(repo, claim, root, sample=DELTA_SAMPLE):
    """Returns the findings for one claim; an empty list means nothing changed."""
    path = metadata_path(claim["type"], claim["name"], claim.get("object"), root)
    if path is None:
        return [Finding(claim["id"], claim["tab"], "UNSUPPORTED", f"type {claim['type']} has no repo mapping")]

    content = repo.read(path)
    if content is None:
        elsewhere = find_elsewhere(repo, claim, root)
        if elsewhere:
            return [Finding(claim["id"], claim["tab"], "FOUND_ELSEWHERE", elsewhere)]
        return [Finding(claim["id"], claim["tab"], "MISSING", f"{path} not in {repo.ref}")]

    if claim["type"] == "emailAlert":
        alert = check_alert(content, claim)
        return [alert] if alert else []

    findings = [f for f in (check_state(content, claim), check_contains(content, claim)) if f]
    commits = repo.commits_since(path, claim["verified_on"])
    if not commits:
        return findings
    delta = repo.delta_since(path, claim["verified_on"])
    if delta is None:
        findings.append(Finding(claim["id"], claim["tab"], "NO_BASELINE", f"{path} not in the repo on {claim['verified_on']}; verify once and reset verified_on"))
        return findings
    added, removed = delta
    if not added and not removed:
        return findings
    detail = f"{path} changed after {claim['verified_on']} (+{len(added)} -{len(removed)} values)"
    finding = Finding(claim["id"], claim["tab"], "CHANGED_SINCE", detail, commits)
    finding.added, finding.removed = added[:sample], removed[:sample]
    findings.append(finding)
    return findings


def scan(repo, claims, root, sample=DELTA_SAMPLE):
    findings, live = [], []
    for claim in claims:
        if claim["type"] in LIVE_TYPES:
            live.append(claim)
            continue
        findings.extend(check_claim(repo, claim, root, sample))
    return findings, live


def soql_literal(value):
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def live_queries(live):
    """Builds the batched read-only SOQL for the live-only claims."""
    users = sorted({c["name"] for c in live if c["type"] == "user"})
    jobs = sorted({c["name"] for c in live if c["type"] == "cronJob"})
    queries = []
    if users:
        names = ",".join(soql_literal(u) for u in users)
        queries.append(f"SELECT Name, IsActive FROM User WHERE Name IN ({names}) ORDER BY Name LIMIT 500")
    if jobs:
        names = ",".join(soql_literal(j) for j in jobs)
        queries.append("SELECT CronJobDetail.Name, State, CronExpression, NextFireTime, TimeZoneSidKey "
                       f"FROM CronTrigger WHERE CronJobDetail.Name IN ({names}) LIMIT 50")
    return queries


def print_report(repo, claims, findings, live, fetch_error):
    print(f"ref {repo.ref} @ {repo.ref_date()}")
    if fetch_error:
        print(f"WARNING {fetch_error}; using the last fetched ref above")
    print(f"claims {len(claims)} | repo-checked {len(claims) - len(live)} | findings {len(findings)} | live-only {len(live)}")
    for f in findings:
        print(f"{f.kind:<16} {f.tab:<28} {f.claim_id}: {f.detail}")
        for commit in f.commits[:3]:
            print(f"{'':<46}{commit}")
        for value in f.added:
            print(f"{'':<46}+ {value}")
        for value in f.removed:
            print(f"{'':<46}- {value}")
    for query in live_queries(live):
        print(f"LIVE SOQL: {query}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("claims")
    parser.add_argument("repo")
    parser.add_argument("--ref", default="origin/Production")
    parser.add_argument("--meta-root", default="unpackaged/main/default")
    parser.add_argument("--fetch", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--full", action="store_true", help="list every changed value, not a sample")
    args = parser.parse_args()

    repo = Repo(args.repo, args.ref)
    if repo.git("rev-parse", "--verify", args.ref) is None:
        print(f"ref {args.ref} not found in {args.repo}", file=sys.stderr)
        return 2

    with open(args.claims, encoding="utf-8") as handle:
        claims = json.load(handle)["claims"]

    fetch_error = fetch(repo) if args.fetch else None
    findings, live = scan(repo, claims, args.meta_root, None if args.full else DELTA_SAMPLE)

    if args.json:
        payload = {"ref": repo.ref, "ref_date": repo.ref_date(), "fetch_error": fetch_error,
                   "findings": [asdict(f) for f in findings], "live_soql": live_queries(live)}
        print(json.dumps(payload, indent=2))
    else:
        print_report(repo, claims, findings, live, fetch_error)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
