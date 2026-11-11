---
cluster: dispute-adjustments
name: Dispute record changes
status: confirmed
count_90d: 11
---
## Definition
A dispute needs its type/reason changed, to be re-attached to a different invoice/bill, recalled or cancelled, or is not reflecting on the invoice.

## Detection signals
- 'dispute' in subject
- Dispute__c links
- Sub_Category Finance / Finance Issue
- Example subjects (paraphrased): Change a dispute's type or reason · Re-attach a dispute to a different invoice or bill · Cancel or recall a dispute

## How we resolve it
- Type/reason changes: edit the dispute fields directly (requesters cannot after submission).
- Re-attaching: link the dispute to the correct invoice/bill; if the invoice was not yet sent for approval no recall is needed - cancel instead.
- 'Deduction not reflected': verify the invoice balance; a colleague may have reverted the deduction.
- Deal Payment object is deprecated - use disputes; questions go to Revenue Accounting.
- Approval blocked with 'You can't approve this dispute before you credit <invoice>': the guard is the active flow `Dispute_remove_invoice_when_rejected_by_finance`, which checks `Invoice__r.Credit_Date__c`. Credit the invoice first, then approve; if the dispute points at the wrong invoice, re-attach it.
- **Consult the team leader before crediting an invoice or re-attaching a dispute** (owner feedback 2026-09-27) - these change finance records.
- A dispute opened on a secondary account does not attach to the primary invoice. Move it to the primary, then mark it for the next cycle or pick the open invoice and send to Finance to credit and reissue. (learned 2026-10-14 from closed cases)
- A dispute with reason Advertisers numbers cannot be approved without the client numbers screenshot: attach it in Notes & Attachments on the dispute. (learned 2026-10-15 from closed cases)
- A requester who cannot submit a dispute to Finance needs the dispute owner or team leader to submit it; Finance only processes submitted disputes. (learned 2026-10-15 from closed cases)
- An invoice generated with tax by mistake: Finance credits it and a new invoice is generated without tax. (learned 2026-10-15 from closed cases)
- A dispute attached by hand to an already-approved invoice routes to finance approval; re-tick the attach-to-next-invoice flag and detach it so it attaches automatically to the next invoice. (learned 2026-09-30 from closed cases)
- Dispute__c needs the client numbers screenshot under Notes and Attachments before it can be approved; reason, year and correction period are edited only after the dispute is reopened or approved. (learned 2026-11-08 from closed cases)
- Supply deal disputes blocked from Send to BI: edit validation rule Cant_Change_Send_to_bi_when_supply_deal on Dispute__c and remove the Send to BI condition. (learned 2026-11-08 from closed cases)

## What to ask the requester
- Dispute link and the target invoice/bill?
- Cancel completely or just recall?
- Should the deduction land on the next cycle, or on the activity month's invoice through a Finance credit and reissue? (learned 2026-10-14 from closed cases)
- Ask for a screenshot of the error shown by the send-to-BI tool on the Business Operations page. (learned 2026-11-08 from closed cases)

## Canonical answer
**Summary:** A `Dispute__c` record needs a type or reason change, a different invoice or bill, a cancel or recall, Finance submission, or its deduction is missing from the invoice. Requesters cannot edit after submission. "You can't approve this dispute before you credit <invoice>" comes from `Dispute_remove_invoice_when_rejected_by_finance` reading an empty `Invoice__r.Credit_Date__c`. Disputes opened on a secondary (Invoiced With) account never attach to the primary's invoice.
**Suggested resolution:**
1. Open the `Dispute__c` and its linked invoice or bill, and read the dispute's Chatter.
2. Type or reason change: edit it and confirm. Reason Advertisers numbers needs the client screenshot in Notes & Attachments before approval.
3. Opened on a secondary account: move it to the primary, then ask: next cycle, or the activity month's invoice through a Finance credit and reissue.
4. Re-attach: consult the team leader, link the correct invoice or bill; never sent for approval: cancel instead.
5. Not submitted to Finance: the dispute owner or team leader submits it; Finance processes only submitted disputes.
6. Credit block: with the team leader, credit the invoice, then approve. Invoice generated with tax by mistake: Finance credits it and a new invoice is generated without tax.
7. Cancel or recall: ask which. Already synced to Finance: AR credit process.

## Common mistakes
- Crediting or re-attaching without the team leader's OK (owner feedback 2026-09-27).
- Opening a dispute on an agency's secondary (Invoiced With) account instead of the primary. (learned 2026-10-14 from closed cases)

## Escalate when
- Approved disputes already synced to Finance - AR credit process.
