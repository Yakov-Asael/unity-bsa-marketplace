# Salesforce Flow Standards

**Business Systems Analyst Development Guidelines — Unity**
V2 (Flow Manual tab) + Version 1.0 (April 2026) | Review Cycle: Quarterly | Synced 2026-11-15

This is the authoritative ruleset for the `unity-flow-reviewer` and `unity-metadata-builder` skills. Source of truth: the team's "Salesforce Flow Design Standards & Best Practices" Google Doc. Where V2 and v1.0 differ, V2 wins.

---

## 0. Architecture (V2)

- **One flow per object** per trigger context. Use the **Trigger Explorer** to manage execution order. Keep **Fast Field Updates (Before-Save)** separate from **Actions & Related Records (After-Save)**.
- **Entry criteria** as specific as possible. Never run on every update unless necessary: choose "Only when a record is updated to meet the condition requirements".
- **Subflows:** any logic repeated more than twice (error logging, standard notifications) moves to a subflow.

---

## 1. Mandatory Requirements (Zero Tolerance)

These rules have **ZERO TOLERANCE**. Any flow violating them is **REJECTED in code review** and **BLOCKED from deployment**.

### Rule 1: NO DML or SOQL Inside Loops
- NEVER place Get/Create/Update/Delete Records elements inside a Loop element.
- All database operations occur outside loops.
- **Why:** governor limits (100 SOQL, 150 DML per transaction). Even 10 records fail in production.

✓ Correct: `Get Records (ALL) → Loop → Assignment (add to collection) → Update Records (collection)` = 1 SOQL + 1 DML
❌ Incorrect: `Loop → Update Records (item)` = 100+ DML, FAILS

### Rule 2: ALL DML Operations Must Have Fault Connectors
- Every Create/Update/Delete Records element MUST have a Fault Connector (red path). No exceptions.
- **Why:** without fault paths, errors fail silently — no user feedback, no audit trail, data inconsistency.
- Minimum: display `{!$Flow.FaultMessage}`; screen flows show a friendly error screen; auto-launched flows email an admin; critical flows create an error log record.

### Rule 3: NO Hardcoded IDs
- NEVER hardcode 15- or 18-char Salesforce IDs (Record Types, Users, Queues, Profiles, custom records).
- **Why:** IDs are environment-specific; flows break on sandbox refresh and fail to deploy.
- Approved alternatives: Dynamic Lookup (Get Records by DeveloperName), Custom Metadata Types, Custom Settings, Custom Labels.

---

## 2. Naming Conventions

**Flow label (V2):** `[Object] - [Trigger Type] - [Brief Description]`, e.g. `Account - After Update - Assign Sales Manager`.
**Flow API name (v1.0):** `[Object]_[TriggerType]_[BusinessProcess]`, e.g. `Account_AfterUpdate_AssignSalesManager`.
Bad: `NewFlow1`, `acc update`, `test`.

**Flow type prefixes:**

| Trigger Type | Prefix | Example |
|---|---|---|
| Record-Triggered (Before Save) | `[Object]_BeforeSave_` | `Account_BeforeSave_SetDefaults` |
| Record-Triggered (After Save, create) | `[Object]_AfterCreate_` | `Case_AfterCreate_NotifyTeam` |
| Record-Triggered (After Save, update) | `[Object]_AfterUpdate_` | `Opportunity_AfterUpdate_AssignOwner` |
| Screen Flow | `[Object]_ScreenFlow_` | `Contact_ScreenFlow_BulkUpdate` |
| Scheduled | `Scheduled_` | `Scheduled_DailyAccountCleanup` |
| Auto-launched (Invocable) | `Invocable_` | `Invocable_SendCustomEmail` |

**Variable prefixes (camelCase):**

| Prefix | Type | Example |
|---|---|---|
| `var_` | Text/generic | `var_accountPriority` |
| `rec_` | Record variable | `rec_currentOpportunity` |
| `col_` | Collection variable | `col_relatedCases` |
| `txt_` | Text output | `txt_emailBody` |
| `is_` | Boolean | `is_highPriority` |
| `num_` | Number | `num_totalAmount` |
| `for_` | Formula | `for_isNewDeal` |
| `con_` | Constant | `con_maxRetryAttempts` |
| `date_` | Date variable | `date_startDate` |

**Element names:** `[ElementType]_[Description]`
- Get Records: `Get_Active_Accounts`
- Decision: `Dec_` or `Check_` → `Dec_Is_High_Value`
- Assignment: `Assign_Status`
- Loop: `Loop_Through_Contacts`

---

## 3. Design Patterns

**Pattern 1 — Bulk processing:** `Trigger → Decision (add {!$Record} to col_) → Loop (build col_recordsToUpdate) → Update Records (collection)`.
**Pattern 2 — Error handling:** every DML fault path → `Subflow_Log_Error(txtErrorMessage={!$Flow.FaultMessage}, txtFlowName={!$Flow.APIName}, txtRecordId={!$Record.Id})`.
**Pattern 3 — Dynamic ID lookup:** `Get Records on RecordType where SObjectType + DeveloperName → store rec_recordType → use {!rec_recordType.Id}`.
**Pattern 4 — Subflow for reusability:** extract logic used in 3+ flows or 10+ elements. Naming `Subflow_[Purpose]` (e.g., `Subflow_SendEmailNotification`).

---

## 4. Error Handling

Every DML requires a fault connector, and **every fault path calls the shared `Subflow_Log_Error`** (V2: one generic error subflow). Don't build a new one.
- **The Unity org's subflow:** `Subflow_Log_Error` (label "Subflow - Log Error", autolaunched, Active in UAT, on SFDC-IS `Production` via PR #1929). It writes to **`ErrorObject__c`**. The Google Doc's v1.0 text says `Error_Log__c`; the org uses `ErrorObject__c`.
- **Inputs:** `txtErrorMessage` = `{!$Flow.FaultMessage}`, `txtFlowName` = the flow API name, `txtRecordId` = the triggering record ID.
- **Screen Flow:** after the subflow call, show an error screen with a friendly message and `{!$Flow.FaultMessage}` in smaller text.

Do not expose technical jargon to end users; provide actionable next steps + support contact.

---

## 5. Bulkification Rules

Governor limits per transaction: 100 SOQL, 150 DML, triggers process up to 200 records. **Every flow MUST handle 200 records.**
- Get all records once (1 SOQL) → build collection in loop → single DML on collection.
- Use collection variables: `col_accountsToUpdate`, `col_tasksToCreate`, etc.

---

## 6. Configuration Management

| Value Type | Custom Label | Custom Metadata | Dynamic Lookup |
|---|---|---|---|
| Record Type ID | Quick | Best | Best |
| User ID | Acceptable | Best | Best |
| Queue ID | Acceptable | Best | Best |
| Static Text | Best | Overkill | N/A |
| Complex Config | Limited | Best | N/A |

---

## 7. Documentation Standards

**Flow Description (required):** Purpose, Trigger, Object(s), Owner (BSA name), Last Modified. Must include the **User Story ID**.
**Element descriptions:** required and specific ("Get all active Account Team Members where Role = 'Sales Manager'" — not "Get records").
**Version history:** `v1.3 — 2026-04-20 — [Name] — [what changed]`.
**Process Map and ERD (V2):** update them when the business logic or data model changes.

---

## 8. Testing Requirements

- Single-record test passes.
- **Bulk test: 200+ records** without governor-limit breaches (Data Loader / mass update). Execution < 5 min.
- Null handling; intentional fault-path trigger; permission tests.
- Debug log analysis: no `SOQL_EXECUTE_BEGIN` / `DML_BEGIN` inside loops; total SOQL < 100, DML < 150.

---

## 9. Code Review Checklist

**Auto-fail (reject immediately):** SOQL/DML in loops; missing fault connectors; hardcoded IDs; no bulk-test evidence.
**High priority:** naming conventions; descriptions populated; bulk-tested; user-friendly error messages.
**Medium:** reusable logic in subflows; no dead ends; collections over looping DML.

A flow deploys only when: self-review complete, peer review approved, all auto-fail criteria pass, bulk testing done, debug logs clean.

---

## 10. Common Patterns Library

Bulkified record update; create related records; dynamic record-type assignment; conditional email notification; `Subflow_Log_Error` reusable error handler (inputs `txtErrorMessage`, `txtFlowName`, `txtRecordId`; writes `ErrorObject__c` in the Unity org).

---

## 11. Quick Reference

**Governor limits:** SOQL 100, DML 150, records retrieved 50,000, heap 6 MB, CPU 10 s.

**Deployment Readiness Score (score before deployment):**

| Criteria | Points |
|---|---|
| No DML/SOQL in loops | 30 |
| All DML has fault connectors | 30 |
| No hardcoded IDs | 20 |
| Bulk tested (200+ records) | 10 |
| Proper naming conventions | 5 |
| Complete documentation | 5 |
| **TOTAL** | **100** |

**Minimum score to deploy to production (Gearset): 100/100. Anything less = REJECT.**
**Build gate in UAT (`unity-metadata-builder`):** zero-tolerance pass and at least 85/100 to build the flow inactive. Bulk-test points come after the build; the analyst activates the flow in UAT, runs the bulk test, and re-scores before promotion.

The three zero-tolerance rules apply to ALL flows, no exceptions.
