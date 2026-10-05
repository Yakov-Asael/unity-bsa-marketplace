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

## How we resolve it
- **Move an opportunity - Advertiser:** if **live** (`Go Live Date` not null) check the destination account has credit and go-live set up; if not live, just move. Then move all open related records: Internal apps, Cases, invoices **not yet approved by Finance**, credit requests.
- **Move an opportunity - Publisher:** move the opp, then all open related records: Internal apps, Cases, bills **not yet approved by Finance**, credit requests.
- Missing from pipeline: requester must be the `Sales_Manager__c` on the account (SSA Integrations hides opps). Lead conversion: leads must be created via the + button process (validation). Package 'rows per region' faults are flow errors fixed centrally.
- **Go live date (Sales) change** (owner feedback 2026-09-22, corrected (owner feedback 2026-09-27, round 3)): a field edit, not an opportunity move - and it must be made **on both records**: `Opportunity.Go_Live_Date_Sales__c` on the account's operational opportunity **and** the go-live date on the Account (`Account.Go_Live_Date__c`). Updating only one leaves the dashboard and the account flags inconsistent. Do not apply the move checklist.
- Restricting how a record type is created (e.g. 'Ads deal desk' = `Opportunity.Mobile_Growth` only from the account) (owner feedback 2026-09-27): a validation rule alone is wrong - it would also fire inside the screen flow `Create_Opportunity_Deal_Ads`. Guard the rule so it exempts the flow path (a flag the flow sets, or the flow's user/context), and block only UI creation from the Opportunities tab.

## What to ask the requester
- Opportunity and target account links?
- Reason for the move (credit sharing? duplicate?)
- Screenshot of the error?

## Canonical answer
**Summary:** The requester wants an opportunity moved, a go-live date changed, a pipeline visibility gap, a lead conversion or 'rows per region' error fixed, or a record-type creation restriction. Most are a single field edit; the known mistake is the move checklist on a go-live date change, or updating `Opportunity.Go_Live_Date_Sales__c` without `Account.Go_Live_Date__c`. SSA Integrations hides opportunities from anyone but the account's `Sales_Manager__c`.
**Suggested resolution:**
1. If go-live date: edit `Opportunity.Go_Live_Date_Sales__c` on the operational opportunity and `Account.Go_Live_Date__c` together; no move checklist.
2. If move: for a live advertiser opportunity (`Go Live Date` not null) confirm credit and go-live on the destination account first; then move the opportunity and its open Internal apps, Cases, invoices or bills not yet approved by Finance, and credit requests.
3. If missing from pipeline: set the requester as `Sales_Manager__c` on the account.
4. If lead conversion fails: recreate the lead through the + button process; 'rows per region' faults are fixed centrally.
5. If a record-type restriction (e.g. `Opportunity.Mobile_Growth` only from the account): guard the validation rule to exempt the screen flow `Create_Opportunity_Deal_Ads`; block only UI creation from the Opportunities tab.
6. If closed-won or revenue-bearing: escalate to Revenue Accounting; bank detail changes to Finance.

## Common mistakes
- Treating a go-live date update as an opportunity move (owner feedback 2026-09-22).
- Updating the go-live date on the opportunity only; the Account field must change too (owner feedback 2026-09-27, round 3).

## Escalate when
- Changes to closed-won deals or revenue-bearing opps - Revenue Accounting.
- Bank detail changes - Finance.
