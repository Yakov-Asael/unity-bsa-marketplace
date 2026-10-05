---
cluster: case-management-config
name: Support case process configuration
status: confirmed
count_90d: 13
---
## Definition
Changes or bugs in how support cases behave: milestones, auto-close, assignment rules, reopened cases, record-type fields, division freezes.

## Detection signals
- 'tickets'
- 'Milestone'
- 'assignment'
- record type field
- Supersonic freeze/switch
- Example subjects (paraphrased): Support tickets not auto-closing or missing milestones · Ticket assignment rules for a team · Fields missing on a support record type

## How we resolve it
- Milestone/auto-close problems: review the entitlement and the 21-day close flow; fix the logic and monitor.
- Assignment changes: update assignment rules / queue membership; reassign open tickets in bulk when an owner changes.
- Record-type field gaps: add the field to the page layout and picklist values for that record type.
- Division freezes/switches (e.g. subsidiary migration): validation rules blocking edits for a date window, then bulk update.
- Status jumps after a post/comment (e.g. to 'On DSE' while Pending Customer) (owner feedback 2026-09-22): **open the metadata repo before answering** - `flows/Case_Update_Status_when_case_comment_is_created` (comment → Pending Customer / other status by author type), feed-item and email-message flows on Case, assignment rules and Omni/queue routing; read the case's Status history for the automation user that made the change. In the 2026-09 metadata copy no active Case flow sets 'On DSE' - so check queue routing and any Slack/Centro handler next.

## What to ask the requester
- Example ticket numbers showing the problem?
- Which record type / queue?
- Desired behavior in one sentence?

## Canonical answer
**Summary:** Support cases misbehave - missing milestones, no auto-close, wrong assignment, a status jump after a comment, missing record-type fields, or edits blocked in a division freeze. Each maps to one mechanism in the metadata repo (flow, assignment rule, page layout, validation rule); name it before answering. This cluster is pending approval.
**Suggested resolution:**
1. Get example ticket numbers, the record type / queue and the desired behavior in one sentence.
2. If milestones / auto-close: review the entitlement and the 21-day close flow; fix and monitor.
3. If assignment: update the assignment rules / queue membership; bulk-reassign open tickets when an owner changes.
4. If a status jumped after a comment: read `Case_Update_Status_when_case_comment_is_created` and the feed-item / email-message flows, then the Status history for the automation user. 'On DSE' is set by no active Case flow: check queue routing and any Slack/Centro handler.
5. If a record-type field is missing: add it to that record type's page layout and enable its picklist values.
6. If a division freeze or switch: add a validation rule for the date window, then bulk update after it.
7. SLA definition changes: support leadership; cross-division routing changes also escalate.

## Common mistakes
- Answering an automation question without inspecting the metadata repo (flows, workflow rules, validation rules) and naming the mechanism (owner feedback 2026-09-22).

## Escalate when
- Changes to SLA definitions - support leadership.
- Cross-division routing changes.
