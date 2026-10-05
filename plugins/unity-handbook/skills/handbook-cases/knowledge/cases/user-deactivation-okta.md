---
cluster: user-deactivation-okta
name: User deactivation after Okta removal
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-22
count_90d: 9
---
## Definition
Automated Okta email: a departed user was frozen and needs manual steps before deactivation in Salesforce.

## Detection signals
- Subject starts 'ERROR - User needs further processing'
- Origin EmailToCase
- sender is the Okta integration
- Example subjects (paraphrased): Automated Okta notice: user frozen, needs processing before deactivation

## How we resolve it
- Reassign the departed user's records/approvals (queues, approver fields, open cases) and remove them from groups, then deactivate the user in Salesforce.
- Owner ruling (owner feedback 2026-09-22): the required action is to deactivate the affected user in Salesforce (Setup → Users) once their open records and approver roles are reassigned.

## What to ask the requester
- Nothing - the request is self-contained.

## Canonical answer
**Summary:** Okta removed a departed user and Salesforce froze them; the automated notice ('ERROR - User needs further processing', Origin EmailToCase, from the Okta integration) means the user still owns records or holds queue memberships or approver roles. Open cases would sit with an inactive owner, approvals routed to them would stall, and approver matrix rows naming them would break the SOX-controlled chains for Credit, Invoice, Dispute and Bills. Nothing to ask; the request is self-contained.
**Suggested resolution:**
1. Reassign open cases and other open records owned by the user to the right teammate or queue.
2. Check approver fields pointing at the user, in particular the account Bill / Finance Approver fields; replace the user and reassign records routed to them.
3. If the user sits on a SOX approver matrix row (Credit, Invoice, Dispute, Bills): update the matrix first and keep the evidence - this is the escalation trigger.
4. Remove the user from queues, public groups and Slack/Centro mappings.
5. Setup > Users: deactivate the user; confirm no open records are still owned by them.
6. Close the case; the sender is the Okta integration, so no reply is needed.

## Common mistakes

## Escalate when
- User is an approver on SOX-relevant matrices - update matrices first.
