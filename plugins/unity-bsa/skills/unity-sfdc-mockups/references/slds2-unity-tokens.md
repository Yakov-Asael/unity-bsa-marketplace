# Unity SFDC Theme — Official Tokens

These are Unity's real Salesforce theme tokens (from the org Branding / SLDS 2 theme settings). Use these exact values — do not substitute SLDS defaults or invent colors.

## Core tokens

| Role | Hex | Use |
|---|---|---|
| **Brand color** | `#2196F3` | The Unity blue. Primary actions, key accents. |
| **Primary button background** | `#2196F3` | Filled (brand) buttons. White text/icon. |
| **Darker blue** | `#0F61A3` | Hover state, secondary accent, emphasis text on light blue. |
| **Near-black** | `#141514` | Body text, nav, icons, headings. (This is the "black", not pure #000.) |
| **Button content on blue** | `#FFFFFF` | Text and icons inside filled blue buttons. |
| **Link** | `#2196F3` | Hyperlinks and inline actions (semibold). |

## Brand-based ramp (surfaces & states, light → dark, approximate)
`#EAF2FD` · `#D2E4FB` · `#5B9BE0` · `#3D6FA6` · `#274C77` · `#16304F` · `#0A1B30`
Use the light stops (`#EAF2FD`, `#D2E4FB`) for selected/active fills and callout backgrounds; dark stops for dark-mode or strong emphasis.

## Aesthetic (match Unity's real LWCs, NOT classic Salesforce admin UI)
Unity's shipped features are modern and clean — this is the standard:
- **Rounded cards:** white surface, `border-radius:16px`, soft shadow (`0 1px 3px rgba(16,30,54,.08)`), generous padding, on a light gray page (`#F3F3F4`).
- **Buttons:** `border-radius:8px`. Primary = filled `#2196F3`, white text, semibold. Secondary = white bg, `#2196F3` text + border. Hover → `#0F61A3`.
- **Links:** `#2196F3`, semibold, no underline.
- **Titles:** `#141514`, weight 600. Icon in a soft blue rounded square (`#EAF2FD` bg, `#2196F3` glyph).
- **Tables/preview:** minimal — light header row (`#F8F9FB`), thin row dividers (`#F0F1F4`), NOT striped/bordered SLDS tables.
- **Process / loading states:** centered card, **Unity logo**, bold uppercase headline, blue progress bar (`#2196F3` on `#E8EEF7`), percentage in `#2196F3`, subtle full-width cancel.
- **Density:** low. One card per logical step. Lots of white space.

## Rules
- Primary action = **blue `#2196F3`**, white text (NOT black).
- Reserve `#141514` for text/nav/icons.
- Blue family only for accents — no other accent colors.
- Keep it modern and rounded, matching Unity's real product UI.
