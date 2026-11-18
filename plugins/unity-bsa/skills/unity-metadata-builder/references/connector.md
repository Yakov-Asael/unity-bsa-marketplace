# Build connector: "Beta - Salesforce Grow Admin - UAT" (Headless 360)

Tools: `discover`, `describe`, `dispatch_readonly` (GET), `dispatch` (writes). Mapped from the recipes on 2026-11-15. Use this table instead of re-running `discover`. Run `describe <recipe>` only when a row says so or a call fails unexpectedly.

## Before the first write in a session

1. `dispatch_readonly GET /services/data/v66.0/query` with `q=SELECT Id, Name, IsSandbox FROM Organization`. It must return `00DQI00000J4hjN2AR`, `IsSandbox=true`. The hook records it and blocks writes until it has.
2. For flows: read the REST version once with `GET /services/data/` and use the latest version in flowbuilder paths.

## Rules for every write

- **Permissions and layouts are recommend-only.** Claude reads them (reuse recon, verification) but never writes them.

- `/headless/metadata` body is a JSON object `{type, fullName, xmlRep}`. `xmlRep` is one XML string on a single line (escape or remove newlines). A stringified body returns 500.
- **Never trust the write response.** A create can return 500 and still commit. Always read back, then report "verified" only from the read-back.
- **Full replace vs merge** (below) decides whether you must read the current definition first. For full-replace types, always read, change, then write the whole thing. Keep the read as the rollback snapshot.
- **Deletes aren't available** in this beta (403). Removing anything is a manual Setup step.
- `400 UNSUPPORTED_OPERATION`: that type/operation isn't enabled on the org → manual path. `500 METADATA_CRUD_ERROR … FileBasedMetadataDao`: missing entitlement → manual path.

## Per type

| Type | Write | Read-back | Replace / merge | Notes |
|---|---|---|---|---|
| Custom field | `POST` (create) / `PUT` (update) `/headless/metadata`, `type=CustomField`, `fullName=Object.Field__c` | `GET /headless/metadata?type=CustomField&fullName=…` | full definition per field | `xmlRep` = `<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata"><fields><fullName>Field__c</fullName>…</fields></CustomObject>` (local name inside). Picklists: `<restricted>true</restricted>`. Recipe: `platform-custom-field-generate` |
| Custom object | `POST` / `PUT` `/headless/metadata`, `type=CustomObject`, `fullName=Obj__c` | GET same | **merge** on PUT | No `<fullName>` inside `xmlRep`. `deploymentStatus=Deployed`, `visibility=Public`, `sharingModel=ReadWrite` (or `ControlledByParent` with a master-detail). Description required. Recipe: `platform-custom-object-generate` |
| Validation rule | `PUT /headless/metadata`, `type=CustomObject`, `xmlRep` with only `<validationRules>…</validationRules>` | GET the CustomObject, find the rule | merge | Not live-tested yet: if it's rejected, use the manual path. Name: letters, digits and single underscores, no `__c`. Check the formula first with `POST /services/data/v67.0/connect/formula/validate` `{entityName, formula, formulaType:"Validation", returnType:"Boolean"}` (dry run) |
| Global value set | `POST` / `PUT` `/headless/metadata`, `type=GlobalValueSet`, `fullName=<Name>__gvs` | GET same | **full replace** | Values left out become inactive. Fields reference it by the bare name (no `__gvs`). Create it before the field. Recipe: `platform-value-set-generate` |
| Permission set (new or existing), field and object access, assignments | **none: recommend only** | `SELECT Field, PermissionsRead, PermissionsEdit FROM FieldPermissions WHERE Parent.Name=…` after the analyst says done | — | Claude never writes permissions. Put the recommendation in the Build Plan and give the Setup steps from `references/manual-paths.md`. The hook blocks `PermissionSet`, `FieldPermissions`, `ObjectPermissions`, `PermissionSetAssignment` and related writes (B23) |
| Flow | `POST /services/data/vXX.0/flowbuilder/flow/actions/save` `{flow:{fullName, metadata:<full flow JSON>}, saveType}` | `GET …/flowbuilder/flow/{flowId}/validation-results`; `GET …/flow/{definitionId}/versions` | **full replace** | `saveType`: `createNewFlow` (new), `saveAsNewVersion` (existing, keeps the active version), `saveDraft` + `currentFlowId` (edit the current draft). Saves land as Draft; `InvalidDraft` = failed even on 201. Dry run first: `POST …/flowbuilder/flow/actions/validate` `{flow:{fullName, metadata}}`. New flows need `processMetadataValues` `CanvasMode=AUTO_LAYOUT_CANVAS` and `locationX/locationY` on elements. Check the API name is free first. **Activation isn't possible through the connector**: the analyst activates in Flow Builder. Recipe: `automation-flow-coordinate` (author) |
| Page layout and layout assignment | **none: the analyst sets it** | Tooling `SELECT LayoutId FROM ProfileLayout WHERE …`, or the field in the layout via `GET /tooling/sobjects/Layout/{id}` | — | Recommend the layout, section and field behavior in the Build Plan; the analyst places it in Setup. The hook blocks `Layout` and `Profile` writes (B19, B23) |
| List view | none | — | — | **Manual path.** No connector recipe writes list views |

## The Unity rules win

The connector's own guidance says to add fault paths only when the user asks. Unity's standard is stricter: every Create/Update/Delete gets a fault path to `Subflow_Log_Error` (not possible on before-save updates, Decisions, Assignments, Screens, Loops or Subflow elements). Never point a fault path at an End or at the element's own success target.
