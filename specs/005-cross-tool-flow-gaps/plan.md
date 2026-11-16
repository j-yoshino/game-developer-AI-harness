# Implementation Plan: Codex・Antigravity での実装フローの穴を塞ぐ

**Branch**: `feat/cross-tool-flow-gaps` | **Date**: 2026-11-16 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/005-cross-tool-flow-gaps/spec.md`

## Summary

前回(004)の同期の仕組みを広げて、3 つの穴を塞ぐ。(1) `AGENTS.md` に、Claude 固有の道具の読み替え表を足す(`.claude/` は変えない)。(2) 相談役の読み取り専用の制限を、Antigravity は `tools` の変換で、Codex は指示と手順で扱い、できない部分は共有の一覧に明記する。(3) superpowers を、環境構築方式(プラグインとして導入)で両ツールに入れる。手順書(`docs/共有環境/環境構築.md`)と、Antigravity IDE 向けの配置スクリプト(プロジェクト単位)を作る。Codex は、アプリのサイドバーから、ユーザーが導入する。スキルのコピーは、しない(ユーザーの指示)。調査の途中で、前回の生成物の不具合の可能性も見つかった(Antigravity のエージェントの `tools` と `model` の名前が、Claude のままコピーされている)。これも同じ変更で直す。

## Technical Context

**Language/Version**: Python 3(`scripts/sync-agent-env.py` の拡張)、Markdown

**Primary Dependencies**: なし(標準ライブラリのみ)。公式ドキュメントの確認結果(research.md)

**Storage**: ファイル。正本は `.claude/` と `vendor/superpowers/skills/`(読み取りのみ)

**Testing**: `--check`、frontmatter の変換結果の確認、孤児の削除、コピーの件数と名前の重なり、`.claude/`・`vendor/` の差分 0。実機は、ユーザー検収

**Target Platform**: Windows 11。実機は、Codex アプリと Antigravity IDE(ユーザーのマシンに導入済み)

**Project Type**: 開発ハーネスの設定(スクリプトと生成ファイル、文書)

**Constraints**:
- `.claude/` と `vendor/` を編集しない。
- 生成物は手で直さない。
- 外部のプラグインを、確認なしに導入しない。
- 公式で確認できなかった対応は、「未確認」と書く(推測で埋めない)。

**Scale/Scope**: 更新 3(`scripts/sync-agent-env.py`、`AGENTS.md`、`docs/共有環境/共有の一覧.md`)、新規 2(`scripts/setup-antigravity-plugins.py`、`docs/共有環境/環境構築.md`)、更新 1(`.gitignore`)、生成物の変化: `.agents/agents/` 9 件の書き換え、`.codex/agents/` の読み取り専用の注意

## Constitution Check

`.specify/memory/constitution.md` は、テンプレートのままで未記入。`AGENTS.md` と `answer-policy.md` を制約として確認する。

| 制約 | 判定 |
|---|---|
| 計画と実装は spec-kit を正本とする | 適合。プラグインに `writing-plans` などが含まれるが、「使わない」方針は指示で守らせる(Claude と同じ) |
| 曖昧さが残る間は進まない | 適合。残る未確認点は、research に「未確認」と書き、共有の一覧に載せる |
| `vendor/` は編集しない | 適合(読むだけ) |
| 外向きの操作は確認してから | 適合。配置はリポジトリの中(`.agents/plugins/`)で、ホームは変えない。Codex の導入は、ユーザーが操作する |
| 作業ブランチは `develop` から | 適合 |

## Project Structure

### Documentation (this feature)

```text
specs/005-cross-tool-flow-gaps/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/sync-script-changes.md
├── checklists/requirements.md
└── tasks.md            # /speckit-tasks の出力
```

### Source Code (repository root)

```text
scripts/sync-agent-env.py     # 拡張: エージェントの変換、読み取り専用の注意
scripts/setup-antigravity-plugins.py   # 新規: superpowers を .agents/plugins/superpowers/ へ置く(--dry-run あり)
.gitignore                    # 更新: .agents/plugins/superpowers/ を追跡しない
docs/共有環境/環境構築.md        # 新規: Codex と Antigravity IDE への superpowers の導入手順
AGENTS.md                     # 「道具名の読み替え表」の節を追加
docs/共有環境/共有の一覧.md     # 更新: 読み取り専用の可否、superpowers、変換できなかった項目
.agents/agents/               # 再生成(frontmatter の変換)
.codex/agents/                # 読み取り専用の注意を追加
```

**Structure Decision**: 新しいファイルは作らない。前回の仕組みに足す。

## 決めたこと(research から)

- 読み替え表は、`AGENTS.md` の中に置く(R6)。
- Codex のエージェントは、読み取り専用にできない(公式)。指示と、親の設定の手順で扱う(R4)。
- Antigravity のエージェントの frontmatter は、変換する。これにより、既存の ECC 由来の 5 件の内容も変わる(004 の rules と同じ扱い)。
- superpowers は、環境構築方式で入れる(ユーザーの指示。コピーはしない)。Codex は、アプリのサイドバーからユーザーが導入する。Antigravity IDE は、プロジェクトの `.agents/plugins/superpowers/` へ置く(プロジェクト単位。Git では追跡しない)(R5)。

## Complexity Tracking

憲章に違反がないため、記入なし。
