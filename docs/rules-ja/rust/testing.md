> 日本語訳(参照用)。原文(英語): `.claude/rules/rust/testing.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `**/*.rs`

# Rust テスト

> このファイルは [common/testing.md](../common/testing.md) を Rust 固有の内容で拡張します。

## テストフレームワーク

- 単体テストには、`#[cfg(test)]` モジュールと **`#[test]`**
- パラメーター化テストとフィクスチャには **rstest**
- プロパティベーステストには **proptest**
- トレイトベースのモックには **mockall**
- 非同期テストには **`#[tokio::test]`**

## テストの構成

```text
my_crate/
├── src/
│   ├── lib.rs           # Unit tests in #[cfg(test)] modules
│   ├── auth/
│   │   └── mod.rs       # #[cfg(test)] mod tests { ... }
│   └── orders/
│       └── service.rs   # #[cfg(test)] mod tests { ... }
├── tests/               # Integration tests (each file = separate binary)
│   ├── api_test.rs
│   ├── db_test.rs
│   └── common/          # Shared test utilities
│       └── mod.rs
└── benches/             # Criterion benchmarks
    └── benchmark.rs
```

単体テストは、同じファイル内の `#[cfg(test)]` モジュールに置きます。統合テストは `tests/` に置きます。

## 単体テストのパターン

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn creates_user_with_valid_email() {
        let user = User::new("Alice", "alice@example.com").unwrap();
        assert_eq!(user.name, "Alice");
    }

    #[test]
    fn rejects_invalid_email() {
        let result = User::new("Bob", "not-an-email");
        assert!(result.is_err());
        assert!(result.unwrap_err().to_string().contains("invalid email"));
    }
}
```

## パラメーター化テスト

```rust
use rstest::rstest;

#[rstest]
#[case("hello", 5)]
#[case("", 0)]
#[case("rust", 4)]
fn test_string_length(#[case] input: &str, #[case] expected: usize) {
    assert_eq!(input.len(), expected);
}
```

## 非同期テスト

```rust
#[tokio::test]
async fn fetches_data_successfully() {
    let client = TestClient::new().await;
    let result = client.get("/data").await;
    assert!(result.is_ok());
}
```

## mockall によるモック

トレイトは本番コードに定義し、モックはテストモジュールで生成します。

```rust
// Production trait — pub so integration tests can import it
pub trait UserRepository {
    fn find_by_id(&self, id: u64) -> Option<User>;
}

#[cfg(test)]
mod tests {
    use super::*;
    use mockall::predicate::eq;

    mockall::mock! {
        pub Repo {}
        impl UserRepository for Repo {
            fn find_by_id(&self, id: u64) -> Option<User>;
        }
    }

    #[test]
    fn service_returns_user_when_found() {
        let mut mock = MockRepo::new();
        mock.expect_find_by_id()
            .with(eq(42))
            .times(1)
            .returning(|_| Some(User { id: 42, name: "Alice".into() }));

        let service = UserService::new(Box::new(mock));
        let user = service.get_user(42).unwrap();
        assert_eq!(user.name, "Alice");
    }
}
```

## テストの命名

シナリオが分かる、説明的な名前を付けます。
- `creates_user_with_valid_email()`
- `rejects_order_when_insufficient_stock()`
- `returns_none_when_not_found()`

## カバレッジ

- 行カバレッジ 80% 以上を目標にする
- カバレッジの報告には **cargo-llvm-cov** を使う
- ビジネスロジックに集中する — 生成コードと FFI バインディングは除外する

```bash
cargo llvm-cov                       # Summary
cargo llvm-cov --html                # HTML report
cargo llvm-cov --fail-under-lines 80 # Fail if below threshold
```

## テストのコマンド

```bash
cargo test                       # Run all tests
cargo test -- --nocapture        # Show println output
cargo test test_name             # Run tests matching pattern
cargo test --lib                 # Unit tests only
cargo test --test api_test       # Specific integration test (tests/api_test.rs)
cargo test --doc                 # Doc tests only
```

## 参照

プロパティベーステスト、フィクスチャ、Criterion によるベンチマークを含む包括的なテストパターンは、スキル `rust-testing` を参照してください。
