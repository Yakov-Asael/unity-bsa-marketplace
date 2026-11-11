# Findings to flag

Report these briefly after delivering the workbooks. They're observations for the control owner, not changes to make — this skill never writes to Salesforce.

| Check | How to see it | Why it matters |
|---|---|---|
| Deactivated users still assigned a Modify All permission set | `permset_users.csv` where `User Active = false` (yellow in the workbook) | Auditors read an active assignment as access, even if the user can't log in. Easy to clean before sign-off. |
| Modify All via a business profile | Profile-owned rows other than System Administrator / Integration (e.g. Finance on Invoice__c) with active users > 0 | Broad access through a profile is harder to justify than a named permission set. |
| Approvers that are inactive users | `SELECT Id, Name FROM User WHERE IsActive = false AND Id IN (<approver ids>)` | An inactive approver stamped on new records stalls approvals. |
| Matrix Name ≠ Approver1 | Name text mentions one person, Approver1 is another (e.g. "Noam Kreimer" rows → May Kempner Reik) | Usually a reassignment where the label wasn't updated; worth a note so reviewers aren't confused. |
| Orphan matrix rows | `Object_API_Name__c = null` count (68 in Oct 2026) | Rows that no process reads; noise in any report without the object filter. |
| Custom setting coverage | Rows per object in `custom_setting.csv` | Only Invoice and Credit route through Dynamic_Approval_Process__c; Bills and Dispute route by flow, so their Custom Settings tab is context, not a control point. |

Oct 2026 results for comparison: Bills — Delete_Bills 6 users (2 inactive), Modify_All_accounts_Payments_for_finance 29 users (6 inactive); Invoice — Finance profile 42 active users, Invoices_Mazi_s_approval (Tal Rahamim, Bar Damti); Dispute — main profiles only; Credit — Modify_All_Credit_Check 5 users (all credit approvers), Credit_Check_Modify_All 1 user. Main profiles everywhere: System Administrator 20 active, Integration 12, SSO_Integration_User 1.
