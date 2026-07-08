# Skill & Plugin Creator Guide

How to build a skill for the Unity BSA marketplace that's clean, planned, on-brand, and passes review. Read this before you propose or build anything.

---

## 1. What a skill is (and isn't)

A **skill** is a focused, automatically-triggered capability. Good skills are:
- **Narrow** — one clear job, so Claude picks the right one instead of guessing.
- **Standard-enforcing** — they encode a *real* Unity standard (a template, ruleset, or process), not generic advice.
- **Adaptive** — they *fit the use case*; the template guides, it doesn't get forced onto every request.
- **In their lane** — they hand off to other skills rather than overlapping.

A skill is **not** a dumping ground of loosely-related features, and it is **never** built from a one-line request.

## 2. Anatomy of a plugin

```
plugins/<plugin>/
├── .claude-plugin/plugin.json   # name, version, description, author, keywords
├── README.md                    # banner + what it does + skills table
├── assets/banner.png            # the plugin banner
└── skills/
    └── <skill-name>/            # one folder per skill (see §3)
```

The repo root also holds `.claude-plugin/marketplace.json` (the marketplace entry) — the maintainer keeps that current.

## 3. Anatomy of a skill

```
skills/<skill-name>/
├── SKILL.md                 # the skill itself (instructions FOR Claude)
├── README.md                # human-facing docs (banner + how it works)
├── assets/banner.png        # on-brand banner (scripts/make-banner.js)
└── references/              # progressive disclosure — detail lives here
    └── <topic>.md
```

**`SKILL.md`** has YAML frontmatter + a lean body:
- `name:` — kebab-case, **must equal the folder name**.
- `description:` — third person, **trigger-rich**. Say *what it does*, *when to use it*, and end with `Trigger on: <keywords>`. This is how Claude decides to fire the skill — invest in it.
- **Body** — instructions written *to Claude* (imperative: "Load `references/x.md`", "Produce…"), not docs for a human. Keep it under ~3,000 words; push detail into `references/`.
- Include the standard blocks: **Operating Principles** (plan first · self-review · end with a Next Step · English · *fit the use case*), any **Modes**, and a **Boundary** note vs. adjacent skills.

**`references/`** — templates, rulesets, cheat-sheets the skill loads on demand. This keeps SKILL.md lean and lets the skill cite the *real* Unity standard.

**`README.md`** — banner on top, a bold one-line intro, "How it works", modes/output tables, triggers, and the references it uses. (See any existing skill's README.)

## 4. The mandatory process

Never skip a step. This is the same process the whole plugin was built with.

1. **Brief** — open a **"New skill" issue** and fill every field (problem, triggers, inputs, outputs/modes, the real standard it enforces, a concrete example, handoffs/boundaries, out-of-scope). *A one-liner is not a brief.*
2. **Design** — agree the modes, the references you'll need, the description/triggers, and the boundary vs. other skills. Confirm before building.
3. **Build** — copy `_template/skill/` to `skills/<skill-name>/`, write SKILL.md + references, generate the banner, write the README.
4. **Test on a real Unity example** — run the skill against the concrete example from the brief. Paste the result in the PR. If it's wrong, fix before review.
5. **Docs** — README done, and **add the skill's row to the plugin `README.md` skills table** (CI fails otherwise).

## 5. Writing a description that triggers well

- Third person, specific: *"Reviews Salesforce Flows against Unity's standards… Use when the user pastes Flow XML or asks to review a flow."*
- End with explicit keywords: `Trigger on: flow, screen flow, fault path, governor limits, …`.
- Avoid overlap with existing skills' triggers — if two skills claim the same words, both mis-fire. Check the plugin README table first.

## 6. Unity conventions (every skill)

- Respond in **English**.
- **Plan → self-review → end with a single Next Step.**
- **Fit the use case, don't force the template.** Hard rules (standards, palette, gates) stay non-negotiable; structure flexes.
- **Palette:** brand blue `#2196F3`, dark blue `#0F61A3`, ink `#141514`, white — no other accents.
- **Respect boundaries** — don't do another skill's job; hand off.

## 7. Build it — commands

```bash
# 1. scaffold
cp -r _template/skill plugins/unity-bsa/skills/<skill-name>

# 2. write SKILL.md, references/, README.md   (edit the TODO markers)

# 3. banner  (needs Node; run `npm install` inside scripts/ once)
node scripts/make-banner.js <skill-name> "<Title>" "<tagline>" <lucide-icon>
#   e.g. node scripts/make-banner.js unity-data-model "Data Model" "Reviews ERDs and data models" database

# 4. update the plugin README skills table (add your row)

# 5. validate before opening the PR
python3 scripts/validate_plugin.py
```

Pick a Lucide icon name from https://lucide.dev/icons (e.g. `database`, `shield`, `search`, `git-branch`).

## 8. Common pitfalls

- One-line brief → **rejected**. Start from the issue form.
- SKILL.md that reads like human docs → it should instruct *Claude*.
- Detail crammed into SKILL.md → move it to `references/`.
- Forgetting the plugin README row or the banner → **CI fails**.
- A description that overlaps another skill → mis-triggering; tighten the triggers and add a boundary note.
- Inventing a "standard" → skills must enforce a *real* Unity template/ruleset; link it in the brief.
