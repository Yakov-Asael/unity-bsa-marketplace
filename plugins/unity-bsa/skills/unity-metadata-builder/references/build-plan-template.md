# Build Plan (one screen, needs explicit approval)

Show this before the first write. Build only after the analyst replies **approve build plan**. Any change to the plan needs a new approval.

```markdown
## Build Plan: <ISITBA-n or design name> <title>
**Org:** ironSource UAT (00DQI00000J4hjN2AR, sandbox), confirmed <time> by Organization query
**Spec:** <PRD/TDD link> · design ✅ build-ready · understanding check ✅

| # | Type | API name | Change | Reused? | Build route |
|---|---|---|---|---|---|
| 1 | CustomField | Account.Credit_Check_Status__c | new Picklist (restricted) | new | connector |
| 2 | Flow | Account_AfterUpdate_SetCreditStatus | new, Draft | uses Subflow_Log_Error | connector |

**Order:** value sets → objects → fields → validation rules → flows. List views are manual.

**Recommended for you to apply in Setup** (Claude doesn't write these; I verify after you say done):
| # | What | Recommendation |
|---|---|---|
| R1 | Field access | `Credit_Check_Edit` (existing): read/edit on #1. No profiles |
| R2 | Page layout | Account Layout → section "Credit": #1, behavior Edit |
**Suggestions accepted:** <list> · **declined:** <list>
**Risks:** <high-volume object? field count %? integrations updating this object?>
**Flow gate:** reviewer score <n>/100, zero-tolerance ✅ (build needs ≥85 and all zero-tolerance rules)
**Rollback:** current definitions read before update are kept in this session's notes; new components are removed in Setup (deletes aren't available through the connector).
**After the build:** read-back of each item → you apply R1, R2… → I verify them → hand-offs (QA, Gearset) → session summary.

Reply **approve build plan** to start.
```
