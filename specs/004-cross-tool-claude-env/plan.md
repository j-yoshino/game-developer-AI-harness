# Implementation Plan: Codex・Antigravity を Claude と同じ環境で使えるようにする

**Branch**: `feat/cross-tool-claude-env` | **Date**: 2026-11-15 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/004-cross-tool-claude-env/spec.md`

## Summary

`.claude/` を正本とし、スキル 18、エージェント 9、rules 27、フック 1 を、Codex と Antigravity CLI が読む場所に生成する。方式は、Python の同期スクリプト 1 つ(コピーと変換。`--check` で検査)。Windows の Git は、このリポジトリでシンボリックリンクを使えない(`core.symlinks=false`)ため、リンクでは作らない。ツールが対応しない項目は、無理に作らず、一覧に理由と出典を書く。あわせて、直下の `.claude-plugin/` に `plugin.json` を足す。

## Technical Context

**Language/Version**: Python 3(同期スクリプト)、JSON・TOML(生成する設定)、Markdown(一覧と文書)、Bash(既存のフック)

**Primary Dependencies**: Python 3 の標準ライブラリのみ(`tomllib` は読み取り用のため、TOML は文字列で書き出す)。外部パッケージは使わない

**Storage**: ファイル。正本は `.claude/`、生成物は `.agents/` と `.codex/`

**Testing**: `--check`(正本との一致)、件数、frontmatter の変換結果、`claude plugin validate .`、Claude 側の差分。実機(Codex・Antigravity)は、未導入のためユーザー検収

**Target Platform**: Windows 11(Git Bash、PowerShell)。他の OS での動作は、確認しない

**Project Type**: 開発ハーネスの設定(スクリプトと生成ファイル)

**Performance Goals**: 同期は、数秒以内に終わる(ファイル約 80 件)

**Constraints**:
- `vendor/` は編集しない。
- シンボリックリンクを使わない(`core.symlinks=false`)。
- `.claude/` の中身と Claude 側の動作を変えない。
- 生成物は、手で直さない。直したら、同期で上書きされる。
- rules は英語で書く(`docs/rules-ja/` に訳)。今回は、rules を書き換えない。
- Antigravity の rules は、1 ファイル 24,000 バイトまで、`always_on` 合計 20,000 トークンまで。

**Scale/Scope**: 新規スクリプト 2(同期、Antigravity 向けフック変換)、生成ファイル約 80、更新 2(`AGENTS.md`、直下の `.claude-plugin/`)、一覧 1

## Constitution Check

`.specify/memory/constitution.md` は、テンプレートのままで未記入である。代わりに、`AGENTS.md` と `answer-policy.md` を制約として確認する。

| 制約 | 判定 |
|---|---|
| 計画と実装は spec-kit を正本とする | 適合 |
| 曖昧さが残る間は進まない | 適合。spec の [NEEDS CLARIFICATION] は 0 件。残る未確認点は、research に「未確認」と書き、完了の判定で扱う |
| `vendor/` は編集しない | 適合 |
| rules は英語、訳は `docs/rules-ja/` | 適合(rules は変更しない) |
| 作業ブランチは `develop` から | 適合(`feat/cross-tool-claude-env`) |
| 外向きの操作(push、PR、マージ)は、確認してから | 適合(計画に含めない) |
| 新しいソースファイルの Doxygen ヘッダー | 対象外(C/C++、C#、Rust のみの規則。Python は対象外) |

## Project Structure

### Documentation (this feature)

```text
specs/004-cross-tool-claude-env/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── sync-script.md
│   └── share-matrix.md
├── checklists/requirements.md
└── tasks.md             # /speckit-tasks の出力
```

### Source Code (repository root)

```text
scripts/
└── sync-agent-env.py            # 新規。同期と --check
.claude/                          # 正本(変更しない)
.agents/
├── skills/<name>/                # 生成(スキル 18)
├── agents/<name>.md              # 生成(エージェント 9)
├── rules/<name>.md               # 生成(rules 27)
├── hooks.json                    # 生成(Antigravity 向けフック)
└── hooks/window-reminder-ag.py   # 新規。出力を injectSteps の形に変える
.codex/
├── agents/<name>.toml            # 生成(エージェント 9)
└── hooks.json                    # 生成(Codex 向けフック)
.claude-plugin/
├── marketplace.json              # 既存(変更なし)
└── plugin.json                   # 新規
docs/共有環境/共有の一覧.md          # 新規(置き場は tasks で確定)
AGENTS.md                         # 共有の方法と、rules の案内の節(Codex 向け)を追記
```

**Structure Decision**: 生成物は Git に含める(ツールがファイルを読むため)。正本は `.claude/` だけ。スクリプトは `scripts/` に置く(`.claude/` は、Claude の設定の置き場であり、他のツール向けの道具を置かない)。

## 決めたこと(research から)

- 参照は「生成(コピー)」(R1)。リンクは使わない。
- 既存の ECC 由来の `.agents/rules/` 15 件は、`trigger` が無く、Antigravity に捨てられる見込み。生成物で置き換える(ユーザーが同意済み。R4、R8)。スキル 6 とエージェント 5 は一致しているため、差分は出ない。
- Codex の rules は、生成せず、`AGENTS.md` の案内の節で、`.claude/rules/` を読ませる(ユーザーの指示)。状態は「一部」と明記する。Antigravity のフックは `PreInvocation` で近似し、動作が一致しない可能性を明記する(R5)。
- 直下の `plugin.json` は、置いて検証し、問題があれば置かずに報告する(R6)。

## Complexity Tracking

憲章に違反がないため、記入なし。
