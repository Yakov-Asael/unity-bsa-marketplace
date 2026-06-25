# Unity PRD / TDD Template (Combined)

Unity uses a single combined PRD/TDD template. The TDD is a deeper version of the same document, with section 5 (Detailed Design) fully expanded. Keep it focused — target 2–4 pages. Do not pad. Do not invent scope; ask for missing sections.

---

# {Title}

| Field | Value |
|---|---|
| Status / review status | Draft |
| Date Created |  |
| Document Author(s) |  |
| Related Document(s) |  |

## 1. Motivation
Grounded in a real user pain, not a feature request. State the "Why" before the "How".

## 2. High-Level ERD
Objects involved and the relationships between them.

## 3. Stakeholders
Who is affected / who signs off.

## 4. Flow Description
Narrative of the automation / solution at a glance.

## 5. Detailed Design

### 5.1 POC split
Divide into POCs if there is logic owned by another team.

### 5.2 Logic
Step-by-step logic of the solution.

### 5.3 Fields & Objects related
New/modified fields with type, API name, and formula logic where relevant.

### 5.4 Error Handling
Map every integration/DML outcome:
- **Status = 200** — Success
- **Status = 400** — connection failed
- **Status = 300** — duplicate detected
- **If the request fails, create an Error_Object__c row:**
  - Object — `Error_Object__c`
  - Request Body — JSON received
  - Message — error message that was raised
  - Stack Trace — place in code
  - Class Name

## 6. Backfilling
*If needed* — how existing data is brought in line with the new design.

## 7. Go-live tasks
Deployment / activation checklist.

## 8. Open Questions
Each open question must have an **assigned owner**.
