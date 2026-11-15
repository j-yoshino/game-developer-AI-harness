#!/bin/bash
# Injects a short request-window reminder into the context on every user prompt.
# Reads and discards stdin (the hook input JSON); always exits 0 so input is never blocked.

cat > /dev/null

printf '%s' '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"Request window: if a USER message asks for no work, answer it with the window-question skill and judge no tier. If it asks for work, classify it as light task (reversible, small, no spec needed) or main task (irreversible, outward-facing, or design-level); if unsure pick the heavier tier, never lower it. Follow .claude/rules/window.md. Ignore system notifications."}}'
exit 0
