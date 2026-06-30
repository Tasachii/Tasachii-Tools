#!/usr/bin/env node
// slide-craft · visual self-check.
//
// Loads a generated deck in headless Chromium, walks every `.slide`, and for
// each one: makes it visible, measures overflow, screenshots it at 1920×1080,
// and reports any slide whose content spills past the stage or overlaps.
//
// Usage:  node screenshot-check.mjs <deck.html> [outDir]
// Output: <outDir>/slide-01.png … and a JSON report on stdout.
//
// Needs Playwright (auto-installs Chromium on first run):
//   npm i -D playwright   # or:  npx playwright install chromium
//
// Exit code 0 = all slides clean · 1 = at least one slide has an issue.

import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';

const htmlArg = process.argv[2];
if (!htmlArg) {
  console.error('usage: node screenshot-check.mjs <deck.html> [outDir]');
  process.exit(2);
}
const htmlPath = resolve(htmlArg);
const outDir = resolve(process.argv[3] || dirname(htmlPath) + '/.slide-craft-check');
mkdirSync(outDir, { recursive: true });

const W = 1920, H = 1080;
const TOL = 2; // px tolerance — sub-pixel rounding is not an overflow

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts && document.fonts.ready);

const count = await page.locator('.slide').count();
const report = [];

for (let i = 0; i < count; i++) {
  // Force exactly one slide visible at the authored stage size, unscaled.
  await page.evaluate((idx) => {
    const stage = document.querySelector('.deck-stage');
    if (stage) stage.style.transform = 'none';
    document.querySelectorAll('.slide').forEach((s, k) => {
      const on = k === idx;
      s.classList.toggle('active', on);
      s.classList.toggle('visible', on);
    });
  }, i);
  await page.waitForTimeout(120); // let reveal transitions settle

  const metrics = await page.evaluate((idx) => {
    const slide = document.querySelectorAll('.slide')[idx];
    const r = slide.getBoundingClientRect();
    // Does any descendant extend past the slide's box?
    let overX = 0, overY = 0, clipped = [];
    slide.querySelectorAll('*').forEach((el) => {
      const b = el.getBoundingClientRect();
      if (b.width === 0 || b.height === 0) return;
      overX = Math.max(overX, b.right - r.right, r.left - b.left);
      overY = Math.max(overY, b.bottom - r.bottom, r.top - b.top);
      if (b.right - r.right > 2 || b.bottom - r.bottom > 2) {
        clipped.push((el.className || el.tagName).toString().slice(0, 40));
      }
    });
    return {
      scrollOverflow: {
        x: slide.scrollWidth - slide.clientWidth,
        y: slide.scrollHeight - slide.clientHeight,
      },
      boxOverflow: { x: Math.round(overX), y: Math.round(overY) },
      clipped: [...new Set(clipped)].slice(0, 6),
    };
  }, i);

  const n = String(i + 1).padStart(2, '0');
  await page.locator('.slide').nth(i).screenshot({ path: `${outDir}/slide-${n}.png` });

  const bad =
    metrics.scrollOverflow.x > TOL || metrics.scrollOverflow.y > TOL ||
    metrics.boxOverflow.x > TOL || metrics.boxOverflow.y > TOL;
  report.push({ slide: i + 1, ok: !bad, ...metrics, shot: `${outDir}/slide-${n}.png` });
}

await browser.close();

const problems = report.filter((r) => !r.ok);
console.log(JSON.stringify({
  deck: htmlPath, slides: count, clean: problems.length === 0,
  problems, screenshots: outDir,
}, null, 2));
process.exit(problems.length === 0 ? 0 : 1);
