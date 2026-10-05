---
cluster: marketing-campaign-uploads
name: Event meeting / lead uploads to campaigns
status: approved
approved_by: Yakov Asael
approved_on: 2026-09-22
count_90d: 13
---
## Definition
Marketing asks to upload event meetings or leads from a sheet into a Salesforce Campaign, or asks about the events dashboard.

## Detection signals
- Sub_Category Marketing
- Google Sheet + Campaign link
- 'upload ... meetings/leads'
- Ads Event Dashboard
- Example subjects (paraphrased): Upload event meetings from a sheet into a Campaign · Upload leads for an event campaign · Events dashboard not showing a new campaign

## How we resolve it
- Upload from the shared sheet into the named Campaign as event meetings (opportunities) or leads; the sheet must follow the original template (first/last name split, valid meeting-type values).
- Meetings can only connect to open opportunities - closed-won opps fail.
- Events dashboard lags the data load - run a sync/refresh and allow a few hours.
- Owner procedure (owner feedback 2026-09-22): insert `Event_Meeting__c` records from the sheet. Templates: Aura tab https://docs.google.com/spreadsheets/d/1xORNDfFDcWl-pEsk-kIZzru6WQ4Nyfg6JTCYBIQRvxc/edit?gid=448404497 ; Ads tab https://docs.google.com/spreadsheets/d/1xORNDfFDcWl-pEsk-kIZzru6WQ4Nyfg6JTCYBIQRvxc/edit?gid=1673559987 . Map the requester's sheet onto the matching template first.

## What to ask the requester
- Sheet link (shared) and Campaign link?
- Leads or meetings/opportunities?

## Canonical answer
**Summary:** Marketing needs event meetings or leads from a Google Sheet loaded into a named Campaign, or asks about the Ads Event Dashboard. The load inserts `Event_Meeting__c` records (or leads) mapped from the original events template (Aura and Ads tabs, first/last name split, valid meeting-type values). Meetings attach only to open opportunities, so closed-won rows fail; the dashboard lags the load by hours.
**Suggested resolution:**
1. Confirm the sheet is shared with you and the Campaign link is present; ask if not.
2. Ask whether the rows are leads or meetings/opportunities; the template columns differ.
3. Map the sheet onto the matching template tab (Aura or Ads), fixing the name split and meeting-type values there; if it needs a new mapping, escalate first.
4. If a meeting row points at a closed-won opportunity: skip it and note the reason on the sheet.
5. Insert the `Event_Meeting__c` records (or leads) linked to the Campaign; the Campaign count must equal the loaded rows.
6. If the complaint is the dashboard: run a sync/refresh and tell the requester to allow a few hours.
7. Send the requester: loaded N meetings/leads, M rows skipped (notes on your sheet); the dashboard updates within hours.

## Common mistakes

## Escalate when
- Template deviations that need re-mapping.
