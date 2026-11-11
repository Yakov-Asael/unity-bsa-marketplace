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
- 'Unhandled Fault has occurred in this flow' when creating a credit check on an account. (learned 2026-10-15 from closed cases)
- Error: We could not find any Credit associated with this Advertiser. (learned 2026-11-08 from closed cases)

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
- Automated credit increase requests consider only accounts with no overdue balance; the filter was overdue = 0 and skipped credit (negative) balances, now included. Overdue accounts are excluded by design. (learned 2026-10-14 from closed cases)
- Credit is released automatically only through the Ironclad path: a new opportunity for the new contract, Generate Ads IO, then IO signed and credit approved. (learned 2026-10-14 from closed cases)
- Bulk RMG and credit-line requests: one data loader file with ParentId, Account_Manager__c, Invoiced_with__c and the RWR flags; Invoiced With = the primary, AM = the requesting AM, flags true. (learned 2026-10-14 from closed cases)
- 'Unhandled Fault' when creating a credit check (New_Credit_Check) can be a website value that is too long: ask the requester to shorten the link and resubmit. (learned 2026-10-15 from closed cases)
- Copy existing credit searches by Legal Entity Name and Country; if nothing matches, select the account that holds the credit as Advertiser Network or paste its UA opportunity number. (learned 2026-11-08 from closed cases)

## What to ask the requester
- Account link and org / core ID?
- Is the credit check Approved and the IO fully signed?
- What does the requester expect to see in uDash (screenshot)?

## Canonical answer
**Summary:** Credit not usable in the dashboard, orgs to connect to a parent's line, an automated credit request that did not run, a sharing error, a missing prepay, or a Credit Check fault. Orgs share a parent's line through `Account.Invoiced_with__c`; credit is released automatically only through the Ironclad path.
**Suggested resolution:**
1. If 'approve RMG and connect orgs to our credit line': all org accounts need one parent; set `Account.Invoiced_with__c` on each secondary to the primary, `Account_Manager__c` to the requesting AM, and tick **Real Money Onboarding** and **Real Money IO**. Many orgs: one data loader file with those columns plus `ParentId`.
2. If credit is not released: check it is not already released. New contract: new opportunity, **Generate Ads IO**; IO signed and credit approved release it. Approved but IO unsigned: mark the signed IO; not approved: Finance. Amount present but not in uDash: **Sync Credit**.
3. If the automated credit request did not run: check the overdue balance; overdue accounts are excluded by design.
4. If sharing fails: align legal entity and payment terms on both accounts.
5. If 'Unhandled fault' in `New_Credit_Check`: read the `ErrorObject__c` row; usual cause is an over-long Website value, so the requester shortens it and resubmits.
6. If a prepay 'disappeared' after an Invoiced With change: it follows `Invoiced_with__c`; prepay switch: the client adds the deposit in uDash.
7. Tapjoy dashboard negative despite Salesforce credit: TJ Finance funds it on the Ad Ops request. Still wrong: Product team.

## Common mistakes
- Writing an eight-step investigation for an RMG + connect request; the owner's answer is the four steps above (owner feedback 2026-10-04).
- Routing 'connect these orgs to X's credit line' to rwr-real-money-sync; it is an `Invoiced_with__c` connection (owner feedback 2026-09-22).
- Suggesting a manual credit request or manager changes before checking the overdue balance that made the automation skip the account. (learned 2026-10-14 from closed cases)
- Releasing credit by hand before checking whether it is already released. (learned 2026-10-14 from closed cases)

## Escalate when
- Credit rejected for open balance or poor payment history - Finance ruling required.
- Any request to add budget or top up funds - Finance only.
- Dashboard still wrong after IO check, Sync Credit and Invoiced With are all in order - last resort: approach the Product team for assistance (owner feedback 2026-09-27, round 3).
- Tapjoy dashboard funding (negative balance despite Salesforce credit) is done by TJ Finance on the Ad Ops request: tag them there. (learned 2026-10-15 from closed cases)
