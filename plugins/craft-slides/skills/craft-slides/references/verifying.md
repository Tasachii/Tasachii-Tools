# Verifying the deck

A deck is not done because the HTML was written. It is done when every slide has been seen at
1920×1080 and none overflow, overlap, or clip. Read at Phase 4.

## The self-check

```bash
node scripts/screenshot-check.mjs path/to/deck.html
```

The script (Playwright + headless Chromium) walks every `.slide`, makes it visible at the
authored 1920×1080 size, measures overflow, screenshots it, and prints a JSON report:

```json
{ "slides": 10, "clean": false,
  "problems": [ { "slide": 4, "boxOverflow": { "x": 0, "y": 38 }, "clipped": ["grid-4"] } ],
  "screenshots": "…/.craft-slides-check" }
```

`clean: true` and exit 0 means every slide fits. Otherwise each problem names the slide, how
far content spills (px), and the offending element.

First run installs Chromium (~once): `npx playwright install chromium` if it isn't present.

## What counts as a problem

| Symptom | Reading |
| --- | --- |
| `scrollOverflow.y > 2` or `boxOverflow.y > 2` | content taller than the slide — it's cut off at the bottom |
| `boxOverflow.x > 2` | content wider than the stage — bleeding off the side |
| `clipped` lists an element | that element's box extends past the slide edge |
| panels visually stacked in the screenshot | overlap — a `scrollHeight` check alone won't catch this; **look at the PNG** |

## Fixing — in order

1. **Split.** Move content to a new slide. Two clean slides beat one crammed slide. Update
   any page numbers.
2. **Reduce.** Cut a bullet, shorten a sentence, drop a redundant element.
3. **Relayout.** Switch a 1-column to 2-column, a 4-card to a 3-card row, a paragraph to a
   list.
4. **Last resort, lightly:** nudge a size token down a step — but never below comfortable
   reading size. Shrinking type until it "fits" is a defect, not a fix.

Re-run the check after each fix until `clean: true`.

## Phone spot-check

Open the deck once narrow (e.g. a 390×844 viewport). The stage must **letterbox** — the same
16:9 slide, scaled down, with bars top/bottom — never reflow into a stacked mobile layout. If
content rearranges on the phone, a layout rule is fighting the fixed stage; find it and
remove it.

## If Playwright is unavailable

Fall back to a manual pass — still mandatory, just by eye:

1. `open` the deck and step through **every** slide at a normal window size.
2. On each, check: nothing cut at the edges, no two panels overlapping, no text smaller than
   ~its neighbours, the headline and body both fully visible.
3. Resize the window narrow and tall; confirm the slide letterboxes rather than reflows.
4. Note any slide that fails and fix it with the order above.

A deck shipped without either pass is unverified — say so rather than implying it was checked.
