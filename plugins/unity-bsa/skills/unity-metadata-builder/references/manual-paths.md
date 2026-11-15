# Manual paths (when the connector can't do a step)

Say exactly this, then give the steps for that type, filled in with the Build Plan values:

> The UAT admin connector can't do this step (`<reason>`). Switch to manual: build it in Setup using the steps below, then tell me when you're done and I'll verify it.

After "done", verify with a read-only query and report what matches and what doesn't. Never mark a manual step verified without the read-back.

## Custom field
Setup → Object Manager → `<Object>` → Fields & Relationships → New → `<type>` → Label `<label>`, Field Name `<API name without __c>`, Description, Help Text, (length / values / restricted) → Next → field-level security: **leave all profiles unchecked** (access comes from the permission set) → Next → page layouts: as the plan says → Save.
Verify: `SELECT QualifiedApiName, DataType, Description FROM FieldDefinition WHERE EntityDefinition.QualifiedApiName='<Object>' AND QualifiedApiName='<API name>'`

## Custom object
Setup → Object Manager → Create → Custom Object → Label, Plural Label, Object Name, Description, Record Name (Text or Auto Number), the "Allow Reports / Activities / Track Field History / Search" options from the plan → Save.
Verify: `SELECT QualifiedApiName, Label FROM EntityDefinition WHERE QualifiedApiName='<Obj__c>'`

## Validation rule
Setup → Object Manager → `<Object>` → Validation Rules → New → Rule Name, Active, Description, Error Condition Formula (paste the validated formula), Error Message, Error Location → Save.
Verify (Tooling): `SELECT ValidationName, Active, ErrorMessage FROM ValidationRule WHERE EntityDefinition.QualifiedApiName='<Object>' AND ValidationName='<Name>'`

## Permission set
Setup → Permission Sets → New (or open `<Name>`) → Object Settings → `<Object>` → Edit → object access and field permissions from the plan → Save.
Verify: `SELECT Field, PermissionsRead, PermissionsEdit FROM FieldPermissions WHERE Parent.Name='<Name>' AND SobjectType='<Object>'`

## Global value set / picklist values
Setup → Picklist Value Sets → `<Name>` (or the field's Values section) → New → one value per line → Save. Reorder if the plan says so.
Verify (Tooling): `SELECT DeveloperName, MasterLabel FROM GlobalValueSet WHERE DeveloperName='<Name>'`

## List view
App Launcher → `<Object>` tab → list view controls (gear) → New → List Name, API name, who sees it (narrowest group) → Save → Filters per the plan → Save → Select Fields to Display → Save.
Verify: `SELECT DeveloperName, Name FROM ListView WHERE SobjectType='<Object>' AND DeveloperName='<API name>'`

## Page layout / assignment
Setup → Object Manager → `<Object>` → Page Layouts → `<Layout>` → drag the field into `<section>` → Save. Assignment: Page Layouts → Page Layout Assignment → Edit Assignment → select profiles/record types → choose `<Layout>` → Save.
Verify (Tooling): `SELECT LayoutId FROM ProfileLayout WHERE ProfileId='<Id>' AND TableEnumOrId='<Object>'`

## Flow
Setup → Flows → New Flow (or open `<API name>`) → build per the reviewed design → Save (label and API name per the Flow Standards, description with the story ID) → don't activate until the reviewer and the bulk test pass.
Verify: `SELECT ApiName, Label, ActiveVersionId, LatestVersionId FROM FlowDefinitionView WHERE ApiName='<API name>'`
