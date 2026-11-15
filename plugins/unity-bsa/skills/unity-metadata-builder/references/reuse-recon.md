# Reuse recon (read-only)

Run after the inventory is agreed and before the Build Plan. Results are **suggestions, never blockers**. Present them as "Before you build: N things you may reuse", and let the analyst pick or skip each.

Run every query through the build connector's `dispatch_readonly` (`GET /services/data/v66.0/query`, or `/tooling/query` for Tooling objects), with filters and `LIMIT`. Never pull a full object schema. Summarize; don't paste raw results.

## Queries

**Fields with a similar meaning** (one per keyword from the inventory, max 3 keywords):
```sql
SELECT QualifiedApiName, Label, DataType, Description FROM FieldDefinition
WHERE EntityDefinition.QualifiedApiName = '<Object>' AND (Label LIKE '%<kw>%' OR QualifiedApiName LIKE '%<kw>%') LIMIT 20
```

**Field count on the object** (Tooling):
```sql
SELECT COUNT() FROM CustomField WHERE TableEnumOrId = '<Object or custom object Id>'
```
At 95% of 800 or more: don't block. Say the object is nearly full, list fields that could be reused, and suggest talking to the lead (Yakov) before adding more.

**Flows already on the object** (one flow per object and trigger context, V2):
```sql
SELECT ApiName, Label, ProcessType, TriggerType, RecordTriggerType, IsActive FROM FlowDefinitionView
WHERE TriggerObjectOrEventLabel = '<Object label>' AND IsActive = true LIMIT 50
```
Suggest extending an existing flow for the same context, or ordering the new one in the Trigger Explorer.

**Subflows to reuse** (`FlowDefinitionView` doesn't support OR; run one query per keyword):
```sql
SELECT ApiName, Label, Description FROM FlowDefinitionView WHERE ApiName LIKE 'Subflow_%' AND IsActive = true LIMIT 50
```
Always confirm `Subflow_Log_Error` is Active in the build org.

**Permission sets, global value sets, custom labels, email templates, custom metadata** (pick only what the inventory touches):
```sql
SELECT Name, Label, Description FROM PermissionSet WHERE IsOwnedByProfile = false AND (Label LIKE '%<kw>%') LIMIT 20
SELECT DeveloperName, MasterLabel FROM GlobalValueSet WHERE MasterLabel LIKE '%<kw>%' LIMIT 20
SELECT Name, Value FROM ExternalString WHERE Name LIKE '%<kw>%' LIMIT 20
SELECT DeveloperName, Name FROM EmailTemplate WHERE Name LIKE '%<kw>%' LIMIT 20
```
(`GlobalValueSet` and `ExternalString` are Tooling objects.)

**Validation rules on the object** (Tooling), to avoid conflicts and to see the bypass pattern:
```sql
SELECT ValidationName, Active, ErrorMessage FROM ValidationRule WHERE EntityDefinition.QualifiedApiName = '<Object>' LIMIT 100
```
The org's bypass convention is a custom permission check such as `$Permission.Skip_Account_Validations_Integration_User` (used in 39 rules). Suggest it when integrations update the object.

## Before saying something doesn't exist

Check the build org live, not memory or a local repo clone. State the evidence and its date.
