---
cluster: new-salesforce-user
name: New Salesforce user
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-17
count_90d: 68
---
## Definition
A new or existing employee asks for a Salesforce login or a copy of a colleague's access.

## Detection signals
- Subject 'New Salesforce User request'
- Sub_Category New User
- Origin Manual (approval flow)
- 'activate ... account'
- Example subjects (paraphrased): New Salesforce User request (approval flow) · Please activate a colleague's SFDC account as ad ops manager · New user for an internal requester

## How we resolve it
- Owner ruling (2026-09-17, superseded 2026-09-22: the owner wants to see the answer, so the cluster now gets a full suggestion): the work is manual: manager approval email, then adding the user to the dedicated Okta group and activating the Salesforce user with the role's profile/permission sets.
- Agent checklist: approval answered → user exists/activated → Okta group membership → permission sets mirrored from the named colleague → closure line 'activated, log in through Okta'.
- Redirects: Sensor Tower and other tools → IT helpdesk catalog; AM change on an account → GTM case form; 'I have access but see nothing' → wrong Lightning app (9 dots → `Aura AM` / `Grow Ads Revenue`).
- Owner procedure (owner feedback 2026-09-22): (1) if the user does not exist in SFDC, add them to the Okta group in Tirith: https://tirith.prd.it.unity3d.com/groups/okta-salesforceIS-1_0_Production-user-manual ; (2) wait until the user is created; if no manager is set, set one (yourself if needed) and submit for approval; (3) once approved, grant access mirroring the similar user the requester named.

## What to ask the requester
- Which role / team, and which colleague's access should be mirrored?
- Has the manager approved (approval email answered)?
- Is the requester connected to Unity Okta?

## Canonical answer
**Summary:** A new or existing employee needs a Salesforce login or a colleague's access mirrored. Nothing is automatic: the Tirith Okta group (`okta-salesforceIS-1_0_Production-user-manual`) creates the Salesforce user, the user record needs a manager before approval can be submitted, and the profile and permission sets are assigned only after approval.
**Suggested resolution:**
1. Look the person up in Setup → Users; get the role, the colleague to mirror and their Okta status.
2. If the ask is Sensor Tower or another tool: IT helpdesk catalog. If an AM change on an account: GTM case form.
3. If the user has access but sees nothing: wrong Lightning app; 9 dots, then `Aura AM` or `Grow Ads Revenue`.
4. If the user is missing in SFDC: add them to the Tirith Okta group and wait for the user record.
5. If the user exists with no manager: set one (yourself if needed) and submit for approval; wait for the manager's answer.
6. Once approved: activate with the colleague's profile and permission sets (sales role: also `belong to mobile sales`) and reply "activated, log in through Okta".
7. If the profile grants admin or finance-approval rights, or the requester is not in Okta: escalate.

## Common mistakes

## Escalate when
- The requester is external / not in Okta.
- The requested profile grants admin-level or finance-approval rights.
