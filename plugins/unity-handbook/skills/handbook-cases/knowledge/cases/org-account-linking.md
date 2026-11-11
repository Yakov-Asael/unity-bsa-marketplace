---
cluster: org-account-linking
name: Org / dashboard account not linked to Salesforce
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-22
count_90d: 17
---
## Definition
A new org or dashboard account (uAds, Tapjoy, Aura) cannot be found in SF or must be linked to an SF account / BI opportunity.

## Detection signals
- 'Org Sync Issue'
- cloud.unity.com org link
- Tapjoy dashboard partner id
- 'link ... to SFDC'
- Example subjects (paraphrased): New org went live but cannot be found in SF · Link a dashboard account (uAds / Tapjoy) to an SF account · Append a partner ID to the BI opportunity

## How we resolve it
- New orgs stream into SF once they have an activity (campaign, placement, project); without one there is no entity to link - ask for the org ID and check.
- Linking: set the org/partner ID on the account's operational (BI) opportunity, or create the opportunity with the partner ID; then the dashboard maps.
- Tapjoy dashboards: find the SF account already tied to the dashboard before creating links (often it exists).
- Owner procedure (owner feedback 2026-09-22): search the org / partner ID in SF. Exists as a **Lead** → convert it. Not found → decide advertiser vs publisher, create the Account and its Opportunity, and log the ID in `Opportunity.BI_Opportunity__c` with the product prefix: uAds → `UP<id>` (publisher) / `UA<id>` (advertiser); Tapjoy / ironSource / iAds → `P<id>` / `A<id>`.
- After linking the org through a new operational opportunity BI_Opportunity__c, also fill the first BI opportunity field on the Account and press Sync Credit so the credit shows in uDash. (learned 2026-10-14 from closed cases)

## What to ask the requester
- Org ID / partner ID and the SF account link?
- Does the org already have a campaign or placement?
- Which product (uAds, Tapjoy, Aura)?

## Canonical answer
**Summary:** A dashboard org or partner account (uAds, Tapjoy, Aura, ironSource) is missing from Salesforce or must be linked to an SF account and BI opportunity. Orgs stream in only once they have activity; the dashboard maps through the prefixed ID in `Opportunity.BI_Opportunity__c` on the operational opportunity. Org unblock requests are product-side, not Salesforce.
**Suggested resolution:**
1. Ask for the org or partner ID, the product, any SF account link, and whether the org has activity.
2. Search the ID across Accounts, Opportunities (`BI_Opportunity__c`) and Leads; a Lead: convert it.
3. Not found and no activity: no change; it streams in once activity exists.
4. Not found with activity: decide advertiser vs publisher, create the Account and Opportunity, set `BI_Opportunity__c` = prefix + ID (uAds `UP`/`UA`; Tapjoy, ironSource, iAds `P`/`A`).
5. Connecting an org to an existing account: create a new operational opportunity with the prefixed ID, fill the first BI opportunity field on the Account, then **Sync Credit** so the credit shows in uDash.
6. Never repoint a `BI_Opportunity__c` that already maps an org: it breaks its connections; create a new opportunity. Fix only a wrong prefix on an unmapped one.
7. Filed as a New User request: the form auto-closes; still create the Account and reply with its link.
8. Org blocked on the dashboard: product team. Many orgs not streaming: the BI sync incident channel.

## Common mistakes
- Editing an existing BI_Opportunity__c value breaks its connections; create a new opportunity with the new BI opportunity instead. (learned 2026-10-14 from closed cases)
- An org account-creation request filed under Category__c User / Sub_Category__c New User triggers the automatic New user form closure; still create the Account and reply with its link. (learned 2026-10-15 from closed cases)

## Escalate when
- Kraken / BI sync incidents affecting many accounts - post in the sync incident channel.
- Requests to unblock a dashboard org are not Salesforce: the block is a product-side control; redirect the requester to the product team. (learned 2026-10-15 from closed cases)
