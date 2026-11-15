# Implementation Plan: 相談役(ゲーム制作の第三者)

**Branch**: `docs/game-advisor-design` | **Date**: 2026-11-15 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/003-game-advisor/spec.md`

**Design source**: [docs/superpowers/specs/2026-11-15-game-advisor-design.md](../../docs/superpowers/specs/2026-11-15-game-advisor-design.md)(承認済みの設計書)

## Summary

抽象的な依頼や、ゲームの体験に関わる変更のとき、別の文脈の相談役(`game-advisor`)を呼び、8つの見方に基づく解釈案と、番号付きの補った点を返させる。ユーザーが合意するまで進まない。合意した補った点は、依頼票(軽作業は納品書の依頼欄)に記録し、納品書で1点ずつ確認でき、検収で覆せる。

方式は、設計書の案 A(別の文脈で動くエージェント。知識は `docs/ゲーム制作/` のファイル)。成果物は、エージェント1つ、知識のファイル(README、見方 8、出典)、窓口の rules・テンプレート・`window-verifier` の更新である。

## Technical Context

**Language/Version**: Markdown(エージェントの定義、rules、知識のファイル、テンプレート)。実行コードはない

**Primary Dependencies**: Claude Code 2.1.233、窓口(spec 001)、確かめる者(spec 002)、任天堂の記事(`docs/ゲーム制作/観点の検証メモ.md` の記事番号)

**Storage**: ファイル(`docs/ゲーム制作/`、依頼票、納品書)

**Testing**: 新しいセッションでの実機検証(quickstart)。自動テストは作らない(助言の質と遵守は、スクリプトでは検査できない)。ただし、機械的に確かめられるもの(ファイルの存在、出典の書式、全文の転記がないこと、個別のソースがないこと)は、タスクの中で、コマンドで確かめる

**Target Platform**: Windows 11、Claude Code のデスクトップアプリと CLI

**Project Type**: 開発ハーネスの設定(エージェント、rules、ドキュメント)

**Performance Goals**: 呼ぶ回数は、依頼1件につき原則 1 回(全案却下のときだけ再び呼ぶ)。軽作業のうち、体験に関わらないものでは呼ばない

**Constraints**:
- サブエージェントの初期コンテキストには、`CLAUDE.md`、`AGENTS.md`、`answer-policy.md` だけが入る。`paths` 付きの rules と、窓口のフックの注入文は届かない(spec 002 research.md R2、R3)。相談役の指示は、自己完結させ、知識のファイルを最初に `Read` させる。
- 呼ぶ指示は `.claude/rules/window.md` に書く。従うかは保証されない(spec の Assumptions)。
- 相談役のファイル書き換えの防止は、`Edit`・`Write`・`Bash`・`Agent` を持たせないことによる。強制の仕組みはない。
- 任天堂の記事は、出典付きの要約のみ。引用は 1 記事から 1 か所、15 語未満。全文を転記しない。
- 桜井さんの動画の二次資料は、個別のソースを、知識のファイルにも相談役の返答にも書かない。内容は、自分の言葉で整理する。
- rules は英語、訳は `docs/rules-ja/`。エージェントの定義も英語で、報告の言語だけ日本語。
- `vendor/` は編集しない。

**Scale/Scope**: 成果物は、エージェント 1、知識のファイル 11(README、見方 8、出典、必要なら補助)、更新 8(下の構成)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

`.specify/memory/constitution.md` は、テンプレートのままで未記入である。代わりに、AGENTS.md と `answer-policy.md` を、実質的な制約として確認する。

| 制約 | 判定 |
|---|---|
| 計画と実装は spec-kit を正本とする。`writing-plans` は使わない | 適合 |
| 曖昧さが残る間は進まない | 適合。spec の [NEEDS CLARIFICATION] は 0 件。SC-008 の基準は、research.md R4 で決める |
| rules は英語、訳は `docs/rules-ja/` | 適合。`window.md` の更新に、訳を含める |
| 作業ブランチは `develop` から切り、`develop` 向けに PR | 適合(`docs/game-advisor-design`) |
| `vendor/` は編集しない | 適合 |
| 著作物の転記をしない | 適合。要約と出典のみ。タスクで、転記がないことを確かめる |
| 新しいソースファイルは、Doxygen 形式のヘッダーを持つ | 対象外。成果物は Markdown |

Phase 1 の設計後の再確認も、同じである(違反なし)。

## Project Structure

### Documentation (this feature)

```text
specs/003-game-advisor/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── delegation-message.md
│   ├── advisor-report.md
│   └── added-points-record.md
└── tasks.md             # /speckit-tasks の出力(この計画では作らない)
```

### Source Code (repository root)

```text
.claude/
├── agents/
│   ├── game-advisor.md           # 相談役(英語)
│   └── window-verifier.md        # 補った点と体感の項目の扱いを追記
└── rules/window.md               # 呼ぶ条件、合意、記録、覆し方を追記
docs/
├── ゲーム制作/
│   ├── README.md                 # 目的、8つの見方、使い方
│   ├── 観点/1-遊びの核.md … 8-時間の速さ.md
│   ├── 出典.md                    # 任天堂の記事の番号・題名・URL・職種・取得日・使った見方
│   └── 観点の検証メモ.md           # 既存
├── rules-ja/window.md            # 上の訳
├── 納品書/_template.md            # 補った点ごとの報告
└── 実装フロー/{概念図,実装フロー}.html   # 相談役の段階と、補った点を覆す戻り
.specify/templates/overrides/spec-template.md   # 「相談役が補った点」の節
AGENTS.md                         # 相談役の説明を追記
```

**Structure Decision**: アプリケーションのコードは作らない。成果物は、エージェントの定義、知識のファイル、rules・テンプレートの更新である。

## Complexity Tracking

憲章に違反がないため、記入なし。
