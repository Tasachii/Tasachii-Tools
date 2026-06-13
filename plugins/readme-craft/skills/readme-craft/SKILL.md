---
name: readme-craft
description: This skill should be used when the user wants to create, rewrite, or update a project README. Trigger on 'FRM', 'frm', 'fix readme', 'fix the readme', 'write a readme', 'make a readme', 'craft readme', 'readme', 'README.md', 'document this project', or when a repo has no README. ('FRM' = Fix ReadMe, the short alias.) Writes READMEs in the author's house style — calm, precise, fact-only, English prose with native UI strings preserved, table-heavy.
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

### 1 — Choose the archetype and audience

The house style is one voice, but the *shape* changes with what you are documenting.
Pick the closest archetype first and read its exemplar — that is the structure to follow:

| Archetype | Exemplar | What leads | What matters most |
| --- | --- | --- | --- |
| End-user app (GUI/PWA/mobile, has a live demo or screenshots) | `references/example-tododesu.md` | Lead paragraph → Try it now → screenshots | Features grouped by area, the experience |
| Library / package (imported by other code) | `references/example-library.md` | **Quickstart** (install + 5-line usage) | API table, compatibility, zero-config use |
| Backend service / API (deployed, not imported) | `references/example-service.md` | **Quickstart** (run it: `docker compose up`) | Env-var + endpoint tables, deploy, health |
| CLI tool | `example-tododesu.md` (its CLI section) | Quickstart (install + first command) | Command reference block, flags |

If the project mixes archetypes (e.g. an app *and* a CLI, like TodoDesu), follow the
dominant one and borrow sections from the others.

**Audience drives ordering.** A library or service is read by developers who want to run
or import it in 30 seconds — lead with a **Quickstart** *before* the "Why this exists"
prose. An end-user app or a portfolio piece can lead with the lead paragraph and the
experience. When the README serves an internal team, drop marketing roadmap/badges and
add the operational sections (deploy, env, health) instead.

### 2 — Gather facts first

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

### 3 — Write sections in this order

This is the canonical shape for an **end-user app**, modelled on
`references/example-tododesu.md`. For a **library or service**, lead with a Quickstart
and follow `example-library.md` / `example-service.md` instead — the sections below
still apply, only the order shifts (Quickstart first, screenshots usually dropped).
Use `##` headings (no `---` rules between them). Drop any section that genuinely does
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

### 4 — Style

- Prefer tables and short bullets over long prose.
- Explain **why** for key design choices — a "Design Decisions" table of `Topic | Decision`.
- Stack as a single bullet, items joined by middot `·`.
- Connectors: em-dash `—` and middot `·`. Minimal emoji; functional symbols
  (`◀ ▶ ⇄ ✓`) are fine.
- Tone: calm, precise, understated, confident. Japanese-aesthetic flavor **only**
  when the project genuinely has it — never forced.

### 5 — Preserve native UI strings

When the app shows Thai (or any non-English) button labels, menu items, or copy,
keep them **exactly** as displayed. Write the surrounding prose in English, but never
translate the live UI strings away. Example: a button labelled `บันทึก` stays
`บันทึก` in the README, optionally glossed once in parentheses.

### 6 — Verify the README itself

A README that links to a missing image or a dead path is a defect. After writing, prove
the document holds up — do not just eyeball it:

1. **Every referenced image exists on disk.** List the image paths the README uses and
   confirm each file is present:

   ```bash
   grep -oE '!\[[^]]*\]\(([^)]+)\)' README.md | sed -E 's/.*\(([^)]+)\)/\1/' \
     | while read -r p; do [ -f "$p" ] && echo "ok   $p" || echo "MISS $p"; done
   ```

   Any `MISS` line means the image link is broken — fix the path or remove the image.

2. **Relative doc links resolve.** Check that local links (e.g. `docs/API.md`) point at
   files that exist; fix or drop the ones that do not.

3. **No invented facts slipped in.** Re-read every number, command, and URL against the
   source. Any claim you could not verify must be a visible `<!-- TODO -->`, not prose.

4. **Commands actually run** (when feasible) — at minimum the install and test commands.

5. **Plugin/manifest validation**, when the repo is a Claude plugin or marketplace:

   ```bash
   claude plugin validate .
   claude plugin validate plugins/<name>
   ```

Report the result of each check rather than assuming it passed.

## References

Load these for the full rules, a worked example, and a ready-to-fill skeleton:

- **`references/example-tododesu.md`** — exemplar for an **end-user app**: the canonical
  shape. Read this first for app/PWA/mobile projects. Copy its *form*, never its facts.
- **`references/example-library.md`** — exemplar for a **library/package**: quickstart
  first, API table front and centre, no forced native title.
- **`references/example-service.md`** — exemplar for a **backend service/API**: run-it
  first, env-var and endpoint tables, deploy and health sections, a status block.
- **`references/style-guide.md`** — the complete house-style rulebook, with
  BEFORE/AFTER examples. Read this before writing prose.
- **`references/template.md`** — a fill-in README skeleton with every section as a
  heading and `<!-- TODO -->` placeholders. Copy it, then replace placeholders with
  verified facts in one pass.
