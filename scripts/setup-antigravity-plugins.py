#!/usr/bin/env python3
"""Place the vendored superpowers plugin into this project for Antigravity (project scope).

Antigravity loads plugin folders from `.agents/plugins/` in the project root (official docs:
https://antigravity.google/docs/plugins). This script copies `vendor/superpowers` there, leaving out
files that the plugin does not need at run time. The copy is a derived artifact: it is not tracked
by Git (see .gitignore) and is rebuilt by running this script again.

Usage:
    python scripts/setup-antigravity-plugins.py --dry-run   # show the destination and files; write nothing
    python scripts/setup-antigravity-plugins.py             # copy

Exit codes: 0 = done, 2 = the vendored plugin is missing or empty (run `git submodule update --init`).

Which files the plugin strictly needs is not documented; if something is missing at run time,
adjust EXCLUDE below.
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "vendor" / "superpowers"
DEST = ROOT / ".agents" / "plugins" / "superpowers"

# Top-level names that are not copied: VCS data, tests, docs, and the manifests of other tools.
EXCLUDE = {
    ".git", ".github", ".agents", "tests", "docs",
    ".codex-plugin", ".cursor-plugin", ".devin-plugin", ".hermes-plugin",
    ".kimi-plugin", ".muse-plugin", ".opencode", ".pi", ".claude-plugin",
}


def selected_files():
    files = []
    for path in sorted(SRC.rglob("*")):
        if not path.is_file():
            continue
        top = path.relative_to(SRC).parts[0]
        if top in EXCLUDE:
            continue
        files.append(path)
    return files


def main(argv):
    dry = "--dry-run" in argv
    unknown = [a for a in argv if a != "--dry-run"]
    if unknown:
        print(f"unknown arguments: {unknown}", file=sys.stderr)
        return 2
    if not (SRC / ".antigravity-plugin" / "plugin.json").is_file():
        print("vendor/superpowers is missing or has no .antigravity-plugin/plugin.json; "
              "run `git submodule update --init vendor/superpowers`.", file=sys.stderr)
        return 2
    files = selected_files()
    print(f"destination: {DEST.relative_to(ROOT).as_posix()}")
    print(f"files: {len(files)} (excluded top-level names: {', '.join(sorted(EXCLUDE))})")
    if dry:
        for f in files[:40]:
            print("  " + f.relative_to(SRC).as_posix())
        if len(files) > 40:
            print(f"  ... and {len(files) - 40} more")
        print("dry run: nothing was written")
        return 0
    if DEST.exists():
        shutil.rmtree(DEST)
    for f in files:
        target = DEST / f.relative_to(SRC)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, target)
    print(f"copied {len(files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
