# Standards per type

Tags: **[FS]** Flow Standards doc (V2 wins over v1.0) · **[RN]** release-notes deck · **[SF]** Salesforce/connector guidance · **[ORG]** observed in the ironSource org · **[P]** proposed in the plan and approved by Yakov (Nov 2026). `scripts/scan.py` enforces the rules marked ⛔ (blocks) and ⚠ (warns).

## Every type
- Description on every component: what it's for and the story ID or design name. ⛔ for fields and flows [FS][P]
- No hardcoded record IDs anywhere: DeveloperName lookup, Custom Metadata, Custom Settings or Custom Labels ⛔ [FS]
- Prefer standard and existing components (reuse recon) [P]
- Access through permission sets, never profiles ⛔ [P][RN]
- Permissions and page layouts are **recommend-only**: Claude writes the recommendation, the analyst applies it in Setup ⛔ [P]

## Custom field
- API name `Snake_Case_Words__c`; prefixes only for integrations (`WD_`, `NS_`); label = API name with spaces ⚠ [ORG 55%][P]
- Help text: one plain sentence that adds more than the label ⚠ [SF] (only 4% of org fields have it [ORG])
- Picklists restricted by default; a global value set when the values are shared [SF][ORG 69% restricted]
- Object at ≥95% of 800 fields: warn, suggest reuse, consult the lead [P]
- External ID only for integration keys [SF]
- No type change on a populated field without the lead [P]

## Custom object
- Description that reads like documentation (purpose, key fields, rules, use), under 50 words; refresh it when its fields or validation rules change, with the analyst's OK [SF]
- AutoNumber name field for logs and transactions, Text for named things [SF]
- `enableReports`, `enableSearch`, `enableActivities`, `enableHistory` on for user-facing objects [SF]

## Validation rule
- Name: `<Purpose>` in Snake_Case without `__c` (e.g. `Require_Close_Reason`) [SF]
- Include the integration bypass `NOT($Permission.<Bypass_Custom_Permission>)` when integrations update the object (org pattern: `Skip_Account_Validations_Integration_User`, used in 39 rules) [ORG]
- Error message says what to do, shown at the field when there's one field [SF]
- Formula validated with the connector's dry run before saving [SF]

## Permission set (recommend only)
- Name `<Feature>_<Access>` (e.g. `Credit_Check_Edit`), with a description of who gets it [P]
- Least privilege: read before edit; no View All / Modify All without the lead [SF]
- Never field permissions on required fields; formula fields read-only [SF]
- After the build, check access in Object Manager's **Field Access** view [RN]

## Global value set / picklist values
- Value API names keep the user's spelling, spaces included [SF]
- Adding values: send the complete current list (full replace) [SF]

## List view
- Manual path. Label under 40 characters; share with the narrowest group that needs it [SF]

## Page layout and assignment (the analyst sets it)
- Add fields to an existing section; field behavior `Edit` / `Required` / `Readonly` [SF]
- Prefer Dynamic Forms on Lightning pages when the object already uses them [SF]

## Flow
- Label `[Object] - [Trigger Type] - [Brief Description]` ⚠; API name `[Object]_[TriggerType]_[Process]` [FS]
- One flow per object and trigger context; order with the Trigger Explorer; before-save for field updates on the same record, after-save for actions and related records [FS V2]
- Specific entry criteria; "only when updated to meet the condition" [FS V2]
- No DML or Get Records inside loops: collect, then one DML [FS] (the reviewer checks this)
- Fault path on every Create/Update/Delete to `Subflow_Log_Error` with `txtErrorMessage={!$Flow.FaultMessage}`, `txtFlowName`, `txtRecordId` ⛔ [FS][ORG]
- Built as Draft; the analyst activates ⛔ [P]
- No Process Builder or workflow rules ⛔ [RN: 49 PBs and 96 rules still to migrate]
- Resource prefixes `var_`, `rec_`, `col_`, `for_`, `con_`; elements `Get_`, `Dec_`/`Check_`, `Assign_` [FS V2]
- Logic repeated more than twice → subflow `Subflow_<Purpose>` [FS V2]
- Send Email by template name, never template ID [RN]
- Reviewer gate: `unity-flow-reviewer` zero-tolerance pass and ≥85/100 to build [P]
- No Apex: logic too complex for Flow is a developer ticket ⛔ [P]
