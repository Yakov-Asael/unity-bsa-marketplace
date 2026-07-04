# Unity QA Test Tracker Template

Plan QA test scenarios in the team's tracker format (source: the "Kraken QA Tracker" Google Sheet). Produce a table with one row per scenario.

## Columns (in order)
| Column | Meaning / values |
|---|---|
| **QA Task** | Short scenario name (e.g., "Onboarding Demand", "AM Change in SFDC") |
| **Test Steps** | Numbered, concrete steps a tester follows |
| **Expected Result** | Precise, testable outcome — list every field/value/state to verify |
| **Inbound/Outbound** | `Inbound` (data/actions into SFDC) or `Outbound` (SFDC → external system, e.g. uDash) |
| **Status** | Workflow state — default `Backlog` (then In Progress / Passed / Failed) |
| **QA Type** | `New Development added` (new feature) or `Sanity Check` (regression) |
| **Priority** | `P0` (critical path) or `P1` (important, not blocking) |
| **Tester** | Assigned tester name |
| **Sandbox comments** | Result notes from sandbox testing |
| **Production Comments** | Result notes from production verification |

## Conventions
- **Expected Result must be specific and verifiable** — name exact fields and expected values ("Legal Entity is not Null", "UnityAds Advertiser", "BI Opportunity … is not Null"), never "works correctly".
- Cover the **full path**: happy path, edge cases, null handling, and cross-object/outbound sync effects.
- Mark **P0** for anything on the core onboarding/credit/sync path; **P1** for secondary checks.
- Distinguish **Inbound** vs **Outbound** so integration round-trips (SFDC ↔ uDash) are both tested.
- Group related scenarios (onboarding, sync, credit, app/contact creation).

## Example row
| QA Task | Test Steps | Expected Result | Inbound/Outbound | Status | QA Type | Priority | Tester |
|---|---|---|---|---|---|---|---|
| AM Change in SFDC | 1. Open the account 2. Change the Account Manager | 1. AM updated in uDash 2. Legal name & address API triggered 3. Is Managed flag set per user logic (SS TLV/China = False, else True) | Outbound | Backlog | New Development added | P0 | (assign) |

Deliver the plan as a markdown table the user can paste into the tracker; offer to add it to the Google Sheet if they want.
