---
cluster: credit-line-issues
name: Credit line not reflected / credit sharing / prepay
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-17
count_90d: 25
---
## Definition
Approved credit not showing in the dashboard, credit sharing errors, credit removal from parent, prepay switches, account paused for credit.

## Detection signals
- 'credit' in subject
- core id / org id
- uDash link
- Credit_Check__c link
- Example subjects (paraphrased): Approved credit not reflected in the Unity dashboard · Credit sharing request fails between accounts · Remove credit from a parent account for unused orgs

## How we resolve it
- Verify: does the account show a credit amount? If **no amount** → open the latest Credit Check: is the IO signed? If not, is the credit approved? Approved → mark the signed IO; not approved → escalate to Finance.
- Re-sync: on the Account layout, highlighted panel → **Sync Credit** button; the dashboard picks up the credit after the sync.
- Credit sharing needs both accounts on the same finance setup (legal entity, payment terms); align, then retry.
- Credit removal from a parent: detach the listed org IDs from the parent's credit line.
- Prepay switches: set the account prepaid; the client adds a deposit in uDash - the team never adds budget. Handover blocked at ≥90% credit used is by design (`Grow_Ads_Account_Handover` flow) - Finance decides.
- Connect orgs/accounts to a parent's credit line (owner feedback 2026-09-22): this is an **Invoiced With** connection - set `Account.Invoiced_with__c` on each listed org account to the primary (invoicing) account. Requests phrased 'approve RMG and connect to the credit line of X' belong here, not to RWR sync.
- 'Approve RMG and connect these orgs to our credit line' - the whole answer is four steps (owner feedback 2026-10-04, sweep 4): (1) the primary and the secondary org accounts must sit under the **same parent account**; (2) set `Account.Invoiced_with__c` on each secondary org to the primary; (3) tick **Real Money Onboarding** = true and **Real Money IO** = true on the account; (4) that is all - the credit and the RWR flag sync to the dashboard from those fields. No separate approval chain, no Sync Credit needed.
- 'Unhandled fault' while creating a Credit Check (screen flow `New_Credit_Check`) (owner feedback 2026-09-27): the known cause was an over-long value in the account's Website field - the flow failed on the field length. Read the flow error email / `ErrorObject__c` row for the record before answering; fix the field, retry.
- Prepay 'disappeared' after an Invoiced With change (owner feedback 2026-09-27): the prepay follows `Account.Invoiced_with__c`. Check which primary the org's account points to and whether that primary holds the credit; verify in uDash (organization → acquire → finance) whether the org ever had a prepayment - often the requester shared the wrong org. Ask for the org that actually held the prepay.

## What to ask the requester
- Account link and org / core ID?
- Is the credit check Approved and the IO fully signed?
- What does the requester expect to see in uDash (screenshot)?

## Canonical answer
**Summary:** Credit not usable in the dashboard, orgs to connect to a parent's line, a sharing error, a missing prepay, or a Credit Check fault. Orgs share a parent's line through `Account.Invoiced_with__c`.
**Suggested resolution:**
1. If 'approve RMG and connect orgs to our credit line': primary and secondary org accounts need one parent account; set `Account.Invoiced_with__c` on each secondary to the primary; tick **Real Money Onboarding** and **Real Money IO** on the account. Credit and the RWR flag sync from those fields; no Sync Credit needed.
2. If no credit amount: latest `Credit_Check__c` approved but IO unsigned: mark the signed IO; not approved: Finance. Amount present but not in uDash: **Sync Credit** on the Account layout's highlighted panel.
3. If sharing fails: align legal entity and payment terms on both accounts.
4. If 'Unhandled fault' in screen flow `New_Credit_Check`: read the `ErrorObject__c` row; known cause: over-long Website value.
5. If a prepay 'disappeared' after an Invoiced With change: it follows `Invoiced_with__c`; confirm in uDash (organization, acquire, finance) the org ever held one.
6. If prepay switch: set the account prepaid; the client adds the deposit in uDash, never the team.
7. Still wrong after all this: Product team, last resort.

## Common mistakes
- Writing an eight-step investigation for an RMG + connect request; the owner's answer is the four steps above (owner feedback 2026-10-04).
- Routing 'connect these orgs to X's credit line' to rwr-real-money-sync; it is an `Invoiced_with__c` connection (owner feedback 2026-09-22).

## Escalate when
- Credit rejected for open balance or poor payment history - Finance ruling required.
- Any request to add budget or top up funds - Finance only.
- Dashboard still wrong after IO check, Sync Credit and Invoiced With are all in order - last resort: approach the Product team for assistance (owner feedback 2026-09-27, round 3).
