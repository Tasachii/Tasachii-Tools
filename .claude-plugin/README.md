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
/plugin install readme-craft@tasachii-tools
/plugin install caffe@tasachii-tools
/plugin install qa@tasachii-tools
```

Each skill triggers by intent, no flags — `tsc` / `/fix readme` for `readme-craft`, `/caffe` or
"keep awake" for `caffe`, and `/qa` or "score this project" for `qa`. The repo README lists the
full trigger set for each.

## Plugins

| Plugin | Description |
| --- | --- |
| `readme-craft` | Create, rewrite, or update project READMEs in a calm, precise, fact-only house style — never invents facts. |
| `caffe` | Keep the Mac awake for long jobs — a thin `caffeinate` wrapper with on / off / status. macOS only. |
| `qa` | Smoke-test and QA a project, score it from four angles (CTO · tech lead · UX/UI · QA), and list every fixable flaw. Asks before fixing. |

## License

MIT © Phasathat Jaruchitsophon
