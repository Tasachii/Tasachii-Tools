# Changelog

All notable changes to Tasachii-Tools are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). Dates are UTC.

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
