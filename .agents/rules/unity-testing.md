---
trigger: glob
description: "Unity Testing"
globs: "Assets/**/*.cs, Assets/**/*.asmdef"
---
<!-- generated from .claude/rules/unity/testing.md. Do not edit; run scripts/sync-agent-env.py. -->
# Unity Testing

> This file extends [common/testing.md](../common/testing.md) with Unity specific content.

Sources (read on 2026-11-15):
- https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/index.html and `.../reference-command-line.html` (the page text itself refers to v1.3.x for the limitations)
- https://docs.unity.com/en-us/engine/current/manual/unity-editor/command-line-arguments/editor

## Framework
- Unity Test Framework (package `com.unity.test-framework`, formerly Unity Test Runner): NUnit-based (NUnit 3.5 per the page), tests in Edit Mode and Play Mode, and on target platforms (Standalone, Android, iOS, ...). Included with Unity 2019.2 and later projects.
- Known limitations listed for v1.3.x: `UnityTest` is not supported on WSA, does not support parameterized tests except `ValueSource`, and does not support NUnit `Repeat`; nested test fixtures cannot be run from the Editor UI; NUnit `Retry` in Play Mode throws `InvalidCastException`.
- Not covered by the pages read: how to write `[Test]`/`[UnityTest]`/`[SetUp]` tests, how to create test assemblies (asmdef), and the Test Runner window.

## Running tests from the command line
```bash
Unity -runTests -batchmode -projectPath <path> -testPlatform EditMode -testResults results.xml
```
- `-testPlatform`: `EditMode` (default when omitted), `PlayMode` (inside the Editor), or any `BuildTarget` value to run in a built player. `-testResults`: NUnit XML, defaults to the project root.
- Filters: `-testFilter` (name or full-name regex; `;`-separated in quotes; `!` negates), `-testCategory`, `-assemblyNames`. Using `-testFilter` with `-testCategory` runs only tests matching both.
- Other options: `-runSynchronously` (Edit Mode only; multi-frame tests such as `[UnityTest]` are excluded), `-testSettingsFile`, `-orderedTestListFile`, `-randomOrderSeed`, `-retry`, `-repeat`, `-playerHeartbeatTimeout` (default 10 minutes), `-forgetProjectPath`.
- Do not add `-quit` to a `-runTests` command: while tests are running it makes the Editor exit immediately without waiting for them (and it can hang an application that is running async code). The default wait for async tasks is 300 seconds (`-quitTimeout` changes it, in seconds).
- A project that is already open in another Editor cannot be opened in batch mode.
- Exit codes: Unity components report no common exit-code definition (read the error messages and stack traces); in `-batchmode`, an exception, a failed asset-server update or another failure exits with code 1. The success exit code is not stated.

## Filled from the C# testing rules
From `.claude/rules/csharp/testing.md` (generic C#; not Unity-specific):
- Name tests by behavior, not by implementation detail (for example `FindById_ReturnsOrder_WhenOrderExists`).
- Structure each test as Arrange, Act, Assert, and keep unit-level and integration-level tests clearly separated.
- Coverage target of 80% or more line coverage. Not verified: which coverage tooling Unity projects should use (none of the Unity pages read cover it).
- Not applicable as written: xUnit, FluentAssertions, Moq/NSubstitute, Testcontainers and `WebApplicationFactory` are .NET server-side choices; the Unity Test Framework is NUnit-based (official page). Whether the other libraries work inside Unity was not checked.
