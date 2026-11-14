> 日本語訳(参照用)。原文(英語): `.claude/rules/cpp/security.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `**/*.cpp`、`**/*.hpp`、`**/*.cc`、`**/*.hh`、`**/*.cxx`、`**/*.h`、`**/CMakeLists.txt`

# C++ セキュリティ

> このファイルは [common/security.md](../common/security.md) を C++ 固有の内容で拡張します。

## メモリ安全性

- 生の `new` / `delete` を使わない — スマートポインターを使う
- C スタイルの配列を使わない — `std::array` または `std::vector` を使う
- `malloc` / `free` を使わない — C++ の確保方法を使う
- どうしても必要な場合を除き `reinterpret_cast` を避ける

## バッファオーバーフロー

- `char*` より `std::string` を使う
- 安全性が重要なときは、境界チェック付きの `.at()` を使う
- `strcpy`、`strcat`、`sprintf` を使わない — `std::string` または `fmt::format` を使う

## 未定義動作

- 変数は必ず初期化する
- 符号付き整数のオーバーフローを避ける
- null やダングリングポインターを決して参照外ししない
- CI でサニタイザーを使う:
  ```bash
  cmake -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined" ..
  ```

## 静的解析

- 自動チェックには **clang-tidy** を使う:
  ```bash
  clang-tidy --checks='*' src/*.cpp
  ```
- 追加の解析には **cppcheck** を使う:
  ```bash
  cppcheck --enable=all src/
  ```

## 参照

詳細なセキュリティガイドラインは、スキル `cpp-coding-standards` を参照してください。
