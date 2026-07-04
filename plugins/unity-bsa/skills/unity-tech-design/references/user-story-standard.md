# Unity User Story Standard

The team had no formal template, so this is the standard. Keep stories small, specific, and testable.

## Story format
`As a [specific role], I want to [action], so that [benefit].`
- **Role** is specific — name *which* user/admin (e.g., "SMB support agent", not "user" or "admin").
- **Action** is what the person does, not what the system does.
- **Benefit** is a real business outcome, not a restatement of the feature.

## Acceptance criteria — pick the format per story
- **Given / When / Then** — for behavioral / scenario-based logic; maps cleanly to test cases (and to `unity-qa-debug`). Use when there are clear pre-conditions and triggers.
- **Declarative checklist** — for configuration, field, or list-of-conditions work; each bullet an independently-testable pass/fail.
Use G/W/T when behaviour depends on state/triggers; use a checklist when it's a set of static conditions. Complex stories can mix both.

## AC quality bar (enforce)
- Each AC is **independently testable** (maps to a single test case).
- **No ambiguous words**: "easy", "fast", "appropriate", "reasonable", "properly", "etc.".
- **Edge cases covered**: null / empty values, empty collections, large data volumes (LDV), permission boundaries.
- **Error scenarios covered**: what happens when it fails?
- Written in **Given/When/Then** or a **clear declarative** form.

## Structure of a finished story
1. **Title** — short, action-oriented.
2. **Story** — the As a / I want / so that line.
3. **Acceptance Criteria** — G/W/T and/or checklist.
4. **Priority** — MoSCoW: Must / Should / Could / Won't (this release).
5. **Notes / dependencies** — related objects, integrations, other teams/POCs.
6. **Out of scope** — what this story explicitly does not cover.

## INVEST check (quality gate)
Independent · Negotiable · Valuable · Estimable · Small · Testable. If a story fails **Small** (too big to finish in a sprint), split it and say how.

## Definition of Ready (Sprint-Ready gate)
A story is **Sprint-Ready** only when: role/action/benefit are specific; every AC is testable and unambiguous; edge + error cases are covered; priority is set; dependencies are named; it's estimable and small enough.
- If it passes → mark **✅ Sprint-Ready**.
- If not → mark **🔴 Not Sprint-Ready**, list exactly what's missing, and rewrite it into a ready version.

## Handoffs
- Finished story → offer `unity-tech-design` to draft the TDD.
- Acceptance criteria → offer `unity-qa-debug` (Mode B) to turn them into QA test scenarios.
