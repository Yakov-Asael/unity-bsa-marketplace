#!/usr/bin/env node
/*
 * Generate an on-brand Unity BSA banner (1200x300 PNG) for a skill.
 *
 * Usage:
 *   node scripts/make-banner.js <skill-name> "<Title>" "<tagline>" <lucide-icon> [outPath]
 * Example:
 *   node scripts/make-banner.js unity-data-model "Data Model" "Reviews ERDs and data models" database
 *
 * Defaults output to plugins/unity-bsa/skills/<skill-name>/assets/banner.png
 * Requires Node 18+ and sharp (`cd scripts && npm install`). Pick icons at https://lucide.dev/icons
 */
const fs = require("fs");
const path = require("path");
const sharp = require("sharp");

const [, , skill, title, tagline, icon, outArg] = process.argv;
if (!skill || !title || !tagline || !icon) {
  console.error('Usage: node scripts/make-banner.js <skill-name> "<Title>" "<tagline>" <lucide-icon> [outPath]');
  process.exit(1);
}

const INK = "#141514", BLUE = "#2196F3", DBLUE = "#0F61A3", WHITE = "#FFFFFF", MUTE = "#9AA7B4";
const W = 1200, H = 300;
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

async function main() {
  const res = await fetch(`https://unpkg.com/lucide-static@latest/icons/${icon}.svg`);
  if (!res.ok) throw new Error(`Could not fetch Lucide icon "${icon}" (${res.status}). Check the name at lucide.dev/icons`);
  const raw = await res.text();
  const inner = raw.replace(/^[\s\S]*?<svg[^>]*>/, "").replace(/<\/svg>\s*$/, "");

  const squares = [[1010, 70, 0.10], [1075, 70, 0.16], [1042, 120, 0.13], [1108, 120, 0.10], [1075, 170, 0.14]]
    .map(([x, y, o]) => `<rect x="${x}" y="${y}" width="52" height="52" rx="8" fill="${BLUE}" opacity="${o}" transform="rotate(45 ${x + 26} ${y + 26})"/>`)
    .join("");

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" font-family="Helvetica, Arial, sans-serif">
  <rect width="${W}" height="${H}" fill="${INK}"/>
  <rect width="6" height="${H}" fill="${BLUE}"/>
  ${squares}
  <rect x="70" y="105" width="92" height="92" rx="20" fill="#1E3047"/>
  <g transform="translate(88,123) scale(2.33)" fill="none" stroke="${WHITE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${inner}</g>
  <text x="196" y="120" fill="${BLUE}" font-size="19" font-weight="bold" letter-spacing="3">UNITY BSA</text>
  <text x="196" y="176" fill="${WHITE}" font-size="46" font-weight="bold">${esc(title)}</text>
  <text x="198" y="216" fill="${MUTE}" font-size="21">${esc(tagline)}</text>
</svg>`;

  const out = outArg || path.join("plugins", "unity-bsa", "skills", skill, "assets", "banner.png");
  fs.mkdirSync(path.dirname(out), { recursive: true });
  await sharp(Buffer.from(svg)).png().toFile(out);
  console.log(`banner written: ${out}`);
}

main().catch((e) => { console.error(e.message); process.exit(1); });
