# qa rubric & output format

## Per-angle 10-point scale
- **9–10** — excellent; a professional in that role would sign off with no concerns.
- **7–8** — good; it ships, with minor nits that don't block.
- **5–6** — usable but with real friction; needs work before it is "good".
- **3–4** — significant problems; a core concern for that role is unmet.
- **1–2** — broken or failing for that role's core responsibility.

Anchor to the role's core responsibility first, then modify for polish. "It looks great but the
submit button does nothing" is a 2 for QA, not a 7.

## What each angle anchors on
Each angle scores against the explicit **five-point checklist** in `SKILL.md` §4; show those five
checks with ✓ / ⚠ / ✗ in the report so every score is traceable. The headline question per angle:
- **🧑‍💼 CTO** — Would I bet the roadmap on this? (value · risk/security · maintainability · cost · licensing)
- **🛠️ Tech Lead** — Would I approve this PR? (code quality · architecture · correctness · conventions · CI)
- **🎨 UX/UI Designer** — Would a user enjoy this? (visual · usability · accessibility/i18n · copy · responsiveness)
- **🧪 QA Tester** — Does it actually work? (smoke · happy path · edge cases · error handling · coverage)

## Output format

    # 📊 QA Scorecard — <project>

    **Overall: N/10** — <one-line verdict; reflects the weakest critical path>

    | Angle | Score | One-line reason |
    |---|---|---|
    | 🧑‍💼 CTO | N/10 | ... |
    | 🛠️ Tech Lead | N/10 | ... |
    | 🎨 UX/UI | N/10 | ... |
    | 🧪 QA Tester | N/10 | ... |

    ## ✅ Passed
    - <smoke-test gates that are green>

    ## 🔴 Weaknesses (worst first)
    - **[blocker] <title>** — `file:line` · why it matters · fix: <how + where>
    - **[high] ...**
    - **[medium] ...**
    - **[low] ...**

    ## Evidence
    - <command output snippets, screenshots, file:line refs>

Then ask: **fix all · critical only · none?** Do not fix until the user chooses.
