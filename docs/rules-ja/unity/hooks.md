> 日本語訳(参照用)。原文(英語): `.claude/rules/unity/hooks.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `Assets/**/*.cs`

# Unity フック

> このファイルは [common/hooks.md](../common/hooks.md) を Unity 固有の内容で拡張します。

出典(2026-11-15 に読んだ): https://docs.unity.com/en-us/engine/current/manual/unity-editor/command-line-arguments/editor(および Test Framework のコマンドラインのページ。`testing.md` を参照)

## 自動化のための Editor コマンドライン引数
| 引数 | 意味(ページによる) |
|---|---|
| `-batchmode` | ユーザー操作なしで実行する。ダイアログを抑制し、コンソール出力は最小限(完全なログはログファイルに残る)。すでに別の Editor で開いているプロジェクトは開けない。 |
| `-quit` | 他のコマンドが終わった後に終了する。`-runTests` とは併用しない(テストを待たずに終了する)。 |
| `-nographics` | GPU デバイスを初期化しない(GI のベイクはできない)。ログ出力が無効になるため、`-logFile` と併用する。 |
| `-projectPath <path>` | 指定したパスのプロジェクトを開く(絶対パスでも相対パスでもよい。空白を含むパスは引用符で囲む)。 |
| `-logFile <path>` | Editor のログの出力先。`-` ならコンソールに出す。 |
| `-executeMethod Class.Method` | プロジェクトを開いた後(アセットサーバーの更新後)に static メソッドを実行する。スクリプトは `Editor` フォルダーに置く。引数は `System.Environment.GetCommandLineArgs` で取得する。 |
| `-buildTarget <name>` | アクティブなビルドターゲットを選ぶ(`win64`、`android`、`ios`、`linux64`、`osxuniversal`、`webgl` など)。 |
| `-silent-crashes` | 自動ビルドやテストで、Standalone Player のクラッシュダイアログを表示しない。 |

終了コード: `-batchmode` では、スクリプトの例外、アセットサーバーの更新の失敗、その他の失敗で終了コード 1 になる。`-executeMethod` では、例外で 1 で終了し、`EditorApplication.Exit` を 0 以外のコードで呼べば任意のコードを返せる。ページには、成功時のコードと、`-quit` と `-executeMethod` を組み合わせたときの終了の扱いは書かれていない。

## コミット前のチェック(上の引数から組み立てた例)
```bash
# Edit Mode tests
Unity -runTests -batchmode -projectPath . -testPlatform EditMode -testResults results.xml -logFile -
# Custom build/validation entry point
Unity -batchmode -quit -projectPath . -executeMethod BuildScripts.Validate -logFile -
```
これらのコマンドは、文書化された引数から組み立てたもので、このリポジトリでは**まだ実行していない**(Unity のプロジェクトがまだなく、`BuildScripts.Validate` は仮の名前)。

## 書かれていないこと
ここで読んだ Unity の公式ページには、Claude Code の `PostToolUse` フックで使うフォーマッターやリンターのコマンドは書かれていない。プロジェクトが採用する `.editorconfig` やアナライザーの設定を使う。

## C# のフックから
`.claude/rules/csharp/hooks.md` は、`dotnet format`、`dotnet build`、`dotnet test --no-build` を `PostToolUse` フックとして挙げている。これらが Unity が生成するプロジェクトで動くかは確認していないため、頼らない。上の Unity のバッチモードのコマンドを使う。
