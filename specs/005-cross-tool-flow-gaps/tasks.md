---

description: "Codex・Antigravity での実装フローの穴を塞ぐ: タスク一覧"
---

# Tasks: Codex・Antigravity での実装フローの穴を塞ぐ

**Input**: `specs/005-cross-tool-flow-gaps/` の spec.md、plan.md、research.md、data-model.md、contracts/、quickstart.md

**Tests**: 自動テストのコードは作らない(spec に指定なし)。各タスクの中で、コマンドを実行して確かめる。実機は、ユーザー検収(T016)。

**Organization**: ユーザーストーリーごとに分ける。US1(読み替え表)は P1。US2(読み取り専用の制限と、エージェントの変換)は P2。US3(superpowers の環境構築)は P3。

## Format: `[ID] [P?] [Story] 説明(ファイルのパス)`

- **[P]**: 並行できる(別のファイル、依存なし)
- 公式で確認できなかった対応は、推測で埋めず、「未確認」と書く。

## Phase 1: Setup

- [X] T001 変更前の記録を、スクラッチパッドに保存する: `.claude/` のファイルの SHA-256(`settings.local.json` を除く)、`git diff --stat -- vendor`、`.agents/agents/` と `.codex/agents/` の現在の内容の控え、`python scripts/sync-agent-env.py --check` の結果

---

## Phase 2: User Story 1 - 道具名を読み替えて実装フローを進められる (Priority: P1) 🎯 MVP

**Goal**: `AGENTS.md` の読み替え表で、実装フローの Claude 固有の道具が、両ツールの操作に読み替えられる。

**Independent Test**: quickstart の 5。洗い出した全項目が、表に載っている。

- [X] T002 [US1] Claude 固有の道具を、`grep` で洗い出し直す(`AskUserQuestion`、`subagent_type`、`` `Agent` ``、`tools:`、`model:`、`claude-code-guide`)。research.md R1 の一覧と一致することを確かめ、差分があれば、research.md を直す
- [X] T003 [US1] `AGENTS.md` に「道具名の読み替え表(Codex・Antigravity 向け)」の節を足す(data-model.md の書式。欄: Claude の道具・項目、Codex、Antigravity、出典)。行: `AskUserQuestion`、`Agent` ツールと `subagent_type`、エージェントの `tools:`、エージェントの `model:`、`claude-code-guide`、スキルの呼び方(`/speckit-…`。未確認)。対応を確認できなかった所は「未確認」、二次資料の所は「二次資料」と書く(research.md R2・R3・R4)。`.claude/` は変えない
- [X] T004 [US1] 表の網羅を確かめる(SC-001、SC-002): T002 の洗い出しの各項目が、表のいずれかの行に当たること、「対応なし」と「未確認」の全行に、理由または確認できなかった旨があること(空欄 0 件)を、コマンドと出力で確かめる

**Checkpoint**: 読み替え表だけで、US1 が単独で完結する。

---

## Phase 3: User Story 2 - 相談役が読み取り専用で動く (Priority: P2)

**Goal**: Antigravity では `tools` で、Codex では指示で、相談役が書き込まないようにする。前回の frontmatter のコピーの不具合も直す。

**Independent Test**: quickstart の 1〜3。変換結果と、`--check`。

- [X] T005 [US2] `scripts/sync-agent-env.py` の `gen_agents` を直す(contracts/sync-script-changes.md): `.agents/agents/<name>.md` を、コピーから、Antigravity の frontmatter への変換にする。`tools`: `Read`→`view_file`、`Grep`→`grep_search`、`Bash`→`run_command`、`Write`・`Edit`→`replace_file_content`、`Glob` と `Agent` は入れない。`model: inherit`、`subagent: true`、`mainAgent: false`。frontmatter の後に生成元のコメント。未知の道具名は、終了コード 2 で、名前を報告して失敗する
- [X] T006 [US2] `scripts/sync-agent-env.py` に、Codex 向けの読み取り専用の注意を足す: 正本の `tools` が `Read`・`Grep`・`Glob` のみのエージェントに限り、`.codex/agents/<name>.toml` の `developer_instructions` の先頭に、「読み取り専用: ファイルの作成・編集・削除や、状態を変えるコマンドをしない」を足す(英語。TOML の文字列が壊れないように確かめる)
- [X] T007 [US2] 同期を実行し(`python scripts/sync-agent-env.py`)、続けて `--check` が終了コード 0 になることを確かめる。実行前後の `git status --short .agents .codex` を記録し、変わったのが `.agents/agents/` の 9 件と、`.codex/agents/` の読み取り専用の注意だけであること(rules・skills は差分なし)を確かめる
- [X] T008 [US2] quickstart の 2 と 3 を実行する: `.agents/agents/game-advisor.md` の frontmatter が `tools` に `view_file` と `grep_search` のみ・`model: inherit`、`window-verifier.md` に `run_command` があること。`.codex/agents/game-advisor.toml` に読み取り専用の注意があり、`window-verifier.toml` には無いこと。`tomllib` で 9 件が読めること。出力を、納品書に貼る
- [X] T009 [US2] `docs/共有環境/共有の一覧.md` を更新する: 相談役の読み取り専用の可否(Antigravity は `tools` で制限、Codex は公式の制限不可と、指示と親のサンドボックスでの対策。出典つき)、変換できなかった項目(`Glob`・`Agent`)、ECC 由来の 5 件のエージェントの内容が変わったこと、前回の「エージェントの frontmatter が未確認」の行の更新

**Checkpoint**: US1 と独立して、エージェントの変換が動く。

---

## Phase 4: User Story 3 - 両ツールで brainstorming を使える (Priority: P3)

**Goal**: superpowers を、環境構築方式で両ツールに入れる手順と、Antigravity IDE の配置を用意する。

**Independent Test**: quickstart の 4。`--dry-run` で置き先と中身を確かめ、実際に置いて、追跡されないことを確かめる。

- [X] T010 [P] [US3] `scripts/setup-antigravity-plugins.py` を作る: `vendor/superpowers` から、`.agents/plugins/superpowers/` へ、除外(`.git`、`tests/`、`docs/`、`.codex-plugin`、`.cursor-plugin`、`.devin-plugin`、`.hermes-plugin`、`.kimi-plugin`、`.muse-plugin`、`.opencode`、`.pi`、`.github`)を除いてコピーする。`--dry-run` は、置く先とファイル数と一覧だけを表示して何も書かない。`vendor/superpowers` が空(submodule が未取得)なら、終了コード 2 で失敗する。`vendor/` には書かない。リポジトリのルートは、スクリプトの位置から見つける。日本語を含む絶対パスを外部コマンドに渡さない(004 で、Git Bash が失敗した)
- [X] T011 [P] [US3] `.gitignore` に `.agents/plugins/superpowers/` を足す(ファイルが無ければ作る)
- [X] T012 [US3] `python scripts/setup-antigravity-plugins.py --dry-run` を実行して、出力(置く先、ファイル数、除外)を確かめる。続けて、実際に置き(`--dry-run` なし)、`.agents/plugins/superpowers/.antigravity-plugin/plugin.json` と `skills/brainstorming/SKILL.md` があること、`git status --short` に出ないこと(追跡されない)、`git diff --stat -- vendor` が 0 件であることを、コマンドと出力で確かめる
- [X] T013 [US3] `docs/共有環境/環境構築.md` を作る: (1) Codex アプリ: サイドバーの Plugins タブから superpowers を導入し、新しい会話を始める(公式の要約とリンク。ユーザーが操作)。CLI は `/plugins`。(2) Antigravity IDE: `python scripts/setup-antigravity-plugins.py` を実行する。読み込まれた項目は、エージェントのサイドパネルの「Customizations」で確かめる。新しく clone したら、再実行する。(3) 注意: プラグインには `writing-plans`・`executing-plans`・`subagent-driven-development` も入るが、`AGENTS.md` の「使わない」方針は、指示で守らせる(強制ではない)。(4) 確かめた範囲と、確かめていない範囲(必須ファイルの範囲、`using-superpowers` の自動読み込み、Codex の一覧に出るか)。`docs/共有環境/共有の一覧.md` に、superpowers の行を足す

**Checkpoint**: 手順書とスクリプトが、US1・US2 と独立して完結する。

---

## Phase 5: Polish & Cross-Cutting

- [X] T014 `.claude/` と `vendor/` の差分が 0 件であること(T001 の記録との比較。SHA-256、`git diff --stat -- .claude vendor`)、`python scripts/sync-agent-env.py --check` が成功すること、`AGENTS.md` の「このリポジトリ独自のルールとスキル」の表に、`scripts/setup-antigravity-plugins.py` と `docs/共有環境/環境構築.md` の行を足したことを確かめる(SC-004)
- [X] T015 納品書を `docs/納品書/005-cross-tool-flow-gaps.md` に、`docs/納品書/_template.md` から書く。完了の判定の各項目に 1 つの節を置き、3 つの欄(何をしたか、確認した方法=コマンドと出力の要点、確認していないこと)を埋める。続けて、`window-verifier` を呼ぶ(本件は必ず呼ぶ)。報告は、末尾に全文で追記し、状態は「確認待ち」にする
- [X] T016 [ユーザー検収] 実機で確かめる(quickstart の 7): (1) Antigravity IDE で `game-advisor` を呼び、書き込まず、固まらないこと。(2) Codex アプリで `window-verifier` を名前で頼めること。(3) 手順書のとおりに、両ツールで superpowers を導入し、`brainstorming` が使えること。結果を、共有の一覧の「実機の結果」に反映する
- [X] T017 納品書の承認を、ユーザーが行う(状態を「確認待ち」から「承認済み」に)

---

## Dependencies & Execution Order

- T001 → US1(T002〜T004)・US2(T005〜T009)・US3(T010〜T013)の順。ただし、3 つの Story は、互いに独立している(US2 のスクリプトの変更と、US3 の新しいスクリプトは別のファイル)。
- US2 の T005・T006 は、同じファイル(`scripts/sync-agent-env.py`)を変えるため、順に行う。T007 は、その後。
- US3 の T010 と T011 は並行できる。T012 は、その後。T013 は T012 の結果を使うため、その後。
- T009(共有の一覧)と T013 の共有の一覧への追記は、同じファイルのため、順に行う。
- Phase 5 は、すべての後。

## Implementation Strategy

1. **MVP**: T001〜T004(読み替え表)。
2. US2(エージェントの変換、読み取り専用)。前回の不具合の可能性を直すため、優先度は高い。
3. US3(superpowers の環境構築)。
4. Phase 5 で、検証、納品書、検査。実機の確認(T016)は、ユーザー。

## Notes

- 外向きの操作(push、PR、マージ)は、このタスクに含めない。
- 公式で確認できなかった箇所(Antigravity の `Glob` に当たる道具、`invoke_subagent` の引数、プラグインの必須ファイルの範囲)は、推測で埋めない。
