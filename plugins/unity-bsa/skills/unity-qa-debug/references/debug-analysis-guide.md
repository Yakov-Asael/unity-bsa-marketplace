# Debug & Error Analysis Guide

Analyze Salesforce failures — Flow fault emails, Flow debug output, and classic Apex debug logs — and return a clear Root Cause Analysis.

## Inputs you may receive
- **Flow fault email** ("An error occurred with your … flow"): includes Flow API name, type, version, the **error element**, the **ExceptionCode**, the element-by-element interview trace, and the input values that were mapped.
- **Flow debug output** from Flow Builder (element path, entered/skipped outcomes, variable values).
- **Classic Apex debug log**: look for `EXCEPTION_THROWN`, `FATAL_ERROR`, `LIMIT_USAGE_FOR_NS` (SOQL/DML/CPU/heap), `SOQL_EXECUTE_BEGIN`/`DML_BEGIN` (watch for these inside loop markers), `CODE_UNIT_STARTED/FINISHED`, `METHOD_ENTRY`.

## Output — always this 3-step RCA structure
1. **Root Cause Analysis (RCA)** — the exact source (element, field, ExceptionCode, the offending value, why it happened). Name the specific element and value from the trace.
2. **Immediate Fix** — step-by-step remediation the BSA can apply now.
3. **Long-term Prevention** — structural change or guardrail so it can't recur (validation, truncation, fault path, test scenario).

Then a single **Next Step**.

## Common Salesforce exception codes → cause & fix
| ExceptionCode / signature | Root cause | Typical fix |
|---|---|---|
| `STRING_TOO_LONG: <field>: data value too large (max length=N)` | A value mapped into the field exceeds its max length | Truncate on the way in — e.g. assignment `LEFT({!source}, N)` — or move to a Long Text Area / expand the field. Add a fault path. |
| `REQUIRED_FIELD_MISSING` | A required field wasn't set before DML | Populate/validate the field before the Create/Update; add default handling |
| `FIELD_CUSTOM_VALIDATION_EXCEPTION` | A validation rule blocked the DML | Read the rule message; satisfy it or adjust the data/flow order |
| `CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY` | A downstream trigger/flow/validation failed | Trace the secondary automation named in the message |
| `System.LimitException: Too many SOQL queries / DML rows` | Query or DML inside a loop / non-bulkified | Move DML/SOQL out of loops; bulkify with collections (see unity-flow-reviewer) |
| `UNABLE_TO_LOCK_ROW` | Row-lock contention / recursion | Check for recursive updates and concurrent processes on the same records |
| `System.NullPointerException` | Dereferencing a null (e.g. `$Record.Parent.X` when Parent is null) | Null-check before use; guard the path |
| `CPU time limit exceeded` | Too much synchronous processing | Simplify logic, reduce loops, move heavy work async |

## Method
1. Identify the **error element** and **ExceptionCode** first.
2. Trace **which input mapping / value** triggered it (the fault email lists each field = value).
3. Note whether the flow had **fault handling** — an unhandled fault reaching the admin email is itself a finding (recommend a fault path per Unity flow standards).
4. Give the RCA in the 3-step structure. Be specific — cite the element name and value.
