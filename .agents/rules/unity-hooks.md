---
trigger: glob
description: "Unity Hooks"
globs: "Assets/**/*.cs"
---
# Unity Hooks

> This file extends [common/hooks.md](../common/hooks.md) with Unity specific content.

Source (read on 2026-11-15): https://docs.unity.com/en-us/engine/current/manual/unity-editor/command-line-arguments/editor (plus the Test Framework command-line page; see `testing.md`).

## Editor command-line arguments for automation
| Argument | Meaning (per the page) |
|---|---|
| `-batchmode` | Runs without user interaction; suppresses dialogs; minimal console output (full log in the log file). A project already open in another Editor cannot be opened. |
| `-quit` | Quits after the other commands finish. Not for use with `-runTests` (it exits without waiting for tests). |
| `-nographics` | Does not initialize a GPU device (no GI baking). Disables log output, so combine with `-logFile`. |
| `-projectPath <path>` | Opens the project at the path (absolute or relative; quote paths with spaces). |
| `-logFile <path>` | Editor log destination; `-` writes to the console. |
| `-executeMethod Class.Method` | Runs a static method after the project opens (after the asset server update); the script must be in an `Editor` folder; arguments via `System.Environment.GetCommandLineArgs`. |
| `-buildTarget <name>` | Selects the active build target (`win64`, `android`, `ios`, `linux64`, `osxuniversal`, `webgl`, ...). |
| `-silent-crashes` | Suppresses the crash dialog of a Standalone Player in automated builds and tests. |

Exit codes: in `-batchmode`, a script exception, a failed asset-server update or another failure exits with code 1. With `-executeMethod`, an exception exits with 1, and `EditorApplication.Exit` with a non-zero code returns a custom code. The page does not state the success code or how `-quit` and `-executeMethod` interact on exit.

## Checks before committing (examples built from the arguments above)
```bash
# Edit Mode tests
Unity -runTests -batchmode -projectPath . -testPlatform EditMode -testResults results.xml -logFile -
# Custom build/validation entry point
Unity -batchmode -quit -projectPath . -executeMethod BuildScripts.Validate -logFile -
```
These commands are assembled from documented arguments and have **not been run** in this repository (no Unity project exists yet; `BuildScripts.Validate` is a placeholder).

## Not covered
No official Unity page read here documents a formatter or linter command for Claude Code `PostToolUse` hooks. Use whichever `.editorconfig`/analyzer setup the project adopts.

## From the C# hooks
`.claude/rules/csharp/hooks.md` suggests `dotnet format`, `dotnet build` and `dotnet test --no-build` as `PostToolUse` hooks. Whether these work on Unity-generated projects was not verified, so do not rely on them; use the Unity batch-mode commands above.
