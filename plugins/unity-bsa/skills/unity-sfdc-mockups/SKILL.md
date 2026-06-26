---
name: unity-sfdc-mockups
description: Produces SLDS 2.0-compliant Salesforce UI mockups and Unity-branded HTML email alerts. Use when the user asks for a mockup, wireframe, Lightning page or Screen Flow UI, an email alert/notification, or an HTML template. Outputs clean, low-density designs in Unity's color palette (black primary, SLDS blue accents and links, no other accent colors). Trigger on: mockup, wireframe, SLDS, Lightning page, screen flow UI, email alert, email notification, HTML template, UI design, layout.
---

# Unity SFDC Mockups

You produce clean, SLDS 2.0-compliant Salesforce UI and Unity-branded HTML email alerts. Premium, uncluttered, on-brand.

## Operating Principles (apply to every response)
1. **Plan first** — confirm the surface (Lightning page / Screen Flow / email) and the key content before designing.
2. **Self-review** against `references/slds2-unity-tokens.md` before presenting.
3. **Not swamped** — one primary action per view; group related fields.
4. End with a single, clear **Next Step**.
5. Always respond in English.

> Load `references/slds2-unity-tokens.md` for the Unity palette + SLDS 2 rules.
> For **Lightning / LWC / screen mockups**, load `references/slds2-components.md` — it has the real SLDS stylesheet link and authentic component blueprints. This is mandatory for Mode A.
> For **email alerts**, use `references/email-alert-template.html` as the starting point.

## Composition
- For email alerts, fill the provided HTML template directly (table layout, inline CSS, email-client safe).
- For static brand art (posters, diagrams), compose with **canvas-design**.

## Palette rules
- Unity colors only: **black, white, grays, and SLDS blue** (`#0176D3`). No other accent colors.
- Primary action = **black** button (`#000000`), white text. Secondary = outlined.
- **Blue is the only accent** — links, in-console actions, badges, and callouts (matches the Salesforce console UI). Surfaces white / light gray (`#F4F4F4`).

## Two output modes

### Mode A — Lightning / Screen Flow / LWC mockup
Produce an **authentic SLDS 2 mockup**, not generic HTML. This is the standard — a weak, non-SLDS layout is a failure.

Steps (per `references/slds2-components.md`):
1. Load the real SLDS stylesheet from the jsdelivr CDN and wrap everything in `<div class="slds-scope">`.
2. Apply the Unity theming override (black brand buttons, blue accents).
3. Build with **genuine SLDS blueprints**: `slds-page-header` at the top, content grouped in `slds-card`s, selections as `slds-form-element` checkboxes, data shown in an `slds-table`, primary actions as `slds-button_brand`, multi-step flows with `slds-path`/`slds-progress`.
4. Use SLDS utility classes for all spacing and grid (`slds-grid`, `slds-col`, `slds-gutters`, `slds-p-around_medium`).
5. **Render the mockup** so the user sees the real Lightning look, then describe the field placement / density / Dynamic Forms notes a BSA needs to implement it.

### Mode B — HTML email alert
Fill `email-alert-template.html`: header bar (Unity wordmark) → optional `ACTION REQUIRED` blue pill → title + intro → label/value info grid → primary + secondary buttons → optional blue callout → signature. Keep it max-width 600px, inline CSS, table-based.

End with the **Next Step** (e.g., "Want this as a rendered preview or as a Salesforce email template?").
