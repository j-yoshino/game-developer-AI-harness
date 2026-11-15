#!/usr/bin/env python3
"""Generate the Codex and Antigravity environment from the Claude source of truth.

Source of truth: .claude/ (skills, agents, rules, hooks).
Generated:       .agents/ and .codex/ (see specs/004-cross-tool-claude-env/contracts/sync-script.md).

Usage:
    python scripts/sync-agent-env.py            # generate (overwrite)
    python scripts/sync-agent-env.py --check    # verify only; writes nothing

Exit codes: 0 = done / in sync, 1 = --check found drift, 2 = invalid input.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULE_MAX_BYTES = 24000  # Antigravity truncates rule files above this size.

# Directories whose contents are fully owned by this script (orphans are removed).
MANAGED_DIRS = [
    ".agents/skills",
    ".agents/agents",
    ".agents/rules",
    ".codex/agents",
]


class InputError(Exception):
    """Raised when a source file cannot be converted."""


def norm(data: bytes) -> bytes:
    """Normalize CRLF to LF so a CRLF checkout (core.autocrlf) is not seen as drift."""
    return data.replace(b"\r\n", b"\n")


def read_text(path: Path) -> str:
    return norm(path.read_bytes()).decode("utf-8")


def split_frontmatter(text: str):
    """Return (frontmatter_text_or_None, body). Frontmatter is a leading --- block."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 3)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5:]


def parse_frontmatter(fm: str) -> dict:
    """Parse the small YAML subset used here: `key: value` and `key:` + `- item` lists."""
    result = {}
    current_list = None
    for raw in fm.split("\n"):
        if not raw.strip():
            continue
        item = re.match(r"^\s+-\s+(.*)$", raw)
        if item and current_list is not None:
            result[current_list].append(unquote(item.group(1).strip()))
            continue
        pair = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if not pair:
            continue
        key, value = pair.group(1), pair.group(2).strip()
        if value == "":
            result[key] = []
            current_list = key
        else:
            result[key] = unquote(value)
            current_list = None
    return result


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def expand_braces(pattern: str):
    """Expand the first {a,b,c} group recursively (Antigravity globs are comma-separated)."""
    match = re.search(r"\{([^{}]*)\}", pattern)
    if not match:
        return [pattern]
    out = []
    for option in match.group(1).split(","):
        out.extend(expand_braces(pattern[: match.start()] + option + pattern[match.end():]))
    return out


# ---------------------------------------------------------------- generators


def gen_skills(desired, errors):
    src = ROOT / ".claude" / "skills"
    for skill in sorted(p for p in src.iterdir() if p.is_dir()):
        for f in sorted(p for p in skill.rglob("*") if p.is_file()):
            rel = f.relative_to(src).as_posix()
            desired[f".agents/skills/{rel}"] = f.read_bytes()


def gen_agents(desired, errors):
    src = ROOT / ".claude" / "agents"
    for f in sorted(src.glob("*.md")):
        desired[f".agents/agents/{f.name}"] = f.read_bytes()
        text = read_text(f)
        fm, body = split_frontmatter(text)
        meta = parse_frontmatter(fm) if fm is not None else {}
        name, desc = meta.get("name"), meta.get("description")
        if not name or not desc:
            errors.append(f"{f.relative_to(ROOT)}: frontmatter needs name and description")
            continue
        instructions = body.lstrip("\n")
        if "'''" in instructions:
            errors.append(f"{f.relative_to(ROOT)}: body contains ''' (cannot be written as a TOML literal string)")
            continue
        toml = (
            f"# generated from .claude/agents/{f.name}. Do not edit; run scripts/sync-agent-env.py.\n"
            f"name = {toml_basic(name)}\n"
            f"description = {toml_basic(desc)}\n"
            f"developer_instructions = '''\n{instructions}'''\n"
        )
        desired[f".codex/agents/{f.stem}.toml"] = toml.encode("utf-8")


def toml_basic(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def gen_rules(desired, errors):
    src = ROOT / ".claude" / "rules"
    seen = {}
    for f in sorted(src.rglob("*.md")):
        parts = f.relative_to(src).parts
        out_name = "-".join(parts)
        if out_name in seen:
            errors.append(f"rules name collision: {out_name}")
            continue
        seen[out_name] = f
        text = read_text(f)
        fm, body = split_frontmatter(text)
        meta = parse_frontmatter(fm) if fm is not None else {}
        body = body.lstrip("\n")
        paths = meta.get("paths") or []
        header = []
        heading = re.search(r"^#\s+(.+)$", body, re.M)
        description = heading.group(1).strip() if heading else out_name
        if paths:
            globs = []
            for p in paths:
                globs.extend(expand_braces(p))
            header = ["trigger: glob", f"description: {json.dumps(description, ensure_ascii=False)}",
                      f'globs: "{", ".join(globs)}"']
        else:
            header = ["trigger: always_on", f"description: {json.dumps(description, ensure_ascii=False)}"]
        rel = f.relative_to(ROOT).as_posix()
        out = "---\n" + "\n".join(header) + "\n---\n" + f"<!-- generated from {rel}. Do not edit; run scripts/sync-agent-env.py. -->\n" + body
        data = out.encode("utf-8")
        if len(data) > RULE_MAX_BYTES:
            errors.append(f"{rel}: generated rule is {len(data)} bytes (> {RULE_MAX_BYTES})")
            continue
        desired[f".agents/rules/{out_name}"] = data


def gen_hooks(desired, errors):
    """Hook settings only call the Claude hook; the script itself is never copied."""
    if not (ROOT / ".claude" / "hooks" / "window-reminder.sh").is_file():
        errors.append(".claude/hooks/window-reminder.sh is missing")
        return
    codex = {
        "hooks": {
            "UserPromptSubmit": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": 'bash "$(git rev-parse --show-toplevel)/.claude/hooks/window-reminder.sh"',
                            "commandWindows": "bash .claude/hooks/window-reminder.sh",
                            "timeout": 10,
                        }
                    ]
                }
            ]
        }
    }
    antigravity = {
        "window-reminder": {
            "PreInvocation": [
                {
                    "type": "command",
                    "command": "python .agents/hooks/window-reminder-ag.py",
                    "timeout": 10,
                }
            ]
        }
    }
    desired[".codex/hooks.json"] = (json.dumps(codex, indent=2) + "\n").encode("utf-8")
    desired[".agents/hooks.json"] = (json.dumps(antigravity, indent=2) + "\n").encode("utf-8")


GENERATORS = [gen_skills, gen_agents, gen_rules, gen_hooks]


# ------------------------------------------------------------------- driver


def collect():
    desired, errors = {}, []
    for gen in GENERATORS:
        gen(desired, errors)
    return desired, errors


def existing_managed_files():
    found = set()
    for d in MANAGED_DIRS:
        base = ROOT / d
        if base.is_dir():
            for f in base.rglob("*"):
                if f.is_file():
                    found.add(f.relative_to(ROOT).as_posix())
    return found


def main(argv):
    check = "--check" in argv
    unknown = [a for a in argv if a not in ("--check",)]
    if unknown:
        print(f"unknown arguments: {unknown}", file=sys.stderr)
        return 2
    desired, errors = collect()
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 2

    drift = []
    for rel, data in sorted(desired.items()):
        path = ROOT / rel
        if not path.is_file():
            drift.append(f"missing: {rel}")
        elif norm(path.read_bytes()) != norm(data):
            drift.append(f"differs: {rel}")
    orphans = sorted(existing_managed_files() - set(desired))
    for rel in orphans:
        drift.append(f"orphan: {rel}")

    if check:
        for line in drift:
            print(line)
        print(f"{len(desired)} generated files, {len(drift)} drifted")
        return 1 if drift else 0

    written = 0
    for rel, data in sorted(desired.items()):
        path = ROOT / rel
        if path.is_file() and norm(path.read_bytes()) == norm(data):
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data if rel.startswith(".agents/skills/") or rel.startswith(".agents/agents/") else norm(data))
        written += 1
    for rel in orphans:
        (ROOT / rel).unlink()
    for d in MANAGED_DIRS:
        base = ROOT / d
        if base.is_dir():
            for sub in sorted((p for p in base.rglob("*") if p.is_dir()), reverse=True):
                if not any(sub.iterdir()):
                    sub.rmdir()
    print(f"{len(desired)} generated files, {written} written, {len(orphans)} orphans removed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
