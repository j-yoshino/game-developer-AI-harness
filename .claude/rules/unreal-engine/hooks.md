---
paths:
  - "Source/**/*.{h,cpp,cs}"
  - "Plugins/**/Source/**/*.{h,cpp,cs}"
---
# Unreal Engine Hooks

> This file extends [common/hooks.md](../common/hooks.md) with Unreal Engine specific content.

Sources (read on 2026-11-15):
- https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-build-tool-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/running-gauntlet-tests-in-unreal-engine

## Build system facts
- UnrealBuildTool (UBT) builds the engine and projects across configurations. Each module has a `.build.cs` that controls module dependencies, extra libraries and include paths; modules compile into DLLs loaded by one executable by default. `BuildConfiguration.cs` holds user-configurable options (for example a monolithic executable).
- The build runs independently of IDE project files; `GenerateProject.bat` in the engine root regenerates `.sln`/`.vcproj` files and should be re-run when source files are added or removed.
- Not covered by the pages read: `.Target.cs`, UBT command-line examples (`Build.bat`, `RunUBT`), and how UBT relates to the `.uproject`. Do not invent UBT command lines; check the Targets and Unreal Automation Tool pages for the engine version in use.

## Checks before committing (examples built from documented commands)
```bash
# Automation tests from the Editor binary
<Editor executable> <project>.uproject -ExecCmds="Automation RunTest Group:MyGroup;Quit" -ReportExportPath="Saved/AutomationReports"
# CI wrapper (Gauntlet)
RunUAT.bat RunUnreal -test=UE.EditorAutomation -runtest=MyTest.One -project=<path to .uproject> -build=editor
```
These commands are assembled from the pages listed above and have **not been run** in this repository (no Unreal project exists yet; `Group:MyGroup`, `MyTest.One` and the Editor executable name are placeholders).

## Not covered
No official page read documents a C++ formatter or linter command for Claude Code `PostToolUse` hooks. Epic's standard (see `coding-style.md`) is not enforced by a documented tool in the pages read.
