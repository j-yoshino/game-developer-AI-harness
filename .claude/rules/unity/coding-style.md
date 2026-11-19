---
paths:
  - "Assets/**/*.cs"
---
# Unity C# Coding Style

Source: https://unity.com/ja/how-to/naming-and-code-style-tips-c-scripting-unity (read in full on 2026-11-15). Unity's article builds on Microsoft's conventions and says the best rules are the ones your team agrees on.

## Precedence

- For `Assets/**/*.cs` this file takes precedence over `.claude/rules/csharp/coding-style.md` (ECC text and the .NET section) when they conflict. Both load because `paths` cannot exclude files.
- The article does not cover comments, brace placement or indentation; those gaps are filled from the C# rules (see "Gaps filled from the C# rules" below).

## Identifiers
- Use meaningful names. No Hungarian notation (`iCounter`, `strName`). No special characters, symbols or Unicode in identifiers (can interfere with Unity command-line tools).
- camelCase: local variables and method parameters. PascalCase: classes, public fields, methods. snake_case and kebab-case appear in the article only as options; kebab-case is recommended for USS (UI Toolkit).

## Fields and variables
- Nouns for non-`bool`; `bool` gets a verb prefix (`isDead`, `hasDamageMultiplier`). No abbreviations; one-letter names only in loops and math. Prefer readability over brevity.
- Public fields PascalCase, private fields camelCase (the article's example prefixes private fields with `_`, e.g. `_isDead`). Constants: `k_` prefix + PascalCase. `m_` and `s_` prefixes are shown only as options and are described as uncommon in modern C#.
- Use `this` to separate members from locals. Decide as a team whether to write `private` explicitly (Microsoft recommends explicit); use `protected` if subclasses need access.
- Initialize fields as in "Project Rules: Initialization" in `.claude/rules/csharp/coding-style.md` (`= default` for value types). This is a project rule that differs from the article, which tells you to remove redundant initializers (its stated reason: fields are automatically set to their default values). One variable per line. Do not repeat the class name (`Player.Score`, not `Player.PlayerScore`). No joke names.
- `var`: team decision; the article describes using it only when the type is obvious and avoiding it when the type is unclear or for primitives outside loops.

## Enums, classes, interfaces, methods
- Enums: PascalCase type and members, singular noun, no prefix or suffix; `[Flags]` enums may be plural; public enums may live outside classes.
- Classes: PascalCase noun or noun phrase. A `MonoBehaviour` class lives alone in a file named after the class. Interfaces: capital `I` + adjective (`IKillable`, `IDamageable<T>`).
- Methods: start with a verb (`GetDirection`, `FindTarget`); parameters camelCase; `bool`-returning methods read as questions (`IsGameOver`, `HasStartedTurn`).

## Events
- Verb phrases: present progressive before the change (`OpeningDoor`), past participle after (`DoorOpened`). Prefer `System.Action`; use `EventHandler` only as a team-wide choice.
- Raising methods are prefixed `On` (`OnDoorOpened`) and use `?.Invoke`. Subscriber handlers include the source name (article example: `GameEvents_DoorOpened`). Custom `EventArgs` only when needed (derive from `System.EventArgs` or use a read-only struct).

## Namespaces
- PascalCase, no symbols or underscores, dot-separated hierarchy (`MyApplication.AI`), matching the folder structure. Use `using` directives at the top of the file. Qualify with a prefix when the same class name exists in several namespaces.

## Coverage
The whole article was read. This repository has no Unity project yet, so the `Assets/` layout is an assumption about the standard structure.

## Gaps filled from the C# rules
The Unity article is silent on these. They come from `.claude/rules/csharp/coding-style.md` (the .NET conventions and the project rules) and apply as written there:
- Formatting: 4 spaces and no tabs, Allman braces, one statement and one declaration per line, a blank line between method and property definitions.
- `var`: the article leaves it to the team; use `var` only when the type is obvious from the right-hand side.
- Comments, file header and period rule: see "Project Rules: Comments and File Header" in `.claude/rules/csharp/coding-style.md`. In short: `//` comments on their own line, a Doxygen file header written as `//!` lines, and every comment line ends with a period.
