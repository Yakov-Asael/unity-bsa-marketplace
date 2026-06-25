# Salesforce Flow Standards

**Business Systems Analyst Development Guidelines — Unity**
Version 1.0 | Effective Date: April 2026 | Review Cycle: Quarterly

This is the authoritative ruleset for the `unity-flow-reviewer` skill. Source of truth: the team's "Salesforce Flow Design Standards & Best Practices" Google Doc.

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
- Approved alternatives: Custom Labels, Dynamic Lookup (Get Records by DeveloperName), Custom Metadata Types.

---

## 2. Naming Conventions

**Flow name:** `[Object]_[TriggerType]_[BusinessProcess]`
Good: `Account_AfterCreate_AssignSalesManager`, `Case_ScreenFlow_CreateFinanceTicket`. Bad: `NewFlow1`, `acc update`, `test`.

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
**Pattern 2 — Error handling:** every DML fault path → `Subflow_Log_Error(ErrorMessage={!$Flow.FaultMessage}, FlowName={!$Flow.APIName}, RecordId)`.
**Pattern 3 — Dynamic ID lookup:** `Get Records on RecordType where SObjectType + DeveloperName → store rec_recordType → use {!rec_recordType.Id}`.
**Pattern 4 — Subflow for reusability:** extract logic used in 3+ flows or 10+ elements. Naming `Subflow_[Purpose]` (e.g., `Subflow_SendEmailNotification`).

---

## 4. Error Handling

Every DML requires a fault connector. Fault paths must:
- **Screen Flow:** error screen with friendly message + `{!$Flow.FaultMessage}` in smaller text.
- **Auto-launched:** email admin with Flow APIName, FaultMessage, Record Id, timestamp.
- **Critical:** create `Error_Log__c` (`Flow_Name__c`, `Error_Message__c`, `Record_Id__c`, `User_Id__c`, `Timestamp__c`, `Stack_Trace__c`).

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

Bulkified record update; create related records; dynamic record-type assignment; conditional email notification; `Subflow_Log_Error` reusable error handler (inputs `txtErrorMessage`, `txtFlowName`, `txtRecordId`; creates `Error_Log__c` + admin email; output `isSuccess`).

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

**Minimum score to deploy: 100/100. Anything less = REJECT.**

The three zero-tolerance rules apply to ALL flows, no exceptions.
