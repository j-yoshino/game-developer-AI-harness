# Implementation Plan: main 用の構成を組み立てる変換ブランチ

**Branch**: `feat/plugin-conversion` | **Date**: 2026-11-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/006-plugin-conversion-branch/spec.md`

## Summary

`develop` の、ツールごとに独立した正本(Claude は `.claude/`、Codex は `.codex/`・`.agents/`、Antigravity は `.agents/`)から、`main` に出す最小の構成を、スクリプトで組み立てる(`scripts/build-main.py`)。結果は、ローカルの変換ブランチにコミットする(`scripts/publish-main-branch.py`。push しない)。自作のものは、プラグインに変換せず、リポジトリ直下の `.claude/`・`.codex/`・`.agents/` に置いたまま出す。外部プラグイン(superpowers、Unity、i-have-adhd)は、`vendor/` に同梱せず、ツールごとの導入の設定(Claude: `.claude/settings.json`、Codex: `.agents/plugins/marketplace.json`、Antigravity: 手順書)で別導入にする。Unreal は、`vendor/` に残す。同じ作業の中で、004・005 の同期スクリプトを廃止し、`.agents/`・`.codex/` を、独立した正本にする。

## Technical Context

**Language/Version**: Python 3(スクリプト)、JSON・Markdown(テンプレート)

**Primary Dependencies**: Python の標準ライブラリのみ。`git`(`ls-files`、`worktree`)。Claude Code(`claude plugin validate`)

**Storage**: ファイル。元は、`git ls-files` の追跡済みのファイルと、`scripts/templates/`

**Testing**: 決定性(2 回の出力の比較)、`--check`、ファイル一覧(含める・含めない)、個人のパスの不在、JSON の妥当性、`claude plugin validate`。実機は、ユーザー検収

**Target Platform**: Windows 11(Git Bash)。Claude Code 2.1.233

**Constraints**:
- `develop` の正本と `vendor/` を書かない。
- 変換ブランチの中身を、手で直さない。
- `main` への push・マージは、スクリプトに含めない。
- 公式で確認できなかった点は、「未確認」と書き、推測で埋めない。
- 日本語を含む絶対パスを、外部コマンドに渡さない。
- 出力に、個人の設定・このマシンの絶対パスを入れない。

**Scale/Scope**: 新規スクリプト 2、テンプレート 5、削除 1(`scripts/sync-agent-env.py`)、編集: `.agents/`・`.codex/` の 46 ファイル(コメントの削除)、`AGENTS.md`、共有の一覧、環境構築の文書

## Constitution Check

`.specify/memory/constitution.md` は、テンプレートのままで未記入。`AGENTS.md` と `answer-policy.md` を制約として確認する。

| 制約 | 判定 |
|---|---|
| 計画と実装は spec-kit を正本とする | 適合 |
| 曖昧さが残る間は進まない | 適合。未確認の点は、research と spec に書いた |
| `vendor/` は編集しない | 適合(読むだけ) |
| 外向きの操作(push、PR、マージ)は、確認してから | 適合(スクリプトに含めない) |
| 作業ブランチは `develop` から | 適合(`feat/plugin-conversion`) |
| rules は英語、訳は `docs/rules-ja/` | 適合(rules は変更しない) |

## Project Structure

### Documentation (this feature)

```text
specs/006-plugin-conversion-branch/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/build-main.md
├── checklists/requirements.md
└── tasks.md            # /speckit-tasks の出力
```

### Source Code (repository root)

```text
scripts/
├── build-main.py                  # 新規: main に出す構成を組み立てる
├── publish-main-branch.py         # 新規: ローカルの変換ブランチにコミットする(push しない)
├── templates/                     # 新規: main-AGENTS.md、main-CLAUDE.md、main-README.md、main-claude-settings.json、main-codex-marketplace.json
└── sync-agent-env.py              # 削除(004・005 の同期の廃止)
.agents/・.codex/                  # 編集: 「generated from …」コメントの削除(46 ファイル)
AGENTS.md                          # 編集: 同期の記述を直す。変換ブランチの説明を足す
docs/共有環境/共有の一覧.md          # 編集: 同期の記述を直す
docs/共有環境/環境構築.md            # 編集: sync-agent-env.py への言及を直す
```

**Structure Decision**: 組み立てた出力は、`develop` にコミットしない(出力先は、リポジトリの外、または変換ブランチ)。`develop` に足すのは、スクリプト、テンプレート、文書のみ。

## 決めたこと(research から)

- 元は、`git ls-files` の追跡済みのファイル。許可リスト方式(一覧にないものは、出力に入れない)。ローカルの状態(`.claude/ecc/`、`.agents/ecc-install-state.json`、`.agents/plugins/superpowers/`)は、自然に除かれる(R2)。
- `main` 用の `.claude/settings.json` を、テンプレートから出力する。窓口のフック(`UserPromptSubmit`)の登録と、外部プラグインのマーケットプレイス・有効化を書き、個人の設定は書かない(R3)。
- Codex の外部プラグインは、`main` 用の `.agents/plugins/marketplace.json`(Git の URL)で指す。Antigravity は、README の手順(`agy plugin install`、IDE は手でフォルダを置く)(R1)。
- Unreal は、`vendor/` の submodule と、`.claude-plugin/marketplace.json` のまま出す(R1)。
- 同期の廃止: `sync-agent-env.py` の削除、「generated from」コメントの削除、文書の修正。過去の納品書と過去の spec は、直さない(R4)。
- 変換ブランチは、毎回、`develop` から生成し直す(R5)。名前は `main-build`(仮)。

## ユーザーに確認して、決まったこと(2026-11-17)

1. 変換ブランチの名前は、`main-build`(仮)。ユーザーが了承。
2. `main` 用の `.claude/settings.json` には、`language` などの個人の設定を、**含めない**。ユーザーが「コメントアウトはできないか」と聞いたが、`settings.json` は、コメントを受け付けない(公式の設定の例のページは、「コメントつきの例は、読むための例で、Claude Code は設定ファイルのコメントを受け付けない」と書いている。コミュニティの報告では、コメントや末尾のカンマがあると、構文エラーになるか、ファイルが警告なしで無視される。JSONC 対応の要望はあるが、出荷されたかは未確認)。コメントを入れると、設定全体(窓口のフックを含む)が、無効になる恐れがある。代わりに、README に、利用者が自分の `.claude/settings.local.json` に足す設定(例: `language`)の、コピーできる例を書く。
3. `.gitignore` は、`main` に含めない(`.agents/plugins/superpowers/` の除外は、`develop` だけの話)。ユーザーが了承。

## Complexity Tracking

憲章に違反がないため、記入なし。
