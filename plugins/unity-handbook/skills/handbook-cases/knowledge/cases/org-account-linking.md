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

## What to ask the requester
- Org ID / partner ID and the SF account link?
- Does the org already have a campaign or placement?
- Which product (uAds, Tapjoy, Aura)?

## Canonical answer
**Summary:** A dashboard org or partner account (uAds, Tapjoy, Aura, ironSource) is missing from Salesforce or must be linked to an SF account and BI opportunity. Orgs stream in only once they have an activity; the dashboard maps through the prefixed ID in `Opportunity.BI_Opportunity__c` on the operational opportunity. Typically there is no activity yet, or the ID is missing or misprefixed.
**Suggested resolution:**
1. Ask for the org or partner ID, the product, any SF account link, and whether the org has a campaign, placement or project.
2. Search the ID across Accounts, Opportunities (`BI_Opportunity__c`) and Leads.
3. If found as a Lead: convert it.
4. If not found and no activity: no change; it streams in once activity exists.
5. If not found with activity: decide advertiser vs publisher, create the Account and Opportunity, set `Opportunity.BI_Opportunity__c` = prefix + ID (uAds `UP<id>`/`UA<id>`; Tapjoy, ironSource, iAds `P<id>`/`A<id>`); for Tapjoy check for an already-linked SF account first.
6. If the account exists but the ID or prefix is wrong: fix `BI_Opportunity__c` on the operational opportunity instead of creating another; it maps after the next sync.
7. If many orgs fail to stream: post in the Kraken / BI sync incident channel.

## Common mistakes

## Escalate when
- Kraken / BI sync incidents affecting many accounts - post in the sync incident channel.
