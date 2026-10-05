---
cluster: upload-adjustments
name: Upload revenue adjustments file
status: confirmed
count_90d: 6
---
## Definition
Finance/ops sends an adjustments file (IAP, Google, monthly) to be uploaded.

## Detection signals
- Subject 'Upload adjustmets'
- attachment-only description
- same requester each month
- Example subjects (paraphrased): Upload the attached monthly adjustments file

## How we resolve it
- Load the adjustments file (revenue/IAP adjustments) through the standard upload; confirm counts back to the requester.

## What to ask the requester
- Is the file attached and in the standard template?

## Canonical answer
**Summary:** Finance or ops sent the recurring adjustments file (IAP, Google or the monthly revenue adjustments) to be loaded through the standard upload. It is a routine load, not a data problem: the same requester sends it each month with an attachment-only description, so everything needed is in the attachment. The risks are a missing or off-template file and rows touching a closed period. This cluster is pending approval.
**Suggested resolution:**
1. Confirm the file is attached and in the standard template (same layout as last month's). If missing or off-template: ask for it in the standard template and pause.
2. Identify which adjustments it carries (IAP, Google or monthly) to use the matching upload.
3. Scan the period the rows adjust and count the rows before loading.
4. If any row falls in a closed period: hold it back and escalate before loading it.
5. Load the remaining rows through the standard adjustments upload for their type.
6. Compare the loaded count with the file's row count; if they differ, review the missing rows with the requester.
7. Reply with the loaded counts and any rows held for a closed period.

## Common mistakes

## Escalate when
- Adjustments touching closed periods.
