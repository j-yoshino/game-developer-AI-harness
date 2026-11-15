# Request Window

Every user message passes through the window first. The window decides how much procedure the request needs, routes it, and reports the result. A hook reminds you of this on every turn.

## Tiers

| Tier | Condition |
|---|---|
| Question | No work. Nothing in files or state changes. |
| Light task | Reversible, small, and not worth a spec (a bug fix, a small change). |
| Main task | Irreversible, outward-facing, or the decision reaches design. Includes new implementation. |

## Judging the tier

Judge on two axes:

- Can it be undone? Does it include an outward-facing operation (publish, send, push, merge)?
- Is there a branch in the decision, where several options are valid?

Rules:

- Judge only the user's messages. Ignore system notifications (background-task results and similar).
- If unsure, choose the heavier tier.
- Never lower a tier. If a light task turns out to need an irreversible operation, raise it to a main task and tell the user.
- A message that mixes a question and a request for work is handled at the work tier.

## Routes

### Question

Call the `window-question` skill by name. Do not produce a request form, a delivery note, or a tier announcement. Answer first, and show evidence (`path:line`, URL, command output) only where it helps the user act. If answering turns out to require changing files or state, raise the tier and tell the user.

### Light task

- Use brainstorming only to size the work and ask what is missing. Do not write a design doc, and do not go on to `writing-plans`.
- Do the work in the main conversation. Use `systematic-debugging` for bugs, `test-driven-development` where tests apply, and `verification-before-completion` before claiming anything is done.
- When finished, write a delivery note to `docs/納品書/<YYYY-MM-DD>-<title>.md` from `docs/納品書/_template.md`. It has one section per item you confirmed with the user (your understanding and what you will not do), each with three fields: what was done, how it was verified (steps, not just "verified"), and what was not verified. The last field is never left empty; if nothing applies, write the Japanese word for "none" that the template specifies.
- Report the note as awaiting confirmation (the status value the template sets). Do not say the work is complete. The user approves the note.
- If you added work the user did not ask for, list it under the note's "added items" section.

### Raising the tier

- Outward-facing operations (push, opening a pull request, merging) make the request a main task: confirm with the user first.
- Committing locally, documentation-only changes, and editing rules or settings files are light tasks.
- If a light task turns out to need an irreversible operation, raise it to a main task and tell the user. Never lower a tier.

### Main task (new implementation)

- Start with brainstorming, then `/speckit-specify`. The spec begins with a request form of five fields: the user's words quoted verbatim (never summarized), your understanding, who it is for, what will not be done, and the completion criteria.
- Ask only about fields that are still empty, with `AskUserQuestion`, in the form of options. Use free text only for facts that only the user has.
- Do not move on to the plan or any implementation until the user has agreed to the "will not do" and "completion criteria" fields.
- When implementation is finished, write a delivery note to `docs/納品書/<NNN-feature>.md` (the same name as `specs/<NNN-feature>/`) from `docs/納品書/_template.md`, with one section per completion criterion. Follow the same rules as for a light task: three fields per section, the last never empty, reported as awaiting confirmation, never as complete.
