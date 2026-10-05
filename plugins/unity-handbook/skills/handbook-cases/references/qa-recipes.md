# Q&A recipes - read-only research for one case

Every Salesforce call here is a read on the Grow PROD connector. The skill never writes. Skip any step whose source is not available in the session and say which sources were used.

## Query laws
- Scope lock: every `Case` query includes `RecordType.DeveloperName = 'Saleforce'`.
- One Salesforce call at a time per connector. Alias every aggregate. `COUNT()` before any row pull.
- Never filter on long-text fields (`Description`, `Resolution__c`, `RecordIds__c`, `Request_Account_Ids__c`): pull by date and match in-session.
- Never `GROUP BY` a formula field. A page of exactly 2,000 rows is truncated; use smaller pages.

## 0. Gate (only when a Salesforce connector is present)
`getUserInfo`, then `SELECT Id, Name, IsSandbox FROM Organization` → `00Db0000000JqmVEAS`, `IsSandbox = false`. Anything else: answer from knowledge only and say which org was seen.

## 1. The case itself (when a case number or link is given)
```sql
SELECT Id, CaseNumber, Subject, Description, Origin, Status, AccountId, CreatedDate, Resolution__c
FROM Case WHERE RecordType.DeveloperName = 'Saleforce' AND CaseNumber = '<number>' LIMIT 1
```
```sql
SELECT Incoming, MessageDate, TextBody FROM EmailMessage WHERE ParentId = '<case Id>' ORDER BY MessageDate ASC LIMIT 20
```
A teammate's outbound reply already on the case is the resolution of record: report it, do not re-diagnose.

## 2. The records the case names
- Account finance fields: `SELECT Id, NetSuit_ID__c, Finance_Approval_Complete__c, Payment_method__c, Subsidiary__c, Credit_Type__c, Credit_Amount__c, Credit_Percentage_Used__c, Is_Primary__c, Invoiced_with__c, Account_Manager__r.Name, Sales_Manager__r.Name, Department__c, Division_Picklist__c, Rating FROM Account WHERE Id = '<id>'`.
- Errors, pulled by date and matched in-session: `SELECT Id, CreatedDate, SObjectType__c, ClassName__c, Message__c, RecordIds__c FROM ErrorObject__c WHERE CreatedDate = LAST_N_DAYS:3 AND SObjectType__c = '<Object>' ORDER BY CreatedDate DESC LIMIT 50`; `SELECT Id, CreatedDate, Integration_Name__c, Interface_Name__c, NetsuiteID__c, accountID__c, Error_Message__c FROM Error_Log__c WHERE CreatedDate = LAST_N_DAYS:3 AND Integration_Name__c = 'NetSuite' ORDER BY CreatedDate DESC LIMIT 50`. Skip `FN_MassActionsBatch` rows.
- Owner history of a case: `SELECT Field, OldValue, NewValue, CreatedDate, CreatedBy.Name FROM CaseHistory WHERE CaseId = '<id>' ORDER BY CreatedDate ASC LIMIT 100`. Several owner changes in the same second are automations, not people.

## 3. Resolved closed cases of the same type
```sql
SELECT COUNT(Id) c FROM Case WHERE RecordType.DeveloperName = 'Saleforce' AND IsClosed = true AND Subject LIKE '%<keyword>%'
```
```sql
SELECT Id, CaseNumber, Subject, Resolution__c, ClosedDate FROM Case
WHERE RecordType.DeveloperName = 'Saleforce' AND IsClosed = true AND Subject LIKE '%<keyword>%' ORDER BY ClosedDate DESC LIMIT 10
```
`Resolution__c` is usually empty; read the outbound replies: `SELECT ParentId, TextBody FROM EmailMessage WHERE ParentId IN (<ids>) AND Incoming = false ORDER BY MessageDate DESC LIMIT 20`.

## 4. The mechanism
Prefer `handbook-code-lookup`, which reads deployed source from the org. If the user has a local SFDC-IS metadata copy: `grep -ril "<field | status value | alert name | flow name>" "<metadata path>/flows" "<metadata path>/workflows" "<metadata path>/objects/<Object>/validationRules" "<metadata path>/permissionsets"`, then read the match (active flag, criteria, recipients, formula) and name it by API name. Typical anchors: `Account.workflow-meta.xml` (credit alerts), `objects/Dispute__c/validationRules`, `flows/Grow_Ads_Account_Handover`, `flows/Mobile_Support_Case_Ownership`, `assignmentRules/Case`.

## 5. u-know
`ask_uknow` with the subject plus the object and field names; cite the article title. Treat it as background, not as the mechanism, unless it names the flow or rule.

## 6. Write the answer
Two sections, under 250 words, numbered steps, percentage confidence from the calibration table, cluster slug at the end. If nothing was found: say so, list what was checked, confidence under 25.
