#!/usr/bin/env python3
"""Commit the assembled `main` layout to a local branch (default: main-build). Never pushes.

The branch is built from scratch on first use (orphan history) and gets one commit per run that
changes anything. `main` and `develop` are never touched. The Unreal submodule is recorded as a
gitlink pointing at the commit that `develop` uses.

Usage:
    python scripts/publish-main-branch.py [--branch main-build] [--allow-dirty]

Exit codes: 0 = done (including "no change"), 2 = invalid input or a refused state.
See specs/006-plugin-conversion-branch/contracts/build-main.md.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UNREAL = "vendor/unreal-engine-skills-for-claude-code-plugin"
PROTECTED = {"main", "develop", "master"}


class Refused(Exception):
    pass


def git(args, cwd=ROOT, check=True):
    r = subprocess.run(["git"] + args, cwd=cwd, capture_output=True)
    out = r.stdout.decode("utf-8", "replace").strip()
    if check and r.returncode != 0:
        raise Refused(f"git {' '.join(args)} failed: {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.returncode, out


def main(argv):
    branch, allow_dirty, i = "main-build", False, 0
    while i < len(argv):
        if argv[i] == "--branch" and i + 1 < len(argv):
            branch, i = argv[i + 1], i + 2
        elif argv[i] == "--allow-dirty":
            allow_dirty, i = True, i + 1
        else:
            print(f"unknown argument: {argv[i]}", file=sys.stderr)
            return 2
    try:
        if branch in PROTECTED:
            raise Refused(f"refusing to write to protected branch {branch!r}")
        if not allow_dirty and git(["status", "--porcelain", "--untracked-files=no"])[1]:
            raise Refused("develop has uncommitted changes to tracked files (commit them, or pass --allow-dirty for a trial run)")
        short = git(["rev-parse", "--short", "HEAD"])[1]
        unreal_sha = git(["rev-parse", "HEAD"], cwd=ROOT / UNREAL)[1]
        tmp = Path(tempfile.mkdtemp(prefix="mainbuild"))
        if not str(tmp).isascii():
            raise Refused("the temporary directory path is not ASCII; set TMP/TEMP to an ASCII path")
        try:
            build, wt = tmp / "build", tmp / "wt"
            r = subprocess.run([sys.executable, "scripts/build-main.py", "--out", str(build)], cwd=ROOT, capture_output=True)
            if r.returncode != 0:
                raise Refused("build-main.py failed: " + (r.stderr or r.stdout).decode("utf-8", "replace").strip())
            exists = git(["rev-parse", "--verify", "--quiet", f"refs/heads/{branch}"], check=False)[0] == 0
            if exists:
                git(["worktree", "add", str(wt), branch])
            else:
                git(["worktree", "add", "--detach", str(wt)])
                git(["checkout", "--orphan", branch], cwd=wt)
                git(["rm", "-rf", "--quiet", "."], cwd=wt, check=False)
            for entry in wt.iterdir():
                if entry.name == ".git":
                    continue
                shutil.rmtree(entry) if entry.is_dir() else entry.unlink()
            for src in build.rglob("*"):
                if src.is_file():
                    dest = wt / src.relative_to(build)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dest)
            # The Unreal files become a gitlink (a submodule), not plain files.
            shutil.rmtree(wt / UNREAL)
            git(["add", "-A"], cwd=wt)
            git(["rm", "-r", "--cached", "--quiet", "--ignore-unmatch", UNREAL], cwd=wt, check=False)
            git(["update-index", "--add", "--cacheinfo", f"160000,{unreal_sha},{UNREAL}"], cwd=wt)
            if git(["diff", "--cached", "--quiet"], cwd=wt, check=False)[0] == 0 and exists:
                print(f"no change on {branch}")
                return 0
            git(["commit", "-q", "-m", f"build: develop {short} から main の構成を組み立てる"], cwd=wt)
            print(f"committed to {branch} (develop {short}); nothing was pushed")
            return 0
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", str(tmp / "wt")], cwd=ROOT, capture_output=True)
            shutil.rmtree(tmp, ignore_errors=True)
    except Refused as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
