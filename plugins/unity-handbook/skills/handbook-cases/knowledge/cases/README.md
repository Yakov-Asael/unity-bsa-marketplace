# Case knowledge base

One file per issue cluster in the Business Systems support pipeline (`Case` record type `Saleforce`). These files are the source of truth the `handbook-cases` skill answers from. They are produced and graded by the Case Resolver pipeline and reach this repo only through a reviewed PR.

## What never goes here
Requester names, emails, account names, case numbers, or any case body text. Patterns and answers only. Paraphrased example subjects in `taxonomy.md` are allowed, stripped of names, emails, account names and identifiers.

## File contract - `<slug>.md`

```
---
cluster: <slug>                       # must equal the filename
name: <human name>
status: proposed | confirmed | approved | needs-work
approved_by: <name>                   # only when approved
approved_on: <YYYY-MM-DD>             # only when approved
count_90d: <n>
---
## Definition
## Detection signals
## How we resolve it
## What to ask the requester
## Canonical answer
## Common mistakes
## Escalate when
```

- `status` lifecycle: `proposed` (clustered) → `confirmed` (owner kept the cluster) → `approved` (canonical answer graded Correct, at least 60% of sampled drafts Correct) or `needs-work`.
- `Canonical answer` follows `../../references/answer-standard.md`.
- `taxonomy.md` lists every cluster with counts and the census line for the run that produced it.
- `../feedback/` holds the owner's grading rounds. They are a historical log of how the answers were corrected, not instructions to run anything.
