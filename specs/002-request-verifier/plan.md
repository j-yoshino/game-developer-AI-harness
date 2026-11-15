# Implementation Plan: 確かめる者(作られたものの独立した検査)

**Branch**: `docs/verifier-design` | **Date**: 2026-11-15 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/002-request-verifier/spec.md`

**Design source**: [docs/superpowers/specs/2026-11-15-verifier-design.md](../../docs/superpowers/specs/2026-11-15-verifier-design.md)(承認済みの設計書)

## Summary

本件の完了前と、コードやテストを変えた軽作業の完了前に、別の文脈の検査役(確かめる者)を呼ぶ。確かめる者は、納品書の主張を完了の判定に照合し、「確認していないこと」の抜けを指摘し、確認方法を最大3つ再実行し、変更ファイルの種類に応じた言語・エンジン別のレビューを入れ子で呼ぶ。報告は、納品書の末尾に、全文で追記する。

方式は、設計書の案 1(証拠を必須にし、独立した検査は判断が要る部分に絞る)と案 A(確かめる者が入れ子でレビューを呼ぶ)。成果物は、カスタムエージェント3つ(`window-verifier`、`unity-reviewer`、`unreal-reviewer`)、窓口の rules と納品書テンプレートの更新である。

## Technical Context

**Language/Version**: Markdown(カスタムエージェントの定義、rules、テンプレート)。実行コードはない

**Primary Dependencies**: Claude Code 2.1.233、既存のレビュー用エージェント(`cpp-reviewer`、`csharp-reviewer`、`rust-reviewer`)、窓口(spec 001)

**Storage**: ファイル(納品書 `docs/納品書/*.md`)

**Testing**: 新しいセッションでの実機検証(quickstart のシナリオ)。自動テストは作らない(遵守と判定の質は、スクリプトでは検査できない)

**Target Platform**: Windows 11、Claude Code のデスクトップアプリと CLI

**Project Type**: 開発ハーネスの設定(エージェント、rules、テンプレート)

**Performance Goals**: 1回の検査で、再実行は最大3つ、レビューは変更の言語の数だけ。軽作業のドキュメントだけの変更では、検査を呼ばない

**Constraints**:
- サブエージェントの初期コンテキストには、`CLAUDE.md`、`AGENTS.md`、`answer-policy.md` だけが入る。`paths` 付きの rules と、窓口のフックの注入文は届かない(research.md R2、R3)。確かめる者とレビューの指示は、自己完結させる。
- 報告の長さの上限は未検証。報告は 150 行以内を目安にする(私の判断)。
- 検査役の書き込みの防止は、`Edit` と `Write` を持たせないことと、指示による。強制はしない(spec の Assumptions)。
- rules は英語、日本語訳は `docs/rules-ja/`。エージェントの定義も、既存と同じく英語で書き、報告の言語だけ日本語にする。
- `vendor/` は編集しない。

**Scale/Scope**: 成果物は8つ(下の構成を参照)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

`.specify/memory/constitution.md` は、テンプレートのままで未記入である。憲章による原則はない。代わりに、AGENTS.md と `answer-policy.md` を、実質的な制約として確認する。

| 制約 | 判定 |
|---|---|
| 計画と実装は spec-kit を正本とする。`writing-plans` は使わない | 適合 |
| 曖昧さが残る間は進まない | 適合。spec の [NEEDS CLARIFICATION] は 0 件。未検証は、タスクで検証する |
| rules は英語、訳は `docs/rules-ja/` | 適合。`window.md` の更新に、訳を含める |
| 作業ブランチは `develop` から切り、`develop` 向けに PR | 適合(`docs/verifier-design`) |
| `vendor/` は編集しない | 適合 |
| 新しいソースファイルは、Doxygen 形式のヘッダーを持つ | 対象外。成果物は Markdown で、C++・C#・Rust・Unity・Unreal のソースではない |

Phase 1 の設計後の再確認も、同じである(違反なし)。

## Project Structure

### Documentation (this feature)

```text
specs/002-request-verifier/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── delegation-message.md
│   ├── verification-report.md
│   └── reviewer-routing.md
└── tasks.md             # /speckit-tasks の出力(この計画では作らない)
```

### Source Code (repository root)

```text
.claude/
├── agents/
│   ├── window-verifier.md        # 確かめる者(英語)
│   ├── unity-reviewer.md         # Unity のレビュー(英語)
│   └── unreal-reviewer.md        # Unreal のレビュー(英語)
└── rules/window.md               # 検査の経路を追記
docs/
├── rules-ja/window.md            # 上の訳
└── 納品書/_template.md            # 証拠の必須化、「確かめる者の報告」の節
AGENTS.md                         # 確かめる者の説明を追記
docs/実装フロー/実装フロー.html      # 確かめる者の段階を追記
```

**Structure Decision**: アプリケーションのコードは作らない。成果物は、エージェントの定義と、rules・テンプレートの更新である。レビュー用エージェントの置き場所は、既存と同じ `.claude/agents/`。

## Complexity Tracking

憲章に違反がないため、記入なし。
