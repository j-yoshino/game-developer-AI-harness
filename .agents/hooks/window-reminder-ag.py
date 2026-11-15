#!/usr/bin/env python3
"""Adapter: run the Claude window-reminder hook and print it in Antigravity's PreInvocation format.

The Claude hook (.claude/hooks/window-reminder.sh) prints
  {"hookSpecificOutput": {"additionalContext": "<text>"}}
Antigravity expects
  {"injectSteps": [{"ephemeralMessage": "<text>"}]}
(see https://antigravity.google/docs/hooks). The reminder text itself stays in the Claude hook,
so there is one source of truth. This adapter fails open: on any error it prints nothing and exits 0.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HOOK = ROOT / ".claude" / "hooks" / "window-reminder.sh"


def main() -> int:
    try:
        sys.stdin.read()  # The hook input JSON is not needed.
        # A relative path with cwd=ROOT: Git Bash cannot open an absolute path that contains
        # non-ASCII characters when it is passed as an argument from Python on Windows.
        result = subprocess.run(
            ["bash", HOOK.relative_to(ROOT).as_posix()],
            input=b"", capture_output=True, timeout=8, check=True, cwd=ROOT,
        )
        text = json.loads(result.stdout.decode("utf-8"))["hookSpecificOutput"]["additionalContext"]
    except Exception:
        return 0
    sys.stdout.write(json.dumps({"injectSteps": [{"ephemeralMessage": text}]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
