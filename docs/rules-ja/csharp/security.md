> 日本語訳(参照用)。原文(英語): `.claude/rules/csharp/security.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `**/*.cs`、`**/*.csx`、`**/*.csproj`、`**/appsettings*.json`

# C# セキュリティ

> このファイルは [common/security.md](../common/security.md) を C# 固有の内容で拡張します。

## シークレット管理

- API キー、トークン、接続文字列をソースコードにハードコードしない
- 環境変数、ローカル開発ではユーザーシークレット、本番ではシークレットマネージャーを使う
- `appsettings.*.json` に本物の認証情報を入れない

```csharp
// BAD
const string ApiKey = "sk-live-123";

// GOOD
var apiKey = builder.Configuration["OpenAI:ApiKey"]
    ?? throw new InvalidOperationException("OpenAI:ApiKey is not configured.");
```

## SQL インジェクションの防止

- ADO.NET、Dapper、EF Core では、常にパラメーター化クエリを使う
- ユーザー入力を SQL 文字列に連結しない
- 動的にクエリを組み立てる前に、並べ替えのフィールドとフィルター演算子を検証する

```csharp
const string sql = "SELECT * FROM Orders WHERE CustomerId = @customerId";
await connection.QueryAsync<Order>(sql, new { customerId });
```

## 入力の検証

- DTO は、アプリケーションの境界で検証する
- データ注釈、FluentValidation、または明示的なガード句を使う
- ビジネスロジックを実行する前に、不正なモデルの状態を拒否する

## 認証と認可

- 独自のトークン解析ではなく、フレームワークの認証ハンドラーを優先する
- 認可ポリシーは、エンドポイントまたはハンドラーの境界で強制する
- 生のトークン、パスワード、PII をログに出さない

## エラー処理

- クライアントに返すメッセージは安全なものにする
- 詳細な例外は、構造化されたコンテキスト付きでサーバー側にログする
- スタックトレース、SQL のテキスト、ファイルシステムのパスを API レスポンスに含めない

## 参照

アプリケーションセキュリティのより広いレビューチェックリストは、スキル `security-review` を参照してください。
