---

description: "窓口(依頼の受付・判定・納品)のタスク一覧"
---

# Tasks: 窓口(依頼の受付・判定・納品)

**Input**: Design documents from `/specs/001-request-window/`

**Prerequisites**: plan.md、spec.md、research.md、data-model.md、contracts/(hook-io.md、request-form.md、delivery-note.md)、quickstart.md

**Tests**: 自動テストは作らない(plan.md の Testing。遵守はスクリプトでは検査できない)。代わりに、各ストーリーの検証タスクで、スクリプトの単体確認と、quickstart のシナリオを行う。**新しいセッションが要る検証は、ユーザーの手が必要**で、`(ユーザー)` と付けた。

**Organization**: タスクはユーザーストーリーごとにまとめた。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 並行して進められる(別のファイルで、未完了のタスクに依存しない)
- **[Story]**: US1(質問)、US2(軽作業)、US3(新規実装)、US4(判定が迷うとき)

## 共通の注意

- `window.md` は英語で書く。日本語を含めない。`paths` の frontmatter を付けない(常時読み込み)。200 行未満。
- `window.md` を編集したら、同じ変更で `docs/rules-ja/window.md` の日本語訳も更新する(AGENTS.md の方針)。
- `window.md` は複数のストーリーが同じファイルに追記するため、`window.md` を編集するタスクは、順に行う([P] を付けない)。
- `vendor/` 配下は編集しない。

---

## Phase 1: Setup

- [X] T001 成果物のフォルダーを作る: `.claude/hooks/`、`.claude/skills/window-question/`、`.specify/templates/overrides/`、`docs/納品書/`

---

## Phase 2: Foundational(全ストーリーの前提)

**Purpose**: 判定の本体と、毎ターンの注意を届ける仕組み。これが無いと、どのストーリーも動かない。

- [X] T002 `.claude/rules/window.md` を英語で作る。判定の本体を書く: 層は質問・軽作業・本件の3つ。2つの軸(取り返しがつくか / 判断の分岐があるか)。「迷ったら層を上げる。層は上げるだけで、下げない」。ユーザーの発言にだけ判定し、システムの通知は対象外とする(research.md R2)。data-model.md の「依頼の層」の表と判定の規則に従う
- [X] T003 `.claude/hooks/window-reminder.sh` を作る(bash)。contracts/hook-io.md に従う: 標準入力を読み捨て、標準出力に `hookSpecificOutput.hookEventName` = `"UserPromptSubmit"` と `additionalContext` を持つ JSON **だけ**を出し、終了コードは 0。注入文は英語で **400 文字以内**。内容は、ユーザーの発言ごとに質問・軽作業・本件を判定する、迷ったら層を上げる、手順は `window.md`、システムの通知は対象外。質問のたびに層の宣言や依頼票を出させる指示を含めない
- [X] T004 T003 のスクリプトを単体確認する: サンプル JSON(contracts/hook-io.md の入力例)を標準入力に流し、(a) 標準出力が妥当な JSON である、(b) `additionalContext` が 400 文字以内、(c) 終了コードが 0、の3点を、実際に実行して確かめる。結果を記録する
- [X] T005 `.claude/settings.local.json` に、UserPromptSubmit のフックを登録する(`type`: `command`、`timeout`: 10)。command のパスの書き方は research.md R3 に従い、**先に確認する**: 作業用の設定ファイルで、フックから環境変数 `CLAUDE_PROJECT_DIR` を出力させ、`claude -p` で実行して、値が入るかを確かめる(モデル呼び出しが失敗しても、フックは発火する。research.md R1)。使えれば `"$CLAUDE_PROJECT_DIR"` を使い、使えなければ相対パスにして、plan.md の制約に「リポジトリ直下で起動する前提」と追記する。登録後、JSON として妥当かを確かめる
- [X] T006 `docs/rules-ja/window.md` を作る。`.claude/rules/window.md` の日本語訳。先頭に、他の訳と同じ形で「日本語訳(参照用)。原文(英語): `.claude/rules/window.md`。この訳は Claude には読み込まれません。」と「適用パス(`paths`): なし(毎セッション読み込まれる)」を書く

**Checkpoint**: 注意を届ける仕組みと、判定の本体ができた。

---

## Phase 3: User Story 1 - 質問に、手続きなしで根拠付きの回答が返る (Priority: P1) 🎯 MVP

**Goal**: 作業を含まない質問に、依頼票も納品書も層の宣言もなく、根拠付きで答える。

**Independent Test**: 作業を含まない質問を3件入力し、依頼票・納品書・層の宣言が出ず、根拠付きで答えが返る(quickstart のシナリオ 1)。

- [X] T007 [P] [US1] `.claude/skills/window-question/SKILL.md` を日本語で作る(research.md R6)。質問への回答の手順: 依頼票も納品書も作らない。層の宣言を出さない。根拠は `path:line`・URL・コマンド出力で示す(「読んだ」のような確認の経緯は書かない)。事実でないものは、事実でないと明示する(`.claude/rules/answer-policy.md` のとおり)。`description` は、自動起動されうるように、「作業を含まない質問に答えるとき」と書く
- [X] T008 [US1] `.claude/rules/window.md` に「質問」の経路を追記する: 質問と判定したら `window-question` を名前で呼ぶ。依頼票・納品書・層の宣言を出さない(SC-006)。質問と作業が混ざった発言は、作業の層で扱う(spec の Edge Cases)
- [X] T009 [US1] `docs/rules-ja/window.md` に、T008 の追記の日本語訳を反映する
- [ ] T010 [US1] (ユーザー)新しいセッションで quickstart のシナリオ 1 を入力し、依頼票・納品書・層の宣言が出ないこと、根拠が示されること、**注入文が届いて従われること**(research.md の未検証 1)を確認する。結果を、この tasks.md の末尾の「検証の記録」に書く

**Checkpoint**: 質問が、窓口を通って答えられる。ここで MVP として止められる。

---

## Phase 4: User Story 2 - 軽作業が、納品書付きで終わる (Priority: P1)

**Goal**: 小さな変更や不具合修正を、メインの会話が superpowers のスキルで作業し、納品書を `docs/納品書/` に残す。

**Independent Test**: 小さな不具合修正を1件依頼し、規模が伝えられ、設計メモや計画に進まず、完了後に納品書が残る(quickstart のシナリオ 2)。

- [X] T011 [P] [US2] `docs/納品書/_template.md` を日本語で作る。contracts/delivery-note.md の書式のとおり: 状態(確認待ち)、依頼、納品日、「完了の判定ごとの報告」(各項目に「何をしたか」「確認した方法」「確認していないこと」)、「追加した項目」。「確認していないこと」は **「空欄不可。なければ「なし」と書く」** とテンプレート内に明記する。「確認した方法」は **「手順を書く。「確認した」だけは不可」** と明記する
- [X] T012 [US2] `.claude/rules/window.md` に「軽作業」の経路を追記する: brainstorming は規模の判定にとどめ、設計メモや計画(`writing-plans`)には進まない。メインの会話が、必要に応じて systematic-debugging、test-driven-development、verification-before-completion を使って作業する。完了後、`docs/納品書/<YYYY-MM-DD>-<題名>.md` を `_template.md` の書式で書く。納品書を置いたら「確認待ち」と報告し、完了とは言わない。承認はユーザーが行う。依頼に無い作業を足したときは、「追加した項目」に書く
- [X] T013 [US2] `docs/rules-ja/window.md` に、T012 の追記の日本語訳を反映する
- [ ] T014 [US2] (ユーザー)新しいセッションで quickstart のシナリオ 2 を入力し、規模が伝えられること、設計メモや計画に進まないこと、`docs/納品書/<日付>-<題名>.md` ができて3欄が埋まり状態が「確認待ち」であること、完了とは言わないことを確認する。結果を「検証の記録」に書く

**Checkpoint**: 軽作業が、窓口を通り、納品書で終わる。

---

## Phase 5: User Story 3 - 新規実装で、依頼票と納品書がそろう (Priority: P2)

**Goal**: 新規実装の spec に依頼票の5欄が埋まり、ユーザーの合意まで実装に入らず、完了後に納品書が残る。

**Independent Test**: 新規実装を1件依頼し、spec に5欄が埋まり、合意前に実装に入らず、完了後に納品書が残る(quickstart のシナリオ 3)。

- [X] T015 [P] [US3] `.specify/templates/overrides/spec-template.md` を作る(research.md R5)。`.specify/templates/spec-template.md`(core)の内容をそのままコピーし、`**Input**` の行の直後、`## User Scenarios & Testing` の前に、contracts/request-form.md の書式の「依頼票」の節(ご要望(原文)、こう理解した、誰のためか、やらないこと、完了の判定)を足す。core のファイルは変えない
- [X] T016 [US3] override が使われることを確かめる(research.md の未検証 3): `.specify/scripts/powershell/resolve-template.ps1` を、`spec-template` に対して実行し、`.specify/templates/overrides/spec-template.md` が返ることを確かめる。返らなければ、原因を調べ、置き場所を直す。結果を記録する
- [X] T017 [US3] `.claude/rules/window.md` に「本件(新規実装)」の経路を追記する: brainstorming から `/speckit-specify` へ進む。spec の依頼票の5欄は、ご要望を原文のまま引用する(要約しない)。埋まらなかった欄だけを、`AskUserQuestion` で選択肢の形で聞く(自由記述はユーザーだけが持つ事実に限る)。ユーザーが spec に合意するまで、plan 以降に入らない。完了後、`docs/納品書/<NNN-feature>.md` を書く(spec の「完了の判定」の各項目に1節)
- [X] T018 [US3] `docs/rules-ja/window.md` に、T017 の追記の日本語訳を反映する
- [ ] T019 [US3] (ユーザー)新しいセッションで quickstart のシナリオ 3 を入力し、spec に依頼票の5欄が埋まること、合意前に実装に入らないこと、完了後に `docs/納品書/<NNN-feature>.md` ができることを確認する。結果を「検証の記録」に書く

**Checkpoint**: 新規実装が、依頼票から納品書まで通る。

---

## Phase 6: User Story 4 - 判定が迷うとき、層が上がる (Priority: P2)

**Goal**: 迷う依頼で、層が上がる方向にだけ動く。

**Independent Test**: push や PR 作成を含む依頼で、本件の確認が取られる(quickstart のシナリオ 4)。

- [X] T020 [US4] `.claude/rules/window.md` に、層を上げる規則を追記する: 外向きの操作(push、PR 作成、マージ)を含む依頼は、本件の確認を取る。ローカルの commit、ドキュメントだけの変更、rules や設定の編集は軽作業。軽作業の途中で、取り返しのつかない操作が必要だと分かったら、本件に上げ、その旨を伝える。層は下げない(data-model.md の「判定の規則」)
- [X] T021 [US4] `docs/rules-ja/window.md` に、T020 の追記の日本語訳を反映する
- [ ] T022 [US4] (ユーザー)新しいセッションで quickstart のシナリオ 4 と 5 を入力し、迷う例で層が上がる方向にだけ動くこと、混在した発言が作業の層で扱われることを確認する。結果を「検証の記録」に書く

**Checkpoint**: 4つのストーリーがそろった。

---

## Phase 7: Polish & Cross-Cutting

- [X] T023 `.claude/rules/window.md` の最終確認: 日本語を含まないこと、`paths` の frontmatter が無いこと、200 行未満であることを、コマンドで確かめる。結果を記録する
- [X] T024 `docs/rules-ja/window.md` が、`.claude/rules/window.md` の全内容を訳していること(節の数と順番が一致)を確かめる
- [X] T025 `AGENTS.md` を更新する: 「このリポジトリ独自のルールとスキル」の表に、`window.md`(毎セッション読み込まれる)、`window-question`、`docs/納品書/`、`.specify/templates/overrides/spec-template.md` を足す。窓口が、brainstorming 以下の流れの前に立つことを、計画フェーズの節に書く。「毎セッション読み込まれるのは `answer-policy.md` だけ」という記述を、`window.md` を含む形に直す
- [X] T026 `docs/実装フロー/実装フロー.html` に、窓口の段階(判定、質問、軽作業、納品書)を追記する。外部通信を足さない。タグの対応を確かめる
- [ ] T027 quickstart.md の「確認する未検証の項目」3点(`additionalContext` の到達と遵守、環境変数、override の使用)が、T005、T010〜T022、T016 で確かめられたことを確認し、spec.md の Assumptions の「未検証」の記述を、確認結果に更新する

---

## Dependencies & Execution Order

- Phase 1 → Phase 2 → Phase 3 以降。Phase 2 は、全ストーリーをブロックする。
- ストーリー間の依存: US1〜US4 は、Phase 2 の後、互いに独立している。ただし `window.md` と `docs/rules-ja/window.md` を、全ストーリーが追記するため、それらを編集するタスクは、順に行う。
- 各ストーリー内: 経路の追記(window.md)→ 訳 → 検証(ユーザー)の順。
- Phase 7 は、全ストーリーの後。

### 並行できるもの

- T007(スキル)、T011(納品書のテンプレート)、T015(override の spec テンプレート)は、別のファイルで、互いに依存しないため、並行できる。
- 検証タスク(T010、T014、T019、T022)は、ユーザーが同じセッションで続けて行える。

## Implementation Strategy

### MVP(US1 だけ)
1. Phase 1・2 を完了する。
2. Phase 3(質問)を完了する。
3. T010 で、注入文が届いて従われるかを確かめる。**ここで、案 A が機能するかが分かる**。従わなければ、注入文を直し、それでも従わなければ、設計書の案 B への移行を検討する。

### 段階的に足す
- US1 の検証が通ったら、US2 → US3 → US4 の順に足す。各ストーリーの後、検証して止められる。

## 検証の記録

### 実装時に、こちらで確認したもの(2026-11-15)
- T004: フックのスクリプトに、サンプル JSON を流した。標準出力は妥当な JSON 1つ(`hookSpecificOutput` のみ)、`additionalContext` は 320 文字(上限 400)、終了コード 0。
- T005: `claude -p` で、フックから環境変数を出力させた。`$CLAUDE_PROJECT_DIR` が設定される(値は起動したディレクトリ)。`settings.local.json` は JSON として妥当。
- T016: `resolve-template.ps1 spec-template` が、override の spec テンプレート(依頼票の節を含む)を返す。`speckit-specify` が実際に使うかは、未確認。
- T023: `window.md` は 53 行。frontmatter なし。日本語は、フォルダー名 `docs/納品書` のパスのみ(それ以外の日本語はない)。
- T024: 見出しと、箇条書き・表の行数が、原文(22)と訳(22)で一致。
- T026: 実装フローの HTML に窓口の節を追記。タグの対応を確認。外部通信なし。

### ユーザーの手が必要なもの(未実施)
- T010、T014、T019、T022: 新しいセッションでの quickstart のシナリオ 1〜5。
- T027: 上の検証が終わってから、spec の Assumptions の「未検証」を最終更新する(現時点で確認できた分は、更新済み)。

### T010、T014、T019、T022 の結果
(未実施)
