---
cluster: commission-hierarchy-team
name: Commission data / TL view / team hierarchy
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-27
count_90d: 13
---
## Definition
Missing people under a team leader's view, wrong team assignment, or commission numbers not matching after handovers.

## Detection signals
- 'TL view'
- 'Commission'
- 'team'
- 'hierarchy'
- Sub_Category Commissions
- Example subjects (paraphrased): Add a rep under their manager's TL view · Commission numbers missing after handovers · Add a user to a sales team

## How we resolve it
- TL view / hierarchy: update the user's manager/team fields (keep a backup of the previous hierarchy) - payout processes depend on it.
- Team membership for commission: add the user to the correct team record; teams and managers may differ from Workday - confirm.
- Missing commission data after a mid-period handover: spend sits with one AM; the dashboard corrects on refresh.
- Owner rule (owner feedback 2026-09-27): a TL (CM role) sees a team member in the commission tab **only when that member sits under the TL in the Salesforce hierarchy** (manager / role). Put the user under the TL; the `Commission_Line__c.Is_my_Team_Reports__c` formula then returns true.

## What to ask the requester
- User and manager names, team, effective quarter?
- Is this for the current payout cycle (urgent)?

## Canonical answer
**Summary:** A TL cannot see a rep in the commission tab or numbers are off after a handover. The TL view is not sharing: a TL (CM role) sees a member only when that member sits under the TL in the Salesforce hierarchy (manager / role), which `Commission_Line__c.Is_my_Team_Reports__c` evaluates. Team membership for commission is a separate record; both may differ from Workday.
**Suggested resolution:**
1. Get user and manager names, team and effective quarter; current payout cycle means urgent.
2. If the change alters a closed quarter's payout: stop and escalate to Sales Ops.
3. Note the previous manager / role and team first; payout processes depend on the hierarchy.
4. Move the user under the TL in the Salesforce hierarchy (manager / role); expected result: `Is_my_Team_Reports__c` turns true on their commission lines.
5. Add the user to the correct team record; confirm with the requester rather than copying Workday.
6. If numbers are off after a mid-period handover: spend sits with one AM until the dashboard refreshes; re-check before correcting manually.
7. Tell the requester the user is now under their hierarchy and on the team; the commission tab shows them after the next refresh.

## Common mistakes

## Escalate when
- Any change that alters a closed quarter's payout - Sales Ops.
