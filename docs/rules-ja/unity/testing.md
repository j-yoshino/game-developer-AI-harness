> 日本語訳(参照用)。原文(英語): `.claude/rules/unity/testing.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `Assets/**/*.{cs,asmdef}`

# Unity テスト

> このファイルは [common/testing.md](../common/testing.md) を Unity 固有の内容で拡張します。

出典(2026-11-15 に読んだ):
- https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/index.html と `.../reference-command-line.html`(制限事項については、ページ本文自体が v1.3.x を指している)
- https://docs.unity.com/en-us/engine/current/manual/unity-editor/command-line-arguments/editor

## フレームワーク
- Unity Test Framework(パッケージ `com.unity.test-framework`、旧 Unity Test Runner): NUnit ベース(ページによると NUnit 3.5)。Edit Mode と Play Mode、および対象プラットフォーム(Standalone、Android、iOS など)でテストできる。Unity 2019.2 以降のプロジェクトに含まれる。
- v1.3.x について挙げられている制限: `UnityTest` は WSA に対応していない、`ValueSource` を除くパラメーター化テストに対応していない、NUnit の `Repeat` に対応していない。ネストされたテストフィクスチャは Editor の UI から実行できない。Play Mode で NUnit の `Retry` を使うと `InvalidCastException` が発生する。
- 読んだページに書かれていないこと: `[Test]` / `[UnityTest]` / `[SetUp]` を使ったテストの書き方、テスト用アセンブリ(asmdef)の作り方、Test Runner ウィンドウ。

## コマンドラインからのテスト実行
```bash
Unity -runTests -batchmode -projectPath <path> -testPlatform EditMode -testResults results.xml
```
- `-testPlatform`: `EditMode`(省略時の既定)、`PlayMode`(Editor 内)、またはビルド済みのプレイヤーで実行する任意の `BuildTarget` の値。`-testResults`: NUnit XML。既定はプロジェクトのルート。
- フィルター: `-testFilter`(名前またはフルネームの正規表現、`;` 区切りは引用符で囲む、`!` で否定)、`-testCategory`、`-assemblyNames`。`-testFilter` と `-testCategory` を併用すると、両方に一致するテストだけが実行される。
- その他: `-runSynchronously`(Edit Mode のみ。`[UnityTest]` のような複数フレームのテストは除外される)、`-testSettingsFile`、`-orderedTestListFile`、`-randomOrderSeed`、`-retry`、`-repeat`、`-playerHeartbeatTimeout`(既定10分)、`-forgetProjectPath`。
- `-runTests` のコマンドに `-quit` を付けない。テストの実行中に付けると、Editor がテストの完了を待たずに即座に終了する(非同期コードの実行中だとアプリケーションがハングすることもある)。非同期タスクの既定の待機時間は300秒(`-quitTimeout` で秒単位に変更できる)。
- すでに別の Editor で開いているプロジェクトは、バッチモードで開けない。
- 終了コード: Unity の各コンポーネントに共通の終了コードの定義はない(エラーメッセージとスタックトレースを読む)。`-batchmode` では、例外、アセットサーバーの更新の失敗、その他の失敗で終了コード 1 になる。成功時の終了コードは書かれていない。
