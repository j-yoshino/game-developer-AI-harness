---
trigger: glob
description: "C++ Coding Style"
globs: "**/*.cpp, **/*.hpp, **/*.cc, **/*.hh, **/*.cxx, **/*.h, **/CMakeLists.txt"
---
# C++ Coding Style

> This file extends [common/coding-style.md](../common/coding-style.md) with C++ specific content.

## Modern C++ (C++17/20/23)

- Prefer **modern C++ features** over C-style constructs
- Use `auto` when the type is obvious from context
- Use `constexpr` for compile-time constants
- Use structured bindings: `auto [key, value] = map_entry;`

## Resource Management

- **RAII everywhere** — no manual `new`/`delete`
- Use `std::unique_ptr` for exclusive ownership
- Use `std::shared_ptr` only when shared ownership is truly needed
- Use `std::make_unique` / `std::make_shared` over raw `new`

## Naming Conventions

- Types/Classes: `PascalCase`
- Functions/Methods: `snake_case` or `camelCase` (follow project convention)
- Constants: `kPascalCase` or `UPPER_SNAKE_CASE`
- Namespaces: `lowercase`
- Member variables: `snake_case_` (trailing underscore) or `m_` prefix

## Formatting

- Use **clang-format** — no style debates
- Run `clang-format -i <file>` before committing

## Reference

See skill: `cpp-coding-standards` for comprehensive C++ coding standards and guidelines.

## Project Conventions: C++ Core Guidelines

Source: https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines (read in full on 2026-11-15; IDs below are upstream rule IDs). This section takes precedence over the generic ECC text above. In Unreal Engine code under `Source/`, `.claude/rules/unreal-engine/coding-style.md` takes precedence over this section.

### Philosophy and interfaces (P, I)
- P.1-P.3: express intent in code, write ISO standard C++, state intent through names, types and algorithms. P.4-P.7: static type safety; compile-time checks over run-time checks; detect run-time errors early. P.8-P.9: no leaks, no waste. P.10: prefer immutable data. P.11: encapsulate messy low-level code. P.12-P.13: use analyzers and good libraries.
- I.1-I.4: explicit, strongly typed interfaces; no non-const globals (I.2); avoid singletons (I.3). I.5-I.8: state pre/postconditions (`Expects()`/`Ensures()`). I.9: constrain template parameters with concepts. I.10: signal failure with exceptions. I.11-I.13: never transfer ownership via raw pointer or reference; `not_null` for non-null pointers; pass arrays as `span`. I.22: avoid complex global initialization. I.23-I.24: few parameters, no adjacent same-type parameters. I.25-I.27, I.30: abstract-class interfaces; C-style subset or Pimpl for ABI; contain rule violations inside implementations.

### Functions (F)
- F.1-F.3: name meaningful operations; one logical operation per function; keep functions short. F.4-F.6: `constexpr` where compile-time evaluation is needed; `inline` only for tiny hot functions; `noexcept` when the function cannot throw. F.7: take `T*`/`T&`, not smart pointers, unless ownership matters. F.8-F.11: prefer pure functions; unnamed unused parameters; name reusable operations; unnamed lambda for one-off use.
- Parameters F.15-F.21: cheap-to-copy "in" by value, others by `const&`; "in-out" by non-const `&`; "will move from" by `X&&` + `std::move`; "forward" by `TP&&` + `std::forward`; return values over out-parameters; return a named struct for multiple outputs. F.60: `T*` when "no argument" is valid, else `T&`. F.22-F.27: `T*`/`owner<T*>` for one object, `not_null<T>`, `span<T>`, `zstring`, `unique_ptr` to transfer ownership, `shared_ptr` to share.
- Returns F.42-F.49: `T*` only for a position, never ownership; never return pointers/references to locals (F.43); do not return `T&&`, `std::move(local)` or `const T`; `main` returns `int`; assignment returns `T&`. F.50-F.56: lambda when a function will not do; default arguments over overloads; capture by reference for local lambdas, by value for non-local (F.52-F.53); no `[=]` with `this` (F.54); no `va_arg` (F.55); early returns to avoid nesting (F.56).

### Classes (C)
- C.1-C.9: group related data; `class` for invariants, `struct` when members vary independently; member function only if it needs the representation; helpers in the same namespace; minimize exposure; `class` if any member is non-public; no type definition and variable in one statement.
- C.10-C.13: prefer concrete types; make them regular; no `const`/reference members in copyable or movable types; declare members in dependency order.
- Default operations: C.20 rule of zero; C.21 define or delete all of copy/move/destructor together; C.22 consistent semantics. Destructors C.30-C.37: define only when needed; release all resources; handle owning raw members; base destructor `public virtual` or `protected` non-virtual; must not fail; `noexcept`.
- Constructors C.40-C.52: constructor for invariants; fully initialized objects; throw if a valid object cannot be built; copyable classes get a default constructor; simple non-throwing default constructors; default member initializers; `explicit` single-argument constructors; initialize in declaration order; initialization over assignment; factory for virtual behavior during initialization; delegating and inheriting constructors.
- Copy/move C.60-C.67: non-virtual `operator=` taking `const&`/`&&`, returning `&`; copy copies, move moves and leaves a valid source; self-assignment safe; move operations `noexcept`; polymorphic classes suppress public copy/move. Other C.80-C.90: `=default`/`=delete` explicitly; no virtual calls in constructors/destructors (C.82); `noexcept` `swap` (C.83-C.85); symmetric `noexcept` `==` (C.86), careful with `==` on bases (C.87); `noexcept` hash (C.89); no `memset`/`memcpy` on non-trivially-copyable types (C.90).
- Containers C.100-C.109: follow the STL; value semantics, move operations, initializer-list constructor, empty default constructor; `*` and `->` for pointer-like handles.
- Hierarchies C.120-C.153: hierarchies only for inherently hierarchical concepts; interfaces are pure abstract classes without data; exactly one of `virtual`/`override`/`final` (C.128); distinguish interface from implementation inheritance; avoid trivial getters/setters, unnecessary `virtual`, `protected` data and mixed access levels (C.131-C.134); `final` sparingly (C.139); no different default arguments on overriders (C.140); polymorphic objects through pointer/reference to avoid slicing (C.145); `dynamic_cast` only when navigation is unavoidable (C.146-C.148); no naked `new`/`delete` (C.149-C.151); never convert derived-class arrays to base pointers (C.152); prefer virtual calls over casts (C.153).
- Overloading C.160-C.170: operators keep conventional meaning; non-member for symmetric operators; overload only roughly equivalent operations; avoid implicit conversion operators; `using` declarations for customization points such as `swap`; define operators in the operands' namespace. Unions C.180-C.183: only to save memory for never-simultaneous alternatives; prefer `variant` or tagged unions; no type punning.

### Enumerations and resources (Enum, R)
- Enum.1-Enum.8: enumerations over macros; `enum class`; define operations for them; no `ALL_CAPS` enumerators; avoid unnamed enums; specify underlying type and values only when necessary.
- R.1-R.6: RAII for every resource; raw pointers and references are non-owning; raw pointers in interfaces only for single objects (arrays use `span`); prefer scoped objects; avoid non-const globals. R.10-R.15: no `malloc`/`free`; no explicit `new`/`delete`; give allocations to a manager immediately; one allocation per statement; no `[]` parameters; overload allocation and deallocation as a pair.
- Smart pointers R.20-R.37: `unique_ptr`/`shared_ptr` express ownership; prefer `unique_ptr`; `make_shared`/`make_unique`; `weak_ptr` to break cycles; take smart pointers as parameters only to express lifetime semantics (by value to take or share ownership, `&` to reseat); do not pass pointers/references obtained from an aliased smart pointer.

### Expressions and statements (ES)
- Declarations ES.1-ES.12: prefer the standard library and suitable abstractions; no duplication; small scopes; declare in `for`/`if` initializers; short local names, longer non-local names; avoid similar-looking names and `ALL_CAPS` (except macros); one name per declaration; `auto` to avoid repeating type names; no name reuse in nested scopes.
- Initialization ES.20-ES.28: always initialize; declare near first use and only with a value; prefer `{}`; `unique_ptr` for owning pointers; `const`/`constexpr` by default; one purpose per variable; `std::array` instead of stack C arrays; lambdas for complex initialization.
- Macros and expressions ES.30-ES.34, ES.40-ES.50: no macros for constants or functions; if unavoidable, unique `ALL_CAPS` names; no C variadics; avoid complicated expressions, parenthesize when unsure; simple pointer use (prefer `span`); no undefined evaluation order; no magic numbers; no lossy conversions; `nullptr`; avoid casts, use named casts, never cast away `const`.
- ES.55-ES.65: avoid the need for range checks; `std::move` only to hand over to another scope; no naked `new`/`delete`; `delete[]` for arrays; do not compare pointers into different arrays; do not slice; use `T{e}`; never dereference invalid pointers.
- Statements ES.70-ES.87: `switch` over `if` chains on constants; range-`for` for sequences; `for` with an obvious loop variable, `while` otherwise; avoid `do`, `goto`, and heavy `break`/`continue`; no implicit fall-through (`[[fallthrough]]`); `default` only for common cases; no unnamed guard objects (ES.84); visible empty statements; do not modify loop variables in the body; no redundant `== true`/`!= nullptr`.
- Arithmetic ES.100-ES.107: do not mix signed and unsigned; unsigned for bit manipulation only; signed for arithmetic; no overflow, underflow or integer division by zero; do not use `unsigned` to avoid negatives or for subscripts (use `gsl::index`).

### Performance, concurrency, errors, constants (Per, CP, E, Con)
- Per.1-Per.7: do not optimize without reason, early, or in non-critical code; complex or low-level code is not automatically faster; measure; design interfaces that allow later optimization. Per.10-Per.19: rely on the type system; compute at compile time (`constexpr`); compact data and predictable memory access matter most. Per.12-Per.15, Per.17, Per.30 are empty upstream.
- CP.1-CP.9: assume code runs multi-threaded; no data races; minimize shared writable data; think in tasks; never `volatile` for synchronization; validate with tools. CP.20-CP.26: RAII locks only; acquire several mutexes together (`scoped_lock`); no unknown code under a lock; prefer `jthread`; never `detach()`. CP.31-CP.32, CP.40-CP.44: pass small data by value; `shared_ptr` across unrelated threads; minimize context switches, thread creation and critical sections; condition-variable waits need a predicate; name your lock objects. CP.50-CP.53: keep the mutex with its data; no capturing lambdas as coroutines; no locks across suspension points; coroutine parameters by value. CP.60-CP.61: `future`/`async()` for task results. CP.100-CP.111, CP.200: avoid lock-free code unless required; no hand-written double-checked locking (`call_once`, function-local static); `volatile` only for non-C++ memory.
- E.1-E.8: design the error strategy early; throw when a function cannot do its job; exceptions only for errors; constructors establish invariants; RAII prevents leaks; state pre/postconditions. E.12-E.19: `noexcept` when throwing is impossible; never throw while directly owning a resource; throw user-defined types by value, catch by reference; destructors, deallocation, `swap` never fail; do not catch everything everywhere; minimize `try`/`catch`; `final_action` for cleanup without a handle. E.25-E.28: without exceptions, simulate RAII, fail fast, use error codes systematically, avoid global error state. E.30-E.31: no exception specifications; order `catch` clauses correctly.
- Con.1-Con.5: objects immutable by default; member functions `const` unless they change observable state; pointers and references to `const` by default; `const` for objects that do not change after construction; `constexpr` for compile-time values.

### Templates, C, source files, library (T, CPL, SF, SL)
- T.1-T.5, T.10-T.13: use templates to raise abstraction; constrain every template argument with concepts, preferring standard concepts and concept names over `auto`. T.20-T.26: concepts need meaningful semantics, a complete set of operations, axioms, and use-pattern definitions; avoid complementary constraints. T.40-T.49: function objects for algorithm operations; require only essential properties; alias templates; `using` over `typedef`; avoid highly visible unconstrained templates and type erasure where possible. T.60-T.69: minimize context dependencies; put non-dependent members in a non-templated base; specialization or tag dispatch for alternatives; `{}` over `()`; no unqualified calls unless intended as customization points. T.80-T.84: do not naively templatize hierarchies or mix hierarchies with arrays; no virtual member templates; non-template core for a stable ABI. T.100-T.103: variadic templates instead of C varargs; `initializer_list` for homogeneous lists. T.120-T.125: use template metaprogramming only when needed, prefer standard facilities. T.140-T.150: name reusable operations; do not specialize function templates (overload); check concepts with `static_assert`. T.4, T.67, T.101-T.102 have no body upstream.
- CPL.1-CPL.3: prefer C++ to C; if C is required use the common subset compiled as C++; call C interfaces from C++.
- SF.1-SF.13: `.cpp` for code and `.h` for interfaces; no object or non-inline function definitions in headers; headers for all shared declarations; a `.cpp` includes its own header first; `using namespace` only for transition, foundation libraries or local scope, never at global scope in a header; unique include guards; no cyclic dependencies; no reliance on indirect includes; self-contained headers; quoted includes for relative paths, angle brackets otherwise; portable header names. SF.20 is empty upstream. SF.21-SF.22: no unnamed namespace in headers; unnamed namespaces for internal entities.
- SL.1-SL.4: use libraries, prefer the standard library, add nothing to `std`, use it type-safely. SL.con.1-SL.con.4: `array`/`vector` over C arrays; `vector` by default; avoid bounds errors; no `memset`/`memcpy` on non-trivially-copyable types. SL.str.1-SL.str.12: `std::string` owns, `string_view`/`span<char>` refer; `zstring` for C strings; `char*` only for a single character; `std::byte` for raw bytes; `s` suffix for string literals. SL.io.1-SL.io.50: character-level input only when needed; consider ill-formed input; prefer iostreams; `sync_with_stdio(false)` unless using `printf`; no `endl`. SL.C.1: no `setjmp`/`longjmp`. No rules were present under SL.regex or SL.chrono in the text read.

### Architecture, non-rules, profiles (A, NR, Pro)
- A.1, A.2, A.4: separate stable from unstable code; package reusable parts as libraries; no cycles among libraries.
- NR.1-NR.7 are non-rules (myths): do not insist on declarations at the top, a single `return`, avoiding exceptions, one class per file, two-phase initialization, `goto exit` cleanup, or `protected` data.
- Profiles: Type.1-Type.8 (avoid casts, never downcast with `static_cast`, never cast away `const`, no C-style casts, initialize everything, avoid naked unions, avoid varargs); Bounds.1-Bounds.4 (no pointer arithmetic, constant-expression indexing only, no array-to-pointer decay, no unchecked library functions); Lifetime.1 (never dereference a possibly invalid pointer).

### Naming and layout (NL)
- NL.1-NL.3: do not state in comments what code says; comment intent; keep comments crisp. NL.4: consistent indentation. NL.5: no type information in names. NL.7: name length proportional to scope. NL.8: consistent naming style. NL.9: `ALL_CAPS` for macros only. NL.10: prefer `underscore_style`. NL.11: readable literals (digit separators, suffixes).
- NL.15-NL.21: sparing whitespace; class members ordered types, constructors/destructor, functions, data, and `public` before `protected` before `private`; K&R-derived layout; `T& operator[]`-style declarators; avoid easily misread names; one statement per line; one name per declaration. NL.25-NL.27: `f()` not `f(void)`; `const int` not `int const`; `.cpp` for implementation and `.h` for interfaces unless the project says otherwise. NL.6, NL.12-NL.14, NL.22-NL.24, NL.28-NL.30 were not present in the text read.

### Not summarized
GSL (support library description), FAQ, and Appendices A-D (libraries, modernizing code, discussion, supporting tools), the glossary and the to-do list contain no numbered rules.

## Project Rules: Comments and File Header

These project rules take precedence over the generic ECC text and over the source conventions above where they differ. In Unreal Engine code, `.claude/rules/unreal-engine/coding-style.md` adds to this section.

### File header (Doxygen)
Start every new C++ source and header file with this block, before any `#include` or `#pragma once`:

```cpp
/**
 * @file PlayerController.cpp
 * @brief Handles player input and movement.
 * @date 2026-11-15
 * @author <output of `git config user.name`>
 */
```

- `@file`: the file name with its extension (Doxygen accepts part of the path when the name is not unique).
- `@brief`: one sentence describing the file.
- `@date`: the creation date as `YYYY-MM-DD`. Write it once when the file is created and never update it (git keeps the history).
- `@author`: the value of `git config user.name`, also for files that Claude creates.
- Exempt: generated files and third-party code. Existing files are not retrofitted unless asked.
- From the Doxygen manual: commands start with `\` or `@`; `\file` marks a comment block as the documentation of its file; `/** */` and `///` blocks are accepted; the manual does not say the file block must come first.

### Comment style (same as the C# rules)
- Use `//` for short explanations. Do not use multi-line `/* */` for explanations; use consecutive `//` lines. Use `/** */` or `///` only for Doxygen documentation blocks.
- Document public declarations with Doxygen comments.
- Put a comment on its own line, never at the end of a line of code.
- Start the text with a capital letter and put one space after `//`.

### Period rule
End every comment line with a period (`.`), including each line of a comment that wraps. Write every line as a complete sentence or phrase so that the period fits. Exceptions, where a period would corrupt the content: the values on `@file`, `@date` and `@author` lines, the mandatory copyright notice, URLs, and lines inside code examples. Lines that contain only a delimiter (`/**`, ` */`) are not comment text.

## Project Rules: Initialization

These project rules take precedence over the generic ECC text and over the Core Guidelines section above where they differ (ES.23 prefers `{}` for every initializer; this project uses `{}` only for default values). In Unreal Engine code, `.claude/rules/unreal-engine/coding-style.md` applies them as well.

- Always initialize (ES.20). A variable that should hold the default value of its type (zero, `false`, `nullptr`, or the default-constructed object) is initialized with an empty brace pair, never left uninitialized and never written as `= 0`, `= false` or `= nullptr`.
- A variable that should hold any other value is initialized with `=`. Do not use braces with a value (`Count{5}`).
- Applies to default member initializers, local variables and namespace-scope variables.

```cpp
int Count{};
bool bReady{};
Foo* Target{};
int Limit = 5;
float Speed = 600.0f;
```

- Not verified: how this rule interacts with narrowing checks and with `auto` (`auto X = 5;` is allowed; `auto X{};` is not valid).
