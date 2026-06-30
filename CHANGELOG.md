# Changelog

All notable changes to Tasachii-Tools are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). Dates are UTC.

## 0.8.0 — 2026-06-30

### Changed
- **Prefixed every plugin with `craft-`** for one consistent, easy-to-type namespace —
  `readme-craft` → `craft-readme`, `caffe` → `craft-caffe`, `qa` → `craft-qa`, `slide-craft` →
  `craft-slides`. Each rename moves the plugin dir, `plugin.json` name, marketplace entry, skill
  (dir + `SKILL.md` name), README sections, and internal reference strings. Install commands are now
  `/plugin install craft-readme@tasachii-tools` (and `craft-caffe` / `craft-qa` / `craft-slides`);
  the skills are invoked as `/craft-readme`, `/craft-caffe`, `/craft-qa`, `/craft-slides`. Every
  friendly trigger is kept — `tsc` / `/fix readme` / `FRM`, `/caffe` / "keep awake", `/qa` / "rate
  this", `/slides` / "make a deck", and all Thai phrases — so existing phrasing still works.
- Marketplace `metadata.version` → 0.8.0 (a notable catalog change: all four plugins renamed).
  Plugin versions are unaffected — `craft-readme` 0.4.0, `craft-caffe` 0.2.0, `craft-qa` 0.1.0,
  `craft-slides` 0.1.0.
- `scripts/`: all file reads/writes now use `with open(...)` context managers (no dangling handles).

### Added
- CI: a `ruff check scripts/` step in `manifest-check`, so the guard scripts are linted on every
  push/PR instead of relying on a local run.

### Fixed
- The install guide (`.claude-plugin/README.md`) was missing the slides plugin entirely — it listed
  only three plugins. It now lists all four (`craft-readme` / `craft-caffe` / `craft-qa` /
  `craft-slides`) in the install block, trigger line, and table.

## 0.7.0 — 2026-06-30

### Added
- `slide-craft`: a new plugin that builds a single self-contained HTML slide deck which
  designs itself around the topic. It grounds every slide in the user's real content (a repo,
  URL, or file) and never invents a number, feature, or name — it asks or leaves a visible
  `[[TODO]]`; treats Thai/English as first-class (font pairing, mixed-script spacing, TH/EN
  layouts); verifies its own output by screenshotting every slide at 1920×1080 and fixing
  overflow before delivery; writes present-ready slides (an explanatory line plus a hidden
  speaker note, not bare headlines); and runs auto by default (no interview unless asked). A
  presenter/brand name is treated as content — asked for, never defaulted — so the deck ships
  nameless. Includes a fixed-stage `viewport-base.css`, curated anti-slop style presets, a
  Thai/bilingual typography guide, an HTML/JS architecture reference, and a Playwright
  `screenshot-check.mjs`. An independent rewrite of the approach in zarazhangrui's MIT
  `frontend-slides`; no files copied.

### Changed
- Marketplace `metadata.version` → 0.7.0 (the catalog grew: `slide-craft` added). Plugin
  versions are unaffected — `readme-craft` stays at 0.4.0, `caffe` at 0.2.0, `qa` at 0.1.0.

## 0.6.1 — 2026-06-30

### Added
- `scripts/check-plugins.py` + a CI step: structurally validates every `plugin.json` and each
  `SKILL.md`'s frontmatter, so a malformed plugin is caught in CI without needing the Claude CLI.
- `scripts/test_checks.py` + a CI step: self-tests both guards — they must pass on the real repo
  and must catch an injected version drift and a malformed plugin.
- `caffe`: an early macOS guard — on a non-Darwin host it bails with a clear message and points at
  the platform equivalent, instead of running a `caffeinate` that isn't there.
- README: a Contents table of contents.

### Changed
- `scripts/check-versions.py` now parses the README "## Plugins" table structurally (tolerant of
  layout / backtick changes) instead of substring-matching.
- Versioning doc clarified: `metadata.version` is the marketplace's **repo release** version
  (it bumps each release); plugins stay independently versioned. `caffe` → 0.2.0; marketplace → 0.6.1.

## 0.6.0 — 2026-06-30

### Added
- `qa`: a new plugin that smoke-tests and QAs a whole project, then scores it from four angles
  — CTO, tech lead, UX/UI designer, and QA tester, **each against an explicit five-point
  checklist** shown with ✓ / ⚠ / ✗ so the score is traceable — and returns a detailed, fixable
  weakness list (severity, `file:line`, why it matters, how to fix). It runs the project's own
  build / lint / test / validate, and for a web app drives a local browser via the
  chrome-devtools MCP (free, local). It never auto-fixes — it scores, then asks.

### Changed
- Marketplace `metadata.version` → 0.6.0 (the catalog grew: `qa` added). Plugin versions are
  unaffected — `readme-craft` stays at 0.4.0, `caffe` at 0.1.0.

## 0.5.0 — 2026-06-30

### Added
- `caffe`: a new plugin that keeps the Mac awake for long-running jobs — a thin wrapper over
  macOS `caffeinate -dimsu` with plain-language on / off / status. The keep-awake process is
  detached (`nohup`), so it survives closing the terminal or the Claude Code session, but not
  a reboot. macOS only.

### Changed
- Marketplace `metadata.version` → 0.5.0 (the catalog grew: `caffe` added). Plugin versions
  are unaffected — `readme-craft` stays at 0.4.0.

## 0.4.0 — 2026-06-30

### Added
- `readme-craft`: `/fix readme` (and `/fix-readme`, `fix readme`) as an explicit, immediate
  trigger. Typing it is treated as an unambiguous instruction to fix the current project's
  README — the skill begins the workflow right away instead of asking what the user means.
  Complements the existing `tsc` / `FRM` short aliases.
- CI: a `manifest-check` workflow (via `scripts/check-versions.py`) keeps every plugin's
  `plugin.json` version in lockstep with its row in the README Plugins table, and checks the
  marketplace version is valid semver — guarding the version drift this release would
  otherwise have shipped.

### Changed
- Versioning is now independent and documented: each plugin owns its version in `plugin.json`;
  the marketplace `metadata.version` tracks the catalog (the plugin set and repo structure),
  not a single plugin's release. CI no longer forces the two to match.

### Fixed
- README and the install guide were behind the manifests — the Plugins table showed `0.3.0`
  and both omitted the `/fix readme` / `tsc` / `FRM` shortcuts. They now match the shipped
  `0.4.0` and list every trigger.

## 0.3.0 — 2026-06-14

### Added
- `readme-craft`: a proactive screenshot-demo workflow. For a visual app (web/PWA/mobile/
  desktop) with no images on disk, the skill no longer drops the screenshots section — it
  names the specific views to capture, gives a `docs/images/` path and naming convention,
  offers a capture method, and scaffolds the two-column table behind a visible
  `<!-- TODO -->` until the files land. No broken image links; the never-invent rule still
  holds. This brings new READMEs in line with the TodoDesu / Pocketo screenshot demos.

## 0.2.0 — 2026-06-14

### Added
- `readme-craft`: `tsc` short trigger alias (Tasachii-Tools shorthand for "fix the
  readme"), alongside the existing `FRM`. Guarded so it triggers a README fix only as a
  bare request — never when `tsc` means the TypeScript compiler (`run tsc`, `tsc
  --noEmit`, `tsc -b`, `npx tsc`, a tsc error/flag/path).
- Marketplace README: a "See it in action" section — a Claude Code session transcript and
  a lead-paragraph before/after, the honest analog of a live demo for a skill.

### Changed
- CI link-check excludes the illustrative exemplar READMEs under
  `plugins/readme-craft/skills/readme-craft/references/`, whose relative links are part of
  the sample and intentionally do not resolve here.
- CI link-check now also runs when the workflow file itself changes, not only on `*.md`.

### Fixed
- Link-check no longer fails on the exemplars' sample links (broken on the first `*.md`
  push after CI was introduced).

## 0.1.0 — 2026-06-12

### Added
- Initial marketplace with the `readme-craft` plugin.
- `readme-craft` skill: an archetype-aware README writer (app · library · service · public
  OSS) that reads the real project, asks when a fact cannot be read, and leaves a visible
  `<!-- TODO -->` rather than guessing.
- Reference set: a full house-style guide, a fill-in template, four worked exemplars, and a
  copy-ready link-check GitHub Action.
- `FRM` short trigger alias.
- CI link-check workflow (lychee, on push/PR and weekly).
