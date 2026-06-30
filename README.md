# Tasachii-Tools（タサチー・ツールズ）

A personal Claude Code plugin marketplace — calm, precise tools for everyday development
work. Each plugin installs on demand and triggers by intent, not configuration. No server,
no telemetry; everything runs locally inside Claude Code.

**Repo** — https://github.com/Tasachii/Tasachii-Tools · **Owner** — Phasathat Jaruchitsophon

## Contents

- [Quick start](#quick-start)
- [Plugins](#plugins)
- [readme-craft](#readme-craft) · [caffe](#caffe) · [qa](#qa) · [slide-craft](#slide-craft)
- [Repository layout](#repository-layout)
- [Versioning](#versioning) · [License](#license)

## Quick start

Add the marketplace inside Claude Code, then install the plugins you want:

```text
/plugin marketplace add Tasachii/Tasachii-Tools
/plugin install readme-craft@tasachii-tools
/plugin install caffe@tasachii-tools
/plugin install qa@tasachii-tools
/plugin install slide-craft@tasachii-tools
```

Restart Claude Code once so the skills load, then trigger by intent — say `tsc` to fix a
README, `/caffe` to keep the Mac awake, `/qa` to score a project, or `/slides` to build a deck.

Developing the marketplace locally instead of from GitHub:

```text
/plugin marketplace add .                          # add this checkout as a marketplace
/plugin install <plugin>@tasachii-tools            # install a plugin from it
/plugin marketplace update tasachii-tools          # pull the latest after pushing a change
```

## Plugins

| Plugin | Version | What it does |
| --- | --- | --- |
| `readme-craft` | 0.4.0 | Writes and rewrites project READMEs in a fact-only house style. Reads the real code or asks — never invents facts. |
| `caffe` | 0.2.0 | Keeps the Mac awake for long jobs — a thin `caffeinate` wrapper with on / off / status. macOS only (guards non-macOS). |
| `qa` | 0.1.0 | Smoke-tests and QAs a project, scores it from four angles (CTO · tech lead · UX/UI · QA), and lists every fixable flaw. Asks before fixing. |
| `slide-craft` | 0.1.0 | Builds a self-contained HTML slide deck that designs itself around the topic — grounded in real content, Thai/English aware, with presenter notes and a 1920×1080 overflow self-check. |

Every plugin is a **skill**, not a flag-driven command: you talk to Claude Code normally and
the skill activates when it detects what you want. Each one reads the real project before it
acts, and none of them touch a network beyond what the task needs.

## readme-craft

Writes, rewrites, and updates a project's README in a calm, table-heavy, fact-only style. It
reads the actual project first — `package.json`, stack, scripts, license, live URL,
screenshots that really exist — asks when a fact cannot be read, and leaves a visible
`<!-- TODO -->` rather than guessing. English prose throughout, but the app's native UI
strings (e.g. Thai labels like `บันทึก`) are kept exactly as shown.

### How to use it

| You type in Claude Code | What happens |
| --- | --- |
| `/fix readme` · `fix readme` · `tsc` · `FRM` | Shortest triggers — reads your code and drafts or updates the README right away |
| `write a readme` · `make a readme` | The same, spelled out |
| `readme` · `README.md` · `document this project` | Short keyword still triggers; gathers facts, then writes |
| *(open a repo with no README)* | It offers to write one |

`tsc` is the Tasachii-Tools shorthand for *fix the readme* — it stays out of the way when you
actually mean the TypeScript compiler (`run tsc`, `tsc --noEmit`, `npx tsc`).

The before/after on a lead paragraph — the single most-rewritten line in any README:

| | Lead paragraph |
| --- | --- |
| **Before** | A blazingly fast, fully-featured, production-ready expense tracker built with cutting-edge web technologies for a seamless experience. |
| **After** | Pocketo is a kakeibo-style expense tracker that runs entirely in the browser — no server, no account, no tracking. Log income and spending in three taps; the month's balance updates as you type. Data lives in `localStorage` and stays on the device. |

The "after" keeps only what the code proves; every hype word in the "before" is gone because
none of it could be read from the repo.

## caffe

A small macOS utility — keep the Mac awake so a long job (render, download, browser
automation, training) isn't interrupted by sleep. It manages a detached `caffeinate -dimsu`
process; nothing is installed and nothing persists past a reboot. On a non-Darwin host it
bails early with a clear message instead of running a `caffeinate` that isn't there.

| You type in Claude Code | What happens |
| --- | --- |
| `/caffe` · `caffe` · `keep awake` · `อย่าให้เครื่องหลับ` | Starts keep-awake — display, idle, disk, and system sleep are all held off |
| `caffe off` · `ปิด caffe` | Stops it; the Mac sleeps normally again |
| `caffe status` | Reports whether keep-awake is on and which sleep assertions are held |

> Runs `caffeinate` detached with `nohup`, so it survives closing the terminal or the Claude
> Code session — but not a reboot. Closing the lid with no external display or power still
> sleeps. It can set a permanent `sudo pmset` policy, but only if you ask.

## qa

Smoke-test and QA a whole project, then score it the way four reviewers would — CTO, tech
lead, UX/UI designer, and QA tester. It runs the project's own checks (`build` / `lint` /
`test` / `validate`); for a web app it drives a local browser via the chrome-devtools MCP
(free, on your machine, nothing sent to a cloud).

| You type in Claude Code | What happens |
| --- | --- |
| `/qa` · `qa this` · `ตรวจโปรเจค` | Smoke-tests the current project and scores it from four angles |
| `/qa localhost:5173` · `qa <url>` | Drives the web app in a local browser, then scores the flow |
| `rate this` · `score this project` | The same — a quality verdict with evidence |

It leads with a four-angle scorecard (`N/10` each plus an overall), every angle scored against
an explicit five-point checklist shown with ✓ / ⚠ / ✗, then lists every weakness with a
severity tag, `file:line`, why it matters, and how to fix it. **It never fixes on its own — it
scores, then asks** whether to fix all, only the critical items, or none.

## slide-craft

Builds a presentation as a single self-contained HTML file — zero dependencies, authored at a
fixed 1920×1080 stage that scales to any screen, 16:9 everywhere. You talk to Claude Code
normally (`/slides`, "turn this repo into a deck", "ทำสไลด์") and it designs the deck around
the subject, grounded in your real content. It improves on a plain slide generator in five
ways:

- **Grounds content** in your real material (a repo, URL, or file) — never invents a number,
  feature, or name; it asks or leaves a visible `[[TODO]]`.
- **Thai/English is first-class** — correct font pairing, mixed-script (pangu) spacing, and
  TH/EN layouts; no synthetic italic or uppercase on Thai.
- **Verifies itself** — screenshots every slide at 1920×1080 and fixes overflow or overlap
  before handing the deck over.
- **Present-ready** — an explanatory line on the slide plus a hidden speaker note, not bare
  headlines.
- **Auto by default** — no interview unless asked; one strong design, shown.

The look is chosen *for the topic* — a distinctive display face, a committed palette, one
atmospheric device — never generic AI-slop. A presenter or brand name is treated as content,
so the deck ships nameless and asks rather than assuming.

### How to use it

| You type in Claude Code | What happens |
| --- | --- |
| `/slides` · `make a deck` · `ทำสไลด์` | Builds a deck — grounds content, picks a design, generates, self-verifies, opens it |
| `turn this repo into a deck` · `<path>` · `<url>` | Reads the real source first, then builds from it |
| `convert deck.pptx` | Extracts text, images, and notes, then redesigns to web |
| `interview me first` | Runs the fuller purpose / length / density questions before building |
| `improve this deck.html` | Reads the deck, keeps its design system, re-verifies after edits |

Navigate with arrow keys / space / swipe. Press **E** to edit text in place (⌘/Ctrl+S saves),
**N** to show speaker notes. After it builds, it offers to deploy to a live URL or export a PDF.

> The visual self-check needs Node + Playwright (it installs Chromium on first run); without
> them it falls back to a manual pass and says so. An independent rewrite of the approach in
> zarazhangrui's MIT `frontend-slides`; no files copied.

### Design decisions

| Topic | Decision |
| --- | --- |
| Content | Grounded, never invented — read the source, ask, or leave a visible `[[TODO]]`. A made-up stat on a pitch deck is the failure this prevents. |
| Names | A presenter / brand / author name is content — asked for, never defaulted. The skill ships nameless so anyone can use it. |
| Thai | First-class: every font stack carries a Thai face, mixed script gets pangu spacing, no synthetic italic or uppercase on Thai. |
| Verification | Screenshots every slide at 1920×1080 and fixes overflow / overlap before delivery — not a `scrollHeight` guess. |
| Density | Present-ready — an explanatory line on the slide plus a hidden speaker note, not telegraphic headlines. |
| Output | One self-contained `.html`, fixed 1920×1080 stage, inline edit + speaker notes, deploy / PDF on request. |

## Repository layout

```text
Tasachii-Tools/
├── .github/workflows/
│   ├── link-check.yml           # CI — re-checks every Markdown link
│   └── manifest-check.yml       # CI — versions, plugin validation, guard self-test
├── scripts/
│   ├── check-versions.py        # README ↔ plugin-version drift guard
│   ├── check-plugins.py         # plugin.json + SKILL.md structural validation
│   └── test_checks.py           # self-test for both guards
├── .claude-plugin/
│   ├── marketplace.json         # marketplace manifest (name: tasachii-tools)
│   └── README.md                # install guide
├── plugins/
│   ├── readme-craft/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/readme-craft/
│   │       ├── SKILL.md                       # the skill + workflow
│   │       └── references/                    # house-style guide, template, 4 exemplars, CI action
│   ├── caffe/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/caffe/SKILL.md              # keep-awake (caffeinate) utility
│   ├── qa/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/qa/
│   │       ├── SKILL.md                       # the four-angle QA procedure
│   │       └── references/rubric.md           # 10-point scale + output format
│   └── slide-craft/
│       ├── .claude-plugin/plugin.json
│       └── skills/slide-craft/
│           ├── SKILL.md                       # the deck builder + workflow
│           ├── references/                    # viewport-base.css, presets, thai-bilingual, architecture, verifying
│           └── scripts/screenshot-check.mjs   # Playwright overflow/overlap checker
├── CHANGELOG.md
└── README.md
```

## Versioning

Each plugin is versioned independently in its own `plugin.json` — the number shown in the
Plugins table above. The marketplace's `metadata.version` (currently `0.7.0`) is the **repo
release** version: it bumps on each published release (a new plugin, or a notable change),
while plugin versions move on their own — the two are not kept in lockstep.

CI enforces the discipline: `check-versions.py` holds each plugin's `plugin.json` version and
its Plugins-table row together and checks the marketplace version is semver, `check-plugins.py`
validates every manifest and skill frontmatter, and `test_checks.py` self-tests both guards. A
separate `link-check` re-checks every Markdown link on push, on PR, and weekly.

## License

MIT © Phasathat Jaruchitsophon
