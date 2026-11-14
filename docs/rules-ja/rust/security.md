> 日本語訳(参照用)。原文(英語): `.claude/rules/rust/security.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `**/*.rs`

# Rust セキュリティ

> このファイルは [common/security.md](../common/security.md) を Rust 固有の内容で拡張します。

## シークレット管理

- API キー、トークン、認証情報をソースコードにハードコードしない
- 環境変数を使う: `std::env::var("API_KEY")`
- 必要なシークレットが起動時に無ければ、すぐに失敗させる
- `.env` ファイルは `.gitignore` に入れておく

```rust
// BAD
const API_KEY: &str = "sk-abc123...";

// GOOD — environment variable with early validation
fn load_api_key() -> anyhow::Result<String> {
    std::env::var("PAYMENT_API_KEY")
        .context("PAYMENT_API_KEY must be set")
}
```

## SQL インジェクションの防止

- 常にパラメーター化クエリを使う — ユーザー入力を SQL 文字列に整形して入れない
- クエリビルダーや ORM(sqlx、diesel、sea-orm)をバインドパラメーターと一緒に使う

```rust
// BAD — SQL injection via format string
let query = format!("SELECT * FROM users WHERE name = '{name}'");
sqlx::query(&query).fetch_one(&pool).await?;

// GOOD — parameterized query with sqlx
// Placeholder syntax varies by backend: Postgres: $1  |  MySQL: ?  |  SQLite: $1
sqlx::query("SELECT * FROM users WHERE name = $1")
    .bind(&name)
    .fetch_one(&pool)
    .await?;
```

## 入力の検証

- ユーザー入力はすべて、処理の前にシステムの境界で検証する
- 型システムで不変条件を強制する(newtype パターン)
- 検証するのではなくパースする — 境界で、構造化されていないデータを型付きの構造体に変換する
- 不正な入力は、明確なエラーメッセージ付きで拒否する

```rust
// Parse, don't validate — invalid states are unrepresentable
pub struct Email(String);

impl Email {
    pub fn parse(input: &str) -> Result<Self, ValidationError> {
        let trimmed = input.trim();
        let at_pos = trimmed.find('@')
            .filter(|&p| p > 0 && p < trimmed.len() - 1)
            .ok_or_else(|| ValidationError::InvalidEmail(input.to_string()))?;
        let domain = &trimmed[at_pos + 1..];
        if trimmed.len() > 254 || !domain.contains('.') {
            return Err(ValidationError::InvalidEmail(input.to_string()));
        }
        // For production use, prefer a validated email crate (e.g., `email_address`)
        Ok(Self(trimmed.to_string()))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}
```

## unsafe コード

- `unsafe` ブロックを最小限にする — 安全な抽象化を優先する
- すべての `unsafe` ブロックに、不変条件を説明する `// SAFETY:` コメントを付ける
- 手軽さのために、借用チェッカーを回避する目的で `unsafe` を使わない
- レビューでは `unsafe` コードをすべて監査する — 正当化がなければ危険信号
- C ライブラリの周りには、安全な FFI ラッパーを優先する

```rust
// GOOD — safety comment documents ALL required invariants
let widget: &Widget = {
    // SAFETY: `ptr` is non-null, aligned, points to an initialized Widget,
    // and no mutable references or mutations exist for its lifetime.
    unsafe { &*ptr }
};

// BAD — no safety justification
unsafe { &*ptr }
```

## 依存関係のセキュリティ

- `cargo audit` を実行し、依存関係の既知の CVE をスキャンする
- `cargo deny check` を実行し、ライセンスとアドバイザリーへの準拠を確認する
- `cargo tree` で、推移的な依存関係を監査する
- 依存関係を最新に保つ — Dependabot または Renovate を設定する
- 依存関係の数を最小限にする — 新しいクレートを足す前に評価する

```bash
# Security audit
cargo audit

# Deny advisories, duplicate versions, and restricted licenses
cargo deny check

# Inspect dependency tree
cargo tree
cargo tree -d  # Show duplicates only
```

## エラーメッセージ

- 内部のパス、スタックトレース、データベースのエラーを API レスポンスに含めない
- 詳細なエラーはサーバー側にログし、クライアントには汎用的なメッセージを返す
- 構造化されたサーバー側のログには `tracing` または `log` を使う

```rust
// Map errors to appropriate status codes and generic messages
// (Example uses axum; adapt the response type to your framework)
match order_service.find_by_id(id) {
    Ok(order) => Ok((StatusCode::OK, Json(order))),
    Err(ServiceError::NotFound(_)) => {
        tracing::info!(order_id = id, "order not found");
        Err((StatusCode::NOT_FOUND, "Resource not found"))
    }
    Err(e) => {
        tracing::error!(order_id = id, error = %e, "unexpected error");
        Err((StatusCode::INTERNAL_SERVER_ERROR, "Internal server error"))
    }
}
```

## 参照

unsafe コードのガイドラインと所有権のパターンは、スキル `rust-patterns` を参照してください。
一般的なセキュリティのチェックリストは、スキル `security-review` を参照してください。
