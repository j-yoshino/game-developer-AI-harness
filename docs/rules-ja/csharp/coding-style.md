> 日本語訳(参照用)。原文(英語): `.claude/rules/csharp/coding-style.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `**/*.cs`、`**/*.csx`

# C# コーディングスタイル

> このファイルは [common/coding-style.md](../common/coding-style.md) を C# 固有の内容で拡張します。

## 標準

- 現行の .NET の規約に従い、nullable 参照型を有効にする
- 公開 API と internal API では、アクセス修飾子を明示することを優先する
- ファイルは、そこで定義する主要な型に合わせる

## 型とモデル

- 不変の値のようなモデルには `record` または `record struct` を優先する
- 同一性とライフサイクルを持つエンティティや型には `class` を使う
- サービスの境界と抽象化には `interface` を使う
- アプリケーションコードで `dynamic` を避け、ジェネリクスか明示的なモデルを優先する

```csharp
public sealed record UserDto(Guid Id, string Email);

public interface IUserRepository
{
    Task<UserDto?> FindByIdAsync(Guid id, CancellationToken cancellationToken);
}
```

## 不変性

- 共有される状態には、`init` セッター、コンストラクター引数、不変コレクションを優先する
- 更新後の状態を作るとき、入力のモデルをその場で変更しない

```csharp
public sealed record UserProfile(string Name, string Email);

public static UserProfile Rename(UserProfile profile, string name) =>
    profile with { Name = name };
```

## 非同期とエラー処理

- `.Result` や `.Wait()` のようなブロッキング呼び出しより `async` / `await` を優先する
- 公開される非同期 API には `CancellationToken` を渡す
- 具体的な例外を投げ、構造化されたプロパティ付きでログを出す

```csharp
public async Task<Order> LoadOrderAsync(
    Guid orderId,
    CancellationToken cancellationToken)
{
    try
    {
        return await repository.FindAsync(orderId, cancellationToken)
            ?? throw new InvalidOperationException($"Order {orderId} was not found.");
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "Failed to load order {OrderId}", orderId);
        throw;
    }
}
```

## フォーマット

- フォーマットとアナライザーの修正には `dotnet format` を使う
- `using` ディレクティブを整理し、不要なインポートを削除する
- 式形式のメンバーは、読みやすさが保たれる場合だけ使う

## プロジェクト規約: .NET C# コーディング規則

出典: https://learn.microsoft.com/ja-jp/dotnet/csharp/fundamentals/coding-style/coding-conventions(日本語の機械翻訳ページ、2026-11-15 に全文を読了、更新日 2026-10-04)。`dotnet/docs` チームが自分たちのサンプルで使っている規則です。ページ自身が、これを「信頼できる唯一のリストではなく、一般的な C# 規則の例」と述べています。この節は、上の汎用的な ECC の記述より優先します。`Assets/`(Unity)では `.claude/rules/unity/coding-style.md` が優先し、`Source/` 配下の Unreal のビルドスクリプトでは `.claude/rules/unreal-engine/coding-style.md` が優先します(タブを使います)。

### 言語ガイドライン
- 新しい C# の機能とバージョンを使い、古い構文を避ける。処理できる例外だけを `catch` する。フィルターなしで `Exception` を捕まえない。具体的な例外型で意味のあるメッセージを出す。
- コレクション操作には LINQ、I/O には `async` / `await`(デッドロックに注意し、必要なら `ConfigureAwait`)。
- 型には言語キーワードを使う(`string`、`int`)。ランタイム型は使わない。符号なし型が本質的でない限り `int` を使う。
- `var` は、右辺から型が明らかなとき(`new`、明示的なキャスト、リテラル)だけ使う。メソッド名から型を推測しない。変数名に型の名前を付けない。`for` ループと LINQ のクエリ結果では `var` を使い、`foreach` では型を明示する。`dynamic` は実行時の型付けが必要なときだけで、`var` の代わりにしない。
- 文字列: 短い連結には文字列補間(`$"..."`、位置指定ではなく式ベース)、ループ内で足すときは `StringBuilder`、エスケープや逐語的文字列より生文字列リテラル(`"""`)。
- コンストラクター: `record` のプライマリコンストラクターの引数は PascalCase、`class` / `struct` のプライマリコンストラクターの引数は camelCase。初期化を強制したいときはコンストラクターではなく `required` プロパティ。
- コレクションはコレクション式(`[ ... ]`)で初期化する。デリゲートは独自のデリゲート型より `Func<>` / `Action<>`、インスタンス化は短い構文で。
- リソース: `Dispose` を呼ぶだけの `try` / `finally` は `using` に置き換え、波かっこのない `using` 宣言を優先する。削除する必要のないイベントハンドラーにはラムダ式。
- オブジェクト: 変数の型とオブジェクトの型が同じなら `var x = new X();` または `X x = new();`。オブジェクト初期化子を使う。静的メンバーは、派生クラスではなく宣言したクラスの名前で呼ぶ。
- LINQ: クエリ変数には意味のある名前、匿名型のプロパティ名は PascalCase、曖昧なプロパティ名は付け替える、`where` を他の句より先に、内側のコレクションには `join` ではなく複数の `from`。
- 名前空間: ファイルスコープ(`namespace X;`)、`using` ディレクティブは名前空間宣言の外に置く。安全なコーディングのガイドラインに従う。
- 日本語ページの `&&` / `||` の節は、本文とコード例が食い違っているため、ここでは要約していない。

### スタイル
- スペース4つでタブは使わない、Allman 形式の波かっこ(各波かっこを独立した行に)、1行に1ステートメント・1宣言、メソッドとプロパティの定義の間に1行以上の空行、式の優先順位を明確にするための括弧、継続行は4スペースのインデント、長いステートメントは分割し二項演算子の前で改行する。
- コメント: 短い説明は `//`、`/* */` は避ける、メソッド・クラス・フィールド・すべての公開メンバーに XML ドキュメントコメント、コメントは独立した行に書き、大文字で始め、`//` の後に空白を1つ、すべてのコメント行の末尾にピリオド(下の「プロジェクトルール: コメントとファイルヘッダー」を参照)。
- 65文字の行長制限はドキュメント表示用で、このプロジェクトには適用しない。`.editorconfig` に従う。
- クラス・メソッド・フィールドの命名規則は、このページでは扱われていない。`.editorconfig` と既存のコードに従う。
- ページは、規約を `.editorconfig` とコード分析で強制することを勧めている。このリポジトリには、まだどちらも用意されていない。

## プロジェクトルール: コメントとファイルヘッダー

これらのプロジェクトルールは、汎用的な ECC の記述や、上の .NET の節と食い違う場合に、それらより優先します。Unity のコード(`Assets/`)と、Unreal のビルドスクリプト(`Source/**/*.cs`)にも適用されます。

### ファイルヘッダー(Doxygen、`//!` の行で書く)
新しい C# ファイルは、`using` ディレクティブより前に、次のブロックで始めます。

```csharp
//! @file PlayerController.cs
//! @brief Handles player input and movement.
//! @date 2026-11-15
//! @author <output of `git config user.name`>
```

- `@file`・`@brief`・`@date`・`@author`: 意味・書式・対象外は `.claude/rules/cpp/coding-style.md` と同じ(作成日は `YYYY-MM-DD` で1回だけ書く、作者は `git config user.name`、生成ファイルとサードパーティは対象外、既存ファイルは依頼がない限り後から追加しない)。
- `///` ではなく `//!` を使う理由: Doxygen のマニュアルは、C# を含む言語で、コメントブロックを2行以上の `///` または `//!` で書けるとしている。有効な言語要素の上にない `///` の XML ドキュメントコメントは、コンパイラ警告 CS1587(レベル2。文書化された例は、名前空間の上の summary)を出すことがあるため、ヘッダーには `//!` を使う。未検証: `//!` でビルドが警告を出さないこと、および、同じ C# ファイルで Doxygen が `@file` のブロックと XML タグを一緒に扱えるか(マニュアルは XML タグに対応しているとしか述べていない)。
- メンバーのドキュメントは、.NET の節のとおり、XML ドキュメントコメント(`///` と `<summary>`)のままにする。

### ピリオドの規則
すべてのコメント行の末尾にピリオド(`.`)を付ける。折り返したコメントの各行も含む。ピリオドが収まるように、各行を完結した文または句として書く。ピリオドを付けると内容が壊れる場合は例外とする: `@file`・`@date`・`@author` の行の値、URL、コード例の中の行。区切りだけの行はコメントのテキストではない。
