# Build & Deliver a Unity Deck as Google Slides

The skill cannot edit Google Slides natively (no Slides API). It produces a finished deck on Unity's real template design and delivers it as a **new Google Slides file in the requesting user's Drive**, which they then move where they want.

## Pipeline

### 1. Plan the deck (gate)
Confirm: which template type (project review vs general), the topic, the section content, and the audience. Present the slide outline and get the user's OK before building. Fit content to the use case — don't force every template section if it doesn't apply.

### 2. Export the template as the design base
Use the Google Drive connector to export the chosen template (IDs in `deck-templates.md`) to PowerPoint:
- Tool: `download_file_content`
- `fileId`: the template ID
- `exportMimeType`: `application/vnd.openxmlformats-officedocument.presentationml.presentation`

Save the returned bytes as a local `.pptx`. This preserves Unity's masters, theme, fonts, and colors.

### 3. Build the deck
Compose with the **pptx** skill. Open the exported template as the base, then fill/duplicate its layouts with the planned content. Keep Unity rules from `deck-templates.md` (palette, one idea per slide, not swamped). Put speaker detail in notes.

**Make it visual — text-only slides are a fail.** Add real visuals, sized to the use case (not every slide needs the same treatment, and only add a diagram where it genuinely clarifies):
- **Real icons (not hand-drawn shapes).** Hand-drawing icons from pptx shapes looks broken. Instead rasterize professional icons to PNG and embed via `addImage`:
  1. Fetch Lucide icons (MIT) — e.g. `curl -fsSL https://unpkg.com/lucide-static@latest/icons/<name>.svg`.
  2. Recolor: replace `currentColor` with Unity blue `#2196F3` (or white on dark slides).
  3. Rasterize with `sharp` (`npm i sharp`): `sharp(Buffer.from(svg)).resize(256,256).png().toFile(...)`. (No `rsvg`/`cairosvg`/`inkscape` in this env — use sharp.)
  4. Place inside a soft `#E3EEFB` circle for accent icons.
  Useful icons: clock, circle-check, users, triangle-alert, upload, file-text, database, target, arrow-right.
- **Product mockups** as native pptx shapes (rounded card + button + rows) — e.g. show the LWC being described. High impact, editable, no assets.
- **Stat callouts** (big 34–40pt numbers), **3-card** rows, **connected step flows** (numbered circles + connector line + a per-step icon).
- **Sandwich:** dark title + closing slides, light content slides.
- **Avoid** accent stripes / underlines under titles (AI-slide tells), centered body text, and cramming.

### 4. Deliver — hand over the `.pptx` for one-step Google Slides import
**Do NOT try to push the deck into Drive via `create_file`.** Uploading a real deck requires inlining the whole binary as base64 (≈200K characters even for a small deck), which is not reliably producible in a tool call. That path only works for text Google Docs (`textContent`), not binary presentations.

Instead, deliver the finished `.pptx` to the user and give the one-step import instruction:
- Save the `.pptx` to the user's working folder (or session artifacts) so it appears for them.
- Tell them: **drag the file into Google Drive and open it** — Drive opens it as Google Slides — or in Slides use **File → Open → Upload**. It becomes a fully editable native Google Slides deck, which they place wherever they want.

## Notes
- The `.pptx` is built on Unity's template design language, so the imported Slides deck keeps Unity branding.
- Google Slides conversion of a clean `.pptx` is high-fidelity; if a layout drifts, fix the pptx build, not the Slides file.
- Never overwrite the source templates.
- Offer the raw `.pptx` as the primary deliverable; Google Slides is reached via the one-step import.
