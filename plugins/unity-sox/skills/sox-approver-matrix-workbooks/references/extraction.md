# Extraction reference

All queries run against Grow production after the two-step identity gate. One call at a time.
Ids in CSVs are the first 15 characters of the 18-char Id (matches the report export and previous quarters).

## CSV rules
- Header row exactly as `config.json → objects[].columns` (or the headers below for shared files).
- Standard CSV quoting. Dispute amounts like `1,000` and matrix names contain commas — they must be quoted.
- Blank for null. Write rows exactly as returned: no dedup, no trimming, no "fixing" names. Odd data (e.g. a matrix Name that mentions a different person than Approver1) is a finding, not something to correct.

## 1. Matrix rows per object
Use the `soql` in `config.json` for each object.

| Object | Approx rows (Oct 2026) | How to pull |
|---|---|---|
| Bill__c | 86 | One call, relationship names |
| Invoice__c | 154 | One call, relationship names |
| Credit_Check__c | 383 | One call, but delegate to a subagent: ~80K tokens of JSON |
| Dispute__c | 1,399 | Subagent. Ids only, `LIMIT 700`, page with `AND Id > '<last>'`, resolve names after |

CSV column mapping:
- Bills: `Id[:15], Name, 'Bill__c', Division__c, Office__c, Approver1__r.Name, Approver2__r.Name`
- Invoice: `Id[:15], Name, 'Invoice__c', Division__c, Approver1__r.Name, Approver2__r.Name`
- Credit: `Id[:15], Name, 'Credit_Check__c', Division__c, Sub_Division__c, Department__c, Office__c, Team__c, Team_for_Approval__c, Credit_Amount__c, Account_Manager__r.Name, Approver1..Approver_4 names`
- Dispute: `Id[:15], Dispute_Type__c, Division__c, Department__c, Team__c, Dispute_Amount__c, Approver1..Approver5 names`

Why Ids-then-names for Dispute: relationship objects add ~200 characters of `attributes` per approver per row. With five approver slots × 1,400 rows that is the difference between ~120K and ~400K tokens.

### Subagent brief (copy, fill the folder)
> Read-only extract from Salesforce Grow production (org 00Db0000000JqmVEAS, already gated). Load the soqlQuery tool of the Grow read connector. Issue SOQL serially. Run these queries [paste from config.json] and write CSVs with the Write tool to `<run folder>` with these headers [paste]. 15-char Ids, quote values with commas, blank for nulls, no edits. For Dispute, page with `Id >` and resolve user Ids with one User query. After writing, run `SELECT COUNT(Id) c_<obj> FROM Approver_Matrix__c WHERE Object_API_Name__c = '<obj>'` and, for Dispute, `SELECT ApproverN__c a, COUNT(Id) c FROM Approver_Matrix__c WHERE Object_API_Name__c='Dispute__c' GROUP BY ApproverN__c` for N=1..5 and confirm the CSV matches. Report row counts, SOQL used, errors verbatim. Don't paste CSV contents back.

If the subagent had to transcribe large tool results by hand (it happens when results overflow to a file), the GROUP BY checks plus a 3-row spot check by the main agent are mandatory.

## 2. Modify All — `modify_all.csv`
Per object:
```sql
SELECT Id, Parent.Profile.Name, Parent.Name, Parent.IsOwnedByProfile,
       PermissionsCreate, PermissionsDelete, PermissionsEdit, PermissionsModifyAllRecords, SobjectType
FROM ObjectPermissions
WHERE SobjectType = '<obj>' AND PermissionsModifyAllRecords = true
```
Header: `SobjectType,ObjectPermissions Id,Profile Name,Permission Set Name,Is Profile-owned,Create,Delete,Edit,Modify All`
(`Permission Set Name` = `Parent.Name`; for profile-owned rows that's the internal `X00e…` name.)

## 3. Permission-set assignees — `permset_users.csv`
For every row with `IsOwnedByProfile = false`:
```sql
SELECT Id, PermissionSet.Name, Assignee.Name, Assignee.Profile.Name, Assignee.FN_Role__c, Assignee.IsActive
FROM PermissionSetAssignment
WHERE PermissionSet.Name IN (<sets>) AND IsActive = true
ORDER BY PermissionSet.Name, Assignee.Name
```
Write one row per (object, set, assignment) — a set that grants Modify All on several objects (e.g. SSO_Integration_User) repeats per object.
Header: `SobjectType,Permission Set,Assignment Id,Assignee,Assignee Profile,FN Role,User Active`

Oct 2026 non-profile sets: Delete_Bills, Modify_All_accounts_Payments_for_finance (Bill__c); Invoices_Mazi_s_approval (Invoice__c); Modify_All_Credit_Check, Credit_Check_Modify_All (Credit_Check__c); SSO_Integration_User (all four). New sets show up on their own — don't hard-code the list.

## 4. Active users per Modify All profile — `profile_users.csv`
```sql
SELECT Profile.Name, COUNT(Id) c_users FROM User
WHERE IsActive = true AND Profile.Name IN (<profile names from step 2>)
GROUP BY Profile.Name
```
Header: `Profile,Active Users`. Profiles missing from the result have 0 active users (Oct 2026: Pardot Admin, System Administrator Custom).

## 5. Custom setting — `custom_setting.csv`
```sql
SELECT Id, Name, SetupOwnerId, Object_API_Name__c, Object_API_Field_Name__c,
       Approver_Matrix_API_Field_Name__c, Output_Field__c, LastModifiedDate, LastModifiedBy.Name
FROM Dynamic_Approval_Process__c ORDER BY Object_API_Name__c, Name
```
If the field list may have changed, describe the object first and name fields explicitly (never `FIELDS(ALL)`; skip anything that looks like a secret or tax id).
Header: `Id,Name,SetupOwnerId (Location),Object API Name,Object API Field Name,Approver Matrix API Field Name,Output Field,Last Modified Date,Last Modified By`
Oct 2026: 19 rows — 13 Credit_Check__c, 6 Invoice__c, none for Bills/Dispute (they route by flow).

## 6. Counts for verify.py
```sql
SELECT COUNT(Id) c_bill FROM Approver_Matrix__c WHERE Object_API_Name__c = 'Bill__c'
```
…one per object, then `python scripts/verify.py <run folder> --counts bill=.. invoice=.. dispute=.. credit=..`.

Useful context query (orphans and other matrices):
```sql
SELECT Object_API_Name__c, COUNT(Id) c_am_obj FROM Approver_Matrix__c GROUP BY Object_API_Name__c
```
Oct 2026: Dispute 1,399 · Credit 383 · Opportunity__c 161 (Ads Deal Desk, includes the "Integration fee" upsell type) · Invoice 154 · Bill 86 · blank 68 · Tier__c 26 (deprecated Deal Payment) · Payment_Term_Request__c 12 · Case 7.
