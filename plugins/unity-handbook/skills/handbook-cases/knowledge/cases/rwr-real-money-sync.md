---
cluster: rwr-real-money-sync
name: RWR / real-money onboarding sync
status: confirmed
count_90d: 9
---
## Definition
Real-money (RWR/RMG) addendum signed but flag not synced to the dashboard, or RWR onboarding request errors.

## Detection signals
- 'RWR'
- 'RMG'
- 'real money'
- Internal_Request__c link
- Example subjects (paraphrased): RWR addendum signed but not synced to the dashboard · RWR onboarding request error · Turn on RMG for an org

## How we resolve it
- Check the Ironclad addendum exists; the real-money flag is set by the onboarding form (button on the account) - complete/mark it and the dashboard syncs.
- Onboarding request validation errors: fix the Internal Request record and let the requester retry.

## What to ask the requester
- Account link and org ID?
- Was the onboarding form submitted after signing?

## Canonical answer
**Summary:** A real-money (RWR/RMG) addendum was signed but the flag has not reached the dashboard, or the onboarding request errors. The signature does not set the flag; the onboarding form from the button on the account does, and that request is an `Internal_Request__c` record with validation, so an unsubmitted or failing form leaves the flag unset. This cluster is pending approval.
**Suggested resolution:**
1. Ask for the account link and org ID, and whether the onboarding form was submitted after signing.
2. Confirm the Ironclad addendum exists. If missing: do not set the flag; it must be signed in Ironclad first.
3. If the form was not completed: complete or mark it from the button on the account; the flag sets and the dashboard syncs.
4. If the onboarding request is in error: fix the failing field on the `Internal_Request__c` record linked from the case; let the requester retry.
5. If the ask is 'approve RMG and connect to a credit line': that is a credit-line issue on `Account.Invoiced_with__c` (credit-line-issues cluster), not an RWR flag.
6. If the flag is set in Salesforce but not on the dashboard: hand to the BI/platform team with the account and org ID.

## Common mistakes
- 'Approve RMG and connect to a credit line' requests are credit-line-issues (`Account.Invoiced_with__c`), not an RWR flag problem (owner feedback 2026-09-22).

## Escalate when
- Dashboard-side flag issues - BI/platform team.
