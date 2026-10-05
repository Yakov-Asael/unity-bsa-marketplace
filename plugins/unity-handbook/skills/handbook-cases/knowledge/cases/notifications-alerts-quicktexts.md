---
cluster: notifications-alerts-quicktexts
name: Notifications, alerts, email templates and quick texts
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-27
count_90d: 16
---
## Definition
Change who receives an alert, alert content/format, Slack/Centro alert fields, email templates, Chatter group names, quick texts.

## Detection signals
- 'alert'
- 'notification'
- 'email'
- 'Quick Text'
- Chatter group
- Example subjects (paraphrased): Add or remove a recipient on an automated email · Change alert content or an email template · Quick texts missing for a team

## How we resolve it
- Recipient changes: edit the flow/email alert recipient list or the public group used by it.
- Content changes: update the email template; Slack alerts that attach the record carry fixed fields - explain what can and cannot change.
- Quick texts: assign the folder/permission for the team's package; team notification tags depend on group membership.
- 'Credit approved' email not received (owner feedback 2026-09-22): flow `Credit_was_Approved_Email_Alert` (on Credit Check) sends the workflow email alerts `Credit_Check_Approved`, `Credit_Check_Approved_Aura_Israel`, `Credit_Check_Approved_Aura_SF` (template `Credit_Check_was_approved`); recipients are the **Credit Check creator** plus fixed users - a requester who did not create the Credit Check gets nothing. Fix = add them as recipient / have the AM create the check; also check the user's email deliverability.
- Always open the metadata repo for alert questions (`workflows/<Object>.workflow-meta.xml` alerts, `flows/` emailAlert / emailSimple actions) and name the alert; search u-know for the alert's documentation when available.
- New notification for a case origin (e.g. 'email me when a case is created with Origin = Slack, all divisions') (owner feedback 2026-09-27): clone the existing per-team case alert (flow or workflow email alert) with the Origin condition; confirm the recipient per division with the requester before activating.

## What to ask the requester
- Which alert / template (name or example email)?
- Who should receive it and for which record types?

## Canonical answer
**Summary:** An alert or automated email is missing, reaches the wrong people, needs new content, or a new rule is wanted. The template carries the content, the alert definition or a public group the recipients, and usually the requester is not in it. Name the alert; a generic 'check recipient logic' reply is the known mistake.
**Suggested resolution:**
1. Get the alert or template name; find the matching workflow email alert (`workflows/<Object>.workflow-meta.xml`) or flow `emailAlert` / `emailSimple` action and read its recipient set.
2. If the requester is not a recipient: add them to the alert's recipient list or its public group.
3. If a 'Credit approved' email is missing: flow `Credit_was_Approved_Email_Alert` sends `Credit_Check_Approved`, `Credit_Check_Approved_Aura_Israel` and `Credit_Check_Approved_Aura_SF` to the Credit Check creator plus fixed users; add the requester or have the AM create the check.
4. If content must change: update the email template; Slack/Centro alerts carry fixed record fields.
5. If a notification per case origin: clone the per-team case alert with an Origin condition; confirm recipients per division first.
6. If quick texts are missing: assign the team's package folder and permission.
7. If the alert feeds a SOX control or finance approval: escalate first.

## Common mistakes
- Generic 'check recipient logic' answers without naming the flow / email alert from the metadata repo (owner feedback 2026-09-22).

## Escalate when
- Alerts feeding SOX controls or finance approvals.
