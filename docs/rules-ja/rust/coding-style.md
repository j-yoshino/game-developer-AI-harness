> 日本語訳(参照用)。原文(英語): `.claude/rules/rust/coding-style.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `**/*.rs`

# Rust コーディングスタイル

> このファイルは [common/coding-style.md](../common/coding-style.md) を Rust 固有の内容で拡張します。

## フォーマット

- 強制には **rustfmt** — コミット前に必ず `cargo fmt` を実行する
- リントには **clippy** — `cargo clippy -- -D warnings`(警告をエラーとして扱う)
- インデントは4スペース(rustfmt の既定)
- 行の最大幅: 100 文字(rustfmt の既定)

## 不変性

Rust の変数は既定で不変です。これを活かします。

- 既定では `let` を使い、変更が必要なときだけ `let mut` を使う
- その場で変更するより、新しい値を返すことを優先する
- 関数が確保する場合としない場合があるときは `Cow<'_, T>` を使う

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

## 命名

標準的な Rust の規約に従います。
- 関数・メソッド・変数・モジュール・クレートは `snake_case`
- 型・トレイト・enum・型パラメーターは `PascalCase`(UpperCamelCase)
- 定数と static は `SCREAMING_SNAKE_CASE`
- ライフタイム: 短い小文字(`'a`、`'de`)— 複雑な場合は説明的な名前(`'input`)

## 所有権と借用

- 既定では借用(`&T`)し、保存または消費が必要なときだけ所有権を取る
- 根本原因を理解しないまま、借用チェッカーを満たすためにクローンしない
- 関数の引数は、`String` より `&str`、`Vec<T>` より `&[T]` を受け取る
- `String` を所有する必要のあるコンストラクターには `impl Into<String>` を使う

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

## エラー処理

- 伝播には `Result<T, E>` と `?` を使う — 本番コードでは決して `unwrap()` を使わない
- **ライブラリ**: `thiserror` で型付きのエラーを定義する
- **アプリケーション**: 柔軟なエラーコンテキストのために `anyhow` を使う
- `.with_context(|| format!("failed to ..."))?` でコンテキストを足す
- `unwrap()` / `expect()` は、テストと、本当に到達しない状態のためだけに取っておく

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

## ループよりイテレーター

変換にはイテレーターチェーンを優先し、複雑な制御フローにはループを使います。

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

## モジュールの構成

型ではなく、ドメインで構成します。

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

## 可視性

- 既定は private。内部での共有には `pub(crate)` を使う
- クレートの公開 API になるものだけを `pub` にする
- 公開 API は `lib.rs` から再エクスポートする

## 参照

Rust の包括的なイディオムとパターンは、スキル `rust-patterns` を参照してください。

## プロジェクト規約: Rust API Guidelines — Naming

出典: https://rust-lang.github.io/api-guidelines/naming.html(Naming の章のみ、2026-11-15 に全文を読了)。API Guidelines の他の章は対象外です。この節は、上の汎用的な ECC の記述より優先します。

### 大文字小文字(C-CASE)
- UpperCamelCase: 型、トレイト、enum のバリアント。snake_case: モジュール、関数、メソッド、ローカル変数、マクロ。SCREAMING_SNAKE_CASE: static と定数。型パラメーター: 通常は `T` のような大文字1文字。ライフタイム: `'a`、`'de` のような短い小文字。
- 頭字語は UpperCamelCase では1語として扱い(`Uuid`、`Usize`、`Stdin`)、snake_case では小文字にする。1文字の単語は末尾以外に置かない(`btree_map` は可、`b_tree_map` は不可。`PI_2` は可、`PI2` は不可)。
- コンストラクターは `new` または `with_more_details`、変換コンストラクターは `from_xxx`。クレート名に `-rs` や `-rust` の接頭辞・接尾辞を付けない。

### 変換(C-CONV)
- `as_`: コストなし、借用から借用、抽象度を下げる(`str::as_bytes`)。`to_`: コストあり、借用から所有、または `Copy` 型の所有から所有(`str::to_lowercase`)。`into_`: 所有権を消費して所有型を返す、コストは場合による(`String::into_bytes`)。
- 1つの値を包むラッパーは `into_inner()` を提供する。`mut` は戻り値の型の中の位置に合わせて置く(`as_mut_slice`。`as_slice_mut` ではない)。

### getter・イテレーター・feature・単語の順序
- C-GETTER: `get_` 接頭辞を付けず、フィールド名を使う(`first()`)、可変版は `first_mut()`。`get` は、それが唯一の明らかなアクセサーであるときだけ(`Cell::get`)。検証付きのアクセスには、`unsafe` な `_unchecked` 版を検討する。
- C-ITER、C-ITER-TY: コレクションは `iter`(`&U`)、`iter_mut`(`&mut U`)、`into_iter`(`U`)をメソッドとしてだけ提供する。同種のコレクションでない型は別の名前を使う(`bytes`、`chars`)。イテレーターの型名はメソッド名に合わせる(`into_iter` → `IntoIter`、`keys` → `Keys`)。
- C-FEATURE: Cargo の feature に `use-` / `with-` の接頭辞を付けない。標準ライブラリ用の feature は `std`。feature は加算的なので `no-abc` のような名前は使わない。
- C-WORD-ORDER: 単語の順序は標準ライブラリに合わせて一貫させる(`ParseAddrError`。`AddrParseError` ではない)。

## プロジェクトルール: コメントとファイルヘッダー

これらのプロジェクトルールは、汎用的な ECC の記述や、上の命名の節と食い違う場合に、それらより優先します。

### ファイルヘッダー(Rust には Doxygen がない)
Rust には `@file`・`@brief`・`@date`・`@author` がありません。同等のものは、ファイル先頭の内側の行ドキュメントコメント(`//!`)です。内側のドキュメントコメントは、それを囲む要素のドキュメントになり、ファイルの先頭の `//!` ブロックは、そのファイルをモジュールとして文書化します(Rust Reference)。`rustdoc` はこれを Markdown として描画し、最初の空行までの段落を、モジュール一覧の要約に使います(rustdoc book)。新しい `.rs` ファイルは、次のブロックで始めます。

```rust
//! Handles player input and movement.
//!
//! - **Date**: 2026-11-15
//! - **Author**: <output of `git config user.name`>
```

- 1行目は `@brief` に当たる。1文で、末尾にピリオドを付け、1行に収める。
- `@file` は省く。`rustdoc` がすでにモジュールのパスとファイルの場所を示すため。
- **Date**: `YYYY-MM-DD` 形式の作成日で、1回だけ書き、更新しない。**Author**: `git config user.name` の値。
- 日付と作者は、生成される公開ドキュメントに表示される(受け入れたトレードオフ)。ブロックは、`use` 項目より前に置く。生成ファイルとサードパーティのコードは対象外。既存のファイルは、依頼がない限り後から追加しない。

### ピリオドの規則
`//`・`///`・`//!` のすべてのコメント行の末尾にピリオド(`.`)を付ける。折り返したコメントの各行も含む。ピリオドが収まるように、各行を完結した文または句として書く。ピリオドを付けると内容が壊れる場合は例外とする: `Date` と `Author` の値、URL、コード例の中の行。
