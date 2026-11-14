> 日本語訳(参照用)。原文(英語): `.claude/rules/cpp/testing.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `**/*.cpp`、`**/*.hpp`、`**/*.cc`、`**/*.hh`、`**/*.cxx`、`**/*.h`、`**/CMakeLists.txt`

# C++ テスト

> このファイルは [common/testing.md](../common/testing.md) を C++ 固有の内容で拡張します。

## フレームワーク

**GoogleTest**(gtest/gmock)を **CMake/CTest** と組み合わせて使います。

## テストの実行

```bash
cmake --build build && ctest --test-dir build --output-on-failure
```

## カバレッジ

```bash
cmake -DCMAKE_CXX_FLAGS="--coverage" -DCMAKE_EXE_LINKER_FLAGS="--coverage" ..
cmake --build .
ctest --output-on-failure
lcov --capture --directory . --output-file coverage.info
```

## サニタイザー

CI では、常にサニタイザー付きでテストを実行します。

```bash
cmake -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined" ..
```

## 参照

C++ のテストパターン、TDD のワークフロー、GoogleTest/GMock の使い方の詳細は、スキル `cpp-testing` を参照してください。
