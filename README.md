# Tasachii-Tools（タサチー・ツールズ）

A personal Claude Code plugin marketplace — calm, precise tools for everyday
development work. Plugins are installed on demand and trigger by intent, not config.

---

## Plugins

| Plugin | Version | What it does |
| --- | --- | --- |
| `readme-craft` | 0.1.0 | Writes and rewrites project READMEs in a fact-only house style. Reads the real code or asks — never invents facts. |

---

## Quick start

**Local (test before pushing)**
```text
/plugin marketplace add .                     # register this folder
/plugin install readme-craft@tasachii-tools   # install the README writer
```

**From GitHub (after pushing)**
```text
/plugin marketplace add Tasachii/Tasachii-Tools
/plugin install readme-craft@tasachii-tools
```

---

## House style

The skills here share one aesthetic — calm, understated, table-heavy, and honest:

- **Fact-only.** No invented numbers, commands, or features. Unverifiable facts become
  visible TODOs, never guesses.
- **English prose, native UI preserved.** Surrounding text is English; live UI strings
  (e.g. Thai labels like `บันทึก`) stay exactly as the app shows them.
- **Tables over prose.** Decisions carry their *why*.

---

## Repository layout

```text
Tasachii-Tools/
├── .claude-plugin/
│   ├── marketplace.json        # marketplace manifest
│   └── README.md               # install guide
├── plugins/
│   └── readme-craft/
│       ├── .claude-plugin/plugin.json
│       └── skills/readme-craft/
│           ├── SKILL.md
│           └── references/{style-guide.md, template.md}
└── README.md
```

---

## License

MIT © Phasathat Jaruchitsophon
