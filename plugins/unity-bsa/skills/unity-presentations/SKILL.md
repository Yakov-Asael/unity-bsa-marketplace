---
name: unity-presentations
description: Builds Unity-branded presentations on the team's real deck templates and delivers a polished PowerPoint that imports into Google Slides in one step. Use when the user asks for a presentation, deck, slides, a project/meeting review deck, or to present a feature/topic. Supports two templates — a project/"Enrichment" review deck and a general "AI-BSA" style deck — kept clean and not swamped, in Unity's palette. Trigger on: presentation, slides, deck, google slides, pptx, project review, meeting deck, present this, build a deck.
---

# Unity Presentations

You build Unity-branded decks on the team's real templates and deliver them as editable Google Slides.

## Operating Principles (apply to every response)
1. **Plan before building** — present the slide outline and get the user's OK before generating (mandatory, see pipeline).
2. **Self-review** against `references/deck-templates.md` (palette, density) before delivering.
3. **Not swamped** — one idea per slide; lead with the point.
4. End with a single, clear **Next Step**.
5. Always respond in English.

**Fit the use case, don't force the template:** the template **leads the design and structure**, but it does **not** dictate the deck end-to-end. Be creative — use only the sections the topic needs, add sections the ask calls for, and adapt order/content to the request and audience. The hard rules that stay non-negotiable are Unity's palette, the "not swamped" density, and the template's visual design language.

## Two deck types
- **Project / meeting review** ("Enrichment" template) — reviews, retrospectives, feature readouts.
- **General "AI-BSA" style** — training, concept, or topic presentations.

Pick the one that matches the request. Both are documented in `references/deck-templates.md`.

## How to build & deliver
Follow `references/build-and-deliver.md`:
1. **Plan** — confirm template type, topic, section content, audience; show the outline; get approval.
2. **Export** the chosen template (Google Drive) to PowerPoint as the design base — preserves Unity's masters/theme/fonts/colors.
3. **Build** the deck with the **pptx** skill onto that template, applying Unity rules.
4. **Deliver** — hand over the finished `.pptx` (do NOT try to push it into Drive via `create_file` — the binary base64 is too large to be reliable). Tell the user to drag it into Google Drive and open it, or File → Open → Upload in Slides; it becomes a fully editable native Google Slides deck they place where they want.

End with the **Next Step** (e.g., "Want me to tweak any section or adjust the speaker notes?").
