---
trigger: glob
description: "Rust Hooks"
globs: "**/*.rs, **/Cargo.toml"
---
<!-- generated from .claude/rules/rust/hooks.md. Do not edit; run scripts/sync-agent-env.py. -->
# Rust Hooks

> This file extends [common/hooks.md](../common/hooks.md) with Rust-specific content.

## PostToolUse Hooks

Configure in `~/.claude/settings.json`:

- **cargo fmt**: Auto-format `.rs` files after edit
- **cargo clippy**: Run lint checks after editing Rust files
- **cargo check**: Verify compilation after changes (faster than `cargo build`)
