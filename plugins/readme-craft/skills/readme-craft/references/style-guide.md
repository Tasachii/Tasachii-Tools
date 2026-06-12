# README House Style Guide

The complete rulebook for `readme-craft`. The skill writes calm, precise, fact-only
READMEs. When in doubt, prefer a table, a verified number, or a TODO over prose or a
guess.

---

## 0 — The non-negotiable: no invented facts

Every number, command, URL, and feature must be **read** from the project or
**confirmed** by the user. If it cannot be verified, write a visible TODO:

```markdown
<!-- TODO: confirm test count (could not read from package.json) -->
```

Banned: "fast", "blazingly fast", "lots of tests", "fully featured", "robust",
"seamless", "production-ready" (unless a deploy proves it). Replace each with a
concrete number or delete it.

---

## 1 — Title

Themed and native names are encouraged. Two accepted shapes:

- `Name（native script）` — a native reading in **fullwidth** parentheses.
  Prefer a Japanese katakana reading when it fits the name's sound.
- `Name native — English subtitle` — name plus a short English descriptor.

Examples in house style:

| Project | Title line |
| --- | --- |
| Pocketo | `Pocketo（ポケット）` |
| TodoDesu | `TodoDesu トドデス。` |
| Sendo | `Sendo（センド）— Thai logistics invoicing` |

Use fullwidth parentheses `（）` around the native script, not ASCII `()`.

---

## 2 — Lead paragraph

One dense paragraph. It states **what it does** and **the core idea**, nothing else.
When the app is local-first or private, say so explicitly and concretely:

> "...runs entirely in the browser — no server, no account, no tracking. Data lives
> in `localStorage` and never leaves the device."

No marketing adjectives. One paragraph, then a `---` rule.

---

## 3 — Stack

A single bullet, items separated by middot `·`:

```markdown
- **Stack** — React 18 · Vite · TypeScript · Tailwind · IndexedDB (Dexie)
```

List only what the project actually depends on (read it from `package.json`).

---

## 4 — Explain *why* (Design Decisions)

Key choices get a short rationale in a `Topic | Decision` table:

```markdown
| Topic | Decision |
| --- | --- |
| Storage | `localStorage`, not a backend — keeps the app offline and private. |
| Routing | Hash routing — works on GitHub Pages with no server config. |
| State | No Redux — the data is small; React context is enough. |
```

A decision without a reason is just a fact; the table is where the *why* lives.

---

## 5 — Installation

Separate **Windows** and **Mac** blocks — the copy command differs. State the runtime
version and link to it.

````markdown
**Requirements** — [Node 20+](https://nodejs.org)

**Mac / Linux**
```bash
git clone https://github.com/Tasachii/example.git
cp .env.example .env        # copy env template
npm install
```

**Windows**
```bat
git clone https://github.com/Tasachii/example.git
copy .env.example .env       :: copy env template
npm install
```
````

---

## 6 — Running guide

Every command in a code block carries an inline `# ...` comment explaining it:

```bash
npm run dev        # start Vite dev server on :5173
npm run build      # type-check + bundle to dist/
npm run preview    # serve the production build locally
```

No bare command lists — the comment is mandatory.

---

## 7 — Tutorial / Usage

Numbered steps, or bold lead-ins that name the action and its cost in taps/clicks:

```markdown
1. **Log an expense (3 taps).** Tap ＋, type the amount, pick a category.
2. **Review the month.** The home screen totals income − expense automatically.
3. **Export.** Settings → Export → CSV.
```

Keep each step to one action.

---

## 8 — Native UI strings

Preserve the app's real labels exactly. Surrounding prose is English; the live strings
are not translated away. Gloss once, in parentheses, if helpful:

```markdown
- Tap **บันทึก** (Save) to store the entry.
- The bottom tabs are **รายรับ** · **รายจ่าย** · **สรุป**.
```

Never replace `บันทึก` with `Save` in the README body — show what the user sees.

---

## 9 — Punctuation & symbols

| Use | For |
| --- | --- |
| `—` (em-dash) | Strong connector, subtitle separator |
| `·` (middot) | Joining stack items, tab names, inline lists |
| `◀ ▶ ⇄ ✓` | Functional UI/state symbols |
| Emoji | Sparingly, only when it carries meaning |

---

## 10 — Tone

Calm, precise, understated, confident. Short sentences. No hype. Japanese-aesthetic
flavor (negative space, restraint, a katakana title) **only** when the project actually
has that character — never bolted on.

---

## 11 — License

Close with:

```markdown
## License

MIT © Phasathat Jaruchitsophon
```

Add a domain disclaimer when relevant, e.g. for a finance app:

> Not financial or filing advice. Figures are for personal tracking only.

---

## 12 — BEFORE / AFTER examples

**Example A — lead paragraph**

> ❌ BEFORE
> A blazingly fast, fully-featured, production-ready expense tracker built with the
> latest cutting-edge web technologies for a seamless user experience.

> ✓ AFTER
> Pocketo is a kakeibo-style expense tracker that runs entirely in the browser — no
> server, no account, no tracking. Log income and spending in three taps; the month's
> balance updates as you type. Data lives in `localStorage` and stays on the device.

**Example B — running guide**

> ❌ BEFORE
> ```
> npm run dev
> npm run build
> ```

> ✓ AFTER
> ```bash
> npm run dev        # start Vite dev server on :5173
> npm run build      # type-check + bundle to dist/
> ```
