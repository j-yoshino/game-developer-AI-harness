#!/bin/bash
# Injects a short request-window reminder into the context on every user prompt.
# Reads and discards stdin (the hook input JSON); always exits 0 so input is never blocked.

cat > /dev/null

printf '%s' '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"Request window: for each USER message, first classify it as question (no work, nothing changes), light task (reversible, small, no spec needed) or main task (irreversible, outward-facing, or design-level). If unsure, pick the heavier tier; never lower a tier. Follow .claude/rules/window.md. Ignore system notifications."}}'
exit 0
