---
name: readme-craft
description: This skill should be used when the user wants to create, rewrite, or update a project README. Trigger on 'write a readme', 'readme', 'README.md', 'document this project', or when a repo has no README. Writes READMEs in the author's house style — calm, precise, fact-only, English prose with native UI strings preserved, table-heavy.
---

# readme-craft

Writes project READMEs in a calm, precise, understated house style. English prose,
fact-only, table-heavy, with native UI strings preserved exactly as the app shows them.

## Top rule — never invent facts

Do **not** write test counts, bundle sizes, feature lists, version numbers, commands,
or URLs that have not been verified. Three options, in order:

1. **Read** the real source — `package.json`, lockfiles, config, `src/`, `docs/`.
2. **Ask** the user when a fact cannot be read.
3. **Leave a TODO** — `<!-- TODO: verify test count -->` — when neither is possible.

A marked TODO is always correct; a confident guess is a defect. Vague claims
("fast", "lots of tests", "blazingly") are banned — concrete numbers only.

## Workflow

### 1 — Gather facts first

Before writing a single section, collect:

| Fact | Where to look |
| --- | --- |
| Stack / language | `package.json`, `pyproject.toml`, `go.mod`, file extensions |
| Scripts / commands | `package.json` `scripts`, `Makefile`, CI configs |
| Live URL | `package.json` `homepage`, deploy config, ask user |
| License | `LICENSE` file, `package.json` `license` |
| Author | `package.json` `author`, git config, ask user |
| Local-first / offline | service-worker, no-backend, localStorage usage |
| Screenshots | `docs/`, `assets/`, `.github/` image files that actually exist |
| Node / runtime version | `engines`, `.nvmrc`, `.tool-versions` |

If a fact is missing and cannot be read, ask the user a short batch of questions
rather than guessing.

### 2 — Write sections in this exact order

This is the canonical shape, modelled on `references/example-tododesu.md` — read that
file first; it is the target this skill writes toward. Use `##` headings (no `---`
rules between them, the way the exemplar does). Drop any section that genuinely does
not apply; keep the order of the ones that remain.

1. **Title** — `# Name native。` or `Name（native script）` or `Name native — English subtitle`.
2. **Lead paragraph** — one dense paragraph right under the title: what it does + the
   core idea, ending with the privacy/local-first stance when true
   ("No accounts, no cloud, no tracking.").
3. **Try it now** — `**Try it now:** <url>` when there is a live demo. (Badges are
   optional and only used when their data is verified — license, version.)
4. **Screenshots** — paired 2-column tables with a descriptive caption per image in the
   header row (`| Today — Wa theme | Focus — ensō ring |`). Only images that exist on disk.
5. **Why this exists** — the choice or insight the project resolves; the core design idea.
6. **Features** — grouped under `###` subheadings (e.g. Task management / Views /
   Platform). Bullets are full, specific sentences with parenthetical detail; **bold**
   the marquee items. This is where the README earns its detail.
7. **Architecture** — an ASCII diagram and/or a package/module table
   (`Package | Role | Key technology`), then a "Design decisions worth noting:" list of
   **bold lead-in.** bullets that each explain *why*.
8. **Requirements** — runtime versions and OS notes, as bullets.
9. **Installation** — clean code blocks (no comments); prose between blocks for context.
   Split Windows vs Mac only when the commands actually differ.
10. **Usage** — `###` subsections as needed: Development · (Hosting/Deploy) · Daily use ·
    CLI reference (aligned plain block) · a short numbered tutorial · Configuration table.
11. **Running commands** — keep code blocks clean. Add an inline `# ...` comment only
    when a command's purpose isn't obvious; never annotate self-explanatory commands.
12. **Testing** — the command plus one line on what the suite covers.
13. **Project documentation** — bullet list of doc links, each with an `—` description.
14. **Roadmap** — what shipped and what's next, as prose or a checklist of real plans.
15. **License** — `MIT © Author name`, plus any domain disclaimer.

### 3 — Style

- Prefer tables and short bullets over long prose.
- Explain **why** for key design choices — a "Design Decisions" table of `Topic | Decision`.
- Stack as a single bullet, items joined by middot `·`.
- Connectors: em-dash `—` and middot `·`. Minimal emoji; functional symbols
  (`◀ ▶ ⇄ ✓`) are fine.
- Tone: calm, precise, understated, confident. Japanese-aesthetic flavor **only**
  when the project genuinely has it — never forced.

### 4 — Preserve native UI strings

When the app shows Thai (or any non-English) button labels, menu items, or copy,
keep them **exactly** as displayed. Write the surrounding prose in English, but never
translate the live UI strings away. Example: a button labelled `บันทึก` stays
`บันทึก` in the README, optionally glossed once in parentheses.

### 5 — Validate

After writing, run both checks and report the result:

```bash
claude plugin validate .                          # marketplace manifest
claude plugin validate plugins/readme-craft       # the plugin manifest
```

## References

Load these for the full rules, a worked example, and a ready-to-fill skeleton:

- **`references/example-tododesu.md`** — the canonical style exemplar: a complete, real
  README in the exact target style. Read this first and match its shape, section order,
  heading names, bullet detail level, and tone. Copy its *form*, never its facts.
- **`references/style-guide.md`** — the complete house-style rulebook, with
  BEFORE/AFTER examples. Read this before writing prose.
- **`references/template.md`** — a fill-in README skeleton with every section as a
  heading and `<!-- TODO -->` placeholders. Copy it, then replace placeholders with
  verified facts in one pass.
