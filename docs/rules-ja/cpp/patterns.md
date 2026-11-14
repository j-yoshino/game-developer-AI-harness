> 日本語訳(参照用)。原文(英語): `.claude/rules/cpp/patterns.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `**/*.cpp`、`**/*.hpp`、`**/*.cc`、`**/*.hh`、`**/*.cxx`、`**/*.h`、`**/CMakeLists.txt`

# C++ パターン

> このファイルは [common/patterns.md](../common/patterns.md) を C++ 固有の内容で拡張します。

## RAII(Resource Acquisition Is Initialization)

リソースの寿命をオブジェクトの寿命に結び付けます。

```cpp
class FileHandle {
public:
    explicit FileHandle(const std::string& path) : file_(std::fopen(path.c_str(), "r")) {}
    ~FileHandle() { if (file_) std::fclose(file_); }
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;
private:
    std::FILE* file_;
};
```

## Rule of Five / Zero

- **Rule of Zero**: 独自のデストラクター、コピー/ムーブコンストラクター、代入演算子を必要としないクラスを優先する
- **Rule of Five**: デストラクター/コピーコンストラクター/コピー代入/ムーブコンストラクター/ムーブ代入のいずれかを定義するなら、5つすべてを定義する

## 値セマンティクス

- 小さい型や trivial な型は値渡しにする
- 大きい型は `const&` で渡す
- 戻り値は値で返す(RVO/NRVO に任せる)
- シンク引数にはムーブセマンティクスを使う

## エラー処理

- 例外的な状況には例外を使う
- 存在しないかもしれない値には `std::optional` を使う
- 想定内の失敗には `std::expected`(C++23)または result 型を使う

## 参照

C++ のパターンとアンチパターンの包括的な内容は、スキル `cpp-coding-standards` を参照してください。
