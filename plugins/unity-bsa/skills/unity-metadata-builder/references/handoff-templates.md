# Hand-off templates

There's no official channel yet: give the analyst the text, and they choose where to send it (Jira comment on the story, Slack or DM).

## Gearset promotion (after every successful build)

Claude never creates branches, commits or deploys. Promotion to production is the analyst's Gearset comparison and deployment.

```markdown
**Ready for Gearset: <ISITBA-n> <title>**
Built in ironSource UAT on <date> by <analyst>, verified by read-back.

Components to include in the Gearset comparison (UAT → Production):
| Type | API name | New / changed |
|---|---|---|
| CustomField | Account.Credit_Check_Status__c | new |

Flows: deploy as built; activation is a separate step after the bulk test.
Flow review: <score>/100, zero-tolerance ✅. Production needs 100/100 including the 200-record bulk test.
Test evidence: <link to QA tracker rows>
Process Map / ERD updated: <yes/no/n.a.>
```

## QA (always)

Hand off to `unity-qa-debug` Mode B with: the story and AC, the component list, and these mandatory scenarios: positive, negative, null/blank values, a user without the permission set, the fault path (force an error and confirm a row in `ErrorObject__c`), and the 200-record bulk update.

## Consult the lead (Yakov)

Use for: an object at 95% of its field limit or more, a flow change on a high-volume object, a field type change on a populated field, anything destructive, or a design question the spec doesn't answer. These are recommendations, not blocks, except where the guardrails block.

```markdown
**Consult: <ISITBA-n>, <one-line topic>**
What I want to build: <one paragraph>
Why I'm asking: <the risk, with numbers, e.g. "Case has 794/800 custom fields">
Options I see: 1) <reuse X>, 2) <build Y>, 3) <defer>
What I need from you: <decision>
```

## Optional

- Demo for stakeholders: `unity-presentations`.
- Stakeholder update: `unity-comms`.
