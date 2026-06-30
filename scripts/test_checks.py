#!/usr/bin/env python3
"""Self-test for the CI guards: they must PASS on the real repo and FAIL on injected drift.

Run with `python3 scripts/test_checks.py` (from the repo root). No test framework needed.
"""
import importlib.util
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cv = _load("check_versions", "check-versions.py")
cp = _load("check_plugins", "check-plugins.py")


def _fixture(tmp):
    """Copy just the inputs the guards read."""
    shutil.copytree(os.path.join(ROOT, ".claude-plugin"), os.path.join(tmp, ".claude-plugin"))
    shutil.copytree(os.path.join(ROOT, "plugins"), os.path.join(tmp, "plugins"))
    shutil.copy(os.path.join(ROOT, "README.md"), os.path.join(tmp, "README.md"))
    return json.load(open(os.path.join(tmp, ".claude-plugin/marketplace.json")))


def main():
    failures = []

    # 1. Real repo must pass both guards.
    real_cv, real_cp = cv.check(ROOT), cp.check(ROOT)
    if real_cv:
        failures.append(f"check-versions should pass on the real repo, got: {real_cv}")
    if real_cp:
        failures.append(f"check-plugins should pass on the real repo, got: {real_cp}")

    # 2. A drifted README version must be caught by check-versions.
    with tempfile.TemporaryDirectory() as tmp:
        mkt = _fixture(tmp)
        first = mkt["plugins"][0]["name"]
        open(os.path.join(tmp, "README.md"), "w").write(
            "## Plugins\n\n| Plugin | Version | What |\n| --- | --- | --- |\n"
            f"| `{first}` | 9.9.9 | drifted |\n"
        )
        if not cv.check(tmp):
            failures.append("check-versions did NOT catch a drifted README version")

    # 3. A malformed plugin.json must be caught by check-plugins.
    with tempfile.TemporaryDirectory() as tmp:
        mkt = _fixture(tmp)
        src = mkt["plugins"][0]["source"]
        pj_path = os.path.join(tmp, src, ".claude-plugin/plugin.json")
        pj = json.load(open(pj_path))
        pj.pop("version", None)
        json.dump(pj, open(pj_path, "w"))
        if not cp.check(tmp):
            failures.append("check-plugins did NOT catch a plugin.json missing 'version'")

    if failures:
        for f in failures:
            print(f"::error::{f}")
        sys.exit(1)
    print("Guard self-tests passed: green on the real repo, and both injected faults were caught.")


if __name__ == "__main__":
    main()
