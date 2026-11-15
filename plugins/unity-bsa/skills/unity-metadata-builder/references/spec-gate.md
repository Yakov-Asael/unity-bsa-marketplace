# Spec gate and understanding check

Nothing is built from one sentence. The gate has three parts, run in order. Ask in batches of at most five questions.

## 1. The two documents

| Needed | Missing → |
|---|---|
| An ISITBA story (`ISITBA-<n>`) with acceptance criteria | Hand off to `unity-tech-design` Mode B to write it |
| A PRD or TDD for anything beyond a single field | Hand off to `unity-tech-design` Mode A |

Grade what exists with the sibling standards (don't copy them here):
- the story: `unity-tech-design/references/user-story-standard.md` (INVEST, Definition of Ready, AC for edge, null, 200-record, permission and error cases);
- the PRD/TDD: `unity-tech-design/references/prd-tdd-template.md` and that skill's self-review checklist.

"Not sprint-ready" stops the build. List the gaps, quoting the vague lines.

## 2. The Metadata inventory

The design must contain this table. If it doesn't, build it together with the analyst from the design, then confirm it.

| Type | API name | Label | Data type / details | Why it's needed | Reused or new |
|---|---|---|---|---|---|

Add your own suggestions as extra rows marked **Suggested**: a missing field, a better type, field access, help text, an existing field to reuse, a subflow. The analyst accepts or rejects each one. Don't take their list as final, and don't block on a suggestion.

## 3. Understanding check

Before the Build Plan, the analyst explains in their own words:
1. **Trigger and entry criteria:** what starts it, and on which records exactly?
2. **Failure:** what happens when it fails, and who finds out? (Every fault path goes to `Subflow_Log_Error`.)
3. **Who is affected:** which users, profiles and integrations see or run it?

If the explanation doesn't match the spec, point at the mismatch and ask again. Don't build until it matches.

## Design artifacts (when they apply)

- Any UI (screen flow, Lightning page, email alert): a mockup first with `unity-sfdc-mockups` (SLDS 2, Unity tokens and icons), so every build looks alike.
- A data-model or process change: the Process Map / ERD update is part of the Definition of Done (Flow Standards V2).

## Don't limit creativity

The gate checks that a design exists and is understood. It doesn't prescribe the solution. If the analyst picks a valid approach you wouldn't, say what you'd do differently and why in one or two lines, then build theirs.
