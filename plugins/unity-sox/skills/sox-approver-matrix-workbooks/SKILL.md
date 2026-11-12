---
name: sox-approver-matrix-workbooks
description: 'Builds the quarterly SOX approver-matrix control workbooks (Bills, Invoice, Dispute, Credit) from Salesforce Grow production via the Salesforce MCP connector, in the previous quarters'' layout (Results, IPE, Modify All users, Custom Settings, Approval). Use whenever someone asks for the quarterly approver matrix review or control, "new control files like last quarter", fresh Bills/Invoice/Dispute/Credit approver matrix workbooks, a Modify All review for those objects, or the Dynamic Approval Process custom setting export, including Hebrew phrasings like "בקרת מטריצת מאשרים" or "בקרה רבעונית". Companion to sox-approver-matrix (macOS screenshot pipeline): this skill needs no local browser run; screenshot evidence is added after. Not for editing matrix records, approver alignment reviews, or the SOX access and change-management reviews.'
---

# SOX Approver Matrix Workbooks (connector edition)

Produces one workbook per object, named `<Object> Approver Matrix - <Month> <Year>.xlsx`:

| Workbook | Matrix object filter | Approval tab approvers |
|---|---|---|
| Bills | `Object_API_Name__c = 'Bill__c'` | Eyal Kaner, Yathish Rai |
| Invoice | `Invoice__c` | Eyal Kaner, Yathish Rai |
| Dispute | `Dispute__c` (+ Team Summary tab) | Tal Rahamim, Eyal Kaner |
| Credit | `Credit_Check__c` | Eyal Kaner |

Everything scope-specific (columns, SOQL, report ids, approvers, tab names) lives in `config.json` — change scope there, not in code. **Deal Payment (Tier__c) is deprecated and is no longer part of the control.**

Each workbook has the tabs the auditors are used to from previous quarters:
**Results** (matrix rows, report columns) · **IPE** (report, population, completeness query, evidence placeholder) · **Modify All users** (ObjectPermissions query + result + permission-set assignees) · **Custom Settings** (Dynamic Approval Process rows, this object's rows highlighted) · **Approval** (approver, date, Y/N, comment — left blank for sign-off).

## Why it works this way

The control proves two things: the approver matrix the auditors see is complete and current, and only the right people can change approval records. So every number must be traceable to a query against **production**, run in one sitting, and reconciled. The steps below exist to protect that: the identity gate stops a sandbox from sneaking in, serial calls stop the connector from cross-pairing responses (it has happened), and the cross-foot proves nothing was dropped or invented on the way into the file.

What this skill **cannot** produce is the screenshot evidence (report page with Total Records and the macOS menu-bar clock). That stays a human/Mac step — either the user screenshots the four reports, or runs the `sox-approver-matrix` pipeline. Never fill the IPE tab with old screenshots or anything that implies evidence was captured; leave the highlighted placeholder.

## Workflow

### 1. Confirm scope (one short question only if unclear)
Default: all four objects, current month/year in the file names, Grow production. Previous-quarter files are useful as a layout reference if the user shares links (read them with the Google Sheets connector — tab names, headers, the Modify All query text, the Approval columns). Over-grid images (screenshots) are not readable via the API; that's expected.

### 2. Identity gate — two calls, serial
1. `getUserInfo` on the Salesforce read connector.
2. Exactly: `SELECT Id, Name, IsSandbox, InstanceName, OrganizationType, FiscalYearStartMonth FROM Organization`

Proceed only if `Id = 00Db0000000JqmVEAS` (ironSource / Grow) and `IsSandbox = false`. Connector names and ids are hints, not identity. If the `one-crm-analyst` skill is installed, its gate rules apply too.

### 3. Extract to CSVs
Read `references/extraction.md` — it has every SOQL statement, column order, paging and the token-saving pattern. Summary:

- Write all CSVs into one run folder (e.g. `sox_<mon><yy>/`) with the exact file names in `config.json`.
- **Bills (~90 rows) and Invoice (~150)** fit in one call with relationship names (`Approver1__r.Name`).
- **Credit (~380) and Dispute (~1,400) are large.** Delegate their extraction to a subagent that writes the CSVs itself, so the raw JSON doesn't flood the main context. For Dispute query approver **Ids**, page with `LIMIT 700` + `Id > last`, then resolve names with one `User` query.
- Modify All: `ObjectPermissions` per object → `modify_all.csv`; assignees of every non-profile permission set → `permset_users.csv`; active-user count per profile → `profile_users.csv`.
- Custom setting `Dynamic_Approval_Process__c` → `custom_setting.csv` (explicit field list, never `FIELDS(ALL)`).
- Run one Salesforce call at a time. Give aggregates unique aliases (`COUNT(Id) c_bill`) so a mis-paired response is obvious.

### 4. Verify before building
```bash
python scripts/verify.py <run_folder> --counts bill=86 invoice=154 dispute=1399 credit=383
```
Pass the counts from fresh `SELECT COUNT(Id) c_<obj> FROM Approver_Matrix__c WHERE Object_API_Name__c = '<obj>'` queries. The script checks every CSV parses, has the configured header, has no duplicate Ids, and matches its count. Then spot-check 3 Dispute rows (first, middle, last) against a live query with relationship names — any data that was hand-paged or transcribed must be spot-checked. If anything fails, fix the extract; never patch the workbook.

### 5. Build the workbooks
```bash
pip install openpyxl  # if missing
python scripts/build_workbooks.py <run_folder> <output_folder> --month "October 2026" --run-stamp "22 Oct 2026, 10:20-10:46 UTC" --run-by "Yakov Asael"
```
Writes the four `.xlsx` files. Yellow rows in Modify All = an active permission-set assignment on a **deactivated** user; yellow rows in Custom Settings = this object's rows.

### 6. Deliver
- Save to the user's project folder (e.g. `SOX Approver Matrix - <Month> <Year>/`).
- Tell the user to upload each `.xlsx` to Drive and open with Google Sheets (tabs and formatting carry over). Don't push the files through a Drive connector as base64 — it costs a huge amount of context and a single bad character corrupts the file.
- Summarise per workbook: row count, who holds Modify All beyond the main profiles. Then list the two remaining steps: paste report screenshots into each IPE tab; approvers fill the Approval tab.

### 7. Findings worth flagging (read `references/findings.md`)
Deactivated users still assigned Modify All permission sets, Modify All profiles with active users beyond System Administrator/Integration, approver rows pointing at inactive users, matrix rows with blank `Object_API_Name__c`, and which objects actually use the custom setting. Keep it short; a table is fine.

## Output to the user
Keep the reply brief: what was built, a 4-row table (workbook · rows · extra Modify All holders), the two remaining manual steps, and the flagged findings. Show the SOQL only if asked — it's already in the IPE and Modify All tabs.
