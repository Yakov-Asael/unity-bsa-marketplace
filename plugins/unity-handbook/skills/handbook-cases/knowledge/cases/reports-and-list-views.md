---
cluster: reports-and-list-views
name: Reports, dashboards and list views
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-17
count_90d: 24
---
## Definition
Build or change a report/dashboard/list view, add columns or filters, export data, subscribe, or ask what a metric means.

## Detection signals
- 'report'
- 'dashboard'
- 'list'
- 'column'/'filter'
- Sub_Category Report/Dashboard
- Example subjects (paraphrased): Build or adjust a report / dashboard · Add a filter or columns to a list view or pipeline screen · Export a large account list

## How we resolve it
- Owner ruling: the suggestion should give the agent the **steps to build the report** - object/report type, filters, groupings, columns, folder and sharing - not a promise to build it.
- **Fraud deduction breakdown by app for a publisher bill** (owner feedback 2026-10-04): the per-app payout is not on the bill lines; run the BigQuery query against `unity-it-iltools-prd.grow_wrk.uads_base_supply_publishers` filtered on `db = 'fraud'`, `biDate` inside the bill's activity month and `account_id` = the publisher's Salesforce account id, `GROUP BY account_id, opportunity, line_id, line_name` with `SUM(amount_usd) AS payout`; export and attach to the case (`line_name` = app name, `line_id` = game id). For a recurring need, save the query and run it after each billing run.
- List views: clone the view, add the filter/columns, share the URL. Report filters 'changing by themselves' = edited via a filtered dashboard. Dashboards refresh on schedule - run a refresh after loads. Users subscribe to reports themselves; flows are admin-only.

## What to ask the requester
- Which object, fields, filters and grouping?
- Who needs to see it (folder / sharing)?
- One-off export or a recurring view?

## Canonical answer
**Summary:** The requester wants a report, dashboard change, list view, export or metric explained. Give the steps to build it - report type, filters, groupings, columns, folder and sharing - not a promise. Filters that 'change by themselves' were edited via a filtered dashboard; dashboards show loaded data only after a refresh; users subscribe themselves.
**Suggested resolution:**
1. Ask for the object, fields, filters, grouping, one-off or recurring, and who needs to see it (folder and sharing).
2. Build in their folder: report type, filters, groupings, columns; save and share the link; export once if one-off.
3. If a list view: clone the closest view, add filter and columns, share the URL.
4. If a fraud deduction breakdown by app for a publisher bill (per-app payout is not on the bill lines): query BigQuery `unity-it-iltools-prd.grow_wrk.uads_base_supply_publishers` with `db = 'fraud'`, `biDate` in the bill's activity month, `account_id` = the publisher's account, `GROUP BY account_id, opportunity, line_id, line_name`, `SUM(amount_usd) AS payout`; attach the export (`line_name` = app); if recurring, save and rerun after each billing run.
5. If the data is not in Salesforce (BI warehouse, cross-org) or it is someone's private report: escalate; do not clone or reshare.

## Common mistakes

## Escalate when
- Cross-org or BI-warehouse data that Salesforce reports cannot produce.
- Requests for other people's private reports.
