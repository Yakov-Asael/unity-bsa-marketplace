#!/usr/bin/env python3
"""Build the SOX approver-matrix workbooks from the extracted CSVs.

Usage:
  python build_workbooks.py <run_folder> <output_folder> --month "October 2026"
         [--run-stamp "22 Oct 2026, 10:20-10:46 UTC"] [--run-by "Name"] [--config ../config.json]
         [--only bill,invoice]

Reads the CSV names from config.json. Writes "<Display> Approver Matrix - <month>.xlsx".
"""
import argparse, csv, json, os, sys
from collections import Counter
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
BOLD = Font(bold=True)
HEAD = PatternFill("solid", fgColor="D9E2F3")
FLAG = PatternFill("solid", fgColor="FFF2CC")


def read(folder, name):
    path = os.path.join(folder, name)
    if not os.path.exists(path):
        sys.exit(f"Missing CSV: {path}")
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def table(ws, r, rows, flag=None):
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = ws.cell(r + i, j + 1, v)
            if i == 0:
                c.font, c.fill = BOLD, HEAD
            elif flag and flag(row):
                c.fill = FLAG
    return r + len(rows)


def autosize(ws, cap=45):
    for col in ws.columns:
        n = max((len(str(c.value)) for c in col if c.value is not None), default=8)
        ws.column_dimensions[get_column_letter(col[0].column)].width = min(max(10, n + 2), cap)


def results_tab(wb, rows):
    ws = wb.active
    ws.title = "Results"
    table(ws, 1, rows)
    ws.freeze_panes = "A2"
    autosize(ws)


def ipe_tab(wb, obj, n, cfg, stamp, run_by):
    ws = wb.create_sheet("IPE")
    host, rid = cfg["org"]["lightning_host"], obj["report_id"]
    lines = [
        ("IPE - Information Produced by the Entity", True),
        ("", False),
        ("Report", True),
        (f"{obj['report_name']}  (Report Id {rid})", False),
        (f"https://{host}/lightning/r/Report/{rid}/view", False),
        ("", False),
        ("Population", True),
        (f"Approver_Matrix__c where Object API Name = {obj['sobject']}", False),
        (f"Rows in Results tab: {n}", False),
        ("", False),
        (f"Completeness check (SOQL, Grow PRODUCTION org {cfg['org']['org_id_18']})", True),
        (f"SELECT COUNT(Id) FROM Approver_Matrix__c WHERE Object_API_Name__c = '{obj['sobject']}'  ->  {n}", False),
        (f"Extracted: {stamp}" + (f", run as {run_by}" if run_by else ""), False),
        ("", False),
        ("EVIDENCE TO ADD BEFORE SUBMITTING", True),
        ("Paste the screenshot of the report above here (Filters visible, Total Records visible, macOS menu-bar clock showing date/time).", False),
        ("Total Records in the screenshot must equal the Results row count above.", False),
    ]
    for i, (text, bold) in enumerate(lines, 1):
        c = ws.cell(i, 1, text)
        if bold:
            c.font = BOLD
        if text.startswith("EVIDENCE"):
            c.fill = FLAG
    ws.column_dimensions["A"].width = 110


def modify_all_tab(wb, obj, ma, ps, pu):
    ws = wb.create_sheet(obj["modify_all_tab"])
    s = obj["sobject"]
    q = ("SELECT Id, Parent.Profile.Name, Parent.Name, Parent.IsOwnedByProfile, PermissionsCreate, "
         "PermissionsDelete, PermissionsEdit, PermissionsModifyAllRecords, SobjectType\n"
         f"FROM ObjectPermissions\nWHERE SobjectType = '{s}' AND PermissionsModifyAllRecords = true")
    ws.cell(1, 1, q).alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[1].height = 60
    ws.cell(3, 1, "Query result").font = BOLD
    mine = [r for r in ma[1:] if r[0] == s]
    rows = [["Profile Name", "Permission Set Name", "Profile-owned", "Create", "Delete", "Edit",
             "Modify All", "Active users (profile)"]]
    for r in mine:
        owned = r[4].lower() == "true"
        rows.append([r[2], r[3], r[4], r[5], r[6], r[7], r[8], pu.get(r[2], "0") if owned else ""])
    r0 = table(ws, 4, rows) + 1
    ws.cell(r0, 1, "Permission set users").font = BOLD
    r0 += 1
    sets = [r[3] for r in mine if r[4].lower() == "false"]
    if not sets:
        ws.cell(r0, 1, "No additional permission sets - Modify All only via the profiles above.")
        r0 += 2
    for name in sets:
        ws.cell(r0, 1, name).font = BOLD
        r0 += 1
        ws.cell(r0, 1, "SELECT Id, Assignee.Name, Assignee.Profile.Name, Assignee.FN_Role__c, Assignee.IsActive "
                       f"FROM PermissionSetAssignment WHERE PermissionSet.Name = '{name}' AND IsActive = true")
        r0 += 1
        assignees = [[x[2], x[3], x[4], x[5], x[6]] for x in ps[1:] if x[0] == s and x[1] == name]
        if not assignees:
            ws.cell(r0, 1, "(no active assignments)")
            r0 += 2
            continue
        r0 = table(ws, r0, [["Assignment Id", "Assignee", "Assignee Profile", "FN Role", "User Active"]] + assignees,
                   flag=lambda row: str(row[4]).lower() == "false") + 1
    zero = [r[2] for r in mine if r[4].lower() == "true" and pu.get(r[2], "0") == "0"]
    note = "Yellow rows = active permission-set assignment on a deactivated user."
    if zero:
        note = f"Profiles with 0 active users: {', '.join(zero)}. " + note
    ws.cell(r0, 1, note).font = Font(italic=True)
    autosize(ws, 60)
    ws.column_dimensions["A"].width = 60
    return sets


def custom_settings_tab(wb, obj, cs, cfg):
    ws = wb.create_sheet("Custom Settings")
    c = cfg["custom_setting"]
    s = obj["sobject"]
    ws.cell(1, 1, f"Custom Setting: {c['label']} ({c['api_name']}, key prefix {c['key_prefix']}) - all org-level rows").font = BOLD
    n = sum(1 for r in cs[1:] if len(r) > 3 and r[3] == s)
    ws.cell(2, 1, f"Rows for {s}: {n} (highlighted). Total rows: {len(cs) - 1}")
    table(ws, 4, cs, flag=lambda row: len(row) > 3 and row[3] == s)
    autosize(ws)


def approval_tab(wb, obj):
    ws = wb.create_sheet("Approval")
    table(ws, 1, [["Approver Name", "Approval Date", "Approved? (Y/N)", "Comment"]] +
          [[a, "", "", ""] for a in obj["approvers"]])
    autosize(ws)
    ws.column_dimensions["D"].width = 60


def team_summary_tab(wb, rows):
    hdr = rows[0]
    i_type, i_div, i_team = hdr.index("Dispute Type"), hdr.index("Division"), hdr.index("Team")
    data = rows[1:]
    cnt = Counter((r[i_div], r[i_team], r[i_type]) for r in data)
    types = sorted({r[i_type] for r in data})
    out = [["Division", "Team"] + types + ["Grand Total"]]
    for div in sorted({k[0] for k in cnt}):
        tot = [0] * len(types)
        for team in sorted({k[1] for k in cnt if k[0] == div}):
            v = [cnt.get((div, team, t), 0) for t in types]
            tot = [a + b for a, b in zip(tot, v)]
            out.append([div, team] + [x or "" for x in v] + [sum(v)])
        out.append([f"{div or '(blank)'} Total", ""] + tot + [sum(tot)])
    out.append(["Grand Total", ""] + [sum(1 for r in data if r[i_type] == t) for t in types] + [len(data)])
    ws = wb.create_sheet("Team Summary")
    ws.cell(1, 1, "Count of matrix lines by Division / Team / Dispute Type").font = BOLD
    table(ws, 3, out, flag=lambda row: str(row[0]).endswith("Total"))
    autosize(ws)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_folder")
    ap.add_argument("output_folder")
    ap.add_argument("--month", required=True, help='e.g. "October 2026"')
    ap.add_argument("--run-stamp", default="", help="when the extract ran, e.g. '22 Oct 2026, 10:20-10:46 UTC'")
    ap.add_argument("--run-by", default="")
    ap.add_argument("--config", default=os.path.join(HERE, "..", "config.json"))
    ap.add_argument("--only", default="", help="comma-separated object keys")
    a = ap.parse_args()

    cfg = json.load(open(a.config, encoding="utf-8"))
    sh = cfg["shared_csvs"]
    ma = read(a.run_folder, sh["modify_all"])
    ps = read(a.run_folder, sh["permset_users"])
    pu = {r[0]: r[1] for r in read(a.run_folder, sh["profile_users"])[1:]}
    cs = read(a.run_folder, cfg["custom_setting"]["csv"])
    only = {k.strip() for k in a.only.split(",") if k.strip()}
    os.makedirs(a.output_folder, exist_ok=True)

    for obj in cfg["objects"]:
        if only and obj["key"] not in only:
            continue
        rows = read(a.run_folder, obj["csv"])
        if rows[0] != obj["columns"]:
            sys.exit(f"{obj['csv']}: header {rows[0]} does not match config columns {obj['columns']}")
        wb = Workbook()
        results_tab(wb, rows)
        ipe_tab(wb, obj, len(rows) - 1, cfg, a.run_stamp, a.run_by)
        sets = modify_all_tab(wb, obj, ma, ps, pu)
        custom_settings_tab(wb, obj, cs, cfg)
        approval_tab(wb, obj)
        if obj.get("team_summary"):
            team_summary_tab(wb, rows)
        name = f"{obj['display']} Approver Matrix - {a.month}.xlsx"
        wb.save(os.path.join(a.output_folder, name))
        print(f"{name}: {len(rows) - 1} rows; extra Modify All sets: {', '.join(sets) or 'none'}")


if __name__ == "__main__":
    main()
