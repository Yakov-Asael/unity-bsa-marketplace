---
cluster: opportunity-lead-changes
name: Opportunity / lead record changes
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-17
count_90d: 18
---
## Definition
Move an opportunity to another account, change company/bank/legal-entity info, go-live date, pipeline visibility, lead conversion or app-approval rows.

## Detection signals
- 'move opportunity'
- Opportunity link
- 'lead'
- 'convert'
- 'rows per region'
- Example subjects (paraphrased): Move an opportunity to a different account · Change company / bank / legal-entity details on an opportunity · Lead conversion or app-approval rows failing
- Create Deal button missing in one app (CTV) or an error on submitting an Aura deal from the Aura Sales app. (learned 2026-10-15 from closed cases)

## How we resolve it
- **Move an opportunity - Advertiser:** if **live** (`Go Live Date` not null) check the destination account has credit and go-live set up; if not live, just move. Then move all open related records: Internal apps, Cases, invoices **not yet approved by Finance**, credit requests.
- **Move an opportunity - Publisher:** move the opp, then all open related records: Internal apps, Cases, bills **not yet approved by Finance**, credit requests.
- Missing from pipeline: requester must be the `Sales_Manager__c` on the account (SSA Integrations hides opps). Lead conversion: leads must be created via the + button process (validation). Package 'rows per region' faults are flow errors fixed centrally.
- **Go live date (Sales) change** (owner feedback 2026-09-22, corrected (owner feedback 2026-09-27, round 3)): a field edit, not an opportunity move - and it must be made **on both records**: `Opportunity.Go_Live_Date_Sales__c` on the account's operational opportunity **and** the go-live date on the Account (`Account.Go_Live_Date__c`). Updating only one leaves the dashboard and the account flags inconsistent. Do not apply the move checklist.
- Restricting how a record type is created (e.g. 'Ads deal desk' = `Opportunity.Mobile_Growth` only from the account) (owner feedback 2026-09-27): a validation rule alone is wrong - it would also fire inside the screen flow `Create_Opportunity_Deal_Ads`. Guard the rule so it exempts the flow path (a flag the flow sets, or the flow's user/context), and block only UI creation from the Opportunities tab.
- A Finance validation blocks changing the country on publishers of an Israeli legal entity. It is SOX-relevant: never edit or bypass it without Finance and Tax approval. (learned 2026-10-14 from closed cases)
- To restrict an Opportunity record type to the account-side flow, use a validation rule; users with the Deal Desk permission set bypass it, so confirm with the requester who holds that set. (learned 2026-10-14 from closed cases)
- Deal Desk restriction rule on Opportunity: RecordType Mobile_Growth AND ISNEW() AND Finance_Approver__c blank AND NOT the skip-validations permission; the message sends users to the account Create Deal button. (learned 2026-10-15 from closed cases)
- Closed-won deals resubmitted for approval by mistake: confirm in the approval history they were already fully approved, then cancel the new approval request. (learned 2026-10-15 from closed cases)
- Create Deal missing or failing on submit for CTV or Aura: add the Create Deal button to the CTV account page layout and add the missing allowed value to the deal validation rule. (learned 2026-10-15 from closed cases)

## What to ask the requester
- Opportunity and target account links?
- Reason for the move (credit sharing? duplicate?)
- Screenshot of the error?
- Is this a true change of legal entity? Tax needs the new entity registration letter, tax id and full address; a new entity may need a new publisher on the platform. (learned 2026-10-14 from closed cases)

## Canonical answer
**Summary:** The requester wants an opportunity moved, a go-live date changed, a pipeline visibility gap, a lead conversion fixed, a Create Deal or approval problem solved, or a record-type creation restriction. Most are a single field edit; the known mistake is the move checklist on a go-live date change, or updating `Opportunity.Go_Live_Date_Sales__c` without `Account.Go_Live_Date__c`. SSA Integrations hides opportunities from anyone but the account's `Sales_Manager__c`.
**Suggested resolution:**
1. If go-live date: edit `Opportunity.Go_Live_Date_Sales__c` on the operational opportunity and `Account.Go_Live_Date__c` together; no move checklist.
2. If move: for a live advertiser opportunity confirm credit and go-live on the destination first; then move the opportunity with its open Internal apps, Cases, unapproved invoices or bills, and credit requests.
3. If missing from pipeline: set the requester as `Sales_Manager__c` on the account.
4. If lead conversion fails: recreate the lead through the + button process.
5. If Create Deal is missing or fails (CTV, Aura): add the button to the CTV account page layout, or the missing allowed value to the deal validation rule.
6. If closed-won deals were resubmitted for approval by mistake: confirm in the approval history they were fully approved, then cancel the new request.
7. If a record-type restriction: validation rule on `Mobile_Growth` with `ISNEW()`, blank `Finance_Approver__c` and NOT the skip-validations permission, pointing users to the account's Create Deal button; Deal Desk holders bypass it.
8. Closed-won revenue changes: Revenue Accounting; bank details: Finance.

## Common mistakes
- Treating a go-live date update as an opportunity move (owner feedback 2026-09-22).
- Updating the go-live date on the opportunity only; the Account field must change too (owner feedback 2026-09-27, round 3).

## Escalate when
- Changes to closed-won deals or revenue-bearing opps - Revenue Accounting.
- Bank detail changes - Finance.
- Country or legal-entity change on an Israeli entity: Finance and Tax decide; keep the case pending until they approve. (learned 2026-10-14 from closed cases)
