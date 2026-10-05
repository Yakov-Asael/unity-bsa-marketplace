---
cluster: new-ironclad-user
name: New Ironclad user
status: confirmed
count_90d: 13
---
## Definition
Requester needs an Ironclad login (contracts / IO signing / release forms).

## Detection signals
- Subject 'New Ironclad User request'
- Sub_Category User Permissions/Privileges
- Origin Manual
- Example subjects (paraphrased): New Ironclad User request · Ironclad permission to upload contracts

## How we resolve it
- Add the user to the Ironclad group matching their role (e.g. Grow Legal Team for legal reviewers); access is via Okta.
- If someone on the team already has the New/upload button, permissions are group-based - mirror that group.

## What to ask the requester
- Do they need to review/sign on behalf of legal, or only initiate/upload?

## Canonical answer
**Summary:** The requester has no Ironclad login, or cannot see the New/upload button for contracts, IO signing or release forms. Ironclad permissions are group-based and login goes through Okta, so the case is a group assignment matching the requester's role (legal reviewers sit in Grow Legal Team), not an account creation. Signing on behalf of legal is a separate signatory right we do not grant. This cluster is pending approval.
**Suggested resolution:**
1. Ask whether the requester needs to sign on behalf of legal or only initiate/upload; upload-only is a routine group add.
2. Ask whether a teammate already has the New/upload button; if so, mirror that group.
3. If no teammate is named: add the requester to the Ironclad group matching their role (Grow Legal Team for legal reviewers).
4. If the requester already has a login: the missing button means their group lacks the right; move them to the correct one.
5. If the role has no matching group, or signing on behalf of legal is requested: grant only initiate/upload and escalate the signatory part.
6. Send the requester: added to the Ironclad group for your role - log in through Okta and New/upload will appear.

## Common mistakes

## Escalate when
- Legal signatory rights.
