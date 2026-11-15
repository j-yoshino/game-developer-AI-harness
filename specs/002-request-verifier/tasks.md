---

description: "確かめる者のタスク一覧"
---

# Tasks: 確かめる者(作られたものの独立した検査)

**Input**: Design documents from `/specs/002-request-verifier/`

**Prerequisites**: plan.md、spec.md、research.md、data-model.md、contracts/(delegation-message.md、verification-report.md、reviewer-routing.md)、quickstart.md

**Tests**: 自動テストは作らない(plan.md の Testing。検査の質と遵守は、スクリプトでは検査できない)。代わりに、静的な確認(定義の書式、言語、行数)と、quickstart のシナリオによる実機検証を行う。**新しいセッションが要る検証は、ユーザーの手が必要**で、`(ユーザー)` と付けた。

**Organization**: タスクはユーザーストーリーごとにまとめた。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 並行して進められる(別のファイルで、未完了のタスクに依存しない)
- **[Story]**: US1(本件の検査)、US2(軽作業の検査の判定)、US3(納品書の抜けの指摘)、US4(言語・エンジン別のレビュー)、US5(差し戻しと上限)

## 共通の注意

- `.claude/agents/*.md` と `.claude/rules/window.md` は、英語で書く。検査の報告の言語だけ、日本語にする(報告の形式は contracts/verification-report.md)。日本語を含めてよいのは、`docs/納品書` のパスと、報告の形式の例(日本語の見出し)だけ。
- `window.md` を編集したら、同じ変更で `docs/rules-ja/window.md` の日本語訳も更新する。
- `window.md` と `window-verifier.md` は、複数のストーリーが同じファイルに追記するため、同じファイルを編集するタスクは、順に行う([P] を付けない)。
- サブエージェントの初期コンテキストには、`paths` 付きの rules と窓口の注入文が届かない(research.md R2、R3)。エージェントの指示は、自己完結させる。
- `Edit` と `Write` は、検査役とレビュー用エージェントの `tools` に含めない。
- `vendor/` 配下は編集しない。

---

## Phase 1: Setup

- [ ] T001 既存のレビュー用エージェント(`.claude/agents/cpp-reviewer.md`、`csharp-reviewer.md`、`rust-reviewer.md`)の frontmatter と見出しの形を読み、新しいエージェントの書式(`name`、`description`、`tools`、`model`、重大度の段階、変更の取り方)を、メモとして、`specs/002-request-verifier/research.md` の末尾に追記する

---

## Phase 2: Foundational(全ストーリーの前提)

**Purpose**: 検査役の骨格と、納品書の書式と、窓口の共通の手順。これが無いと、どのストーリーも動かない。

- [ ] T002 [P] `docs/納品書/_template.md` を更新する(data-model.md「納品書(拡張)」): 「確認した方法」を **「コマンドと出力(要点)を書く。コマンドを持たない確認(目視など)は、その旨を書く」** とテンプレート内に明記する。末尾に「確かめる者の報告」の節を足し、検査を通したときは報告の全文を貼る、通さないときは「検査不要: <理由>」の1行を書く、と注記する
- [ ] T003 `.claude/agents/window-verifier.md` を英語で作る(contracts/delegation-message.md、contracts/verification-report.md)。frontmatter: `name: window-verifier`、`description`(委任メッセージを受けて、作られたものを別の文脈で検査する、と書く。「use proactively」は書かない)、`tools: Read, Grep, Glob, Bash, Agent`(`Edit` と `Write` は含めない)、`model: sonnet`。本文: 役割、入力(委任メッセージの6つの節)、ファイルを書き換えない、報告は日本語、報告の形式(contracts/verification-report.md の全欄)を、そのまま書く。変更ファイルの一覧は、`git` で自分でも取り直して突き合わせる
- [ ] T004 `.claude/rules/window.md` に、検査の共通の手順を追記する(英語): 納品書を書いた後、検査が必要なら、`Agent` ツールで `subagent_type: window-verifier` を呼ぶ。委任メッセージは contracts/delegation-message.md の形式で、ユーザーの原文・依頼票(軽作業は納品書の「依頼」欄の全文)・納品書の本文・変更ファイルの一覧を貼る。メインの判断(問題ない、など)を書かない。返ってきた報告の全文を、納品書の末尾の「確かめる者の報告」の節に、そのまま追記する。判定が承認可なら、「確認待ち」で報告する
- [ ] T005 `docs/rules-ja/window.md` に、T004 の追記の日本語訳を反映する
- [ ] T006 静的な確認: `window-verifier.md` の frontmatter が、YAML として妥当で、`tools` に `Agent` を含み、`Edit` と `Write` を含まないこと、`name` がファイル名と一致することを、コマンドで確かめる。`window.md` が日本語を含まない(`docs/納品書` のパス以外)こと、frontmatter がないこと、200 行未満であることを、確かめる。結果を、末尾の「検証の記録」に書く

**Checkpoint**: 検査役の骨格と、窓口の共通の手順ができた。

---

## Phase 3: User Story 1 - 本件の完了前に、独立した検査が通る (Priority: P1) 🎯 MVP

**Goal**: 本件の完了前に、確かめる者が検査し、報告が納品書に追記される。

**Independent Test**: 新規実装を1件依頼し、完了前に検査が通り、報告が納品書に追記され、状態が「確認待ち」である(quickstart のシナリオ 1)。

- [ ] T007 [US1] `.claude/rules/window.md` の「Main task」の経路に、検査を追記する(英語): 実装が終わり、納品書を書いたら、報告する前に、必ず確かめる者を呼ぶ(T004 の手順に従う)。「確認した方法」には、コマンドと出力(要点)を貼る(納品書のテンプレートの規則)
- [ ] T008 [US1] `docs/rules-ja/window.md` に、T007 の追記の日本語訳を反映する
- [ ] T009 [US1] (ユーザー)新しいセッションで、利用できるエージェントの一覧に `window-verifier` が出ることを確認し(quickstart の準備)、シナリオ 1 を実施する。完了前に確かめる者が呼ばれ、報告の全文が納品書の末尾に追記され、状態が「確認待ち」であることを確認する。**入れ子の可否は、T018 で確かめる**。結果を「検証の記録」に書く

**Checkpoint**: 本件が、検査を通って納品される。ここで MVP として止められる。

---

## Phase 4: User Story 2 - 軽作業は、コードを変えたときだけ検査される (Priority: P1)

**Goal**: 軽作業で、コードやテストを変えたときだけ、検査が通る。

**Independent Test**: コードを変える軽作業と、ドキュメントだけの軽作業を、1件ずつ依頼し、前者だけで検査が通る(quickstart のシナリオ 2・3)。

- [ ] T010 [US2] `.claude/rules/window.md` の「Light task」の経路に、検査が必要かの判定を追記する(英語、data-model.md「検査の対象の判定」): 作業の差分(`git diff --name-only` と、未追跡のファイル)に、ソースファイル(`.cpp` `.hpp` `.cc` `.hh` `.cxx` `.h` `.cs` `.rs`)またはテストファイル(`tests/` か `Tests/` 配下、ファイル名に `Test` か `_test` を含む)があるときだけ、検査を通す。ドキュメント、rules、設定、HTML だけの変更は、納品書の「確かめる者の報告」の節に、「検査不要: <理由>」の1行を書く。迷ったら、検査する側に倒す。軽作業の納品書の「依頼」欄には、「こう理解した」と「やらないこと」を全文で書く
- [ ] T011 [US2] `docs/rules-ja/window.md` に、T010 の追記の日本語訳を反映する
- [ ] T012 [US2] (ユーザー)新しいセッションで、シナリオ 2(コードを変える軽作業)とシナリオ 3(ドキュメントだけの軽作業)を実施する。前者で検査が通り、後者で通らず「検査不要」の1行が書かれることを確認する。結果を「検証の記録」に書く

**Checkpoint**: 軽作業の検査の要否が、差分で決まる。

---

## Phase 5: User Story 3 - 納品書の抜けが指摘される (Priority: P2)

**Goal**: 確かめる者が、納品書の主張を完了の判定に照合し、抜けを指摘する。

**Independent Test**: わざと「確認していないこと」に抜けのある納品書を渡し、検査が、その抜けを指摘する(quickstart のシナリオ 4)。

- [ ] T013 [US3] `.claude/agents/window-verifier.md` に、検査の手順を追記する(英語)。(1) 納品書の主張を、完了の判定の各項目に、根拠(`path:line` またはコマンド出力)で照合し、満たす・満たさない・判定不能を書く。納品書の主張を、そのまま信じない。(2) 抜けの基準は **「完了の判定の項目に直結する抜け、つまり、その項目の主張を、確認方法が捕まえていない場合だけ」**。一般的な懸念は「補足」として書き、指摘に数えない。(3) 納品書の確認方法のうち、実行できるコマンドを、最も重要なものから最大3つ再実行する。(4) スタイルだけの指摘は書かない。指摘が無ければ「承認可」と書いてよく、指摘を作り出さない(research.md R6)
- [ ] T014 [US3] (ユーザー)新しいセッションで、シナリオ 4(抜けのある納品書)、シナリオ 6(スタイルの指摘が出ない)、シナリオ 7(納品書にコマンドと出力がある)を実施する。結果を「検証の記録」に書く

**Checkpoint**: 納品書の抜けが、独立した目で、指摘される。

---

## Phase 6: User Story 4 - 言語・エンジン別のレビューが、検査に含まれる (Priority: P2)

**Goal**: 確かめる者が、変更ファイルに応じたレビューを入れ子で呼び、重大な指摘を報告に残す。

**Independent Test**: C++、C#、Rust、Unity、Unreal の変更を1件ずつ用意し、対応するレビューが呼ばれ、CRITICAL と HIGH の指摘が報告に残る(quickstart のシナリオ 5)。

- [ ] T015 [P] [US4] `.claude/agents/unity-reviewer.md` を英語で作る(contracts/reviewer-routing.md「新規のレビュー用エージェントの要件」): frontmatter は `name: unity-reviewer`、`description`、`tools: Read, Grep, Glob, Bash`、`model: sonnet`。本文は、`.claude/rules/unity/` の5つのファイルを、最初に `Read` するよう書く(`paths` 付きの rules は届かないため)。変更は `git diff` で自分で取る。重大度は CRITICAL / HIGH / MEDIUM。Unity の規約・パターン・セキュリティ・テストの観点で検査する。ファイルを書き換えない
- [ ] T016 [P] [US4] `.claude/agents/unreal-reviewer.md` を英語で作る(T015 と同じ要件)。`.claude/rules/unreal-engine/` の5つのファイルを、最初に `Read` するよう書く。Epic の C++ コーディング規約、UObject のポインター型、RPC の検証などの観点で検査する
- [ ] T017 [US4] `.claude/agents/window-verifier.md` に、レビューの振り分けを追記する(英語、contracts/reviewer-routing.md の表と規則): 変更ファイルの一覧から、`Agent` ツールで `subagent_type` を指定して、`unity-reviewer`、`unreal-reviewer`、`cpp-reviewer`、`csharp-reviewer`、`rust-reviewer` を呼ぶ。重なりは特化側だけ。混在は両方。複数あれば並行して呼ぶ。表にない拡張子は呼ばず、報告に「対象外」と書く。返ってきた CRITICAL と HIGH の指摘を、そのまま報告の「レビューの指摘」に含める。MEDIUM 以下とスタイルは含めない
- [ ] T018 [US4] (ユーザー)新しいセッションで、シナリオ 5 を、言語ごとに1件ずつ実施する。対応するレビューが入れ子で呼ばれ、CRITICAL と HIGH の指摘が報告に残ること、重なるファイルは特化側だけが呼ばれることを確認する。**入れ子が動かなければ、案 B(メインが別々に呼ぶ方式)に切り替える**。結果を「検証の記録」に書く

**Checkpoint**: 言語・エンジン別のレビューが、検査に含まれる。

---

## Phase 7: User Story 5 - 差し戻しと、上限を超えたときの扱い (Priority: P3)

**Goal**: 要修正のとき、最大2回まで差し戻し、3回目には作業を止めずに未解決の指摘付きで報告する。

**Independent Test**: 要修正の指摘が残る状況を作り、3回目に、作業が止まらず、未解決の指摘付きで「確認待ち」と報告される(quickstart のシナリオ 8)。

- [ ] T019 [US5] `.claude/rules/window.md` に、差し戻しの手順を追記する(英語、data-model.md「判定の意味と、差し戻し」): 判定が要修正なら、直して納品書を更新し、検査を呼び直す(最大2回)。3回目にも要修正なら、作業を止めず、未解決の指摘を報告の節に載せたまま「確認待ち」で報告する。判定不能は、差し戻しに数えず、そのまま報告する。呼び直すときは、前回の判定を、委任メッセージに書かない(contracts/delegation-message.md)
- [ ] T020 [US5] `docs/rules-ja/window.md` に、T019 の追記の日本語訳を反映する
- [ ] T021 [US5] (ユーザー)新しいセッションで、シナリオ 8 を実施する。要修正の指摘が残る依頼で、差し戻しが2回を超えず、3回目で作業が止まらず、未解決の指摘付きで「確認待ち」と報告されることを確認する。結果を「検証の記録」に書く

**Checkpoint**: 5つのストーリーがそろった。

---

## Phase 8: Polish & Cross-Cutting

- [ ] T022 `.claude/rules/window.md` の最終確認: 日本語を含まない(`docs/納品書` のパス以外)こと、frontmatter がないこと、200 行未満であることを、コマンドで確かめる。結果を記録する
- [ ] T023 `docs/rules-ja/window.md` が、`.claude/rules/window.md` の全内容を訳していること(見出しの数と順番、箇条書きと表の行数が一致)を確かめる
- [ ] T024 3つのエージェントの定義が、contracts と一致していることを確かめる: `window-verifier.md` の報告の形式が contracts/verification-report.md と、振り分けが contracts/reviewer-routing.md と、`unity-reviewer.md` と `unreal-reviewer.md` が「新規のレビュー用エージェントの要件」と、それぞれ一致する。差があれば直す
- [ ] T025 `AGENTS.md` を更新する: 「このリポジトリ独自のルールとスキル」の表に、`window-verifier`、`unity-reviewer`、`unreal-reviewer`(`.claude/agents/`)と、検査が必要かの判定を足す。窓口の説明に、検査の段階を足す
- [ ] T026 `docs/実装フロー/実装フロー.html` に、確かめる者の段階(軽作業の流れと本件の流れに、「検査」の手順)を追記する。外部通信を足さない。タグの対応と、手順の数を、確かめる
- [ ] T027 quickstart.md の「確認する未検証の項目」4点が、T009、T012、T014、T018、T021 で確かめられたことを確認し、spec.md の Assumptions と research.md の「未検証のまとめ」の「未検証」の記述を、確認結果に更新する。窓口の spec(001)の T010 などの検証が済んでいない場合は、そのことを記録する

---

## Dependencies & Execution Order

- Phase 1 → Phase 2 → Phase 3 以降。Phase 2 は、全ストーリーをブロックする。
- ストーリー間の依存: US1〜US5 は、Phase 2 の後、互いに独立している。ただし、`window.md`(T004、T007、T010、T019)、`docs/rules-ja/window.md`、`window-verifier.md`(T003、T013、T017)は、複数のストーリーが同じファイルを編集するため、順に行う。
- US4 の T017 は、T015 と T016(新しいレビュー用エージェント)の後。
- 各ストーリー内: 定義・経路の追記 → 訳 → 検証(ユーザー)の順。
- Phase 8 は、全ストーリーの後。

### 並行できるもの

- T002(納品書のテンプレート)は、T003 と別のファイルで、並行できる。
- T015(`unity-reviewer`)と T016(`unreal-reviewer`)は、別のファイルで、互いに依存しないため、並行できる。
- 検証タスク(T009、T012、T014、T018、T021)は、ユーザーが、同じ新しいセッションで、続けて行える。

## Implementation Strategy

### MVP(US1 だけ)
1. Phase 1・2 を完了する。
2. Phase 3(本件の検査)を完了する。
3. T009 で、カスタムエージェントを呼べるか、報告が追記されるかを確かめる。**ここで、確かめる者の骨格が機能するかが分かる**。

### 段階的に足す
- US1 の検証が通ったら、US2 → US3 → US4 → US5 の順に足す。各ストーリーの後、検証して止められる。
- US4 の T018 で、入れ子が動かなければ、案 B に切り替える(T017 の書き換えと、`window.md` の呼び方の変更が要る)。

## 検証の記録

(T006 と、T009、T012、T014、T018、T021 の結果を、ここに書く)
