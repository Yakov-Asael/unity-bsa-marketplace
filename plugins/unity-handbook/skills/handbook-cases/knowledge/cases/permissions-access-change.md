---
cluster: permissions-access-change
name: Permissions and access changes for existing users
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-17
count_90d: 21
---
## Definition
An existing user needs a permission, profile/role change, object access, or a feature button.

## Detection signals
- 'permission'
- 'access'
- 'role'/'profile'
- Sub_Category User Permissions/Privileges
- Example subjects (paraphrased): Grant access to invoice / bill management pages · Change a user's role or profile after a team move · Permission to edit a specific field or object
- 'Unhandled fault' after submitting the Meeting Action button from a meeting follow-up report on `Event_Meeting__c` records. (learned 2026-10-18 from closed cases)

## How we resolve it
- Owner ruling: name the **exact permission the user is missing**.
- Bill Management page (publisher side) = permission set `Finance_Project_PUB` (Bill_Management_lwc, `Bill__c`, `Bill_Line__c`, FN_Bills pages) or `Invoices_Bills_Management`; Invoice Management (advertiser side) = `Finance_Project_ADV` (Invoice_Management_Lwc, `Invoice__c`, `Invoice_Line__c`). 'No access to Apex class BillManagement…' → the PUB set is missing.
- 'No records found' with access present = scope: the user sees only records where they are the AM.
- Role moves (CP → Sales): profile + permission sets + `belong to mobile sales` flag; the manager field syncs from Workday. Object-level asks (Modify All on Credit) → dedicated permission set, SOX-relevant.
- Omni-Channel missing while access exists: first check which Lightning app the user opens; the Omni-Channel utility is only in the Service Console app. (learned 2026-10-14 from closed cases)
- A field missing in one Lightning app after a layout or permission change: have the user log out and back in before investigating. (learned 2026-10-15 from closed cases)
- 'Unhandled fault' on the Meeting Action screen flow when updating `Event_Meeting__c`: check the user's Marketing User checkbox (`UserPermissionsMarketingUser`). `Event_Meeting__c` is master-detail child of Campaign, so without it the user cannot edit; set it true and retry. (learned 2026-10-18 from closed cases)
- Read access to invoices and bills: assign the Finance ADV and Finance PUB permission sets. (learned 2026-11-08 from closed cases)

## What to ask the requester
- What exactly fails (screenshot / error text)?
- Which colleague has the right access to mirror?
- Is this a permanent role change approved by the manager?

## Canonical answer
**Summary:** An existing user cannot open a page, object or button, or has the access and misreads what they see. Bill Management (publisher) needs permission set `Finance_Project_PUB` (Bill_Management_lwc, `Bill__c`, `Bill_Line__c`, FN_Bills pages); Invoice Management (advertiser) needs `Finance_Project_ADV` (Invoice_Management_Lwc, `Invoice__c`, `Invoice_Line__c`); `Invoices_Bills_Management` covers both. Inside them users see only records where they are the AM. Name the exact missing set; never answer 'check permissions'.
**Suggested resolution:**
1. Ask what exactly fails (screenshot or error text) and which colleague has the right access to mirror.
2. Map the error to the set: 'No access to Apex class BillManagement…' means `Finance_Project_PUB` is missing.
3. Assign the missing permission set, or mirror the named colleague's sets; have the user log out, back in and retry.
4. If the set is assigned but 'No records found': no change - the user is not the AM on those records.
5. If a role move (CP to Sales): confirm manager approval, then update the profile, permission sets and `belong to mobile sales` flag; Workday syncs the manager field.
6. If Modify All (e.g. on Credit), admin-level or finance-approval rights: do not assign; escalate with the exact permission - SOX-relevant, needs a dedicated permission set.

## Common mistakes
- Changing presence configurations or queues before checking the Lightning app the user works in. (learned 2026-10-14 from closed cases)
- Assigning a permission without checking whether the user already has it. (learned 2026-10-14 from closed cases)

## Escalate when
- Admin-level or finance-approval permissions.
- SOX-relevant Modify All changes.
