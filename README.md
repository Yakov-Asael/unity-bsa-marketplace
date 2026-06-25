# Unity BSA Plugin

A Claude Code plugin for the Unity Business Systems team. It packages each "power" of the Unity Salesforce BSA as a focused, standards-enforcing skill.

> Private repo — installing requires access to `Yakov-Asael/unity-bsa-plugin`.

## Skills

**Active (V1):**

| Skill | What it does | Triggers on |
|---|---|---|
| `unity-sf-bsa` | Senior Salesforce Architect persona + router to the focused skills | Salesforce, BSA, org, general delivery questions |
| `unity-flow-reviewer` | Reviews Flow XML/JSON → Deployment Readiness Score /100, zero-tolerance gate, "how to get approved" remediation | review my flow, flow XML, bulkification, fault path |
| `unity-tech-design` | Writes focused PRDs/TDDs from the combined Unity template; plans before writing; self-reviews | write a PRD/TDD, technical design, document this feature |
| `unity-sfdc-mockups` | SLDS 2.0 mockups + Unity-branded HTML email alerts (black + SLDS blue, no other accents) | mockup, SLDS, Lightning page, email alert |
| `unity-comms` | Status updates + stakeholder replies in the team's voice | status update, reply to stakeholder, summarize |

**Work in progress (V2 — not yet active):** `unity-presentations`, `unity-project-management`, `unity-qa-debug`.

## Install

### Option A — Marketplace (recommended, updatable)
In a Claude Code terminal:
```
/plugin marketplace add Yakov-Asael/unity-bsa-plugin
/plugin install unity-bsa
```
Restart Claude Code. Run `/help` and confirm the skills appear.

To update later: re-sync the marketplace, then reinstall.

### Option B — Folder drop (no auto-update)
1. Download `dist/unity-bsa.zip` from this repo.
2. Unzip into your plugins directory (e.g. `~/.claude/plugins/`).
3. Restart Claude Code.

## Standards source
The skills enforce Unity's internal standards (Flow Design Standards, the combined PRD/TDD template, SLDS 2 + Unity palette, comms tone). Each skill carries its own `references/` files as the source of truth.

## Versioning
See `plugins/unity-bsa/.claude-plugin/plugin.json`. Current: **1.0.0**.
