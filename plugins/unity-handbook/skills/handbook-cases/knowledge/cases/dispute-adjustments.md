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

## What to ask the requester
- Dispute link and the target invoice/bill?
- Cancel completely or just recall?

## Canonical answer
**Summary:** A `Dispute__c` record needs a type or reason change, a different invoice or bill, a cancel or recall, or its deduction is not showing on the invoice. Requesters cannot edit after submission; every variant touches a finance record. The block "You can't approve this dispute before you credit <invoice>" comes from the flow `Dispute_remove_invoice_when_rejected_by_finance` reading an empty `Invoice__r.Credit_Date__c`. This cluster is pending approval.
**Suggested resolution:**
1. Open the shared `Dispute__c` record and note the linked invoice or bill; ask if neither was shared.
2. Type or reason change: edit the fields on the dispute and confirm with the requester.
3. Re-attach: consult the team leader, then link the dispute to the correct invoice or bill; if it was never sent for approval, cancel instead.
4. Cancel or recall: ask whether it should go completely (cancel) or only be pulled back (recall).
5. Credit block: consult the team leader, credit the invoice, then approve; if the block names the wrong invoice, re-attach instead.
6. Deduction not reflected: check the invoice balance; a colleague may have reverted it; consult the team leader before re-applying.
7. If already synced to Finance: AR credit process. Deal Payment questions: Revenue Accounting.

## Common mistakes
- Crediting or re-attaching without the team leader's OK (owner feedback 2026-09-27).

## Escalate when
- Approved disputes already synced to Finance - AR credit process.
