---
trigger: glob
description: "Unreal Engine Testing"
globs: "Source/**/*.h, Source/**/*.cpp, Source/**/*.cs, Plugins/**/Source/**/*.h, Plugins/**/Source/**/*.cpp, Plugins/**/Source/**/*.cs"
---
<!-- generated from .claude/rules/unreal-engine/testing.md. Do not edit; run scripts/sync-agent-env.py. -->
# Unreal Engine Testing

> This file extends [common/testing.md](../common/testing.md) with Unreal Engine specific content.

Sources (read on 2026-11-15):
- https://dev.epicgames.com/documentation/unreal-engine/write-cplusplus-tests-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/running-gauntlet-tests-in-unreal-engine

## Writing C++ automation tests
- Simple Test: one atomic test; declare with `IMPLEMENT_SIMPLE_AUTOMATION_TEST(TClass, PrettyName, TFlags)` and implement `RunTest` (`GetTests` is generated).
- Complex Test: the same code over many inputs (for example loading every map); declare with `IMPLEMENT_COMPLEX_AUTOMATION_TEST` and implement both `RunTest` and `GetTests`.
- Latent commands spread work over several frames: `DEFINE_LATENT_AUTOMATION_COMMAND` (or `..._ONE_PARAMETER`), whose `Update` returns `true` when finished; queue with `ADD_LATENT_AUTOMATION_COMMAND`.
- `PrettyName` is a dotted hierarchy ("Group.Subgroup.Test"). `TFlags` is a combination of `EAutomationTestFlags` (the page's examples use `EditorContext`, `EngineFilter`, `ATF_Game`; their meanings are not described there). A test passes or fails through the bool returned by `RunTest`.
- Put test sources in the module's `Private/Tests` folder; a test for one class is named `[ClassFilename]Test.cpp`.
- Not covered by the pages read: assertion helpers such as `TestTrue`/`TestEqual`, Spec and functional tests, and the flag meanings.

## Running tests
- Editor: enable the Functional Testing Editor and the plugins that contain the tests, restart, then **Tools > Test Automation**; select tests in the Automation tab of the Session Frontend and click **Start Tests**. The Session Frontend can also drive other running Editor/Client instances (network tests); tests can be marked client-only.
- Command line (Editor or Client executable):
```bash
-ExecCmds="Automation RunTest Test1+Test2;Quit"
-ExecCmds="Automation RunTest MySet.MySubSet;Quit"
-ExecCmds="Automation RunTest Group:MyGroup;Quit"
-ReportExportPath="<output path>"   # JSON plus HTML report files
-ResumeRunTest                      # with -ReportExportPath: resume at the first not-run test; in-progress tests count as failures
```
- CI with Gauntlet (`RunUAT.bat RunUnreal`): `-test=UE.EditorAutomation` (Editor) or `UE.TargetAutomation` (client/packaged game), `-runtest=<test>`, `-project=<.uproject>`, `-build=editor|<packaged path>`, optional `-platform`, `-device`, `-configuration`. `-ResumeOnCriticalFailure` lets UE.Automation resume after a crash, up to three times. The page does not say where results are stored.
- The pages read do not cover `-unattended`, `-NullRHI`, `-nosplash` or `-testexit`. Some community sources use `RunTests`; the official page uses `RunTest`.

## From the C++ testing rules
- `.claude/rules/cpp/testing.md` assumes GoogleTest, CMake/CTest and lcov. The Unreal pages read use the Automation framework instead, so those commands do not apply here.
- Name tests by behavior within the `Group.Subgroup.Test` hierarchy of `PrettyName`.
- Not verified for Unreal: coverage tooling and the AddressSanitizer/UBSan setup suggested in `cpp/testing.md`.
