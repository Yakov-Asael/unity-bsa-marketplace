---
cluster: bulk-update-data-fix
name: Bulk record update / data fix from a sheet
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-17
count_90d: 19
---
## Definition
Requester provides a sheet or list; the team performs a bulk update (handovers, AM, approvers, ratings, goals, disputes, ticket closure).

## Detection signals
- Sub_Category Bulk update/Data Fix
- Google Sheet link
- 'bulk', 'data fix', 'Handovers Bulk/DATAFIX'
- Example subjects (paraphrased): Bulk account-manager handover from a sheet · Data fix on invoices or actuals for a period · Bulk update of approvers / ratings / goals

## How we resolve it
- Owner ruling: tell the agent **which object and which field** to update, and use a **low batch size for heavy accounts** (accounts with many invoices/bills/opps) so triggers do not hit limits.
- Require a sheet with record IDs/URLs and target values; missing IDs are the usual blocker.
- Handovers from a sheet: `Hand_Over__c` (or direct `Account.Account_Manager__c` for data fixes) - when invoices were already issued for the month, also re-tag `Monthly_Revenue__c` / invoice AM (revenue data fix).
- Report processed/skipped counts and share the updated-records list back.

## What to ask the requester
- Share the sheet with edit/view access.
- Account IDs and new values present for every row?
- Should already-issued invoices for the period be re-tagged too?

## Canonical answer
**Summary:** A sheet drives the same change on many records - handovers, account managers, approvers, ratings, goals, disputes, ticket closure. Bulk loads run the same triggers as single edits, so heavy accounts (many invoices, bills or opportunities) hit limits at a normal batch size; rows without record IDs cannot load. A handover after invoices were issued for the month also leaves `Monthly_Revenue__c` and the invoice AM on the old AM.
**Suggested resolution:**
1. Get sheet access; confirm every row has a record ID or URL and the target value, and return rows without IDs to the requester.
2. Name the object and field before loading - `Hand_Over__c` records for a standard handover, `Account.Account_Manager__c` for a direct data fix.
3. If the change touches a closed financial period or commissions: stop; Finance / Sales Ops approve first.
4. Load with a low batch size for heavy accounts so the triggers stay within limits.
5. If invoices were already issued for the month: ask whether to re-tag them; if yes, re-tag `Monthly_Revenue__c` / the invoice AM.
6. Spot-check loaded records, note the reason on each skipped row, and share processed / skipped counts and the updated-records list back on the sheet.

## Common mistakes

## Escalate when
- Changes affecting closed financial periods or commissions - Finance/Sales Ops approval first.
