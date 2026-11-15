# Build Plan (one screen, needs explicit approval)

Show this before the first write. Build only after the analyst replies **approve build plan**. Any change to the plan needs a new approval.

```markdown
## Build Plan: <ISITBA-n> <story title>
**Org:** ironSource UAT (00DQI00000J4hjN2AR, sandbox), confirmed <time> by Organization query
**Spec:** <PRD/TDD link> · story ✅ sprint-ready · understanding check ✅

| # | Type | API name | Change | Reused? | Build route |
|---|---|---|---|---|---|
| 1 | CustomField | Account.Credit_Check_Status__c | new Picklist (restricted) | new | connector |
| 2 | PermissionSet | Credit_Check_Edit | add read/edit on #1 | existing | connector |
| 3 | Flow | Account_AfterUpdate_SetCreditStatus | new, Draft | uses Subflow_Log_Error | connector |

**Order:** value sets → objects → fields → validation rules → permission sets → list views/layouts → flows.
**Field access:** <permission set → fields → read/edit>. No profiles.
**Suggestions accepted:** <list> · **declined:** <list>
**Risks:** <high-volume object? field count %? integrations updating this object?>
**Flow gate:** reviewer score <n>/100, zero-tolerance ✅ (build needs ≥85 and all zero-tolerance rules)
**Rollback:** current definitions read before update are kept in this session's notes; new components are removed in Setup (deletes aren't available through the connector).
**After the build:** read-back of each item → hand-offs (QA, Gearset).

Reply **approve build plan** to start.
```
