![SOX Approver Matrix Workbooks banner](./assets/banner.png)

# sox-approver-matrix-workbooks

Builds the **quarterly SOX approver-matrix control workbooks** (Bills, Invoice, Dispute, Credit) straight from Salesforce Grow production through the Salesforce MCP connector. The connector edition of [`sox-approver-matrix`](../sox-approver-matrix): no local browser run, no macOS screenshot pipeline.

## What it produces

One workbook per object, named `<Object> Approver Matrix - <Month> <Year>.xlsx`, each with five tabs: **Results**, **IPE**, **Modify All users**, **Custom Settings**, **Approval**. The Dispute workbook also carries a Team Summary tab. Deal Payment (`Tier__c`) is deprecated and no longer part of the control.

## How it works

- **Identity gate first:** two serial calls confirm the connector points at Grow production (not a sandbox) before anything is extracted.
- **Serial, aliased queries:** one Salesforce call at a time with unique aggregate aliases, so a mis-paired response is obvious.
- **Verify before build:** `scripts/verify.py` checks headers, duplicate Ids and row counts against fresh `COUNT(Id)` queries. Failures are fixed in the extract, never patched in the workbook.
- **Config-driven scope:** columns, SOQL, report ids, approvers and tab names live in `config.json`.
- **Findings:** deactivated users still holding Modify All, extra Modify All profiles, approvers who are inactive users, blank `Object_API_Name__c` rows.

## Boundary

Produces the data workbooks only. Screenshot evidence for the IPE tab stays a human or Mac step (or use `sox-approver-matrix`), and approvers fill the Approval tab. **Not** for editing matrix records, approver alignment reviews, or the SOX access and change-management reviews.

## References & scripts

- `references/` — `extraction.md` (every SOQL statement, paging, token-saving pattern), `findings.md`
- `config.json` — objects, columns, approvers, tab names
- `scripts/` — `verify.py`, `build_workbooks.py` (needs `openpyxl`)
