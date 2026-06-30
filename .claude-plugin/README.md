# Tasachii-Tools — install guide

A personal Claude Code plugin marketplace by Phasathat Jaruchitsophon.

## Add the marketplace

From GitHub:

```text
/plugin marketplace add Tasachii/Tasachii-Tools
```

Locally, before pushing:

```text
/plugin marketplace add .
```

## Install a plugin

```text
/plugin install craft-readme@tasachii-tools
/plugin install craft-caffe@tasachii-tools
/plugin install craft-qa@tasachii-tools
/plugin install craft-slides@tasachii-tools
```

Each skill triggers by intent, no flags — `tsc` / `/fix readme` for `craft-readme`, `/caffe` or
"keep awake" for `craft-caffe`, `/qa` or "score this project" for `craft-qa`, and `/craft-slides` (or `/slides`)
or "make a deck" for `craft-slides`. The repo README lists the full trigger set for each.

## Plugins

| Plugin | Description |
| --- | --- |
| `craft-readme` | Create, rewrite, or update project READMEs in a calm, precise, fact-only house style — never invents facts. |
| `craft-caffe` | Keep the Mac awake for long jobs — a thin `caffeinate` wrapper with on / off / status. macOS only. |
| `craft-qa` | Smoke-test and QA a project, score it from four angles (CTO · tech lead · UX/UI · QA), and list every fixable flaw. Asks before fixing. |
| `craft-slides` | Build a self-contained HTML slide deck that designs itself around the topic — grounded in real content, Thai/English aware, with presenter notes and a 1920×1080 overflow self-check. |

## License

MIT © Phasathat Jaruchitsophon
