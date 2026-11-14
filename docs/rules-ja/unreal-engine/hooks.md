> 日本語訳(参照用)。原文(英語): `.claude/rules/unreal-engine/hooks.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `Source/**/*.{h,cpp,cs}`、`Plugins/**/Source/**/*.{h,cpp,cs}`

# Unreal Engine フック

> このファイルは [common/hooks.md](../common/hooks.md) を Unreal Engine 固有の内容で拡張します。

出典(2026-11-15 に読んだ):
- https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-build-tool-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/running-gauntlet-tests-in-unreal-engine

## ビルドシステムについての事実
- UnrealBuildTool(UBT)は、エンジンとプロジェクトを、さまざまな構成でビルドする。各モジュールには `.build.cs` があり、モジュールの依存関係、追加のライブラリ、インクルードパスを制御する。モジュールは、既定では DLL にコンパイルされ、1つの実行ファイルから読み込まれる。`BuildConfiguration.cs` は、ユーザーが構成できるオプション(たとえばモノリシックな実行ファイル)を持つ。
- ビルドは IDE のプロジェクトファイルとは独立して実行される。エンジンのルートにある `GenerateProject.bat` で `.sln` / `.vcproj` ファイルを再生成する。ソースファイルを追加・削除したときは、再実行する。
- 読んだページに書かれていないこと: `.Target.cs`、UBT のコマンドライン例(`Build.bat`、`RunUBT`)、UBT と `.uproject` の関係。UBT のコマンドラインを自分で作らない。使うエンジンのバージョンの Targets と Unreal Automation Tool のページで確認する。

## コミット前のチェック(文書化されたコマンドから組み立てた例)
```bash
# Automation tests from the Editor binary
<Editor executable> <project>.uproject -ExecCmds="Automation RunTest Group:MyGroup;Quit" -ReportExportPath="Saved/AutomationReports"
# CI wrapper (Gauntlet)
RunUAT.bat RunUnreal -test=UE.EditorAutomation -runtest=MyTest.One -project=<path to .uproject> -build=editor
```
これらのコマンドは、上に挙げたページから組み立てたもので、このリポジトリでは**まだ実行していない**(Unreal のプロジェクトがまだなく、`Group:MyGroup`、`MyTest.One`、Editor の実行ファイル名は仮のもの)。

## 書かれていないこと
読んだ公式ページには、Claude Code の `PostToolUse` フックで使う C++ のフォーマッターやリンターのコマンドは書かれていない。Epic の標準(`coding-style.md` を参照)を強制する、文書化されたツールは、読んだページにはない。

## C++ のフックから
- `.claude/rules/cpp/hooks.md` の CMake と CTest のコマンドは適用されない。読んだ Unreal のページは、ビルドシステムとして UnrealBuildTool を説明している。
- Unreal のコードに、既定のスタイルで `clang-format` を実行しない(`cpp/coding-style.md` は、設定なしの `clang-format -i` を勧めている)。Epic 形式のコード(タブ、Allman 形式の波かっこ)が書き換わってしまう。`coding-style.md` に合わせた設定が必要になる。Epic がそのような設定を提供しているかは確認していない。
