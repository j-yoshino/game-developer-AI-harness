> 日本語訳(参照用)。原文(英語): `.claude/rules/unreal-engine/testing.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `Source/**/*.{h,cpp,cs}`、`Plugins/**/Source/**/*.{h,cpp,cs}`

# Unreal Engine テスト

> このファイルは [common/testing.md](../common/testing.md) を Unreal Engine 固有の内容で拡張します。

出典(2026-11-15 に読んだ):
- https://dev.epicgames.com/documentation/unreal-engine/write-cplusplus-tests-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/running-gauntlet-tests-in-unreal-engine

## C++ の Automation テストを書く
- Simple Test: 1つの原子的なテスト。`IMPLEMENT_SIMPLE_AUTOMATION_TEST(TClass, PrettyName, TFlags)` で宣言し、`RunTest` を実装する(`GetTests` は生成される)。
- Complex Test: 同じコードを多くの入力で実行する(たとえばすべてのマップのロード)。`IMPLEMENT_COMPLEX_AUTOMATION_TEST` で宣言し、`RunTest` と `GetTests` の両方を実装する。
- Latent コマンドは、処理を複数フレームに分ける: `DEFINE_LATENT_AUTOMATION_COMMAND`(または `..._ONE_PARAMETER`)で定義し、`Update` が完了時に `true` を返す。キューには `ADD_LATENT_AUTOMATION_COMMAND` を使う。
- `PrettyName` はドット区切りの階層("Group.Subgroup.Test")。`TFlags` は `EAutomationTestFlags` の組み合わせ(ページの例では `EditorContext`、`EngineFilter`、`ATF_Game` を使っているが、意味はそこでは説明されていない)。テストの成否は、`RunTest` が返す bool で決まる。
- テストのソースはモジュールの `Private/Tests` フォルダーに置く。1つのクラスに対するテストは `[ClassFilename]Test.cpp` と名付ける。
- 読んだページに書かれていないこと: `TestTrue` / `TestEqual` のようなアサーションのヘルパー、Spec テストと Functional テスト、フラグの意味。

## テストの実行
- Editor: Functional Testing Editor と、テストを含むプラグインを有効にして再起動し、**Tools > Test Automation** を開く。Session Frontend の Automation タブでテストを選び、**Start Tests** をクリックする。Session Frontend は、ほかの実行中の Editor / Client のインスタンスも操作できる(ネットワークテスト)。テストはクライアント専用にできる。
- コマンドライン(Editor または Client の実行ファイル):
```bash
-ExecCmds="Automation RunTest Test1+Test2;Quit"
-ExecCmds="Automation RunTest MySet.MySubSet;Quit"
-ExecCmds="Automation RunTest Group:MyGroup;Quit"
-ReportExportPath="<output path>"   # JSON plus HTML report files
-ResumeRunTest                      # with -ReportExportPath: resume at the first not-run test; in-progress tests count as failures
```
- Gauntlet(`RunUAT.bat RunUnreal`)を使った CI: `-test=UE.EditorAutomation`(Editor)または `UE.TargetAutomation`(クライアント/パッケージ済みゲーム)、`-runtest=<test>`、`-project=<.uproject>`、`-build=editor|<packaged path>`、必要に応じて `-platform`、`-device`、`-configuration`。`-ResumeOnCriticalFailure` を付けると、UE.Automation はクラッシュの後に最大3回まで再開できる。ページは結果の保存先を述べていない。
- 読んだページは `-unattended`、`-NullRHI`、`-nosplash`、`-testexit` を扱っていない。コミュニティの情報源には `RunTests` を使うものがあるが、公式ページは `RunTest` を使っている。

## C++ のテストのルールから
- `.claude/rules/cpp/testing.md` は、GoogleTest、CMake/CTest、lcov を前提にしている。読んだ Unreal のページは代わりに Automation フレームワークを使っているため、これらのコマンドはここでは適用されない。
- テストには、`PrettyName` の `Group.Subgroup.Test` の階層の中で、振る舞いで名前を付ける。
- Unreal では未検証: カバレッジのツール、および `cpp/testing.md` が挙げる AddressSanitizer/UBSan の設定。
