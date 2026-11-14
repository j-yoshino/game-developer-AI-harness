---
paths:
  - "**/*.cs"
  - "**/*.csx"
---
# C# Coding Style

> This file extends [common/coding-style.md](../common/coding-style.md) with C#-specific content.

## Standards

- Follow current .NET conventions and enable nullable reference types
- Prefer explicit access modifiers on public and internal APIs
- Keep files aligned with the primary type they define

## Types and Models

- Prefer `record` or `record struct` for immutable value-like models
- Use `class` for entities or types with identity and lifecycle
- Use `interface` for service boundaries and abstractions
- Avoid `dynamic` in application code; prefer generics or explicit models

```csharp
public sealed record UserDto(Guid Id, string Email);

public interface IUserRepository
{
    Task<UserDto?> FindByIdAsync(Guid id, CancellationToken cancellationToken);
}
```

## Immutability

- Prefer `init` setters, constructor parameters, and immutable collections for shared state
- Do not mutate input models in-place when producing updated state

```csharp
public sealed record UserProfile(string Name, string Email);

public static UserProfile Rename(UserProfile profile, string name) =>
    profile with { Name = name };
```

## Async and Error Handling

- Prefer `async`/`await` over blocking calls like `.Result` or `.Wait()`
- Pass `CancellationToken` through public async APIs
- Throw specific exceptions and log with structured properties

```csharp
public async Task<Order> LoadOrderAsync(
    Guid orderId,
    CancellationToken cancellationToken)
{
    try
    {
        return await repository.FindAsync(orderId, cancellationToken)
            ?? throw new InvalidOperationException($"Order {orderId} was not found.");
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "Failed to load order {OrderId}", orderId);
        throw;
    }
}
```

## Formatting

- Use `dotnet format` for formatting and analyzer fixes
- Keep `using` directives organized and remove unused imports
- Prefer expression-bodied members only when they stay readable

## Project Conventions: .NET C# Coding Conventions

Source: https://learn.microsoft.com/ja-jp/dotnet/csharp/fundamentals/coding-style/coding-conventions (Japanese machine-translated page, read in full on 2026-11-15, updated 2026-10-04). These are the conventions the `dotnet/docs` team uses for its samples; the page itself calls them examples of common C# conventions, not an authoritative list. This section takes precedence over the generic ECC text above. Under `Assets/` (Unity) `.claude/rules/unity/coding-style.md` takes precedence; for Unreal build scripts under `Source/` `.claude/rules/unreal-engine/coding-style.md` takes precedence (tabs).

### Language guidelines
- Use current C# features and versions; avoid outdated constructs. Catch only exceptions you can handle; never catch bare `Exception` without a filter; use specific exception types with meaningful messages.
- LINQ for collection work; `async`/`await` for I/O (watch for deadlocks, use `ConfigureAwait` when needed).
- Use language keywords for types (`string`, `int`), not runtime types. Use `int` rather than unsigned types unless the unsigned type is the point.
- `var` only when the type is obvious from the right-hand side (`new`, explicit cast, literal); never infer from a method name; do not name a variable after its type. Use `var` in `for` loops and for LINQ query results; use explicit types in `foreach`. Use `dynamic` only when run-time typing is needed, never as a `var` replacement.
- Strings: interpolation (`$"..."`, expression-based, not positional) for short concatenation; `StringBuilder` when appending in loops; raw string literals (`"""`) over escapes and verbatim strings.
- Constructors: `record` primary-constructor parameters are PascalCase; `class`/`struct` primary-constructor parameters are camelCase; use `required` properties instead of constructors to force initialization.
- Collections: initialize with collection expressions (`[ ... ]`). Delegates: `Func<>`/`Action<>` instead of custom delegate types; short syntax when instantiating delegates.
- Resources: replace `try`/`finally` that only calls `Dispose` with `using`; prefer the brace-less `using` declaration. Event handlers that need no removal: lambda expressions.
- Objects: `var x = new X();` or `X x = new();` when the variable type equals the object type; use object initializers. Call static members through the declaring class name, not a derived class.
- LINQ: meaningful query-variable names; PascalCase property names in anonymous types; rename ambiguous properties; `where` before other clauses; multiple `from` clauses instead of `join` for inner collections.
- Namespaces: file-scoped (`namespace X;`); put `using` directives outside the namespace declaration. Follow the secure coding guidelines.
- The `&&`/`||` section of the Japanese page contradicts its own code sample; it is not summarized here.

### Style
- 4 spaces, no tabs; Allman braces (each brace on its own line); one statement and one declaration per line; at least one blank line between method and property definitions; parentheses to clarify expression precedence; continuation lines indented 4 spaces; break long statements, with line breaks before binary operators.
- Comments: `//` for short notes, avoid `/* */`; XML doc comments for methods, classes, fields and all public members; comment on its own line, starting with a capital letter and ending with a period, one space after `//`.
- The 65-character line limit is for documentation display and does not apply to this project; follow `.editorconfig`.
- Naming rules for classes, methods and fields are not covered by this page; follow `.editorconfig` and existing code.
- The page recommends enforcing conventions with `.editorconfig` and code analysis; neither is set up in this repository yet.
