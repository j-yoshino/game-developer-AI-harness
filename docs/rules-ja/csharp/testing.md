> 日本語訳(参照用)。原文(英語): `.claude/rules/csharp/testing.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `**/*.cs`、`**/*.csx`、`**/*.csproj`

# C# テスト

> このファイルは [common/testing.md](../common/testing.md) を C# 固有の内容で拡張します。

## テストフレームワーク

- 単体テストと統合テストには **xUnit** を優先する
- 読みやすいアサーションには **FluentAssertions** を使う
- 依存のモックには **Moq** または **NSubstitute** を使う
- 統合テストに本物のインフラが必要なときは **Testcontainers** を使う

## テストの構成

- `src/` の構成を `tests/` の下に写す
- 単体・統合・エンドツーエンドのカバレッジを、はっきり分ける
- テストには、実装の詳細ではなく振る舞いで名前を付ける

```csharp
public sealed class OrderServiceTests
{
    [Fact]
    public async Task FindByIdAsync_ReturnsOrder_WhenOrderExists()
    {
        // Arrange
        // Act
        // Assert
    }
}
```

## ASP.NET Core の統合テスト

- API の統合カバレッジには `WebApplicationFactory<TEntryPoint>` を使う
- 認証・検証・シリアル化は、ミドルウェアを迂回せず、HTTP を通してテストする

## カバレッジ

- 行カバレッジ 80% 以上を目標にする
- ドメインロジック、検証、認証、失敗パスにカバレッジを集中させる
- CI では、使える場合はカバレッジ収集を有効にして `dotnet test` を実行する
