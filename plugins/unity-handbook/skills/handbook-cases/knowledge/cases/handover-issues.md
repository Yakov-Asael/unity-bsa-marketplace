---
cluster: handover-issues
name: Handover (HO) fails, rejected or misrouted
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-17
count_90d: 23
---
## Definition
A handover request is auto-rejected, cannot be submitted, shows an unexpected form, needs cancelling, or the AM change did not apply.

## Detection signals
- 'HO'/'handover'
- Hand_Over__c link
- 'auto rejected'
- 'open case' rule
- wrong app layout
- Example subjects (paraphrased): Handover auto-rejected on submit · Cannot hand over an account (error or wrong layout) · Cancel or reverse an approved handover
- Handover requests cannot be created for iAds accounts while uAds and Tapjoy requests go through. (learned 2026-10-14 from closed cases)

## How we resolve it
- Analyze the HO record against the flow chain (owner ruling: the answer is an analysis of the handover flow for the shared record; if none was shared, ask for the Hand_Over__c link).
- Intake screen flow `Grow_Ads_Account_Handover`: for handovers **to SMB** (new owner = the BA integration user, type AM) it stops when the account has an **open case** (`Get_account_open_cases` non-blank; Pending Customer counts) or **`Credit_Percentage_Used__c ≥ 90`**; a **duplicate HO of the same type in progress** stops with 'You can create a new request once it is completed or rejected'.
- Approval process `Grow_HO_Process`: entry needs `Current_Manager__c`; steps = current manager → new manager (if different from submitter's chain) → senior manager when `Quota_Shift_Needed__c` = Yes; a step rejection sets Status Rejected and alerts the creator. Inactive/missing managers route via the `Approver_exist` branch.
- Flow `Handover_Reject_Automatically_after_open_for_30_days`: rejects approvals open >30 days via platform event `Approve_Submit_Reject_Approval_Process__e` - 'auto-rejected' often means it sat unapproved.
- Validation rules: `Cant_Modify_Account_Finance_fields` (account synced to NetSuite and Legal Entity / Billing Country / Payment Terms on the HO differ from the account → cannot submit; also enforced in Apex `HandOverSubmit`), `Hand_Over_Prevent_editing_submitted_HO`, `Block_HO_Creation_for_accounts_by_id`, Aura `Age_to_reach_credit_limits`.
- UI: no HO button / wrong form → wrong Lightning app (9 dots → `Grow Ads Revenue`). Approved AM changes apply next day ~11:00 (`HandOver_Update_new_owner_on_transfer_date`).
- If the AM could not create the handover, move the accounts to the new AM directly and ask for a screenshot of the HO error. (learned 2026-10-14 from closed cases)
- A handover with a future effective date stays pending until that date; if the AM needs it sooner (credit alerts), approve and apply it now. (learned 2026-10-14 from closed cases)
- To apply a pending or not-yet-approved handover now, set Account.Account_Manager__c to the new AM directly and mark the Hand_Over__c Status Completed so the transfer-date flow does not re-apply it. (learned 2026-10-15 from closed cases)

## What to ask the requester
- Hand_Over__c link and the error text or screenshot?
- Is there an open case on the account?
- Which app is the requester using?

## Canonical answer
**Summary:** A `Hand_Over__c` request is auto-rejected, cannot be created or submitted, is pending, or the approved AM change has not applied. `Grow_Ads_Account_Handover` blocks handovers to SMB on an open case or `Credit_Percentage_Used__c` of 90 or more; `Grow_HO_Process` cannot route without `Current_Manager__c`; `Handover_Reject_Automatically_after_open_for_30_days` rejects anything open over 30 days.
**Suggested resolution:**
1. Get the `Hand_Over__c` link and error text; ask if missing.
2. If no HO exists because it could not be created (seen on iAds accounts): move the accounts to the new AM directly and ask for a screenshot of the error.
3. If a duplicate HO is in progress: wait for it to complete or reject.
4. If the new owner is SMB: clear the open case and resubmit; `Credit_Percentage_Used__c` 90 or more: Finance.
5. If synced to NetSuite: align Legal Entity, Billing Country and Payment Terms with the account.
6. If `Current_Manager__c` is empty or inactive: set an active manager and resubmit.
7. If pending (future effective date or not yet approved) and needed now: set `Account.Account_Manager__c` to the new AM and mark the `Hand_Over__c` Status Completed so the transfer-date flow does not re-apply it.
8. If rejected after 30 days: resubmit. Form missing: switch the app to `Grow Ads Revenue`. Approved but unchanged: `HandOver_Update_new_owner_on_transfer_date` applies it next day around 11:00.

## Common mistakes

## Escalate when
- Bulk transfers across teams (use the bulk data-fix process).
- Disputes over who should own an account.
