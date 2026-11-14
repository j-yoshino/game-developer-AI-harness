> 日本語訳(参照用)。原文(英語): `.claude/rules/csharp/hooks.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `**/*.cs`、`**/*.csx`、`**/*.csproj`、`**/*.sln`、`**/Directory.Build.props`、`**/Directory.Build.targets`

# C# フック

> このファイルは [common/hooks.md](../common/hooks.md) を C# 固有の内容で拡張します。

## PostToolUse フック

`~/.claude/settings.json` に設定します。

- **dotnet format**: 編集した C# ファイルを自動整形し、アナライザーの修正を適用する
- **dotnet build**: 編集後も、ソリューションまたはプロジェクトがコンパイルできることを確認する
- **dotnet test --no-build**: 振る舞いを変更した後、最も関係の近いテストプロジェクトを再実行する

## Stop フック

- C# に広範な変更を加えたセッションを終える前に、最後の `dotnet build` を実行する
- `appsettings*.json` が変更されていたら警告し、シークレットがコミットされないようにする
