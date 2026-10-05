---
cluster: am-sync-creative-limit
name: AM change not synced to dashboard (creative limit)
status: confirmed
count_90d: 7
---
## Definition
Account manager / partner manager set in SF is not reflected in the Unity dashboard, so the creative limit stays on.

## Detection signals
- 'Creative Limit'
- 'Sync AM'
- 'dashboard not syncing'
- Example subjects (paraphrased): Creative limit stays on although AM was synced · AM change in SF not reflected in the dashboard

## How we resolve it
- Trigger `Sync AM` on the account again; confirm the partner manager appears in uDash. A known Kraken release incident caused stale syncs - follow the incident channel steps.
- If already synced, ask what the requester expects to see and get a screenshot before changing anything.

## What to ask the requester
- Account link and uDash org link?
- Screenshot of the limit message?

## Canonical answer
**Summary:** The account manager / partner manager saved in Salesforce has not reached the Unity dashboard, so the account is still treated as unmanaged and the creative limit stays on. The Salesforce value is usually right; the **Sync AM** push to uDash did not land, and a known Kraken release incident left syncs stale this way. This cluster is pending approval.
**Suggested resolution:**
1. Open the account and confirm the saved account manager / partner manager is the one the requester expects; if wrong, set it first.
2. Ask for the uDash org link and a screenshot of the limit message; check whether uDash already shows the partner manager.
3. If a Kraken release incident is open: follow the incident channel steps first; a plain re-sync will not recover it.
4. Trigger **Sync AM** on the account; expected result: the partner manager appears in uDash and the creative limit clears.
5. If uDash already shows the manager yet the limit persists: change nothing and ask what the requester expects to see.
6. If still flagged unmanaged after a successful sync: escalate to DSE / platform team. Otherwise ask the requester to refresh and confirm.

## Common mistakes

## Escalate when
- Platform-side flag (unmanaged account) - DSE/platform team.
