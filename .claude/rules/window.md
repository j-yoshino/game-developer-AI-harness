# Request Window

Every user message passes through the window first. A message that asks for no work (a question) is answered with the `window-question` skill; no tier is judged for it. A message that asks for work is judged as a light task or a main task, which decides how much procedure it needs. A hook reminds you of this on every turn.

## Tiers

| Tier | Condition |
|---|---|
| Light task | Reversible, small, and not worth a spec (a bug fix, a small change). |
| Main task | Irreversible, outward-facing, or the decision reaches design. Includes new implementation. |

## Judging the tier

Judge on two axes:

- Can it be undone? Does it include an outward-facing operation (publish, send, push, merge)?
- Is there a branch in the decision, where several options are valid?

Rules:

- Judge only requests for work from the user. Questions get no tier. Ignore system notifications (background-task results and similar).
- If unsure, choose the heavier tier.
- Never lower a tier. If a light task turns out to need an irreversible operation, raise it to a main task and tell the user.
- A message that mixes a question and a request for work is handled at the work tier.

## Verification

After the delivery note is written, and when verification is required (see the routes below), call the `window-verifier` agent before reporting the note.

1. Call it with the `Agent` tool, `subagent_type: window-verifier`.
2. In the delegation message, paste, as separate sections: the user's original words (not summarized), the request form (main task) or the "what I understood" and "what will not be done" text from the note's request field (light task), the full text of the delivery note, the list of changed files (`git diff --name-only` plus `git ls-files --others --exclude-standard`), the tier, and the verification round. The verifier cannot see this conversation.
3. Do not put your own verdict or hints in the message (such as "this is fine" or "check this part").
4. Append the verifier's report to the end of the delivery note, in the last section, which the template reserves for the verifier's report, in full and unedited.
5. If the verdict is approve, report the note as awaiting confirmation. The user approves.
6. If the verdict is "needs fixes", fix the work, update the note, and call the verifier again, at most 2 times. Do not write the previous verdict in the new message. If the third round still needs fixes, do not stop: keep the unresolved findings in the report section and report the note as awaiting confirmation.
7. If the verdict is "undecidable", do not count it as a round: report it as is.

## Routes

### Question (no tier)

Call the `window-question` skill by name. Do not judge a tier, and do not produce a request form, a delivery note, or a tier announcement. Answer first, and show evidence (`path:line`, URL, command output) only where it helps the user act. If answering turns out to require changing files or state, treat it as a request for work and judge its tier then.

### Light task

- Use brainstorming only to size the work and ask what is missing. Do not write a design doc, and do not go on to `writing-plans`.
- Do the work in the main conversation. Use `systematic-debugging` for bugs, `test-driven-development` where tests apply, and `verification-before-completion` before claiming anything is done.
- When finished, write a delivery note to `docs/納品書/<YYYY-MM-DD>-<title>.md` from `docs/納品書/_template.md`. It has one section per item you confirmed with the user (your understanding and what you will not do), each with three fields: what was done, how it was verified (steps, not just "verified"), and what was not verified. The last field is never left empty; if nothing applies, write the Japanese word for "none" that the template specifies.
- In the note's request field, write your understanding and what will not be done in full.
- Verify only when the diff (`git diff --name-only` plus `git ls-files --others --exclude-standard`) contains a source file (`.cpp` `.hpp` `.cc` `.hh` `.cxx` `.h` `.cs` `.rs`) or a test file (under `tests/` or `Tests/`, or a file name containing `Test` or `_test`). Then follow the Verification section. If the change is only documentation, rules, settings, or HTML, do not call the verifier; write one line in the note's last section saying verification was not required and why, in the form the template shows. When unsure, verify.
- After verification (when required), report the note as awaiting confirmation (the status value the template sets). Do not say the work is complete. The user approves the note.
- If you added work the user did not ask for, list it under the note's "added items" section.

### Raising the tier

- Outward-facing operations (push, opening a pull request, merging) make the request a main task: confirm with the user first.
- Committing locally, documentation-only changes, and editing rules or settings files are light tasks.
- If a light task turns out to need an irreversible operation, raise it to a main task and tell the user. Never lower a tier.

### Main task (new implementation)

- Start with brainstorming, then `/speckit-specify`. The spec begins with a request form of five fields: the user's words quoted verbatim (never summarized), your understanding, who it is for, what will not be done, and the completion criteria.
- Ask only about fields that are still empty, with `AskUserQuestion`, in the form of options. Use free text only for facts that only the user has.
- Do not move on to the plan or any implementation until the user has agreed to the "will not do" and "completion criteria" fields.
- When implementation is finished, write a delivery note to `docs/納品書/<NNN-feature>.md` (the same name as `specs/<NNN-feature>/`) from `docs/納品書/_template.md`, with one section per completion criterion. Follow the same rules as for a light task: three fields per section, the last never empty. In the "how it was verified" field, paste the command and its output (the key lines).
- Always follow the Verification section before reporting the note. Then report it as awaiting confirmation, never as complete.
