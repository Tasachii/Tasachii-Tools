# Tasachii-Tools（タサチー・ツールズ）

A personal Claude Code plugin marketplace — calm, precise tools for everyday
development work. Plugins install on demand and trigger by intent, not config. There is
no server and no telemetry; everything runs locally inside Claude Code.

**Repo** — https://github.com/Tasachii/Tasachii-Tools · **Owner** — Phasathat Jaruchitsophon

---

## Plugins

| Plugin | Version | What it does |
| --- | --- | --- |
| `readme-craft` | 0.1.0 | Writes and rewrites project READMEs in a fact-only house style. Reads the real code or asks — never invents facts. |

---

## readme-craft — what it is

A Claude Code **skill** that writes, rewrites, and updates project READMEs. It is not a
command you call with flags — you talk to Claude Code normally and the skill activates
when it detects you want a README. Before writing a word it reads the actual project
(`package.json`, stack, scripts, license, live URL, screenshots that really exist), asks
you when a fact cannot be read, and leaves a visible `<!-- TODO -->` rather than guessing.
The output is calm, table-heavy English prose that keeps your app's native UI strings
(e.g. Thai labels) exactly as shown.

### What it does

1. **Gathers facts first.** Reads code and config; never assumes.
2. **Writes in a fixed order.** Title → lead → quick links → screenshots → Description →
   Installation (Windows + Mac separately) → Running → Tutorial → Architecture →
   config tables → Roadmap → License, each block split by a `---` rule.
3. **Validates.** Runs `claude plugin validate` on the result.

### How to use it

| You type in Claude Code | What happens |
| --- | --- |
| `write a readme` | Reads your code, then drafts a README in house style |
| `readme` · `README.md` | Short keyword still triggers |
| `document this project` | Gathers facts, then writes |
| *(open a repo with no README)* | It offers to write one |

> Restart Claude Code once after installing so the skill loads. Run it **inside** the
> target project so it can read the real files. Fill in any `<!-- TODO -->` markers it
> leaves — those are facts it could not verify on its own.

### Design decisions

| Topic | Decision |
| --- | --- |
| Facts | Read or ask — never invent. An unverifiable fact becomes a visible TODO, not a guess. |
| Language | English prose, but native UI strings (`บันทึก`, menu labels) are preserved verbatim, never translated away. |
| Form | Tables and short bullets over long prose; key choices state their *why*. |
| Tone | Calm, precise, understated. No "fast" / "robust" / "production-ready" filler — concrete numbers only. |

---

## Quick start

**Local (test before pushing)**
```text
/plugin marketplace add .                     # register this folder as a marketplace
/plugin install readme-craft@tasachii-tools   # install the README writer
```

**From GitHub**
```text
/plugin marketplace add Tasachii/Tasachii-Tools   # add the published marketplace
/plugin install readme-craft@tasachii-tools       # install the README writer
```

After editing the skill, push the change and refresh the local copy:
```text
/plugin marketplace update tasachii-tools     # pull the latest from GitHub
```

---

## Repository layout

```text
Tasachii-Tools/
├── .claude-plugin/
│   ├── marketplace.json        # marketplace manifest (name: tasachii-tools)
│   └── README.md               # install guide
├── plugins/
│   └── readme-craft/
│       ├── .claude-plugin/plugin.json
│       └── skills/readme-craft/
│           ├── SKILL.md                       # the skill + workflow
│           └── references/
│               ├── style-guide.md             # full house-style rulebook
│               └── template.md                # fill-in README skeleton
└── README.md
```

---

## Roadmap

- [x] `readme-craft` — README writer
- [ ] More personal skills, added one at a time

---

## License

MIT © Phasathat Jaruchitsophon
