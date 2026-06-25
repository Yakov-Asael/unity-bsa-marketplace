# SLDS 2 + Unity Palette Reference

## Unity palette

| Token | Hex | Use |
|---|---|---|
| Unity black | `#000000` | Primary buttons, header bars, primary text on light surfaces |
| White | `#FFFFFF` | Surfaces, button text on black |
| Light gray | `#F4F4F4` | Panel / section backgrounds |
| Border gray | `#E5E5E5` | Hairline borders, table rules |
| Text | `#1A1A1A` | Body text |
| Muted text | `#5C5C5C` | Labels, secondary text |
| SLDS brand blue | `#0176D3` | Hyperlinks, in-console actions, "action required" badges, accents |
| SLDS blue (dark) | `#014486` | Blue text on light blue callout backgrounds |
| Callout blue | `#EAF5FE` | Background for informational / action-required callouts |
| Callout border | `#0176D3` | Left border on callouts |

## SLDS 2 principles
- When producing component CSS, prefer **styling hooks** (`--slds-g-color-*`, `--slds-g-spacing-*`, `--slds-g-radius-*`) over hardcoded values.
- Clean layouts, logical information grouping, generous white space, rounded corners.
- **Density:** never swamp the user — one primary action per view; group related fields into sections.
- Email alerts are **table-based HTML** (email-client safe), not SLDS components.

## Rules
- Unity colors only: **black, white, grays, and SLDS blue**. No other accent colors.
- Primary action = black button, white text. Secondary = outlined (black border, transparent fill).
- **Blue (`#0176D3`) is the only accent** — used for links, in-console actions, badges, and callouts (matches the Salesforce console UI).
- Match the reference email layout: black header bar with the Unity wordmark → optional blue `ACTION REQUIRED` pill → title + intro → 2-column label/value info grid on light gray → primary + secondary buttons → optional blue-left-border callout on light blue → signature.
- System font stack; max width 600px for emails.
