---
cluster: invoice-am-retag
name: Re-tag monthly invoices to the new AM
status: confirmed
count_90d: 6
---
## Definition
After a handover, last month's invoices/monthly revenue still point at the old AM and must be re-tagged.

## Detection signals
- 'July invoice needs to be moved'
- list of account links
- Sub_Category User Permissions/Privileges (mis-filed)
- Example subjects (paraphrased): Last month's invoices need to move to the new rep after a handover

## How we resolve it
- Re-tag the monthly revenue / invoice AM field for the listed accounts to the new rep; report any account without an invoice for that month.
- Ask whether the invoice and finance approvers should also change.

## What to ask the requester
- Account links, month, and the new AM?
- Should approvers change too?

## Canonical answer
**Summary:** After a handover, last month's invoice or monthly revenue records still carry the old AM, so the new rep's numbers are wrong. The handover changed the account owner but not records already created, so the AM field is re-tagged by hand, and the invoice and finance approvers do not move with it. It usually arrives mis-filed under Sub_Category User Permissions/Privileges. This cluster is pending approval.
**Suggested resolution:**
1. Confirm the account links, the month and the new AM; if any is missing, ask first.
2. Confirm the account owner already shows the new rep; if not, the handover comes first.
3. Ask whether the invoice and finance approvers should change too; otherwise approvals stay with the old rep.
4. If the month belongs to a closed quarter: stop and escalate, because the re-tag changes commission.
5. For each listed account, set the AM field on that month's invoice or monthly revenue record to the new rep; note accounts with no invoice.
6. If the requester confirmed it: change the approvers on the same records; otherwise leave them and say so.
7. Reply with the accounts re-tagged, those without an invoice, and whether the approvers changed.

## Common mistakes

## Escalate when
- Commission impact for a closed quarter.
