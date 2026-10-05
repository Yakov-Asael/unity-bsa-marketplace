---
cluster: ironclad-io-generation
name: IO generation via Ironclad fails
status: confirmed
count_90d: 6
---
## Definition
Generate Ads IO from the opportunity/account pulls empty entity/signer info or cannot pull from Salesforce; Ironclad workflow problems.

## Detection signals
- 'IO'
- 'Ironclad'
- 'Generate Ads IO'
- entity/legal name empty
- Example subjects (paraphrased): Generate Ads IO shows empty entity / signer info · Cannot pull from Salesforce inside Ironclad

## How we resolve it
- Recurring integration bug: entity and signer fields empty when generating from the opportunity - fix applied centrally; ask the requester to retry.
- Workaround: initiate the workflow from the account (legal entity change) instead of the opportunity.
- Legal entity name changes follow the documented knowledge-hub process; do not edit ad hoc.

## What to ask the requester
- Opportunity / account link and a screenshot of the empty step?

## Canonical answer
**Summary:** Generate Ads IO from the opportunity opens the Ironclad workflow with the entity and signer fields empty, or Ironclad cannot pull the record from Salesforce. The empty-field case is a recurring Salesforce-Ironclad integration bug on the opportunity path; a fix was applied centrally, and the account path (legal entity change) pulls the same data and works. This cluster is pending approval.
**Suggested resolution:**
1. Get the opportunity or account link and a screenshot of the empty step; it separates the bug from a missing entity.
2. Check the account's legal entity name in Salesforce. If missing or wrong: route the change through the documented knowledge-hub process; never edit it ad hoc.
3. If the entity is present and the workflow started from the opportunity: ask the requester to retry Generate Ads IO; the central fix usually works.
4. If the retry still shows empty fields: have them start the workflow from the account (legal entity change) instead.
5. If Ironclad shows its own workflow error: collect the screenshot and hand the case to Legal Ops.
6. Send the requester: known integration issue, fixed centrally - retry Generate Ads IO, or start from the account if fields stay empty.

## Common mistakes

## Escalate when
- Ironclad-side workflow errors - Legal Ops.
