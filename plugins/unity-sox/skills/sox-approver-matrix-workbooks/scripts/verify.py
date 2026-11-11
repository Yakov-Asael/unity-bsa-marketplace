#!/usr/bin/env python3
"""Pre-build checks on the extracted CSVs.

Usage:
  python verify.py <run_folder> --counts bill=86 invoice=154 dispute=1399 credit=383 [--config ../config.json]

Checks, per object: file exists, header matches config, every row has the header's width,
no duplicate Ids, Ids are 15 chars, row count equals the COUNT() from production.
Also checks the shared CSVs exist and have the expected headers. Exit code 1 on any failure.
"""
import argparse, csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHARED_HEADERS = {
    "modify_all": ["SobjectType", "ObjectPermissions Id", "Profile Name", "Permission Set Name",
                   "Is Profile-owned", "Create", "Delete", "Edit", "Modify All"],
    "permset_users": ["SobjectType", "Permission Set", "Assignment Id", "Assignee",
                      "Assignee Profile", "FN Role", "User Active"],
    "profile_users": ["Profile", "Active Users"],
}


def load(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_folder")
    ap.add_argument("--counts", nargs="*", default=[], help="key=count from SELECT COUNT(Id)")
    ap.add_argument("--config", default=os.path.join(HERE, "..", "config.json"))
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8"))
    counts = dict(c.split("=") for c in a.counts)
    fails = []

    for obj in cfg["objects"]:
        p = os.path.join(a.run_folder, obj["csv"])
        if not os.path.exists(p):
            fails.append(f"{obj['key']}: missing {obj['csv']}")
            continue
        rows = load(p)
        hdr, data = rows[0], rows[1:]
        if hdr != obj["columns"]:
            fails.append(f"{obj['key']}: header mismatch {hdr}")
        bad = [i + 2 for i, r in enumerate(data) if len(r) != len(hdr)]
        if bad:
            fails.append(f"{obj['key']}: {len(bad)} rows with wrong column count (first lines {bad[:5]})")
        ids = [r[0] for r in data]
        dup = len(ids) - len(set(ids))
        if dup:
            fails.append(f"{obj['key']}: {dup} duplicate Ids")
        wrong = [i for i in ids if len(i) != 15]
        if wrong:
            fails.append(f"{obj['key']}: {len(wrong)} Ids not 15 chars (e.g. {wrong[:3]})")
        exp = counts.get(obj["key"])
        status = "no COUNT given"
        if exp is not None:
            status = "matches COUNT" if int(exp) == len(data) else f"COUNT={exp} MISMATCH"
            if int(exp) != len(data):
                fails.append(f"{obj['key']}: {len(data)} rows vs COUNT {exp}")
        print(f"{obj['key']:8} {len(data):6} rows  {status}")

    for key, hdr in SHARED_HEADERS.items():
        p = os.path.join(a.run_folder, cfg["shared_csvs"][key])
        if not os.path.exists(p):
            fails.append(f"missing {p}")
        elif load(p)[0] != hdr:
            fails.append(f"{key}: header mismatch")
        else:
            print(f"{key:14} {len(load(p)) - 1:4} rows  ok")
    p = os.path.join(a.run_folder, cfg["custom_setting"]["csv"])
    if not os.path.exists(p):
        fails.append(f"missing {p}")
    else:
        print(f"custom_setting {len(load(p)) - 1:4} rows  ok")

    if fails:
        print("\nFAILED:\n- " + "\n- ".join(fails))
        sys.exit(1)
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
