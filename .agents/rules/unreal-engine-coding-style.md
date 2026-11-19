---
trigger: glob
description: "Unreal Engine C++ Coding Style"
globs: "Source/**/*.h, Source/**/*.cpp, Source/**/*.cs, Plugins/**/Source/**/*.h, Plugins/**/Source/**/*.cpp, Plugins/**/Source/**/*.cs"
---
# Unreal Engine C++ Coding Style

Source: https://dev.epicgames.com/documentation/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine?lang=ja (Unreal Engine 5.9 documentation, Japanese page, read in full on 2026-11-15). Epic's in-house standard; the page says compliance is required.

## Precedence
- For `Source/**/*.{h,cpp}` this file takes precedence over `.claude/rules/cpp/coding-style.md` (ECC text and the C++ Core Guidelines section). For `Source/**/*.cs` (build scripts such as `*.Build.cs`, `*.Target.cs`) it takes precedence over `.claude/rules/csharp/coding-style.md` (Epic uses tabs in C# too). Both load because `paths` cannot exclude files.

| Topic | C++ Core Guidelines / ECC | Unreal (follow this) |
|---|---|---|
| Naming | `underscore_style` (NL.10) | PascalCase with type prefixes |
| Braces | K&R-derived (NL.17) | Allman (brace on a new line) |
| `auto` | allowed (ES.11); ECC also suggests structured bindings | avoid `auto`; no structured bindings |
| Standard library | prefer it (SL.1, SL.2) | avoid standard containers and strings except in interop code |
Same in both: enumerations use `enum class`.

## Naming
- PascalCase, each word capitalized, usually no underscores; US English spelling in code and comments.
- Type prefixes: `T` templates, `U` UObject-derived, `A` AActor-derived, `S` SWidget-derived, `I` abstract interfaces, `C` concepts, `E` enums, `F` most other classes and structs, `b` for booleans (required). No prefixes in C#. Typedefs take the prefix of the type they alias; template parameters may use an `In` prefix.
- Macros: ALL_CAPS with underscores, starting with `UE_`. Types and variables are nouns; methods are verbs; `bool`-returning functions read as questions (`IsVisible()`); procedures are a verb plus the object; avoid vague verbs (`Handle`, `Process`). Names must be clear, unambiguous and descriptive; avoid heavy abbreviation.
- Output parameters passed by reference use an `Out` prefix (`bOutResult` for `bool`). Declare one variable per line with a documentation comment above it.

## Portability and standard library
- Use size-explicit types (`int32`, `uint8`, `int64`, `float`, `double`); never depend on the size of `int`; use `bool`, not `BOOL`. Use explicit sizes for serialization and replication.
- Standard library use was historically avoided. Allowed with conditions: `<atomic>` (new code), `<type_traits>` (lowercase `value`/`type`), `<initializer_list>` (only for brace initialization), `<regex>` (editor-only code, encapsulated), `<limits>`, `<cmath>`. `memcpy`/`memset` only with a clear performance gain. Do not mix UE and standard idioms in the same API.

## C++ features
- The engine builds with and requires C++20. Use `static_assert`, `override` and `final` (strongly recommended) and `nullptr` (not `NULL`).
- Do not use `auto` except for lambdas stored in variables, iterators and template code; no structured bindings. Prefer range-based `for` (`TMap` yields `TPair` with `Key`/`Value`).
- Lambdas: keep short; explicit captures instead of `[&]`/`[=]`; for deferred execution avoid reference captures and `this` (use `TWeakObjectPtr`); give large lambdas an explicit return type.
- Replace plain enums with `enum class` (works with `UENUM`; exposed Blueprint enums must be `uint8`). Flag enums use `ENUM_CLASS_FLAGS` with `None` = 0.
- `const` on parameters, methods, loop variables and locals, but not on return types (it blocks move). Use `MoveTemp`; by-value sink parameters are an exception to the `const` rule. Default member initializers are allowed but trigger rebuilds and patch limits when headers change, so they suit game code.
- Not stated on the page: rules for exceptions, RTTI, the ternary operator and threading.

## Formatting
- Allman braces; braces even around single statements; align `else if` with `if`. Tabs, width 4 (also in C#); spaces only for alignment.
- `switch`: comment intentional fall-through, always `default`, end cases with `break` or equivalent. Pointer and reference: a space after the symbol (`FShaderType* Ptr`). No space between a function name and `(`. One blank line at the end of the file. The first line of each source file carries the required copyright notice exactly.

## Comments and dependencies
- Prefer self-explanatory code; comments state intent, not implementation; update comments with the code; replace magic numbers with named constants.
- Document with JavaDoc-style comments: classes (problem solved and why), methods once at the public declaration (purpose, parameter units/ranges/invalid values, error meaning). Wrap third-party code in searchable marker comments.
- `#pragma once`; include what you use directly without relying on transitive includes; avoid huge headers such as `Core.h`; forward declarations over includes; no standard-library headers inside headers; file names without prefixes (`Scene.cpp`); `Public`/`Private` folders per module; be careful with `FORCEINLINE`; no heavy `static` variables in headers.

## API design and general rules
- No `bool` parameters (use enum flags); bundle many parameters into a struct; no `bool`/`FString` overloads; interfaces start with `I`, have no data members and are pure virtual; write both `virtual` and `override`; pass UObjects by pointer; members private by default; `final` for classes not meant to be derived. New APIs go in the `UE::` namespace (not for `UCLASS`/`USTRUCT` or macros); no global `using` in headers; implementation details in a `Private` namespace.
- Platform-specific code lives in platform-named subdirectories; avoid scattering `PLATFORM_[PLATFORM]` checks, add static functions to abstraction layers such as `FPlatformMisc`.
- Wrap string literals in `TEXT()`; no variable shadowing; split complex expressions; do not check in debug code; make behavior-neutral mass formatting or renames separate changes; use inclusive terms (allow/deny list, primary/replica).

## Comments, file header and period rule
Follow "Project Rules: Comments and File Header" in `.claude/rules/cpp/coding-style.md` (the C# comment style, the Doxygen file header, and a period at the end of every comment line), with these Unreal specifics:
- The mandatory copyright notice stays on line 1 of every source file (see Formatting). Put the Doxygen file header right after it, before any include.
- Epic's JavaDoc-style documentation comments (`/** */`) at public declarations are Doxygen blocks and stay allowed. They follow the period rule too.
- The period rule does not apply to the copyright notice, which must match exactly.
- For `Source/**/*.cs` build scripts use the C# header form (`//!` lines) from `.claude/rules/csharp/coding-style.md`, with Epic's tabs.

## Initialization
Follow "Project Rules: Initialization" in `.claude/rules/cpp/coding-style.md`: `{}` for default values (`int32 Count{};`), `=` for any other value (`float Speed = 600.0f;`). It applies to `UPROPERTY` members and to default member initializers in headers. Not verified in this repository: that UnrealHeaderTool accepts the brace form on `UPROPERTY` members.

## Gaps filled from the C++ rules
- The Epic page does not state rules for exceptions, RTTI, the ternary operator or threading. The Core Guidelines section in `.claude/rules/cpp/coding-style.md` applies there, except that its error-handling rules (E.*) assume exceptions. Whether exceptions are enabled for a given Unreal module was not verified, so check the module's build settings before using them.
- Other C++ rules in `.claude/rules/cpp/coding-style.md` apply unless the table above or Epic's page contradicts them.
