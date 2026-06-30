#!/usr/bin/env python3
"""Guard against version drift across the marketplace, each plugin, and the README.

- Every plugin's `plugin.json` version must appear in the README Plugins table.
- The marketplace `metadata.version` must be valid semver.

Plugin versions and the marketplace (catalog) version are intentionally INDEPENDENT —
this script does not require them to match. Run from the repo root.
"""
import json
import re
import sys

mkt = json.load(open(".claude-plugin/marketplace.json"))
readme = open("README.md").read().replace("`", "")  # drop backticks so table cells match plainly
errors = []

mv = mkt["metadata"]["version"]
if not re.match(r"^\d+\.\d+\.\d+$", mv):
    errors.append(f"marketplace metadata.version is not semver: {mv!r}")

for p in mkt["plugins"]:
    name, src = p["name"], p["source"]
    pv = json.load(open(f"{src}/.claude-plugin/plugin.json"))["version"]
    if f"{name} | {pv} |" not in readme:
        errors.append(
            f"README Plugins table has no row '{name} | {pv} |' (plugin.json says {pv})"
        )

if errors:
    for e in errors:
        print(f"::error::{e}")
    sys.exit(1)

print("Versions consistent: each plugin matches the README; marketplace version is semver.")
