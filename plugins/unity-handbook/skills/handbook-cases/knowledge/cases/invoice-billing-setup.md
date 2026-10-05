---
cluster: invoice-billing-setup
name: Invoice generation errors and billing setup
status: confirmed
count_90d: 15
---
## Definition
Advertiser invoices fail to generate or carry wrong data (view type, BI opportunity, subsidiary, amounts), or billing must be split across entities.

## Detection signals
- INV-######### ids
- 'invoice view type ... Detailed'
- 'BI opportunity'
- 'billing split'
- Example subjects (paraphrased): Invoices not generated - invoice view type must be Detailed · Invoice failed with a governor-limit error · Split billing between two legal entities

## How we resolve it
- Generation failures: set the account's invoice view type to Detailed and regenerate; for governor-limit errors (aggregate rows, collection size) apply the manual workaround and log the bug.
- Wrong BI opportunity on the account: clear the stale value; the correct BI opp is usually already tagged on another opp.
- Separate billing: one account per legal entity, campaigns split between them; 'Send bill per BI opportunity' keeps bills separate on one account.
- Amount mismatches vs Workday: credit and reissue the invoice.
- Blank invoice emails: verify the billing contact addresses on the account.

## What to ask the requester
- Invoice numbers (INV-) and account link?
- Exact error text?
- Which legal entity should be billed?

## Canonical answer
**Summary:** An advertiser invoice did not generate or carries the wrong view type, BI opportunity, subsidiary or amount, or billing must be split across legal entities. Generation reads the account's billing setup (view type, BI opportunity, billing contacts, legal entity), so a stale value repeats on every invoice until corrected; large accounts can also hit governor limits. This cluster is pending approval.
**Suggested resolution:**
1. Get the INV- numbers, account link and error text; ask if missing.
2. If invoices did not generate: set the account's invoice view type to Detailed and regenerate.
3. If the error mentions aggregate rows or collection size: apply the manual workaround and log the bug; repeats on the same account go to development.
4. If the BI opportunity is wrong: clear the stale value on the account, copy the correct one from the opportunity already tagged, regenerate.
5. If billing must be split: one account per legal entity, campaigns split; for separate bills on one account, enable 'Send bill per BI opportunity'.
6. If the amount differs from Workday: credit and reissue; corrections after issuance go to Finance/AR.
7. If the invoice email is blank: fix the billing contact addresses on the account.

## Common mistakes

## Escalate when
- Amount corrections after issuance - Finance/AR.
- Repeated governor-limit failures - development fix.
