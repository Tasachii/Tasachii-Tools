---
name: qa
description: Smoke-test and QA an entire project or app, then return a score from four expert angles — CTO, tech lead, UX/UI designer, and QA tester — followed by a detailed, fixable list of weaknesses and an offer to fix them. Use when the user types "/qa", "qa", "qa this", "qa test", "smoke test", "review this project", "rate this", "score this project", "ตรวจโปรเจค", "ให้คะแนนโปรเจค", "qa โปรเจคนี้", or wants a quality verdict on a repo, codebase, web app, or local dev server. For a web app it drives a local browser via the chrome-devtools MCP (free, local); for any codebase it runs the project's own build / lint / test / validate. Never auto-fixes — it scores, details every flaw with where and how to fix it, then asks.
---

# qa — smoke-test, QA, and score a project from four angles

Run a project through its own checks, judge it as four different experts would, and hand back one
scorecard plus a precise, fixable list of what's wrong. The deliverable is a verdict and a to-do
list — not a wall of logs. **It never fixes anything on its own; it scores, then asks.**

## Inputs
- **Target** — a project directory (default: the current repo) and/or a URL / local dev server
  (`localhost:5173`) for a web app. If it's unclear which project, ask before starting.
- **Focus** (optional) — a specific area ("the checkout flow", "the build"). If omitted, cover the
  whole project at a sensible depth.

## Procedure

### 1. Identify the project
Read the README and manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`,
`.claude-plugin/`, `Makefile`) to learn the stack, the type (web app · library · service · CLI ·
plugin/marketplace), and the commands it actually defines. Never assume a command exists — detect it.

### 2. Smoke test — run only what the project actually has
Run the checks that exist, capture pass/fail and the real output. Map by stack:

| Stack / type | Run what is present |
| --- | --- |
| Node / web | `npm run build`, `lint`, `typecheck`, `test` — only scripts that exist in `package.json` |
| Python | `pytest`, `ruff` / `flake8`, `mypy`, or a documented `--dry-run` entrypoint |
| Rust / Go | `cargo build` / `test` / `clippy`, `go build` / `vet` / `test` |
| Claude plugin / marketplace | `claude plugin validate <each plugin>`, manifest + version consistency |
| Anything | Does it start? Do referenced files and links resolve? Is committed junk present (`git ls-files`)? |

Don't fabricate a test suite that isn't there — record "no tests defined" as a finding, not a fake pass.

### 3. Web apps — drive a real browser (local, free)
If the target is a web app and a dev server is reachable (or you can start it), exercise the happy
path through the **chrome-devtools MCP** (`mcp__chrome-devtools__*`) — local Chrome, no cloud, data
stays on the machine: `navigate_page` → `take_snapshot` / `take_screenshot` → click / fill through the
flow → `list_console_messages` + `list_network_requests` for JS errors and 4xx/5xx. Judge the
screenshots yourself. If chrome-devtools isn't connected, say so and score the rest — don't block.

### 4. Score from four angles
Each gets a score out of 10 with a one- or two-line justification, then an overall:

| Angle | Judges |
| --- | --- |
| 🧑‍💼 CTO | strategy, risk, maintainability, value, bus-factor |
| 🛠️ Tech Lead | code quality, architecture, conventions, correctness, CI |
| 🎨 UX/UI Designer | visual quality, usability, DX, accessibility, copy |
| 🧪 QA Tester | does it pass, edge cases, what breaks, test coverage |

**The overall reflects the weakest critical path** — don't average a broken core flow up because the
homepage is pretty. The scale and output format live in `references/rubric.md`.

### 5. Weaknesses — every flaw, in detail
List all of them, worst first. For each: a **severity tag** (`[blocker]` / `[high]` / `[medium]` /
`[low]`), the **location** (`file:line` or screen / flow), **why it matters**, and **how + where to
fix it**.

### 6. Ask before fixing — never auto-fix
End by asking whether to fix, and let the user scope it (**all · critical only · none**). Fix only
after they choose, then report exactly what changed.

## Honesty rules
- **Separate real bugs from test-environment artifacts.** A clean browser with no Thai font renders
  Thai as boxes — that's the environment, not the app; don't score it down (offer the bundled-webfont
  fix as a robustness note instead). A localhost-only API failing through a tunnel is an artifact too.
- **Cite evidence** — the exact command output, the `file:line`, the screenshot. A score must be
  defensible.
- **Never invent facts** — "no test script in `package.json`" beats a guessed test count.
