<!--
CANONICAL STYLE EXEMPLAR for craft-readme.
This is a real, fact-checked README written in the exact house style the skill targets.
When unsure about structure, section order, heading names, bullet detail level, table
shapes, or tone — match THIS file. Do not copy its facts; copy its shape and voice.
-->

# TodoDesu トドデス。

A local-first todo application for Mac, iPhone, and iPad, paired with a terminal CLI that
shares the same data. Capture a task from the command line in seconds, organize it on a
kanban board from your iPad, run a focus session, and review your week on the calendar —
all backed by a single SQLite file on your machine. No accounts, no cloud, no tracking.

**Try it now:** https://tasachii.github.io/TodoDesu/

| Today — Wa (和) theme | Focus — Pomodoro with the ensō ring |
|---|---|
| ![Today view in the Wa theme](docs/images/today-wa.jpg) | ![Pomodoro focus in the Wa theme](docs/images/focus-wa.jpg) |

| Today — light theme | Board — brush-stroke strikethroughs |
|---|---|
| ![Today view in the light theme](docs/images/today-light.jpg) | ![Kanban board in the Wa theme](docs/images/board-wa.jpg) |

## Why this exists

Most todo apps force a choice: fast capture (terminal tools) or rich organization
(GUI apps). TodoDesu does both against one source of truth. The REST API is the single
authority over the data; the web app and the CLI are equal clients, so a task added with
`todo add` appears in the browser instantly, and a card dragged to *Done* on the board is
reflected in the next `todo list`.

## Features

### Task management
- Quick-add bar on the web (type, press Enter) and `todo add` in the terminal — both
  understand natural-language dates: type "pay rent tomorrow 6pm" and the date is
  detected while you type, shown as a chip, and stripped from the title (with a
  "keep as text" escape hatch)
- Search everything (titles and notes) from the magnifier button or the `/` key
- Keyboard shortcuts: `n` new task, `1–4` switch views, `/` search, `esc` closes
  any sheet
- Tasks carry a due date and time, free-form notes, and a priority (none / low / medium / high)
- **Recurring tasks** — daily, weekly, or monthly; completing one schedules the next
  occurrence automatically (always in the future, even if you finished late)
- Swipe right on a task to complete it, swipe left to delete; both actions show a
  five-second Undo toast
- Deletion is always a soft delete; deleted tasks are recoverable for 30 days before
  being purged
- Tapping a task opens a detail sheet for editing title, notes, schedule, and priority

### Views
- **Today** — sections for Overdue, Today, Tomorrow, and Inbox (tasks without a date)
- **Board** — three columns (To do / In progress / Done) with drag and drop, including
  touch support on iPad; cards can also be reordered within a column
- **Calendar** — month grid with markers on days that have tasks, plus an Upcoming list
  covering the next seven days
- **Focus** — a countdown ring tied to a task, with two styles: a plain timer
  (15/25/45/custom minutes with an optional break) and a Pomodoro cycle (25/5 or 50/10
  work/break rounds with a long break after the fourth round, breaks starting
  automatically). Both play a completion chime and feed daily statistics (minutes
  focused, sessions, tasks completed)

### Platform
- Four themes: auto / light / dark / **Wa (和)** — a warm Japanese mode: washi-paper tones,
  sumi ink, a single vermillion accent, Mincho display type, an ensō focus ring, a hanko
  完 stamp on completed tasks, and brush-stroke strikethroughs
- Installable as a PWA on iPhone, iPad, and Mac (Safari, Add to Home Screen)
- Builds as a native iOS app (Capacitor) ready for the App Store: on the phone the app
  runs fully standalone with an on-device data engine — no server, no account, no
  network. See [`docs/APP_STORE.md`](docs/APP_STORE.md)
- Accessible from other devices on the same Wi-Fi network when LAN mode is enabled
- The focus timer derives remaining time from timestamps, so it stays correct even when
  iOS suspends the page in the background

## Architecture

```
CLI (todo) ----+
               +----> Fastify REST API (127.0.0.1:4521) ----> SQLite (~/.todoo/data.db)
Browser -------+              |
                              +--- serves the built web app (packages/web/dist)
```

The repository is an npm-workspaces monorepo:

| Package | Role | Key technology |
|---|---|---|
| `packages/server` | REST API, data layer, serves the web build | Fastify 5, built-in `node:sqlite` |
| `packages/web` | Progressive web app | React 18, Vite, Tailwind CSS v4, TanStack Query, dnd-kit, framer-motion |
| `packages/cli` | `todo` command | commander, chrono-node, picocolors |

Design decisions worth noting:

- **`node:sqlite` over an ORM or native driver.** Node 23 ships SQLite in the standard
  library, which removes native compilation entirely. The database is one file; backing
  up means copying it.
- **The CLI never touches the database directly.** It speaks to the same API as the
  browser and transparently starts the server when it is not running, so business rules
  live in exactly one place.
- **Timezone-safe by construction.** The server never computes "today"; clients convert
  their local day boundaries to UTC and pass explicit ranges.
- **Fractional ordering.** Card positions use a `REAL` sort key, so dropping a card
  between two others writes a single midpoint value instead of re-indexing the column.

The full plan, requirements, and API contract are in [`docs/`](docs/).

## Requirements

- Node.js 23.4 or newer (for the built-in `node:sqlite` module) — check with `node -v`
- macOS is the primary target; Linux works as well. On **Windows**, the server, web
  app, and tests run fine in PowerShell or WSL; the only macOS-specific command is
  `todo open` (it shells out to `open`)

## Installation

macOS / Linux (Terminal) and Windows (PowerShell) use the same commands:

```bash
git clone https://github.com/Tasachii/TodoDesu.git
cd TodoDesu
npm install
```

Install the `todo` command globally:

```bash
npm run cli:link
```

No database setup is needed — SQLite ships inside Node and the file is created on
first run at `~/.todoo/data.db`.

## Usage

### Development

```bash
npm run dev
```

This starts the API server on `http://127.0.0.1:4521` and the Vite dev server on
`http://localhost:5173` (with `/api` proxied to the backend).

### Free hosting (share it with anyone)

The repository ships a GitHub Pages workflow that publishes the **standalone build** —
the app runs entirely in the visitor's browser with their data in localStorage, so
hosting costs nothing and no server is involved. Enable it once: repo **Settings →
Pages → Source: GitHub Actions**, then every push to `main` deploys to
`https://<user>.github.io/<repo>/`. Visitors on a phone can Add to Home Screen for an
app-like install, and the Settings sheet (gear icon) exports/imports backups to move
data between devices.

### Daily use

```bash
npm run build    # build the web app once
npm start        # serve app + API together at http://127.0.0.1:4521
```

To use TodoDesu from an iPhone or iPad on the same Wi-Fi network:

```bash
TODOO_HOST=0.0.0.0 npm start
```

Then open `http://<your-mac-ip>:4521` in Safari and choose **Add to Home Screen** to
install it as an app. Note that LAN mode has no authentication; use it only on networks
you trust.

### CLI reference

```
todo                          List overdue, today, and inbox tasks
todo add "title"              Add a task
  -d, --due <text>            Natural-language due date ("tomorrow 6pm", "fri 14:00")
  -p, --priority <level>      low | med | high
  -n, --notes <text>          Attach notes
  -r, --repeat <rule>         daily | weekly | monthly (requires --due)
todo list --all               All tasks grouped by status
todo done <n>                 Complete task <n> from the last printed list
todo start <n>                Move task <n> to In progress
todo rm <n>                   Delete task <n> (soft delete)
todo undo                     Undo the last done/rm action
todo focus <n> [-t minutes]   Run a focus session in the terminal (default 25)
todo open                     Open the web app in the browser
todo server <action>          start | stop | status
```

List numbers refer to the most recently printed list, so a typical flow is `todo`,
then `todo done 2`.

### Two-minute tutorial

1. `npm run build && npm start`, then open `http://127.0.0.1:4521`.
2. Type **"pay rent tomorrow 6pm"** in the quick-add bar — watch the date chip appear —
   and press Enter.
3. Press `2` to open the **Board**, drag the card to *In progress*.
4. Press `4` for **Focus**, switch the header toggle to **Pomodoro**, hit *Start
   focusing* — when the chime plays, the break starts by itself.
5. Swipe the task right (or click its circle) to complete it — try the **和** theme
   first (theme button) to see the hanko 完 stamp.
6. Press `/` to search anything you've ever added; open Settings (gear) to export a
   backup. In the terminal, `todo` then `todo done 1` closes the loop.

### Configuration

| Environment variable | Default | Purpose |
|---|---|---|
| `TODOO_PORT` | `4521` | API/server port |
| `TODOO_HOST` | `127.0.0.1` | Bind address; set `0.0.0.0` to allow LAN access |
| `TODOO_DB` | `~/.todoo/data.db` | Database file path (`:memory:` for throwaway runs) |

## Testing

```bash
npm test
```

Runs the server integration suite (every endpoint, via Fastify's injection, no real
network) and the CLI unit tests (natural-language date parsing).

## Project documentation

- [`DESCRIPTION.md`](DESCRIPTION.md) — project story: overview, concept, module diagram, statistics design
- [`docs/PROJECT_GUIDE.md`](docs/PROJECT_GUIDE.md) — the full picture: how every part of the code works, data flows, and design decisions
- [`docs/PLAN.md`](docs/PLAN.md) — technical plan, milestones, and risk register
- [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md) — functional and non-functional requirements
- [`docs/API.md`](docs/API.md) — REST API contract
- [`docs/QA_PLAN.md`](docs/QA_PLAN.md) — test pyramid, pre-commit gates, manual checklist
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — what to build next, with starting points in the code
- [`docs/APP_STORE.md`](docs/APP_STORE.md) — building the native iOS app and shipping to the App Store
- [`SKILLS.md`](SKILLS.md) — log of skills and techniques used while building this project

## Roadmap

Recurring tasks and natural-language quick-add have shipped. Next, in order of value:
cross-device sync (free-tier, keeping the local-first promise), Thai natural-language
dates, and weekly statistics with streaks. The full plan — with starting points in the
code, design constraints, and the ideas we deliberately rejected — lives in
[`docs/ROADMAP.md`](docs/ROADMAP.md): start there if you're picking the project up.
