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

Separate each block with a `---` horizontal rule.

1. **Title** — `Name（native script）` or `Name native — English subtitle`.
2. **Badges** — only badges whose data is verified (license, version, live link).
3. **Lead paragraph** — one dense paragraph: what it does + the core idea. State
   privacy/local-first explicitly when true ("no server, no account, no tracking").
4. **Quick links** — live demo · docs · issues, as a compact row.
5. **Screenshots table** — only images that exist on disk.
6. **Project Description** — what problem it solves, who it's for.
7. **Installation** — separate Windows vs Mac blocks; state runtime version + link.
8. **Running guide** — every command in a code block carries an inline `# ...` comment.
9. **Tutorial / Usage** — numbered steps or bold lead-ins ("**Log an expense (3 taps).**").
10. **Architecture** — only when non-trivial; a short diagram or a Topic | Decision table.
11. **Config / API tables** — options, env vars, endpoints, as tables.
12. **Roadmap** — checked/unchecked list of real plans.
13. **License** — `MIT © Author name`, plus any domain disclaimer.

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

Load these for the full rules and a ready-to-fill skeleton:

- **`references/style-guide.md`** — the complete house-style rulebook, with
  BEFORE/AFTER examples. Read this before writing prose.
- **`references/template.md`** — a fill-in README skeleton with every section as a
  heading and `<!-- TODO -->` placeholders. Copy it, then replace placeholders with
  verified facts in one pass.
