> 日本語訳(参照用)。原文(英語): `.claude/rules/csharp/patterns.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `**/*.cs`、`**/*.csx`

# C# パターン

> このファイルは [common/patterns.md](../common/patterns.md) を C# 固有の内容で拡張します。

## API レスポンスパターン

```csharp
public sealed record ApiResponse<T>(
    bool Success,
    T? Data = default,
    string? Error = null,
    object? Meta = null);
```

## リポジトリパターン

```csharp
public interface IRepository<T>
{
    Task<IReadOnlyList<T>> FindAllAsync(CancellationToken cancellationToken);
    Task<T?> FindByIdAsync(Guid id, CancellationToken cancellationToken);
    Task<T> CreateAsync(T entity, CancellationToken cancellationToken);
    Task<T> UpdateAsync(T entity, CancellationToken cancellationToken);
    Task DeleteAsync(Guid id, CancellationToken cancellationToken);
}
```

## オプションパターン

設定は、コードベースのあちこちで生の文字列を読むのではなく、強く型付けされたオプションで扱います。

```csharp
public sealed class PaymentsOptions
{
    public const string SectionName = "Payments";
    public required string BaseUrl { get; init; }
    public required string ApiKeySecretName { get; init; }
}
```

## 依存性注入

- サービスの境界では、インターフェースに依存する
- コンストラクターは焦点を絞る。サービスの依存が多すぎるなら、責務を分割する
- 寿命は意図して登録する: 状態を持たない/共有されるサービスは singleton、リクエストのデータは scoped、軽量で純粋なワーカーは transient
