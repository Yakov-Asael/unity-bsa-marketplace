---
cluster: bills-workday-sync
name: Bills / payee accounts not syncing to Workday
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-17
count_90d: 25
---
## Definition
Publisher bills or supplier accounts fail to sync SF→Workday (inactive account, NetSuite ID, wrong flag, wrong subsidiary), or bill approval/credit errors.

## Detection signals
- Bill-######## ids
- 'Workday'/'WD'
- P###### payee ids
- Sub_Category Finance / Technical Issue
- Example subjects (paraphrased): Bills not synced to Workday · Payee account not synced to WD - wrong subsidiary · Error when crediting or approving a bill

## How we resolve it
- Decide first whether the *payee account* is synced: `Account.NetSuit_ID__c`.
- **NetSuit_ID__c not null and a short number** → legacy integration ID. Clear it, set `Account.Finance_Approval_Complete__c` = false, then set it back to true to retrigger the sync (Apex `AccountTriggerHandler.Netsuite_afterUpdate` re-examines the account when `Finance_Approval_Complete__c` flips to true with a billing country present).
- **NetSuit_ID__c null** → check `Finance_Approval_Complete__c`: if false, check `BillingCountryCode`; if a country exists set the flag true (sync fires), if no country tell the requester the billing country is missing.
- **Still null** → the account must be `Payment_method__c` = Tipalti and `Subsidiary__c` = Unity for the WD path; fix and retrigger. `Do_Not_Sync_To_NS__c` = true or `Type` = Internal blocks sync entirely.
- Bill-level blockers: `Bill__c.Approved_Without_Issue__c` wrongly true (set false, re-sync); wrong subsidiary (LE130 vs LE202); stuck approval → recall the process and let the approver retry; old bills → **Approve without an issue** in bulk; bulk nullify → **Nullify Bills** button (template) on the finance home page.
- **Always look up the record in the error objects first** (owner feedback 2026-09-27): `ErrorObject__c` (`RecordIds__c`, `Message__c`, `ClassName__c`) and `Error_Log__c` (`Request_Account_Ids__c`, `Error_Message__c`, `Integration_Name__c`) often hold the exact sync error and give the suggestion directly.
- Sync filters to check on every unsynced bill (owner feedback 2026-09-27): `Bill__c.Approved_Without_Issue__c` = false, the bill's Workday/NetSuite id (`Netsuit_ID__c`) not null, bill approval status = Approved by Finance, and the payee account synced to Workday. A payee account without `Department__c` = Publisher does not sync - that was the cause in the graded case.

## What to ask the requester
- Bill numbers and payee (P-number) affected?
- What is the exact error text from WD or SF?
- Which legal entity should the payee be under?

## Canonical answer
**Summary:** A publisher bill missing in Workday usually means its payee account is not synced: a stale legacy `Account.NetSuit_ID__c`, `Finance_Approval_Complete__c` false, a missing billing country, or a wrong path field (`Payment_method__c` Tipalti, `Subsidiary__c` Unity, `Department__c` Publisher). Apex `AccountTriggerHandler.Netsuite_afterUpdate` re-syncs when the flag flips to true with a billing country; `Do_Not_Sync_To_NS__c` = true or `Type` = Internal blocks it.
**Suggested resolution:**
1. Look the bill and account up in `ErrorObject__c` (`RecordIds__c`, `Message__c`) and `Error_Log__c` (`Request_Account_Ids__c`, `Error_Message__c`) first; the message often names the fix.
2. If `NetSuit_ID__c` is a short number: clear it, set `Finance_Approval_Complete__c` false, then true again.
3. If `NetSuit_ID__c` is null with a `BillingCountryCode`: set `Finance_Approval_Complete__c` true; no country: ask the requester for it.
4. If still null: fix the path fields above or `Do_Not_Sync_To_NS__c` / `Type`, then retrigger the same way.
5. On each unsynced bill: `Bill__c.Approved_Without_Issue__c` false, correct subsidiary (LE130 vs LE202), status Approved by Finance; recall a stuck approval so the approver retries.
6. If old bills must be cleared: **Approve without an issue** in bulk, or the **Nullify Bills** button on the finance home page.
7. Bills show in Workday within about ten minutes. Inactive Workday account: Finance/AP; cost-center mapping errors: Workday team.

## Common mistakes
- Answering a 'fraud deduction breakdown by app' request from the bill lines; the split lives in BigQuery (see reports-and-list-views) (owner feedback 2026-10-04).

## Escalate when
- Workday reports the account inactive - Finance/AP must activate it first.
- Cost-center mapping errors - Workday team.
- Mass sync failure across a division (9K+ bills).
