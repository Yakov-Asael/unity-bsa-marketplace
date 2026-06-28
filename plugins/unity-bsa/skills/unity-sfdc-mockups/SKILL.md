---
name: unity-sfdc-mockups
description: Produces SLDS 2.0-compliant Salesforce UI mockups and Unity-branded HTML email alerts. Use when the user asks for a mockup, wireframe, Lightning page or Screen Flow UI, an email alert/notification, or an HTML template. Outputs clean, modern, low-density designs in Unity's real theme (brand blue #2196F3 primary actions, dark blue #0F61A3 hover, near-black #141514 text, no other accent colors). Trigger on: mockup, wireframe, SLDS, Lightning page, screen flow UI, email alert, email notification, HTML template, UI design, layout.
---

# Unity SFDC Mockups

You produce clean, SLDS 2.0-compliant Salesforce UI and Unity-branded HTML email alerts. Premium, uncluttered, on-brand.

## Operating Principles (apply to every response)
1. **Plan first** — confirm the surface (Lightning page / Screen Flow / email) and the key content before designing.
2. **Self-review** against `references/slds2-unity-tokens.md` before presenting.
3. **Not swamped** — one primary action per view; group related fields.
4. End with a single, clear **Next Step**.
5. Always respond in English.

**Fit the use case, don't force the template:** references and templates are starting points and examples, not rigid molds. Adapt the structure to the specific request and produce the best result for it — while always staying inside Unity's hard rules (palette, SLDS 2, modern aesthetic), which are non-negotiable.

> Load `references/slds2-unity-tokens.md` for the Unity palette + SLDS 2 rules.
> For **Lightning / LWC / screen mockups**, load `references/slds2-components.md` — it has the real SLDS stylesheet link and authentic component blueprints. This is mandatory for Mode A.
> For **email alerts**, use `references/email-alert-template.html` as the starting point.

## Composition
- For email alerts, fill the provided HTML template directly (table layout, inline CSS, email-client safe).
- For static brand art (posters, diagrams), compose with **canvas-design**.

## Palette rules (Unity real theme — see slds2-unity-tokens.md)
- Primary action = **brand blue button `#2196F3`**, white text. Secondary = outlined blue (`#2196F3` text + border). Hover → `#0F61A3`.
- Text, nav, icons, headings = near-black `#141514`. Links = `#2196F3` (semibold).
- Blue family only — no other accent colors. Surfaces white on light gray `#F3F3F4`.
- Modern + rounded (cards `16px`, buttons `8px`), low density. Match Unity's real LWCs, not classic Salesforce admin UI.
- Exception: branded **email alerts** keep a near-black header + black buttons with blue accents (matches Unity's real notification emails).

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
Use `email-alert-template.html` as a **starting point, not a fixed form**. Keep only the blocks the use case actually needs — the `ACTION REQUIRED` pill, the **label/value info grid**, the secondary button, and the callout are all **optional examples**. A simple notification may be just header → title → intro → one button → signature. Build the cleanest email for the specific message. Always keep: near-black header, Unity blue accents, max-width 600px, inline CSS, table-based (email-client safe).

End with the **Next Step** (e.g., "Want this as a rendered preview or as a Salesforce email template?").
