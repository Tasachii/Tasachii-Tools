# Tasachii-Tools（タサチー・ツールズ）

A personal Claude Code plugin marketplace — calm, precise tools for everyday development
work. Plugins install on demand and trigger by intent, not config. No server, no
telemetry; everything runs locally inside Claude Code.

**Repo** — https://github.com/Tasachii/Tasachii-Tools · **Owner** — Phasathat Jaruchitsophon

## Quick start

Install from GitHub inside Claude Code:

```text
/plugin marketplace add Tasachii/Tasachii-Tools
/plugin install readme-craft@tasachii-tools
```

Restart Claude Code once so the skill loads, then open a project and say `tsc` (or
`write a readme`).

Developing the marketplace locally instead of from GitHub:

```text
/plugin marketplace add .
/plugin install readme-craft@tasachii-tools
/plugin marketplace update tasachii-tools   # pull the latest after pushing a change
```

## Plugins

| Plugin | Version | What it does |
| --- | --- | --- |
| `readme-craft` | 0.4.0 | Writes and rewrites project READMEs in a fact-only house style. Reads the real code or asks — never invents facts. |
| `caffe` | 0.1.0 | Keeps the Mac awake for long jobs — a thin `caffeinate` wrapper with on / off / status. macOS only. |
| `qa` | 0.1.0 | Smoke-tests and QAs a project, scores it from four angles (CTO · tech lead · UX/UI · QA), and lists every fixable flaw. Asks before fixing. |

## readme-craft

A Claude Code **skill** that writes, rewrites, and updates project READMEs. It is not a
command you call with flags — you talk to Claude Code normally and the skill activates
when it detects you want a README. Before writing a word it reads the actual project
(`package.json`, stack, scripts, license, live URL, screenshots that really exist), asks
you when a fact cannot be read, and leaves a visible `<!-- TODO -->` rather than guessing.
The output is calm, table-heavy English prose that keeps your app's native UI strings
(e.g. Thai labels) exactly as shown.

### How it works

1. **Picks the archetype.** App, library, or backend service — each has its own exemplar
   and section order (a library leads with a quickstart; an app leads with the experience).
2. **Gathers facts first.** Reads code and config; never assumes.
3. **Writes in a fixed order.** Title → lead paragraph → try-it-now → screenshots → why
   it exists → grouped features → architecture → installation → usage → testing → docs →
   roadmap → license, using `##` headings (with a Contents TOC when it runs long).
4. **Verifies.** Confirms every referenced image and link resolves, re-checks each fact,
   and runs `claude plugin validate` when the repo is a plugin. For repos with CI it can
   drop in a link-check Action so links keep working after the README ships.

### See it in action

There is no web URL to open — `readme-craft` is a skill, not a hosted app. Its "demo" is
the transformation itself: you say `tsc` inside a repo, and a thin or missing README
becomes a fact-checked one. A typical Claude Code session looks like this:

```text
you ›  tsc

readme-craft ›  Reading the repo… found package.json (React 18 · Vite · Tailwind),
                LICENSE (MIT), homepage → https://tasachii.github.io/Pocketo/,
                3 screenshots in docs/images/. No test script found.

                Q: Is "kakeibo budgeting" the right one-line description?  [Y/n]
you ›           y

readme-craft ›  Wrote README.md (title → lead → try-it-now → screenshots → features →
                architecture → install → usage → license).
                Verified: 3/3 images exist, 4/4 links resolve, `claude plugin validate` ✓.
                Left 1 TODO: <!-- TODO: confirm test count — no test script in package.json -->
```

The before/after on a lead paragraph — the single most-rewritten line in any README:

| | Lead paragraph |
| --- | --- |
| **Before** | A blazingly fast, fully-featured, production-ready expense tracker built with cutting-edge web technologies for a seamless experience. |
| **After** | Pocketo is a kakeibo-style expense tracker that runs entirely in the browser — no server, no account, no tracking. Log income and spending in three taps; the month's balance updates as you type. Data lives in `localStorage` and stays on the device. |

The "after" keeps only what the code proves: the stack, the storage choice, the tap count.
Every hype word in the "before" is gone because none of it could be read from the repo.

### How to use it

| You type in Claude Code | What happens |
| --- | --- |
| `/fix readme` · `fix readme` · `tsc` · `FRM` | Shortest triggers — `/fix readme` / `fix readme` (says it outright), `tsc` (Tasachii-Tools shorthand), and `FRM` ("Fix ReadMe"); reads your code and drafts/updates the README |
| `write a readme` · `make a readme` | Same thing, spelled out |
| `readme` · `README.md` | Short keyword still triggers |
| `document this project` | Gathers facts, then writes |
| *(open a repo with no README)* | It offers to write one |

`tsc` and `FRM` work mid-sentence too — e.g. "tsc this repo" or "can you fix readme here".
`tsc` here means *Tasachii — fix the readme*, not the TypeScript compiler: it stays out of
the way when you actually mean `run tsc`, `tsc --noEmit`, or any real build command.

> Restart Claude Code once after installing so the skill loads. Run it **inside** the
> target project so it can read the real files. Fill in any `<!-- TODO -->` markers it
> leaves — those are facts it could not verify on its own.

### Design decisions

| Topic | Decision |
| --- | --- |
| Facts | Read or ask — never invent. An unverifiable fact becomes a visible TODO, not a guess. |
| Screenshots | For a visual app it drives the demo in — names the views to capture, gives a `docs/images/` path, and scaffolds the table behind a `<!-- TODO -->` until the files land. Never a broken image link. |
| Archetype | One voice, four shapes — app, library, service, and public OSS each follow their own exemplar. |
| Link rot | Verification runs at write time; a copy-ready CI Action keeps links checked afterward. |
| Comments | Code blocks stay clean; an inline `# ...` is added only when a command's purpose isn't obvious. |
| Language | English prose, but native UI strings (`บันทึก`, menu labels) are preserved verbatim, never translated away. |
| Form | Tables and short bullets over long prose; key choices state their *why*. |
| Tone | Calm, precise, understated. No "fast" / "robust" / "production-ready" filler — concrete numbers only. |

## caffe

A small macOS utility skill — keep the Mac awake so a long job (render, download, browser
automation, training) isn't interrupted by sleep. It manages a detached `caffeinate -dimsu`
process; nothing is installed and nothing persists past a reboot.

| You type in Claude Code | What happens |
| --- | --- |
| `/caffe` · `caffe` · `keep awake` · `อย่าให้เครื่องหลับ` | Starts keep-awake — display, idle, disk, and system sleep are all held off |
| `caffe off` · `ปิด caffe` | Stops it; the Mac sleeps normally again |
| `caffe status` | Reports whether keep-awake is on and which sleep assertions are held |

> Runs `caffeinate` detached with `nohup`, so it survives closing the terminal or the Claude
> Code session — but not a reboot. Closing the laptop lid with no external display or power
> still sleeps. It can set a permanent `sudo pmset` policy, but only if you ask.

## qa

Smoke-test and QA a whole project, then score it the way four reviewers would — CTO, tech lead,
UX/UI designer, and QA tester — and get back a precise, fixable list of what's wrong. It runs the
project's own checks (`build` / `lint` / `test` / `validate`); for a web app it drives a local
browser via the chrome-devtools MCP (free, on your machine, nothing sent to a cloud).

| You type in Claude Code | What happens |
| --- | --- |
| `/qa` · `qa this` · `ตรวจโปรเจค` | Smoke-tests the current project and scores it from four angles |
| `/qa localhost:5173` · `qa <url>` | Drives the web app in a local browser, then scores the flow |
| `rate this` · `score this project` | Same — a quality verdict with evidence |

It leads with a four-angle scorecard (`N/10` each plus an overall) — every angle scored against an
explicit five-point checklist shown with ✓ / ⚠ / ✗ — then lists every weakness with a severity tag,
`file:line`, why it matters, and how to fix it. **It never fixes on its own — it scores, then asks**
whether to fix all, only the critical items, or none.

## Repository layout

```text
Tasachii-Tools/
├── .github/workflows/
│   ├── link-check.yml          # CI — re-checks every Markdown link
│   └── manifest-check.yml      # CI — plugin version ↔ README drift guard
├── scripts/check-versions.py            # manifest-check helper
├── .claude-plugin/
│   ├── marketplace.json        # marketplace manifest (name: tasachii-tools)
│   └── README.md               # install guide
├── plugins/
│   ├── readme-craft/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/readme-craft/
│   │       ├── SKILL.md                       # the skill + workflow
│   │       └── references/
│   │           ├── style-guide.md             # full house-style rulebook
│   │           ├── template.md                # fill-in README skeleton
│   │           ├── example-tododesu.md        # exemplar — end-user app
│   │           ├── example-library.md         # exemplar — library/package
│   │           ├── example-service.md         # exemplar — backend service
│   │           ├── example-oss-library.md     # exemplar — public OSS project
│   │           └── workflow-link-check.yml    # copy-ready link-check Action
│   ├── caffe/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/caffe/SKILL.md           # keep-awake (caffeinate) utility
│   └── qa/
│       ├── .claude-plugin/plugin.json
│       └── skills/qa/
│           ├── SKILL.md                    # the four-angle QA procedure
│           └── references/rubric.md        # 10-point scale + output format
├── CHANGELOG.md
└── README.md
```

## Roadmap

- [x] `readme-craft` — README writer
- [x] `caffe` — keep-awake utility
- [x] `qa` — four-angle project QA
- [ ] More personal skills, added one at a time

## Versioning

Each plugin is versioned independently in its own `plugin.json` — that is the number shown
in the Plugins table above. The marketplace's `metadata.version` tracks the **catalog** (the
set of plugins and the repo's structure) and moves when a plugin is added or removed, not on
a single plugin's release; the two are not kept in lockstep. CI (`manifest-check`, via
`scripts/check-versions.py`) holds each plugin's `plugin.json` version and its Plugins-table
row together, and checks the marketplace version is valid semver.

## License

MIT © Phasathat Jaruchitsophon
