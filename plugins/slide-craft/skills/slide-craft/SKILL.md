---
name: slide-craft
description: This skill should be used when the user wants to build a slide deck, presentation, or pitch deck — or convert a PowerPoint to web. Trigger on '/slides', 'slides', 'slide deck', 'make slides', 'make a deck', 'build a presentation', 'pitch deck', 'present this', 'turn this repo into a deck', 'convert pptx', and the Thai phrases 'สไลด์', 'ทำสไลด์', 'พรีเซนต์', 'ทำเด็ค', 'สไลด์นำเสนอ', 'แปลง ppt'. Builds a single self-contained HTML deck that designs itself around the topic, grounded in the user's real content (a repo, URL, or file — never invented), bilingual Thai/English aware, with presenter notes and an automatic 1920×1080 overflow self-check. Defaults to a fast one-shot; offers an interview only on request.
---

# slide-craft

Build zero-dependency HTML presentations that run entirely in the browser — one
self-contained `.html` file, no npm, no build step. The deck is authored at a fixed
1920×1080 stage and scaled as a whole to fit any screen, so it stays 16:9 everywhere,
phones included.

slide-craft improves on a from-scratch slide generator in five concrete ways:

| Improvement | What it means |
| --- | --- |
| **Content is grounded, never invented** | Slide text comes from the user's real material — a repo, a URL, a file, or what they paste. Unverifiable facts are asked about or left as a visible `[[TODO: …]]`, never guessed. |
| **Bilingual Thai/English is first-class** | Thai is a designed-for language, not an afterthought — correct font pairing, mixed-script spacing, and TH/EN layout patterns. See `references/thai-bilingual.md`. |
| **It verifies its own output** | After generating, it screenshots every slide at 1920×1080 and fixes any overflow or overlap before handing the deck over. See `references/verifying.md`. |
| **Present-ready, not just headlines** | Slides carry enough explanatory copy to make sense when read, plus optional speaker notes for live delivery — not bare title fragments. |
| **Auto by default** | No four-question interview unless asked. It infers purpose, length, and density from the material and ships one strong design. |

## Top rule — never invent the content

A slide that states a number, a feature, a date, or a claim the user did not give and the
code does not show is a defect, not a draft. In order:

1. **Read** the real source — a repo's `README`/`package.json`/`src`, a pasted brief, a
   linked page, an attached file.
2. **Ask** the user when a needed fact cannot be read.
3. **Leave a marker** — `[[TODO: confirm pricing]]` rendered visibly on the slide — when
   neither is possible.

Design is invented freely; **content is not**. "Made-up traction numbers on a pitch deck"
is the failure this rule exists to prevent.

**Names and attribution are content too.** A presenter name, author, company, or brand line
on the cover or closing slide is never assumed and never filled with a default. Ask once how
to sign the deck — a name, a brand, or nothing — and leave it off until told. Do not carry a
name over from a previous deck, from the user's account, or from this plugin's author; the
skill ships nameless so anyone can use it.

## Design philosophy — design around the topic

The deck's look is chosen *for this subject*, not pulled from a fixed skin. Converge away
from generic "AI-slop": no Inter/Roboto/Arial display type, no purple-gradient-on-white, no
identical card grids. Commit to one distinctive typographic voice, a cohesive palette with
sharp accents, and atmosphere (layered gradients, a motif, texture) over flat fills. Pick a
mood that fits the occasion and audience, then hold it across every slide. The curated
starting points live in `references/style-presets.md` — read it at design time; treat its
presets as launch pads, not constraints.

## The fixed stage — non-negotiable invariants

These hold for every slide in every deck:

- Every deck has a `.deck-viewport` filling the window and a `.deck-stage` authored at
  1920×1080 that scales as one unit. It may letterbox; it must not reflow per device.
- Author at the 1920×1080 size in `px`. Do not add responsive breakpoints to rearrange
  slide content for phones.
- Switch slides with `.active`/`.visible` (visibility/opacity), **never** `display:none`.
  Put `display:flex`/`grid` on an inner wrapper, never on `.slide` itself — a later layout
  rule on `.slide` would defeat the visibility switch and show every slide at once.
- Copy the full `references/viewport-base.css` into every deck's `<style>`.
- Include `prefers-reduced-motion` support (it ships in `viewport-base.css`).
- Negate CSS functions with `calc(-1 * clamp(…))` — a bare `-clamp(…)` is silently dropped.

## Workflow

### Phase 0 — detect the mode

| Mode | Trigger | Go to |
| --- | --- | --- |
| **From a source** | "turn this repo / page / file into a deck", a path, or a URL | Phase 1 (ground) |
| **From a brief** | the user pastes or describes the content | Phase 1 (ground) |
| **From PowerPoint** | a `.pptx` path | extract text + images first, then Phase 1 |
| **Enhance** | "improve this deck.html" | read it, keep its system, re-verify after edits |

For a `.pptx`, extract its text, images, and speaker notes before designing (any reliable
extractor works — e.g. `python-pptx`). Preserve slide order and notes.

### Phase 1 — gather the content (auto, grounded)

Default to **auto mode**: do not run a four-question interview. Instead —

1. **Read the real material.** If given a repo, read `README`, `package.json`/manifest, and
   the entry points to learn what the thing actually is. If given a URL, fetch it. If given a
   file, read it. If the user only pasted text, use that. Delegate heavy reading to a
   subagent so the main context stays lean.
2. **Infer the frame** from what you read: purpose (pitch / teach / report / talk), length
   (8–16 slides unless the material clearly needs more), and density (see below).
3. **Ask only when blocked** — a single short line, e.g. "Audience: investors or students?"
   — then continue. Never hold the build for a questionnaire. Fold the attribution question
   in here when the deck needs a name: "Sign it with a name/brand, or leave it off?"
4. **Interview on request only.** If the user says "ask me first" / "interview me", run the
   fuller purpose/length/density/content questions; otherwise skip them.

Detect the deck's language from the material and the user. If the subject is bilingual or the
user writes Thai, read `references/thai-bilingual.md` before designing.

### Phase 2 — choose the design (auto-pick one)

Pick the single style that best fits the subject and mood, build the deck in it, and show it
— do not generate three previews to choose from unless the user asks to compare. Read
`references/style-presets.md` for starting points and the anti-slop rules. Honor an explicit
request ("make it feel like a terminal", "warm and editorial") as the chosen direction.

### Phase 3 — generate

Read `references/html-architecture.md` (structure, navigation JS, inline editing, speaker
notes) and `references/style-presets.md` (the chosen look) before writing. Then:

- One self-contained `.html` file; all CSS/JS inline; fonts from Google Fonts or Fontshare,
  never system fonts.
- Paste the full `viewport-base.css` into `<style>`.
- **Density — present-ready, not telegraphic.** Choose per the material:
  - *Speaker-led (low):* one idea per slide, large type, 1–3 short lines — **plus** a one- or
    two-sentence explanatory sub-line so the slide still reads on its own, and a speaker note
    (see below) carrying what you'd *say* out loud.
  - *Reading-first (high):* self-contained slides — structured grids, short captions, a lead
    sentence per section. Still no walls of text; split a slide before it crowds.
  - When unsure, lean slightly fuller: the common failure is slides so sparse the audience
    can't follow them without the speaker. Every key slide should answer "why does this
    matter?" in a sentence, not only name the topic.
- **Speaker notes.** Attach a short presenter note to each content slide (a `data-notes`
  attribute or a hidden notes block, per `references/html-architecture.md`) — what to say,
  the transition, the number to land. These never show on the slide; they support delivery.
- Comment every section with a `/* === SECTION === */` block.

### Phase 4 — verify before delivering

Do not declare the deck done from the source alone. Run the visual self-check:

```bash
node scripts/screenshot-check.mjs <deck.html>
```

It screenshots each slide at 1920×1080 and reports any slide that overflows or overlaps. Fix
every flagged slide (split content, reduce, or relayout — never shrink text to illegibility),
then re-run until clean. Read `references/verifying.md` for the full procedure and a fallback
when Playwright is unavailable. Also spot-check one phone viewport — the stage should
letterbox, not reflow.

### Phase 5 — deliver

`open` the file in the browser. Then state, briefly: the file path, the style name, the slide
count, and that arrow keys / space / swipe navigate. Mention inline editing is on (hover the
top-left or press **E** to edit text in place; ⌘/Ctrl+S saves). Offer the natural next steps —
revise, deploy to a live URL, or export to PDF — without asking before you build.

## Reference files

Read each only when its phase arrives, to keep context lean.

| File | What it holds | Read at |
| --- | --- | --- |
| `references/viewport-base.css` | Mandatory fixed-stage CSS — copy into every deck | Phase 3 |
| `references/style-presets.md` | Curated anti-slop starting points + the design rules | Phase 2–3 |
| `references/thai-bilingual.md` | Thai/English type pairing, mixed-script spacing, TH/EN layout | Phase 1–3 when bilingual |
| `references/html-architecture.md` | HTML skeleton, navigation JS, inline editing, speaker notes | Phase 3 |
| `references/verifying.md` | The screenshot self-check loop and a no-Playwright fallback | Phase 4 |
| `scripts/screenshot-check.mjs` | Playwright overflow/overlap checker | Phase 4 |

## Credit

The fixed-stage, show-don't-tell approach is inspired by the open-source **frontend-slides**
skill by zarazhangrui (MIT). slide-craft is an independent rewrite in this marketplace's
house style, adding grounded content, first-class Thai, self-verification, and presenter
support; no original files are copied.
