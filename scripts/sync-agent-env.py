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


# Claude tool name -> Antigravity tool name (only names confirmed in the official example).
# Glob and Agent have no confirmed Antigravity counterpart and are left out of the tool list.
AG_TOOLS = {
    "Read": "view_file",
    "Grep": "grep_search",
    "Bash": "run_command",
    "Write": "replace_file_content",
    "Edit": "replace_file_content",
}
AG_UNMAPPED = {"Glob", "Agent"}
# Claude model -> Antigravity model tier (official values: inherit, flash, pro).
# The mapping is the user's choice (opus -> pro, sonnet -> flash); the docs do not define it.
AG_MODELS = {"opus": "pro", "sonnet": "flash", "haiku": "flash"}
READ_ONLY_TOOLS = {"Read", "Grep", "Glob"}
CODEX_READ_ONLY_NOTE = (
    "Read-only: do not create, edit or delete files, and do not run commands that change state. "
    "Report findings only.\n\n"
)
TOML_LITERAL = "'" * 3


def gen_agents(desired, errors):
    src = ROOT / ".claude" / "agents"
    for f in sorted(src.glob("*.md")):
        rel_src = f.relative_to(ROOT).as_posix()
        text = read_text(f)
        fm, body = split_frontmatter(text)
        meta = parse_frontmatter(fm) if fm is not None else {}
        name, desc = meta.get("name"), meta.get("description")
        tools_raw = meta.get("tools")
        if not name or not desc or not isinstance(tools_raw, str):
            errors.append(f"{rel_src}: frontmatter needs name, description and tools")
            continue
        claude_model = meta.get("model")
        if claude_model is not None and claude_model not in AG_MODELS:
            errors.append(f"{rel_src}: unknown model {claude_model!r}; add it to AG_MODELS")
            continue
        ag_model = AG_MODELS.get(claude_model, "inherit")
        tools = [x.strip() for x in tools_raw.split(",") if x.strip()]
        unknown = [x for x in tools if x not in AG_TOOLS and x not in AG_UNMAPPED]
        if unknown:
            errors.append(f"{rel_src}: unknown tool name(s) {unknown}; add them to AG_TOOLS or AG_UNMAPPED")
            continue
        ag_tools = []
        for x in tools:
            if x in AG_TOOLS and AG_TOOLS[x] not in ag_tools:
                ag_tools.append(AG_TOOLS[x])
        instructions = body.lstrip("\n")
        # Antigravity: converted frontmatter (tool and model names differ from Claude).
        ag = ["---", f"name: {json.dumps(name, ensure_ascii=False)}",
              f"description: {json.dumps(desc, ensure_ascii=False)}", "tools:"]
        ag += [f"  - {x}" for x in ag_tools]
        ag += ["subagent: true", "mainAgent: false", f"model: {ag_model}", "---",
               f"<!-- generated from {rel_src}. Do not edit; run scripts/sync-agent-env.py. -->"]
        desired[f".agents/agents/{f.name}"] = ("\n".join(ag) + "\n" + instructions).encode("utf-8")
        # Codex: TOML. A per-agent read-only sandbox is not available, so add an instruction.
        if TOML_LITERAL in instructions:
            errors.append(f"{rel_src}: body contains three single quotes (cannot be written as a TOML literal string)")
            continue
        if set(tools) <= READ_ONLY_TOOLS:
            instructions = CODEX_READ_ONLY_NOTE + instructions
        toml = (
            f"# generated from {rel_src}. Do not edit; run scripts/sync-agent-env.py.\n"
            f"name = {toml_basic(name)}\n"
            f"description = {toml_basic(desc)}\n"
            f"developer_instructions = {TOML_LITERAL}\n{instructions}{TOML_LITERAL}\n"
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
