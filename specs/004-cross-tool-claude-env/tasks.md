---

description: "Codex・Antigravity を Claude と同じ環境で使えるようにする: タスク一覧"
---

# Tasks: Codex・Antigravity を Claude と同じ環境で使えるようにする

**Input**: `specs/004-cross-tool-claude-env/` の spec.md、plan.md、research.md、data-model.md、contracts/、quickstart.md

**Tests**: 自動テストのコードは作らない(spec に指定なし)。代わりに、各タスクの中で、コマンドを実行して確かめる。実機(Codex・Antigravity)は未導入のため、ユーザー検収(T025)。

**Organization**: ユーザーストーリーごとに分ける。US1 が中心(P1)。US2(フック)と US3(プラグイン)は、US1 と独立している。

## Format: `[ID] [P?] [Story] 説明(ファイルのパス)`

- **[P]**: 並行できる(別のファイル、依存なし)
- 生成物は手で書かない。スクリプトで生成する。

## Phase 1: Setup

- [X] T001 Python 3 が使えることを確かめる(`python --version`)。使えなければ、ここで止めて報告する
- [X] T002 Claude 側の「変更前」の記録を、スクラッチパッドに保存する(SC-005 用): `ls .claude/skills`、`ls .claude/agents`、`find .claude/rules`、`bash .claude/hooks/window-reminder.sh < /dev/null` の出力、`git diff --stat -- .claude vendor`、`git status --short`

---

## Phase 2: Foundational(US1・US2 の前に必要)

- [X] T003 `scripts/sync-agent-env.py` の骨組みを作る: リポジトリのルートをスクリプトの位置から見つける、引数(なし / `--check`)、終了コード 0・1・2(contracts/sync-script.md)、frontmatter の読み取り(`---` で囲まれた YAML。外部パッケージを使わず、必要な項目 `name`、`description`、`paths` だけを読む)、LF で書き出す、`--check` では何も書かない

**Checkpoint**: `python scripts/sync-agent-env.py --check` が、何も生成していない状態で動く(ずれを報告して終了コード 1、または一致で 0)

---

## Phase 3: User Story 1 - 1 か所を直せば 3 つのツールに反映される (Priority: P1) 🎯 MVP

**Goal**: スキル 18・エージェント 9・rules 27 が、`.claude/` を直すだけで、参照側に反映される。

**Independent Test**: quickstart の 1〜4。`.claude/` のスキルを 1 つ書き換え、`--check` が検出し、同期で反映される。

- [X] T004 [US1] `scripts/sync-agent-env.py` にスキルの同期を足す: `.claude/skills/<name>/` を `.agents/skills/<name>/` へフォルダごとコピー(data-model.md)
- [X] T005 [US1] `scripts/sync-agent-env.py` にエージェントの同期を足す: `.claude/agents/<name>.md` を `.agents/agents/<name>.md` へコピー
- [X] T006 [US1] `scripts/sync-agent-env.py` に Codex 向けエージェントの生成を足す: `.codex/agents/<name>.toml` に `name`、`description`、`developer_instructions`(本文)を書く。`tools` と `model` は移さない。先頭に `# generated from .claude/agents/<name>.md`。TOML の文字列は、複数行リテラル(`'''`)か、エスケープで、本文に含まれる `"""` や `'''` があっても壊れないようにする(含まれる場合は、終了コード 2 で失敗)
- [X] T007 [US1] `scripts/sync-agent-env.py` に rules の生成を足す: `.claude/rules/<dir>/<file>.md` → `.agents/rules/<dir>-<file>.md`、`window.md` と `answer-policy.md` は `<file>.md`。`paths` あり→`trigger: glob` と `globs: "<カンマ区切り>"`、`paths` なし→`trigger: always_on`。frontmatter の後に `<!-- generated from .claude/rules/... -->`。1 ファイルが 24,000 バイトを超えたら、終了コード 2
- [X] T008 [US1] `scripts/sync-agent-env.py` に孤児の削除を足す: `.agents/skills`、`.agents/agents`、`.agents/rules`、`.codex/agents` のうち、正本に対応しないファイルだけを削除する(`.agents/workflows`、`ecc-install-state.json`、`vendor/` には触らない)。`--check` では、孤児も「ずれ」として報告する
- [X] T009 [US1] 同期を実行し(`python scripts/sync-agent-env.py`)、続けて `--check` が終了コード 0 になることを確かめる。実行前に `git status --short .agents` を記録し、実行後の差分が、想定どおり(rules 15 件の置き換えと、新規ファイルのみ。スキル 6 件・エージェント 5 件は差分なし)であることを確かめる
- [X] T010 [US1] quickstart の 2 と 4 を実行する: 件数(スキル 18/18、エージェント 9/9/9、rules 27/27)、`.agents/rules/cpp-coding-style.md` の frontmatter(`trigger: glob` と `globs`)、`.agents/rules/window.md` の frontmatter(`trigger: always_on`)。出力を、納品書(T023)に貼る
- [X] T011 [US1] quickstart の 3 を実行する: `.claude/skills/window-question/SKILL.md` に一時的な 1 行を足す → `--check` が終了コード 1 でそのファイルを報告 → 同期 → `.agents/` 側に反映 → 1 行を消して再同期 → `git diff -- .claude` が、一時的な変更を含まないことを確かめる(SC-002)
- [X] T012 [US1] `AGENTS.md` に、次の 2 点を追記する(FR-009): (a) 「他のツール(Codex・Antigravity)との共有」の節: `.claude/` が正本であること、`python scripts/sync-agent-env.py` で生成すること、`--check` で検査すること、生成物は手で直さないこと。(b) 「rules の案内(Codex 向け)」の節: 毎回 `.claude/rules/window.md` と `.claude/rules/answer-policy.md` を読む、作業の種類ごとに `.claude/rules/cpp/`・`csharp/`・`rust/`・`unity/`・`unreal-engine/` を読む(対象のファイルの種類を併記)。`AGENTS.md` の内容を変えるため、`CLAUDE.md` の `@AGENTS.md` 経由で Claude にも届く点を、節に注記する。また、`@` による取り込みは、Codex の公式に記載がないため、「読め」という文で書く

**Checkpoint**: US1 が単独で動く。スキル・エージェント・rules が共有される。

---

## Phase 4: User Story 2 - フックの働きを可能な範囲で揃える (Priority: P2)

**Goal**: 窓口フックと同じ注意を、Codex と Antigravity にも注入する(対応する範囲)。

**Independent Test**: 変換スクリプトの出力を、ローカルで確かめる。Codex の設定が、既存のスクリプトを呼ぶ。実機の動作は、ユーザー検収。

- [X] T013 [US2] `scripts/sync-agent-env.py` に Codex 向けフック設定の生成を足す: `.codex/hooks.json` に `UserPromptSubmit` を書き、`bash .claude/hooks/window-reminder.sh` を呼ぶ(スクリプトはコピーしない)。`commandWindows` が必要かは、公式の書式(`command_windows`、JSON での名前)を確かめてから決める。書式が確認できなければ、`command` のみにして、確認できなかったことを共有の一覧に書く
- [X] T014 [P] [US2] `.agents/hooks/window-reminder-ag.py` を作る: `window-reminder.sh` を呼び、その出力の JSON から `additionalContext` を取り出して、Antigravity の `{"injectSteps":[{"ephemeralMessage":"<内容>"}]}` の形にして出力する。`injectSteps` の項目の正確な書式(キー名の入れ子)は、公式(https://antigravity.google/docs/hooks)で再確認する。確認できなければ、確認できなかったと報告し、推測で書かない
- [X] T015 [US2] `scripts/sync-agent-env.py` に Antigravity 向けフック設定の生成を足す: `.agents/hooks.json` に `PreInvocation` を書き、T014 のスクリプトを呼ぶ(`timeout` は 10)。`.agents/hooks/` は、同期の孤児削除の対象にしない
- [X] T016 [US2] 変換の確認: `bash .claude/hooks/window-reminder.sh < /dev/null` の出力(Codex が読む形)が、T002 の記録と一致すること、`python .agents/hooks/window-reminder-ag.py < /dev/null` が、妥当な JSON を出すことを、`python -m json.tool` で確かめる。出力を納品書に貼る
- [X] T017 [US2] 同期と `--check` を再実行し、終了コード 0 を確かめる。`.codex/hooks.json` と `.agents/hooks.json` が、JSON として読めることを確かめる

**Checkpoint**: フックの設定が生成され、変換の出力が正しい。実機の確認は T025。

---

## Phase 5: User Story 3 - 直下の `.claude-plugin` を vendor 側と同じ形に揃える (Priority: P3)

**Goal**: 直下の `.claude-plugin/` に `plugin.json` を足し、4 つのプラグインの有効化を保つ。

**Independent Test**: `claude plugin validate .` と `claude plugin list`。

- [X] T018 [US3] 変更前の `claude plugin list` の出力を記録する(4 つの有効化の確認用)。`claude plugin validate .` の変更前の結果も記録する
- [X] T019 [US3] `.claude-plugin/plugin.json` を作る: `name`(`marketplace.json` の `name` `game-developer-ai-harness` とは別の名前にし、プラグインとしての名前を決める)、`description`、`version`、`license` など、vendor 側(`vendor/superpowers/.claude-plugin/plugin.json`)に倣った必須項目のみ。コンポーネントは持たせない。`marketplace.json` は変更しない
- [X] T020 [US3] `claude plugin validate .` と `claude plugin list` を実行する。エラーが出る、または有効化が変わる、または意図しないプラグインが現れるなら、`.claude-plugin/plugin.json` を削除して元に戻し、その旨と出力を報告する(spec の Assumptions のとおり)。`settings.local.json` は変更しない

**Checkpoint**: 直下の `.claude-plugin/` が、validate を通り、4 つの有効化が保たれる。または、置かないと判断して報告する。

---

## Phase 6: Polish & Cross-Cutting

- [X] T021 共有の一覧を `docs/共有環境/共有の一覧.md` に書く(contracts/share-matrix.md の書式)。実装の結果に合わせて、各行の状態・理由・出典・確認を直す。`一部`・`不可` の全行に、理由と出典を付ける(SC-003)。確認できなかったこと(Antigravity のエージェントの frontmatter、両ツールのフックの Windows での動作、Codex のカスタムエージェントの呼び出し)を、明記する
- [X] T022 `AGENTS.md` の「このリポジトリ独自のルールとスキル」の表に、同期スクリプトと共有の一覧の行を足す。ECC の記録 `.agents/ecc-install-state.json` が、古くなったことを、一覧に書く(ECC の更新・削除の動作は、未検証)
- [X] T023 [P] Claude 側が変わっていないことを確かめる(SC-005、SC-006): T002 の記録と比べて、`.claude/` の差分が 0 件(生成物の追加のみ)、`git diff --stat -- vendor` が 0 件、スキル・エージェントの一覧が一致、`window-reminder.sh` の出力が一致
- [X] T024 納品書を `docs/納品書/004-cross-tool-claude-env.md` に、`docs/納品書/_template.md` から書く。完了の判定の各項目に 1 つの節を置き、3 つの欄(何をしたか、確認した方法=コマンドと出力の要点、確認していないこと)を埋める。続けて、`window-verifier` を呼ぶ(窓口の「検査」の節。本件は必ず呼ぶ)。報告は納品書の末尾に全文で追記し、状態は「確認待ち」にする
- [ ] T025 [ユーザー検収] 実機で確かめる(quickstart の 7): (1) Codex を起動し、`/hooks` でフックを信頼して、スキルが使えること、窓口の注意が注入されること。(2) Antigravity CLI を起動し、スキルと rules が読み込まれること、フックが動くこと。結果を、共有の一覧の「確認」欄に反映する
- [ ] T026 納品書の承認を、ユーザーが行う(状態を「確認待ち」から「承認済み」に)

---

## Dependencies & Execution Order

- Phase 1 → Phase 2 → US1(T004〜T012)の順。T004〜T008 は、同じファイル(`scripts/sync-agent-env.py`)を変えるため、順に行う。
- US2 は、T003 の後なら、US1 と独立。ただし T013・T015 も同じスクリプトを変えるため、US1 の T004〜T008 の後に行う。T014 は別のファイルで、並行できる。
- US3(T018〜T020)は、他と独立。US1・US2 と並行できる。
- Phase 6 は、すべての後。T023 は T021・T022 と別のファイルで、並行できる。

## Implementation Strategy

1. **MVP**: Phase 1・2 と US1(T001〜T012)。ここまでで、スキル・エージェント・rules の共有が動く。
2. US2(フック)、US3(プラグイン)を足す。
3. Phase 6 で、一覧、納品書、検査。実機の確認(T025)は、ユーザー。

## Notes

- 外向きの操作(push、PR、マージ)は、このタスクに含めない。ユーザーに確認してから行う。
- 公式の書式が確認できなかった箇所(T013 の `commandWindows`、T014 の `injectSteps`)は、推測で埋めない。
