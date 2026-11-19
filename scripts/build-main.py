#!/usr/bin/env python3
"""Assemble the minimal `main` layout from the tracked files of `develop`.

The sources of truth are independent per tool (.claude/, .codex/, .agents/). This script copies
the tracked files that belong on `main`, renders a few files from scripts/templates/, and adds the
Unreal plugin (a vendored Epic repository). It never writes to the repository itself.

Usage:
    python scripts/build-main.py --out <dir>           # assemble into <dir> (previous content is replaced)
    python scripts/build-main.py --out <dir> --check   # compare <dir> with a fresh assembly; write nothing

Exit codes: 0 = done / identical, 1 = --check found differences, 2 = invalid input.
See specs/006-plugin-conversion-branch/contracts/build-main.md.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "scripts" / "templates"
UNREAL = "vendor/unreal-engine-skills-for-claude-code-plugin"

# Tracked files that go to main (allow list). Anything else is left out.
ALLOW_PREFIXES = (".claude/", ".codex/", ".agents/")
ALLOW_FILES = {".claude-plugin/marketplace.json", ".gitattributes"}
# Allowed prefixes that must not be copied (local settings, or replaced by a generated file).
EXCLUDE_FILES = {".claude/settings.local.json", ".agents/plugins/marketplace.json"}

# Files rendered from templates: output path -> template name.
RENDERED = {
    ".claude/settings.json": "main-claude-settings.json",
    ".agents/plugins/marketplace.json": "main-codex-marketplace.json",
    "AGENTS.md": "main-AGENTS.md",
    "CLAUDE.md": "main-CLAUDE.md",
    "README.md": "main-README.md",
}

# Personal data must never reach main.
PERSONAL = re.compile(r"C:[\/]+Users|/c/Users|Disas|デスクトップ", re.I)


class InputError(Exception):
    pass


def git(args, cwd=ROOT):
    # Relative paths and cwd only: absolute paths with non-ASCII characters fail in Git Bash on Windows.
    result = subprocess.run(["git"] + args, cwd=cwd, capture_output=True)
    if result.returncode != 0:
        raise InputError(f"git {' '.join(args)} failed: {result.stderr.decode('utf-8', 'replace').strip()}")
    return result.stdout


def tracked(cwd=ROOT):
    return [p for p in git(["ls-files", "-z"], cwd).decode("utf-8").split("\0") if p]


def norm(data: bytes) -> bytes:
    """LF for text files (a CRLF checkout must not change the output); binary files are untouched."""
    return data if b"\0" in data else data.replace(b"\r\n", b"\n")


def assemble():
    files = {}
    # 1. Tracked files that belong on main.
    for rel in tracked():
        if rel in EXCLUDE_FILES:
            continue
        if rel.startswith(ALLOW_PREFIXES) or rel in ALLOW_FILES:
            files[rel] = norm((ROOT / rel).read_bytes())
    # 2. Rendered files.
    for out, name in RENDERED.items():
        tpl = TEMPLATES / name
        if not tpl.is_file():
            raise InputError(f"template missing: scripts/templates/{name}")
        files[out] = norm(tpl.read_bytes())
    # 3. Unreal (vendored). An empty submodule is an error.
    sub = ROOT / UNREAL
    if not sub.is_dir():
        raise InputError(f"{UNREAL} is missing; run `git submodule update --init {UNREAL}`")
    unreal_files = tracked(sub)
    if not unreal_files:
        raise InputError(f"{UNREAL} is empty; run `git submodule update --init {UNREAL}`")
    for rel in unreal_files:
        files[f"{UNREAL}/{rel}"] = norm((sub / rel).read_bytes())
    url = git(["config", "-f", ".gitmodules", "--get", f"submodule.{UNREAL}.url"]).decode("utf-8").strip()
    files[".gitmodules"] = (f'[submodule "{UNREAL}"]\n\tpath = {UNREAL}\n\turl = {url}\n').encode("utf-8")
    # 4. Allow-list sanity: every rendered/template file exists, nothing personal.
    for rel, data in files.items():
        if b"\0" in data:
            continue
        text = data.decode("utf-8", "replace")
        if PERSONAL.search(text):
            raise InputError(f"personal data found in output file: {rel}")
    return files


def existing(out: Path):
    found = {}
    if out.is_dir():
        for p in sorted(out.rglob("*")):
            if p.is_file():
                found[p.relative_to(out).as_posix()] = p.read_bytes()
    return found


def main(argv):
    check = "--check" in argv
    args = [a for a in argv if a != "--check"]
    if len(args) != 2 or args[0] != "--out":
        print("usage: build-main.py --out <dir> [--check]", file=sys.stderr)
        return 2
    out = Path(args[1])
    try:
        files = assemble()
    except InputError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    if check:
        have = existing(out)
        drift = [f"missing: {r}" for r in sorted(files) if r not in have]
        drift += [f"differs: {r}" for r in sorted(files) if r in have and norm(have[r]) != files[r]]
        drift += [f"extra: {r}" for r in sorted(have) if r not in files]
        for line in drift:
            print(line)
        print(f"{len(files)} files, {len(drift)} differences")
        return 1 if drift else 0
    if (out / ".git").exists():
        print("ERROR: refusing to write into a directory that contains .git", file=sys.stderr)
        return 2
    if out.exists():
        shutil.rmtree(out)
    for rel, data in sorted(files.items()):
        path = out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(f"{len(files)} files written")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
