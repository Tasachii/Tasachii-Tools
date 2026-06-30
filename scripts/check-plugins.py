#!/usr/bin/env python3
"""Structural validation of every plugin in the marketplace — no Claude CLI required.

For each plugin listed in the marketplace it checks that:
- the source directory and its `plugin.json` exist;
- `plugin.json` has `name`, `version` (semver), and `description`, and its name matches the
  marketplace entry;
- every skill under `skills/<name>/` has a `SKILL.md` with `name` + `description` frontmatter.
This catches a malformed plugin in CI, where `claude plugin validate` isn't available.
"""
import json
import os
import re
import sys

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
REQUIRED = ["name", "version", "description"]


def _frontmatter(text):
    """Top-level `key: value` pairs from a leading `--- ... ---` YAML block, or None."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def check(root="."):
    errors = []
    mkt = json.load(open(os.path.join(root, ".claude-plugin/marketplace.json")))
    for p in mkt["plugins"]:
        name, src = p["name"], p["source"]
        pdir = os.path.join(root, src)
        pj_path = os.path.join(pdir, ".claude-plugin/plugin.json")
        if not os.path.isdir(pdir):
            errors.append(f"{name}: source dir missing ({src})")
            continue
        if not os.path.exists(pj_path):
            errors.append(f"{name}: missing .claude-plugin/plugin.json")
            continue
        pj = json.load(open(pj_path))
        for f in REQUIRED:
            if not pj.get(f):
                errors.append(f"{name}: plugin.json missing '{f}'")
        if pj.get("name") != name:
            errors.append(f"{name}: plugin.json name {pj.get('name')!r} != marketplace name {name!r}")
        if pj.get("version") and not SEMVER.match(pj["version"]):
            errors.append(f"{name}: plugin.json version not semver: {pj['version']!r}")
        skills_dir = os.path.join(pdir, "skills")
        if os.path.isdir(skills_dir):
            for sk in sorted(os.listdir(skills_dir)):
                sp = os.path.join(skills_dir, sk, "SKILL.md")
                if not os.path.exists(sp):
                    errors.append(f"{name}/{sk}: missing SKILL.md")
                    continue
                fm = _frontmatter(open(sp).read())
                if fm is None:
                    errors.append(f"{name}/{sk}: SKILL.md has no YAML frontmatter")
                    continue
                for key in ("name", "description"):
                    if not fm.get(key):
                        errors.append(f"{name}/{sk}: SKILL.md frontmatter missing '{key}'")
    return errors


def main():
    errors = check(".")
    if errors:
        for e in errors:
            print(f"::error::{e}")
        sys.exit(1)
    n = len(json.load(open(".claude-plugin/marketplace.json"))["plugins"])
    print(f"Plugins valid: {n} plugin(s) checked — manifests and skill frontmatter OK.")


if __name__ == "__main__":
    main()
