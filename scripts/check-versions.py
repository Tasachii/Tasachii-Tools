#!/usr/bin/env python3
"""Guard against version drift across the marketplace, each plugin, and the README.

- Every plugin's `plugin.json` version must match its row in the README "## Plugins" table.
- The marketplace `metadata.version` must be valid semver.

Plugin versions and the marketplace (repo release) version are independent — this does NOT
require them to match. The README table is parsed structurally, so it tolerates layout changes.
"""
import json
import os
import re
import sys

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def _readme_table_versions(text):
    """Parse the '## Plugins' markdown table into {plugin_name: version}."""
    out, in_plugins = {}, False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("## "):
            in_plugins = s.lower().startswith("## plugins")
            continue
        if in_plugins and s.startswith("|"):
            cells = [c.strip().strip("`") for c in s.strip("|").split("|")]
            if len(cells) >= 2 and SEMVER.match(cells[1]):  # skips header + separator rows
                out[cells[0]] = cells[1]
    return out


def check(root="."):
    errors = []
    mkt = json.load(open(os.path.join(root, ".claude-plugin/marketplace.json")))
    mv = mkt["metadata"]["version"]
    if not SEMVER.match(mv):
        errors.append(f"marketplace metadata.version is not semver: {mv!r}")
    table = _readme_table_versions(open(os.path.join(root, "README.md")).read())
    for p in mkt["plugins"]:
        name, src = p["name"], p["source"]
        pv = json.load(open(os.path.join(root, src, ".claude-plugin/plugin.json")))["version"]
        if table.get(name) != pv:
            errors.append(
                f"README Plugins table lists {name}={table.get(name)} but plugin.json says {pv}"
            )
    return errors


def main():
    errors = check(".")
    if errors:
        for e in errors:
            print(f"::error::{e}")
        sys.exit(1)
    print("Versions consistent: each plugin matches the README; marketplace version is semver.")


if __name__ == "__main__":
    main()
