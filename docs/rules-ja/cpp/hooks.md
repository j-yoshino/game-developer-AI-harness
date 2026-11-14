> 日本語訳(参照用)。原文(英語): `.claude/rules/cpp/hooks.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `**/*.cpp`、`**/*.hpp`、`**/*.cc`、`**/*.hh`、`**/*.cxx`、`**/*.h`、`**/CMakeLists.txt`

# C++ フック

> このファイルは [common/hooks.md](../common/hooks.md) を C++ 固有の内容で拡張します。

## ビルドフック

C++ の変更をコミットする前に、次のチェックを実行します。

```bash
# Format check
clang-format --dry-run --Werror src/*.cpp src/*.hpp

# Static analysis
clang-tidy src/*.cpp -- -std=c++17

# Build
cmake --build build

# Tests
ctest --test-dir build --output-on-failure
```

## 推奨 CI パイプライン

1. **clang-format** — フォーマットのチェック
2. **clang-tidy** — 静的解析
3. **cppcheck** — 追加の解析
4. **cmake build** — コンパイル
5. **ctest** — サニタイザー付きのテスト実行
