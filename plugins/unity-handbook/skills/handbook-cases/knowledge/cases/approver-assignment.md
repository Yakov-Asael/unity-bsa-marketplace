---
cluster: approver-assignment
name: Approver / approval-matrix assignment
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-17
count_90d: 24
---
## Definition
An invoice, bill, dispute, credit check, payment-terms or handover approver is missing, inactive or wrong; approver matrices need updating.

## Detection signals
- 'approver'
- 'Approval Matrix'
- 'cannot submit ... for approval'
- departed employee still routed
- Example subjects (paraphrased): Cannot submit invoices - no account or finance approver · Update approver matrix after an employee left · Change payment / dispute approver for an account

## How we resolve it
- 'No approver defined' means the approver matrix did not catch the record. Suggest to the agent: set the **Bill Approver** and/or **Finance Approver** on the account (both if both blank) - and find out why: the mapped user is inactive, or the matrix has no row for this payment approver (invoices/bills), or for disputes no row in the dispute matrix for that team + manager + type.
- Invoice approver change for an AM's book (owner feedback 2026-10-04): two checks only - (1) who is the **payment approver** on the accounts (`Account.Payment_approver_User__c`) and does it need to change; (2) does the **new approver have a row in the Approver Matrix object for Invoice**. Add the row and update the accounts; nothing else.
- Departed approver: replace in every matrix row and reassign records already routed to them.
- Invoices cannot be submitted before the 3rd of the month - a date rule, not an approver problem; tell the requester to retry after the 3rd.
- Delegated approvals: set the requester as delegated approver for the absent approver.

## What to ask the requester
- Which object (invoice, bill, dispute, credit check, payment terms, handover) and which account/division?
- Who should the new approver be, and has that person's manager agreed?

## Canonical answer
**Summary:** 'No approver defined' means the approver matrix did not catch the record: **Bill Approver** / **Finance Approver** is blank on the account, the mapped user is inactive, or no matrix row exists for that payment approver (invoices / bills) or that team + manager + type (disputes).
**Suggested resolution:**
1. Identify the object and the account or division; the matrix differs per object.
2. If invoice approver change for an AM's book, two checks only: does `Account.Payment_approver_User__c` on the accounts need to change, and has the new approver a row in the Approver Matrix object for Invoice? Add the row and update the accounts; nothing else.
3. If 'No approver defined': set the missing **Bill Approver** and/or **Finance Approver** on the account and repair the matrix row.
4. If the approver departed: replace them in every matrix row, then reassign records already routed to them.
5. If the approver is absent: make the requester delegated approver.
6. If refused before the 3rd of the month: date rule, not approvers; the requester retries after the 3rd.
7. Resubmit one record; it should route. Keep the sheet as SOX evidence (Credit, Invoice, Dispute, Bills matrices); refuse making anyone their own approver.

## Common mistakes

## Escalate when
- Changes to SOX-relevant matrices (Credit, Invoice, Dispute, Bills) - keep the evidence trail for the quarterly control.
- Requests to make someone their own approver.
