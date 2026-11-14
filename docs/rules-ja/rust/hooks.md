> 日本語訳(参照用)。原文(英語): `.claude/rules/rust/hooks.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `**/*.rs`、`**/Cargo.toml`

# Rust フック

> このファイルは [common/hooks.md](../common/hooks.md) を Rust 固有の内容で拡張します。

## PostToolUse フック

`~/.claude/settings.json` に設定します。

- **cargo fmt**: 編集後に `.rs` ファイルを自動整形する
- **cargo clippy**: Rust ファイルの編集後にリントを実行する
- **cargo check**: 変更後にコンパイルできることを確認する(`cargo build` より高速)
