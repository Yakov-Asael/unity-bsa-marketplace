# SLDS 2 Component Blueprints (for Lightning / LWC mockups)

Use this for **Mode A** (Lightning page / Screen Flow / LWC mockups). The goal is a mockup that looks like it was built inside a real Salesforce Lightning org — not generic HTML.

## Non-negotiable: load the real SLDS stylesheet
Always start the mockup by loading the official Salesforce Lightning Design System CSS (allowed CDN):

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@salesforce-ux/design-system@2.24.4/assets/styles/salesforce-lightning-design-system.min.css">
```

Then use **genuine SLDS classes** (`slds-*`). Do not hand-roll CSS for things SLDS already provides. Wrap everything in a container with class `slds-scope`.

## Unity theming (apply over SLDS)
Unity primary action = brand blue `#2196F3` (white text); hover `#0F61A3`; text/nav/icons `#141514`. Override SLDS brand hooks:

```html
<style>
  .slds-scope {
    --slds-c-button-brand-color-background:#2196F3;
    --slds-c-button-brand-color-border:#2196F3;
    --slds-c-button-brand-color-background-hover:#0F61A3;
    --slds-c-button-brand-color-border-hover:#0F61A3;
  }
</style>
```

> Prefer the modern Unity LWC aesthetic in `slds2-unity-tokens.md` (rounded cards, blue pills, minimal tables) over heavy classic-SLDS chrome. Use SLDS blueprints for structure, but keep the look clean and modern, not admin-page dated.

## Core blueprints (use these patterns)

### Page header (every screen starts with one)
```html
<div class="slds-page-header">
  <div class="slds-page-header__row">
    <div class="slds-page-header__col-title">
      <div class="slds-media">
        <div class="slds-media__figure">
          <span class="slds-icon_container slds-icon-standard-account">
            <svg class="slds-icon slds-icon_small" aria-hidden="true"><use xlink:href="https://cdn.jsdelivr.net/npm/@salesforce-ux/design-system@2.24.4/assets/icons/standard-sprite/svg/symbols.svg#account"></use></svg>
          </span>
        </div>
        <div class="slds-media__body">
          <h1 class="slds-page-header__title slds-truncate">Long Tail Account Export</h1>
          <p class="slds-page-header__name-meta">Data export tool</p>
        </div>
      </div>
    </div>
  </div>
</div>
```

### Card (group content into cards)
```html
<article class="slds-card">
  <div class="slds-card__header slds-grid">
    <header class="slds-media slds-media_center slds-has-flexi-truncate">
      <div class="slds-media__body"><h2 class="slds-card__header-title">Section title</h2></div>
    </header>
  </div>
  <div class="slds-card__body slds-card__body_inner">…</div>
</article>
```

### Brand button (Unity blue #2196F3, white text)
```html
<button class="slds-button slds-button_brand">Run export</button>
<button class="slds-button slds-button_neutral">Cancel</button>
```

### Data table (the SLDS table, not an HTML table)
```html
<table class="slds-table slds-table_cell-buffer slds-table_bordered slds-table_striped">
  <thead><tr class="slds-line-height_reset">
    <th scope="col"><div class="slds-truncate">Account Name</div></th>
    <th scope="col"><div class="slds-truncate">Annual Revenue</div></th>
  </tr></thead>
  <tbody><tr><th scope="row"><div class="slds-truncate">Acme</div></th><td>$1,200,000</td></tr></tbody>
</table>
```

### Form elements / checkboxes
```html
<div class="slds-form-element">
  <label class="slds-checkbox">
    <input type="checkbox" checked />
    <span class="slds-checkbox_faux"></span>
    <span class="slds-form-element__label">Account Name</span>
  </label>
</div>
```

### File selector
```html
<div class="slds-file-selector slds-file-selector_files">
  <div class="slds-file-selector__dropzone">
    <input type="file" class="slds-file-selector__input slds-assistive-text" />
    <label class="slds-file-selector__body">
      <span class="slds-file-selector__button slds-button slds-button_neutral">Upload file</span>
      <span class="slds-file-selector__text">or drop a CSV here</span>
    </label>
  </div>
</div>
```

### Badges / pills (status)
```html
<span class="slds-badge">284 rows</span>
<span class="slds-badge slds-theme_success">Ready</span>
```

### Path / progress (multi-step processes)
Use `slds-progress` or `slds-path` for stepper flows.

## Rules
- Wrap the mockup in `<div class="slds-scope">…</div>`.
- Use SLDS utility classes for spacing (`slds-p-around_medium`, `slds-m-bottom_small`, `slds-grid`, `slds-col`, `slds-gutters`), never ad-hoc margins.
- Render data as an `slds-table`, selections as `slds-form-element` checkboxes, primary actions as `slds-button_brand` (black via the override above).
- Keep density low: one card per logical step, clear section headers.
- After producing the markup, render it so the user sees the real Lightning look.
