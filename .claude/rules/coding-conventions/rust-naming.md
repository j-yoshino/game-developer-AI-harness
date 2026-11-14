---
paths:
  - "**/*.rs"
  - "**/Cargo.toml"
---

# Rust の命名規則(Rust API Guidelines: Naming)

- 出典: https://rust-lang.github.io/api-guidelines/naming.html (2026-11-15 取得)
- 位置づけ: Rust API Guidelines のうち **Naming の章だけ**。Rust のコーディング規約全体ではない(フォーマットは `rustfmt`、リントは `clippy` に従う)。
- 要約であり原文の転載ではない。
- `.claude/rules/ecc/rust/` の ECC のルールと食い違う場合は、このディレクトリの規約を優先する。

## 大文字小文字(C-CASE)

| 対象 | 形式 |
|---|---|
| 型、トレイト、enum のバリアント | UpperCamelCase |
| モジュール、関数、メソッド、ローカル変数、マクロ | snake_case |
| `static`、`const` | SCREAMING_SNAKE_CASE |
| 型パラメータ | 通常は `T` のような1文字の大文字 |
| ライフタイム | `'a`、`'de` のような短い小文字 |

- 頭字語は、UpperCamelCase では1語として扱う(`Uuid`、`Usize`、`Stdin`)。snake_case では全部小文字。
- 1文字の単語を末尾以外に置かない(`btree_map` は可、`b_tree_map` は不可。`PI_2` は可、`PI2` は不可)。
- コンストラクターは基本 `new` か `with_more_details`。変換系は `from_xxx`。
- クレート名に `-rs` や `-rust` の接頭辞・接尾辞を付けない。

## 変換メソッド(C-CONV)

| 接頭辞 | コスト | 引数 → 戻り値 | 例 |
|---|---|---|---|
| `as_` | ほぼゼロ | 借用 → 借用(抽象度を下げる) | `str::as_bytes` |
| `to_` | 処理コストあり | 借用 → 所有、または `Copy` の所有 → 所有 | `str::to_lowercase` |
| `into_` | 場合による | 所有権を消費して所有型を返す(抽象度を下げる) | `String::into_bytes` |

- 単一の値を包むラッパー型は、中身を取り出す `into_inner()` を用意する。
- `mut` を含む名前は、戻り値の型と同じ位置に `mut` を置く(`as_mut_slice`。`as_slice_mut` は不可)。

## getter(C-GETTER)

- 基本は `get_` を付けない。フィールド名そのもの(`first()`)、可変版は `first_mut()`。
- `get` は、取得対象が1つに決まる場合だけ(例: `Cell::get`)。
- 境界チェックなどの検証を伴う getter には、`unsafe` な `_unchecked` 版の追加を検討する。

## イテレーター(C-ITER、C-ITER-TY)

- コレクションの要素 `U` に対して、`iter`(`&U`)、`iter_mut`(`&mut U`)、`into_iter`(`U`)の3つを揃える。メソッドにだけ使い、関数には使わない。
- `str` のように同種コレクションとみなしにくい型は、`bytes`、`chars` のように別の名前にする。
- イテレーターの型名はメソッド名に対応させる(`into_iter` → `IntoIter`、`keys` → `Keys`)。

## その他

- Cargo の feature(C-FEATURE): `use-` や `with-` のような意味のない語を付けない(`abc` と直接書く)。標準ライブラリ依存は `std` という名前の feature。加算的であるべきなので `no-abc` のような否定形は避ける。
- 単語の並び順(C-WORD-ORDER): 型名の単語順をクレート内と標準ライブラリで一貫させる。エラー型は「動詞・目的語・Error」の順(`ParseAddrError`。`AddrParseError` は避ける)。

## 要約の範囲と未確認事項

- Naming の章の全項目(C-CASE、C-CONV、C-GETTER、C-ITER、C-ITER-TY、C-FEATURE、C-WORD-ORDER)を読んだ。Web 取得の要約を経由しており、原文の細部は未確認。
- API Guidelines の他の章(Interoperability、Macros、Documentation など)は**対象外**。
