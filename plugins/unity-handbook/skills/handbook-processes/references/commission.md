# Commission

> Source: Business Systems analysis handoff (prepared 2026-11-16 by Yakov Asael), re-verified on 2026-11-17 against the SFDC-IS `origin/Production` branch (fetched 2026-11-17, commit 9e74c3946) and the live Grow production org. Unlike the other files in this folder, this one is not a verbatim handbook tab. Where the handoff and Production disagree, the `> **Verified 2026-11-17:**` note wins.

**Process:** Commission, the quarterly sales commission calculation for Grow users · **Built on:** `Commission_Model__c`, `Commission_Model_Line__c`, `Commission_Model_With_Users__c`, `Commission__c`, `Commission_Line__c`, `Group__c`, `Group_Line__c`, `Target__c`, `Commission_Adjustments__c`, the `CM_*` Apex classes and scheduled jobs · **Built and run by:** Business Systems · **Business owner / technical owner:** not confirmed. Do not name anyone. Route the person to Business Systems and say the named owner is still to be filled in.

**Verified against the org:** 2026-11-17. Counts marked "handoff" were taken on 2026-11-15 and not re-run.

**Read this first.** Commission is a calculation engine, not a workflow. Standard lines read Salesforce data (Invoices or Monthly Revenue) through filters. Custom and MBO lines read nothing: Business Systems types a number onto the line. Two scheduled jobs recalculate every Pending commission twice a day. When a number looks wrong, the question is almost always one of: which filter picked the data, is the commission still Pending, or is the line manual.

# 1. What this process does

Each quarter, every user assigned to a Commission Model gets one `Commission__c` record with one `Commission_Line__c` per Model Line. Each line scores Actual / Target x Weight, capped. The line scores sum to the commission score, then the model cap and the kicker apply. The actual freezes at the cut-off date (the 22nd of the month after quarter end). Status moves Pending, then Pending Final Approval, then Approved For Payment. Only Pending commissions are recalculated.

# 2. Objects

| Object | Role |
|---|---|
| `Commission_Model__c` | Setup template: department, type, revenue type, cap, kicker, run-rate switch |
| `Commission_Model_Line__c` | One goal in a model: component, source, weight, cap, group, filters, target type, order |
| `Commission_Model_With_Users__c` | Assigns a user to a model with start and end dates. The formula `Create_Model__c` (Active, today between start and end date, user assigned) drives creation |
| `Commission__c` | One user's quarter: quarter, year, cut-off date, cap, kicker, status |
| `Commission_Line__c` | One goal for that user's quarter: actual, target, weight, cap, score |
| `Group__c` | Population definition (department, division, sub-division, activity, territory, sub-territory, office, team, users, role) |
| `Group_Line__c` | One per group per quarter, named like "Q4 2026 Team A". Totals for invoice, revenue, net revenue, payout |
| `Target__c` | Number targets for a quarter, by user, group or source |
| `Commission_Adjustments__c` | Record types General, Personal, External |
| `Invoice__c`, `Monthly_Revenue__c` | Source data, plus Account and Opportunity |
| `Commission_UI_Source_Mapping__mdt` | Custom metadata, 12 rows (4 live per the handoff). Holds only a run-rate field per source |

Component types: Personal, Group and MBO, each Standard or Custom. Lines are children of a Commission and point back to their Model Line.

# 3. What is in use

**Definition of "in use":** a model with a `Commission_Model_With_Users__c` record where `Create_Model__c = true`. The model's own Active flag is not used.

| Item | Value |
|---|---|
| Models in use | 66 (65 "By Targets", 1 with no type). Re-verified 2026-11-17: 66 |
| User assignments | 135 on 2026-11-17 (handoff: 133 on 2026-11-15). All to individual users, none to groups |
| Models by department | Advertiser 33, Publisher 18, Affiliate 2, no department 13 (handoff) |
| Model Lines | 267: Personal 158, Group 95, MBO 14 (handoff) |
| Personal Standard lines | 71: Net Revenue 26, Invoice 21, Revenue 16, IAB Fees 8 (handoff) |
| Group Standard lines | 91: Invoice 46, Net Revenue 38, Revenue 7 (handoff) |
| Custom lines | 91 (Personal 87, Group 4), all Data Source = Manual, Target Type = Percent (handoff) |
| Custom sources (8 named) | LevelPlay Optimization, OW Health Score, Ad Quality, Geo Expansion, Google Analytics Linking, D28 Campaign Adoption, HoM maturity, Bold SDK. 6 lines have no source name (handoff) |
| Line owner role | Account Manager 176 lines, Sales Manager 49, Ad Ops Manager 12 (handoff) |
| Groups | 91 live lines point to 54 groups (handoff) |
| Revenue types live | "New Business" and "New Business # of days" (or blank) (handoff) |
| Commissions per quarter | Q4 2026: 135 (628 lines). Q3 2026: 133 (612 lines). Q2 2026: 172. Q1 2026: 190. Q4 2025: 234 |
| Kicker | 1 of 134 Q4 commissions (handoff) |
| Run Rate | Enabled on all Q4 commissions (handoff) |

> **Verified 2026-11-17:** the handoff's open question "134 commissions vs 133 assignments" no longer shows. On 2026-11-17 there are 135 in-use assignments (135 distinct users) and 135 Q4 commissions. The cause of the earlier one-record difference was not established. Treat the 2026-11-15 figures as a moving snapshot of a quarter in progress, not as a closed-quarter baseline.

**Status mix (verified 2026-11-17):**

| Quarter | Pending | Pending Final Approval | Approved For Payment |
|---|---|---|---|
| Q4 2026 (in progress) | 135 | 0 | 0 |
| Q3 2026 (closed) | 11 | 8 | 114 |

Q3 still has 11 Pending commissions. Because only Pending is recalculated and the last-quarter job runs daily, those 11 are still being recalculated.

**Not in use today (supported in code, no live lines; handoff):** revenue types BOB (retired) and New Biz; Custom lines with Data Source = External; the 365-day go-live window; the Mediation filter; source variants OW Revenue, OW Net Revenue, Revenue and Net Revenue Non OW, Invoice OW, SuperSonic Profit and Net Revenue, TMR; Platform Fees; Activity variants.

> **Verified 2026-11-17 (correction):** the handoff said the Personal and External adjustment record types are not in use. That holds for Q4 2026 only. Adjustments by their Date field in 2026:
>
> | Quarter | General | Personal | External |
> |---|---|---|---|
> | Q4 | 127 | 0 | 0 |
> | Q3 | 318 | 43 | 1 |
> | Q2 | 14,146 | 14 | 1 |
>
> All-time record counts: General 18,676, External 39,113, Personal 1,250. Do not tell anyone Personal or External adjustments are unused.

# 4. Scoring rules

- Line score = Actual / Target x Weight.
- Line cap: the score cannot exceed Cap x Weight.
- Commission score = sum of line scores, then the model cap, then the kicker.
- Actual = amount at the cut-off date plus adjustments. It tracks live until the cut-off day, then freezes.
- Cut-off: Q1 22 April, Q2 22 July, Q3 22 October, Q4 22 January of the next year. Confirmed in `CM_CommissionUtil.setCutOffDate`.
- Run rate projects the quarter from recent daily averages. Current quarter only. Can be hidden per line.
- Targets: number targets come from `Target__c`; percent targets are typed on the line.
- Status flow: Pending, Pending Final Approval, Approved For Payment (confirmed as the picklist values on `Commission__c.Status__c`). Only Pending is recalculated.
- Revenue types: "New Business" uses the quarter's monthly revenue. "New Business # of days" uses revenue in the first 180 days after go-live.

# 5. Batches and schedules

All times are Israel time. The cron expressions below were read from `CronTrigger` on 2026-11-17 and the UTC `NextFireTime` values are consistent with Israel time (UTC+2 in November). `TimeZoneSidKey` was not queried, so confirm it with `handbook-code-lookup` before quoting a time as current.

| Job | Class | When | Batch size | Writes |
|---|---|---|---|---|
| Commission Create | `CM_CommissionCreateBatch` | 1st of Jan, Apr, Jul, Oct, 06:00 (`0 0 6 1 JAN,APR,JUL,OCT ?`) | 5 | Commission and Commission Lines |
| Update chained from Create | `CM_CommissionUpdateBatch` | Runs when Create finishes | 3 | Same as Update |
| Group Line Create | `CM_GroupLineCreateBatch` | 1st of Jan, Apr, Jul, Oct, 09:00 | default (200) | One Group Line per group |
| Group Line Update | `CM_GroupLineUpdateBatch` | Daily 10:00 and 22:00. Four scheduled jobs whose names start with `CM_GroupLineUpdate` exist, two per time. Confirm their exact names with `handbook-code-lookup` | 1 | Group totals. Queueable fallback (`CM_GroupLineUpdateJob`) above 5,000 records or 1,400 revenue rows |
| Commission Update, this quarter | `CM_CommissionUpdateThisQuarterSchedule` | Daily 10:30 and 22:30 | 1 | Commission and Lines, Pending only |
| Commission Update, last quarter | `CM_CommissionUpdateLastQuarterSchedule` | Daily 10:30 and 22:30 | 1 | Same, for the previous quarter (Q4 maps to the previous year) |
| Missing-target alert | scheduled flow `Commission_Line_Alert_on_Commission_with_no_Target-6` | Weekly, Tuesday 12:00 (`0 0 12 ? * 3 *`) | n/a | Alert only |

> **Verified 2026-11-17 (corrections and additions to the handoff):**
> - The Update batch is launched by two separate schedulers, one for this quarter and one for last quarter, each at 10:30 and 22:30. All six jobs above were in state WAITING.
> - When Create finishes it starts Update itself with batch size 3, not 1.
> - `CM_AggregateToGroupBatch` (with `CM_AggregateToGroupSchedule`, batch size 1) also exists. It aggregates invoice, revenue and payout totals onto `Group__c` for this and last quarter. No scheduled job with that name prefix exists in the org, so it is only launched manually (it has a `webService` entry point per group). Do not describe it as part of the daily run.
> - The Group Line Update jobs exist twice per time. Which pair serves which purpose was not established.

**Create batch steps:** read assignments with Create Model on and a user; load each model and its lines; insert one Commission per user (cap, kicker, quarter, year, cut-off date); insert one Commission Line per model line; start the Update batch. Fields copied from model line to line: component, source, weight, cap, group, department, revenue type, days after go-live, mediation, UI source, monthly threshold, target type, order, default flag, run-rate flag. Failed inserts go to the error log.

**Update batch steps:** load Pending commissions with models, lines, invoices, revenue, targets, adjustments, group lines; reset each line's settings from its model line while keeping manual values; handle Custom lines (apply targets and manual figures); handle Standard lines (group by user role; personal lines read invoices or revenue, group lines read the Group Line); add targets and adjustments; freeze the cut-off amount until the cut-off day; save, logging errors while the rest still saves.

> **Verified 2026-11-17 (correction):** the 130,000-character limit is not just a limit. If `Adjustments_Json__c` on a line is longer than 130,000 characters, the batch sets it to null and writes an error log saying the field "exceeded 130,000 characters and was nullified" with the original length. The adjustment detail on that line is therefore lost, not truncated. The adjustment amount itself is a separate field.

# 6. Filters (how the right data is pulled)

There is no single composite key in code. A line resolves to data through its filters (department, division, sub-division, activity), role matching on the user, and a fixed source-to-field rule. The custom metadata supplies only a run-rate field per source. To reproduce the logic, reproduce the filter set; there is no lookup key to copy.

**Invoices (handoff)**
- Amount in USD is not zero. Not cancelled; type is Invoice. Account not excluded from commission.
- User is the invoice's Account Manager, Sales Manager, Global Biz Dev or Ad Ops Manager.
- Line filters: account division matches the line; sub-division and activity when set; months since go-live when set; monthly threshold when set.

> **Verified 2026-11-17:** the invoice date rule is two-sided, as read from the group aggregation query in `CM_AggregateToGroupBatch`. An invoice counts toward the quarter when either: its Correction Period is in the quarter and its Approval Status is "Submitted and Pending finance approval" or "Approved by finance"; or its To-be-paid date is in the quarter and its Approval Status is neither of those two. The same query also requires `Approved_Without_Issue__c = false`, `Invoice_Cancelled__c = false`, a non-null `Amount_for_invoice_USD__c` and an account not excluded from commission. The handoff's one-line "correction period or to-be-paid date" omits the status condition and the `Approved_Without_Issue__c` exclusion. The personal-line invoice query in `CM_CommissionUpdateBatch` was not re-read in this pass, so do not assert that it applies the same `Approved_Without_Issue__c` condition.

**Monthly Revenue (handoff)**
- Account not excluded from commission. Date falls in the quarter.
- User matches a role on the row: AM, SM, Global Biz Dev, Ad Ops, GM, GOM, SOM.
- Line matches department and division; sub-division and activity when set.
- Revenue type picks the field: quarter value, or the 180-day value.
- Source to field: Net Revenue = profit field, Revenue = revenue field, IAB Fees = IAB fees field, Invoice = amount in USD (Invoice object).

**Commission Adjustments**
- Source equals the line's source. Date falls in the quarter; user matches a role on the adjustment. The amount is added to the line's actual.
- Record type: see the Verified 2026-11-17 note in the in-use section. All three record types occur in closed quarters.

# 7. Custom and MBO lines (manual numbers)

- Not calculated from Salesforce data. Business Systems pushes a number onto the Commission Line, so it works like an external, non-automated input under Business Systems control.
- Data Source = Manual, so the twice-daily batch keeps the typed value on recalculation.
- The engine still applies target (percent), weight, cap and the normal score formula.
- Critical Objectives lines use a baseline: (actual minus last quarter's manual score) / (target minus last quarter's manual score) x weight. Field: `Last_Quarter_Commission_Score_Manual`.
- MBO lines follow the same manual pattern.
- **[UNVERIFIED]** The entry path (commission pages or mass update, via `Ctrl_UserCommission` and `Ctrl_TLCommission`) is described from the code and was not observed live.
- Any integration, including Everstage, needs an input mechanism for these lines: no source table sits behind them.

# 8. Key Commission Line fields

| Field | Role |
|---|---|
| Current commission amount | Actual; typed in on manual lines |
| BI Numbers, Run Rate Amount | Manual reference and run-rate values |
| Target, Weight, Cap, Percentage | Scoring inputs |
| Cut-off date amount | Actual frozen at cut-off |
| Adjustments Amount, Adjustments Json | Adjustments and their detail (Json is nulled above 130,000 characters) |
| Last Quarter Commission Score Manual | Baseline for Critical Objectives |
| Score, Final Score, RR Score | Formula results |

# 9. Everstage decision (neutral, no recommendation)

Business Systems is deciding by 1 February 2027 between Option A (Everstage connects directly to Monthly Revenue and Invoices and rebuilds the rules) and Option B (Everstage consumes the final score from the Salesforce Commission and Commission Line results).

| Criterion | Option A: direct connection | Option B: consume final score |
|---|---|---|
| Everstage builds | Rules, filters, scoring | Intake and payout rules |
| Data it reads | Invoices, revenue, targets, adjustments | Commission and Commission Line results |
| Custom and MBO input | Needs an input route | Stays in Salesforce |
| Who changes the rules | Everstage | Business Systems |
| Freshness | Set by Everstage sync | Twice daily |
| Reconciliation | Against Salesforce output | Against the source results |

Option A rebuilds: setup for 66 models, filters, role matching and group populations, scoring, caps, kicker, run rate, cut-off freeze, approval statuses. Option B exposes: score, cap, kicker, status, line amounts, target, score, frozen cut-off amounts.

Decisions still pending: option choice; live quarter-to-date versus cut-off snapshots; which statuses to mirror; how Custom and MBO numbers reach Everstage; the reconciliation set (a closed quarter, Q3 2026 is available); who owns rule changes after go-live.

# 10. Troubleshooting (candidate clusters, not yet from real cases)

These are expected symptoms, derived from the mechanics above. No closed case has been graded for them yet, so treat each as a hypothesis to check, not a documented fix.

| Symptom | First check |
|---|---|
| A manual value on a Custom line was not saved or was overwritten | The line's Data Source must be Manual. Look at `Current commission amount` and the commission Status: only Pending commissions are recalculated, and a Pending Final Approval or Approved For Payment commission is not touched |
| A user has no commission this quarter | Is there a `Commission_Model_With_Users__c` record with `Create_Model__c = true` on the 1st of the quarter? Create runs once per quarter, on the 1st |
| Commission stuck in Pending | Pending is the default and is changed by the approval step, not by the batch. Check who moves it to Pending Final Approval |
| Wrong group total | Check the `Group_Line__c` for that group and quarter and its last update. Large groups go through the queueable fallback |
| Adjustment detail missing on a line | `Adjustments_Json__c` over 130,000 characters is nulled; look for the error log entry |
| Actual stopped moving | The cut-off date has passed and the amount is frozen |

# 11. Open items (before this file is fully handbook-grade)

1. Name the process owner (business and technical).
2. Confirm the manual-entry path for Custom and MBO lines in the org.
3. Re-run the counts on a closed quarter (Q3 2026) so the figures are not mid-quarter. Partly done: Q3 status mix and line count are above.
4. Confirm cut-off behaviour for last-quarter updates (the last-quarter job exists and runs daily; what it does to a frozen amount after the cut-off day is not verified).
5. Collect real closed Commission cases so `handbook-cases` can grade clusters.
6. Establish the exact names and purpose of the four `CM_GroupLineUpdate*` scheduled jobs.
7. Decide whether `CM_AggregateToGroupBatch` is intentionally unscheduled.

# 12. Who to ask

Business Systems built and runs Commission. The named owner is not confirmed. Say so, and route the person to Business Systems.

# 13. Related files

Source of the analysis: Miro board "Backend" and the deck "Commission process at Grow (Everstage) - native Slides". Code: the `CM_*` Apex classes and `Ctrl_UserCommission` / `Ctrl_TLCommission` in SFDC-IS. For schedules and what a class does, use `handbook-code-lookup`. For current org values, use `handbook-refresh`.
