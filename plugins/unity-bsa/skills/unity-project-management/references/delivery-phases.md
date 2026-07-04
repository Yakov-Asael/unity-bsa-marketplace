# Unity Delivery Phases

The team's Salesforce delivery flow. Each phase has an exit gate and the Unity skill that helps. Scale everything to project size — a small change compresses phases; a high-scope project needs POCs and estimation up front.

## High-level phases
Requirements → Scope → Design (+ Planning/ETA) → Development / Implementation → QA → QA with POC → Go Live

## Phases, gates, and handoffs

| # | Phase | Focus (keep high-level) | Exit gate | Skill |
|---|---|---|---|---|
| 1 | **Requirements** | Gather requirements, **proactively surface what's MISSING** (edge cases, error paths, data, security, reporting, adjacent teams), ask follow-ups | "Why" documented; missing requirements raised; every open question has an owner | `unity-tech-design` (Mode B), `unity-comms` |
| 2 | **Scope** | A **short, precise scope statement** + a **high-level note per major step** — not a detailed in/out list | One-line scope + step outline agreed; rough ETA set | — |
| 3 | **Design + Planning/ETA** | TDD, mockups; **identify POCs (mainly for high-scope / cross-team projects)**; **estimate effort, split dev vs BSA, commit an ETA** | TDD approved; effort estimated & ETA committed; POCs engaged if high-scope | `unity-tech-design` (Mode A), `unity-sfdc-mockups` |
| 4 | **Development / Implementation** | Build per the TDD | Build complete; meets Unity flow standards | `unity-flow-reviewer` |
| 5 | **QA** | High-level only: test scenarios run (details live in `unity-qa-debug`) | Results captured | `unity-qa-debug` |
| 6 | **QA with POC** | High-level only: POC validates, feedback implemented | POC sign-off | `unity-qa-debug`, `unity-comms` |
| 7 | **Go Live** | Deploy; **ask the go-live follow-ups** (below) | Follow-ups resolved; live & monitored | `unity-comms` |

## Planning & ETA
- **Rough ETA** at Scope close; **committed ETA** after Design once work is estimated and split (dev vs BSA implementation).
- Surface dependencies/POCs that affect the timeline early.

## Go-live follow-ups (always ask)
- Is a **backfill / datafix** needed for existing records?
- **Comms plan** — who's told, and how (use `unity-comms`)?
- **Rollback** plan if it goes wrong?
- **Monitoring** — which KPIs/dashboards confirm success?

## Rules
- **Scope is short and precise** — a headline + high-level step notes. Detail belongs in the TDD, not the scope.
- **Surface missing requirements** — don't just consolidate what you were given; think about what's absent.
- **Scale POC identification to project size** — high-scope/cross-team → identify POCs in Design; small changes → skip.
- **Keep QA phases high-level here** — depth is `unity-qa-debug`'s job.
- **Don't skip gates**; requirements before design, design before build.
