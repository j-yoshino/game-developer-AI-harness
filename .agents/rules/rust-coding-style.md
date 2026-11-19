---
trigger: glob
description: "Rust Coding Style"
globs: "**/*.rs"
---
# Rust Coding Style

> This file extends [common/coding-style.md](../common/coding-style.md) with Rust-specific content.

## Formatting

- **rustfmt** for enforcement — always run `cargo fmt` before committing
- **clippy** for lints — `cargo clippy -- -D warnings` (treat warnings as errors)
- 4-space indent (rustfmt default)
- Max line width: 100 characters (rustfmt default)

## Immutability

Rust variables are immutable by default — embrace this:

- Use `let` by default; only use `let mut` when mutation is required
- Prefer returning new values over mutating in place
- Use `Cow<'_, T>` when a function may or may not need to allocate

```rust
use std::borrow::Cow;

// GOOD — immutable by default, new value returned
fn normalize(input: &str) -> Cow<'_, str> {
    if input.contains(' ') {
        Cow::Owned(input.replace(' ', "_"))
    } else {
        Cow::Borrowed(input)
    }
}

// BAD — unnecessary mutation
fn normalize_bad(input: &mut String) {
    *input = input.replace(' ', "_");
}
```

## Naming

Follow standard Rust conventions:
- `snake_case` for functions, methods, variables, modules, crates
- `PascalCase` (UpperCamelCase) for types, traits, enums, type parameters
- `SCREAMING_SNAKE_CASE` for constants and statics
- Lifetimes: short lowercase (`'a`, `'de`) — descriptive names for complex cases (`'input`)

## Ownership and Borrowing

- Borrow (`&T`) by default; take ownership only when you need to store or consume
- Never clone to satisfy the borrow checker without understanding the root cause
- Accept `&str` over `String`, `&[T]` over `Vec<T>` in function parameters
- Use `impl Into<String>` for constructors that need to own a `String`

```rust
// GOOD — borrows when ownership isn't needed
fn word_count(text: &str) -> usize {
    text.split_whitespace().count()
}

// GOOD — takes ownership in constructor via Into
fn new(name: impl Into<String>) -> Self {
    Self { name: name.into() }
}

// BAD — takes String when &str suffices
fn word_count_bad(text: String) -> usize {
    text.split_whitespace().count()
}
```

## Error Handling

- Use `Result<T, E>` and `?` for propagation — never `unwrap()` in production code
- **Libraries**: define typed errors with `thiserror`
- **Applications**: use `anyhow` for flexible error context
- Add context with `.with_context(|| format!("failed to ..."))?`
- Reserve `unwrap()` / `expect()` for tests and truly unreachable states

```rust
// GOOD — library error with thiserror
#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("failed to read config: {0}")]
    Io(#[from] std::io::Error),
    #[error("invalid config format: {0}")]
    Parse(String),
}

// GOOD — application error with anyhow
use anyhow::Context;

fn load_config(path: &str) -> anyhow::Result<Config> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("failed to read {path}"))?;
    toml::from_str(&content)
        .with_context(|| format!("failed to parse {path}"))
}
```

## Iterators Over Loops

Prefer iterator chains for transformations; use loops for complex control flow:

```rust
// GOOD — declarative and composable
let active_emails: Vec<&str> = users.iter()
    .filter(|u| u.is_active)
    .map(|u| u.email.as_str())
    .collect();

// GOOD — loop for complex logic with early returns
for user in &users {
    if let Some(verified) = verify_email(&user.email)? {
        send_welcome(&verified)?;
    }
}
```

## Module Organization

Organize by domain, not by type:

```text
src/
├── main.rs
├── lib.rs
├── auth/           # Domain module
│   ├── mod.rs
│   ├── token.rs
│   └── middleware.rs
├── orders/         # Domain module
│   ├── mod.rs
│   ├── model.rs
│   └── service.rs
└── db/             # Infrastructure
    ├── mod.rs
    └── pool.rs
```

## Visibility

- Default to private; use `pub(crate)` for internal sharing
- Only mark `pub` what is part of the crate's public API
- Re-export public API from `lib.rs`

## References

See skill: `rust-patterns` for comprehensive Rust idioms and patterns.

## Project Conventions: Rust API Guidelines - Naming

Source: https://rust-lang.github.io/api-guidelines/naming.html (Naming chapter only, read in full on 2026-11-15). Other chapters of the API Guidelines are not covered. This section takes precedence over the generic ECC text above.

### Casing (C-CASE)
- UpperCamelCase: types, traits, enum variants. snake_case: modules, functions, methods, local variables, macros. SCREAMING_SNAKE_CASE: statics and constants. Type parameters: usually a single uppercase letter such as `T`. Lifetimes: short lowercase such as `'a`, `'de`.
- Acronyms count as one word in UpperCamelCase (`Uuid`, `Usize`, `Stdin`) and are lowercase in snake_case. Do not put a one-letter word anywhere but the end (`btree_map` yes, `b_tree_map` no; `PI_2` yes, `PI2` no).
- Constructors are `new` or `with_more_details`; conversion constructors are `from_xxx`. Crate names must not have `-rs` or `-rust` affixes.

### Conversions (C-CONV)
- `as_`: free, borrowed to borrowed, lowers abstraction (`str::as_bytes`). `to_`: costly; borrowed to owned, or owned to owned for `Copy` types (`str::to_lowercase`). `into_`: consumes ownership and returns an owned value, cost varies (`String::into_bytes`).
- A wrapper around one value provides `into_inner()`. Put `mut` where it appears in the return type (`as_mut_slice`, not `as_slice_mut`).

### Getters, iterators, features, word order
- C-GETTER: no `get_` prefix; use the field name (`first()`), `first_mut()` for the mutable one. Use `get` only when it is the single obvious accessor (`Cell::get`). For validated access, consider an `unsafe` `_unchecked` variant.
- C-ITER, C-ITER-TY: collections provide `iter` (`&U`), `iter_mut` (`&mut U`), `into_iter` (`U`), as methods only. Types that are not homogeneous collections use other names (`bytes`, `chars`). Iterator type names match the method (`into_iter` -> `IntoIter`, `keys` -> `Keys`).
- C-FEATURE: Cargo features have no `use-`/`with-` prefix; the standard library feature is `std`; features are additive, so no `no-abc` names.
- C-WORD-ORDER: keep word order consistent with the standard library, e.g. `ParseAddrError`, not `AddrParseError`.

## Project Rules: Comments and File Header

These project rules take precedence over the generic ECC text and over the naming section above where they differ.

### File header (Rust has no Doxygen)
Rust has no `@file`, `@brief`, `@date` or `@author`. The equivalent is an inner line doc comment (`//!`) at the top of the file. Inner doc comments document the enclosing item, and a `//!` block at the top of a file documents that file as a module (Rust Reference); `rustdoc` renders it as Markdown and uses the first paragraph, up to the first blank line, as the summary in module listings (rustdoc book). Start every new `.rs` file with:

```rust
//! Handles player input and movement.
//!
//! - **Date**: 2026-11-15
//! - **Author**: <output of `git config user.name`>
```

- The first line is the `@brief` equivalent: one sentence, ending with a period, kept to one line.
- `@file` is omitted: `rustdoc` already shows the module path and file location.
- **Date**: the creation date as `YYYY-MM-DD`, written once and never updated. **Author**: the value of `git config user.name`.
- The date and author appear in the generated public documentation (accepted trade-off). Place the block before any `use` item. Generated files and third-party code are exempt; existing files are not retrofitted unless asked.

### Period rule
End every comment line with a period (`.`), including each line of a comment that wraps, for `//`, `///` and `//!` comments. Write every line as a complete sentence or phrase so that the period fits. Exceptions, where a period would corrupt the content: the `Date` and `Author` values, URLs, and lines inside code examples.
