---
cluster: account-structure-parent-merge
name: Account merge / parent change / payment terms
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-17
count_90d: 17
---
## Definition
Duplicate accounts to merge, parent account change requests (PNR), or payment-terms validation and changes.

## Detection signals
- 'merge'
- 'parent'
- Parent_Name_Request__c link
- 'payment terms'
- Example subjects (paraphrased): Merge duplicate accounts · Parent account change request pending · Payment-terms validation error

## How we resolve it
- 'Merge these accounts' - **there is no real merge** (owner feedback 2026-10-04). The org id is the BI Opportunity (`Opportunity.BI_Opportunity__c`) on the account's operational opportunity, so the work is moving records, in one of three shapes: (a) **publisher** merge: move the org's opportunity (the BI Opportunity) to the target account together with every open record (cases, bills not yet approved by Finance, internal apps, credit requests); (b) **advertiser with two org ids** (two BI opportunities), usually for credit sharing: no move - link the secondary to the primary with **Invoiced With** (`Account.Invoiced_with__c`); (c) **advertiser with one org id**: move the opportunity to the requested main account, **moving the credit first** so the account is not stopped, then every other open record. Tell the requester which account is now primary.
- Parent changes go through Parent_Name_Request (PNR) records and are reviewed; expedite only when campaigns are blocked. 'Only ironSource parents selectable' means the general division parent - explain.
- Payment terms are validated: Net 60 for publishers, Net 30 for advertisers; non-standard terms are locked to Finance/Sales Ops - adjust the validation only with their approval.
- New DSP/account structure questions: one account per legal entity; campaigns split across accounts when billing must be separate.
- Legal entity name / billing address change (owner feedback 2026-09-27): an **advertiser with `Credit_Type__c` = Managed needs a signed IO** before the change; any other account can be changed directly. Confirm which account (the case account may be a different legal entity than the one requested).

## What to ask the requester
- Links to both accounts / the PNR record?
- Which account should survive and why?
- Are bills/invoices affected (separate legal entities)?

## Canonical answer
**Summary:** 'Merge these accounts' is never a Salesforce account merge: the org id is the BI Opportunity (`Opportunity.BI_Opportunity__c`), so the work is moving records in one of three shapes. Parent changes go through reviewed `Parent_Name_Request__c` records; payment terms are validated (Net 60 publishers, Net 30 advertisers).
**Suggested resolution:**
1. Confirm which account should be primary; the case account may be a different legal entity.
2. If publisher merge: move the org's opportunity and every open record (cases, bills not yet Finance-approved, internal apps, credit requests) to the target account.
3. If advertiser with two org ids: set `Account.Invoiced_with__c` on the secondary to the primary; nothing moves.
4. If advertiser with one org id: move the credit first so the account is not stopped, then the opportunity and all other open records.
5. If parent change: the `Parent_Name_Request__c` review runs; expedite only when campaigns are blocked.
6. If non-standard payment terms: do not touch the validation; Finance / Sales Ops decide.
7. If billing or legal entity change: a `Credit_Type__c` = Managed advertiser needs a signed IO first; otherwise edit directly.
8. Tell the requester which account is now primary; cross-entity merges with live invoices escalate to Finance / Sales Ops.

## Common mistakes
- Describing a Salesforce account merge for an org consolidation; the records move, nothing merges (owner feedback 2026-10-04).

## Escalate when
- Merges across legal entities with live invoices.
- Any payment-terms exception.
