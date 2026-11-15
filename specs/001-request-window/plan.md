# Implementation Plan: 窓口(依頼の受付・判定・納品)

**Branch**: `docs/window-design` | **Date**: 2026-11-15 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-request-window/spec.md`

**Design source**: [docs/superpowers/specs/2026-11-15-window-design.md](../../docs/superpowers/specs/2026-11-15-window-design.md)(承認済みの設計書)

## Summary

ユーザーのどの発言にも、最初に「窓口」が動くようにする。作業を求めない発言(質問)は、層を判定せず、質問用のスキルが答える。作業の依頼は、窓口が軽作業・本件に判定し、層ごとの手続きに回し、完了後に納品書を `docs/納品書/` に残す。

方式は、設計書の案 A である。窓口の手順を常時読み込みの rules に書き、UserPromptSubmit フックが毎ターン短い注意を注入する。質問は専用スキル、軽作業と本件は brainstorming と spec-kit、納品書はテンプレートで書式を固定する。遵守は保証されないため、新しいセッションでの実際の挙動で確かめる。

## Technical Context

**Language/Version**: Markdown(rules、スキル、テンプレート)と bash(フックのスクリプト1本)

**Primary Dependencies**: Claude Code 2.1.233(インストール済み)、Git Bash(このマシンにある)、spec-kit 1.2.1、superpowers 7.0.2(brainstorming、systematic-debugging、test-driven-development、verification-before-completion)

**Storage**: ファイル(`docs/納品書/` の Markdown)

**Testing**: (1) フックのスクリプトに JSON を流して出力を確認する。(2) 新しいセッションで、検証用の発言を入力して挙動を確認する。自動テストは作らない(挙動の遵守は、スクリプトでは検査できない)

**Target Platform**: Windows 11、Claude Code のデスクトップアプリと CLI

**Project Type**: 開発ハーネスの設定(rules、フック、スキル、テンプレート)。アプリケーションのコードではない

**Performance Goals**: フックは毎ターン発火する。タイムアウトの既定は 30 秒。実行は 1 秒未満にする

**Constraints**:
- 毎ターン注入する文は短くする(トークン量を含む。SC-006)。
- `window.md` は 200 行未満(公式の目安。長いと遵守率が下がる)。
- rules は英語で書き、日本語訳を `docs/rules-ja/` に置く(AGENTS.md)。
- `vendor/` 配下のファイルは編集しない(submodule)。
- 遵守は保証されない。強制する手段は、第1版にはない。

**Scale/Scope**: 成果物は9つ(下の構成を参照)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

`.specify/memory/constitution.md` は、テンプレートのままで未記入である。憲章に定められた原則がないため、憲章によるゲートはない。代わりに、AGENTS.md と `.claude/rules/answer-policy.md` を、このリポジトリの実質的な制約として確認する。

| 制約 | 判定 |
|---|---|
| 計画と実装は spec-kit を正本とする。`writing-plans` は使わない | 適合。この計画は `/speckit-plan` で書く |
| 曖昧さが残る間は進まない(answer-policy) | 適合。spec の [NEEDS CLARIFICATION] は0件。研究で出た未検証は、タスクで検証する |
| rules は英語、日本語訳は `docs/rules-ja/` | 適合。成果物に訳を含める |
| 作業ブランチは `develop` から切り、`develop` 向けに PR | 注意。`docs/window-design` は `develop` から切ったブランチ(適合) |
| `vendor/` は編集しない | 適合。編集対象は `.claude/`、`.specify/templates/overrides/`、`docs/`、`AGENTS.md` のみ |

Phase 1 の設計後に再確認した結果も、同じである(違反なし)。

## Project Structure

### Documentation (this feature)

```text
specs/001-request-window/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── hook-io.md
│   ├── request-form.md
│   └── delivery-note.md
└── tasks.md             # /speckit-tasks の出力(この計画では作らない)
```

### Source Code (repository root)

```text
.claude/
├── rules/window.md                       # 窓口の手順の本体(英語、paths なし)
├── hooks/window-reminder.sh              # 毎ターンの注意を注入する bash スクリプト
├── skills/window-question/SKILL.md       # 質問への回答の手順
└── settings.local.json                   # hooks の登録を追加
.specify/templates/overrides/spec-template.md   # 依頼票の節を足した spec テンプレート
docs/
├── 納品書/_template.md                    # 納品書のテンプレート
└── rules-ja/window.md                    # window.md の日本語訳
AGENTS.md                                 # 窓口の説明を追記
```

**Structure Decision**: アプリケーションの `src/` や `tests/` は作らない。成果物はすべて設定とドキュメントである。spec テンプレートの変更は、spec-kit の更新で上書きされない `.specify/templates/overrides/` に置く(research.md の R5)。

## Complexity Tracking

憲章に違反がないため、記入なし。
