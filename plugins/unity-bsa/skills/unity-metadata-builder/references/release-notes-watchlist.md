# Release-notes watchlist (Summer '26 + Winter '27, Grow deck, Oct 2026)

Only the items that change how metadata is built. Re-check this list each release.

## Flow
- **Send Email by template name** (action 3.0.1+): use it, so sandbox → production deploys don't break on template IDs. Never reference a template ID.
- **Native date operators in Decisions** (Is Today, Last N Days, ...; Date fields only): prefer them over formula workarounds.
- **Split by Field Value / Split by Date**: one branch per value or date window; keep Decision for multi-condition logic.
- **Batch size on scheduled flows** (1-200, runtime 63.0+): set it when entry criteria may match many records.
- **Flow Test Mode (beta)**: assertions plus mocked actions and subflows. Use it to test fault paths by mocking a failing `Subflow_Log_Error` caller.
- **Save-time warnings** (Winter '27): Create Records missing required fields, or text longer than the field, now warn on save. Treat a warning as a defect.
- **Automatic retry on record lock** (~10 s): don't add retry workarounds.
- **"User Context — Enforces User Permissions" run mode** (API 68+): consider it for screen and autolaunched flows that must respect the running user's access.
- **Edit History and Unused Resources filter**: remove unused resources before handing off.
- **Mass screen flows from list views**: selected IDs arrive in a text collection named exactly `ids`. Use this instead of custom bulk buttons.
- **Reactive visibility** on screens: no extra screen just to refresh visibility.

## Migration context
- 49 Process Builders and 96 workflow rules are still active: never add new ones; build record-triggered flows.
- 65 classic approval processes: new approvals use Flow Approvals.

## Access
- **Field Access view** in Object Manager: use it to confirm who can see a new field after the build.
- **Profile filtering enforced**: flows and reports that display other users' profile names may show less. Don't depend on profile names.
- Access goes through permission sets, never profiles.

## Claude and Salesforce
- The team's sanctioned Salesforce MCP is read-only for production. This skill writes only to UAT, through the build connector.
