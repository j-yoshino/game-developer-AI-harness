---

description: "main 用の構成を組み立てる変換ブランチ: タスク一覧"
---

# Tasks: main 用の構成を組み立てる変換ブランチ

**Input**: `specs/006-plugin-conversion-branch/` の spec.md、plan.md、research.md、data-model.md、contracts/build-main.md、quickstart.md

**Tests**: 自動テストのコードは作らない(spec に指定なし)。各タスクの中で、コマンドを実行して確かめる。実機は、ユーザー検収(T017)。

**Organization**: US1(同期の廃止と、独立した正本、P1)、US2(組み立てるスクリプト、P2)、US3(外部プラグインの別導入、P3)、US4(ローカルの変換ブランチへのコミット、P4)。

## Format: `[ID] [P?] [Story] 説明(ファイルのパス)`

- **[P]**: 並行できる(別のファイル、依存なし)
- 公式で確認できなかった点は、推測で埋めず、「未確認」と書く。
- 日本語を含む絶対パスを、外部コマンドに渡さない(004 で、Git Bash が失敗した)。
- ネットワークを使う導入の試験、ブランチの削除は、実行の前に、ユーザーに確認する。

## Phase 1: Setup

- [X] T001 変更前の記録を、スクラッチパッドに保存する: `.claude/` のファイル(`settings.local.json` を除く)の SHA-256、`git diff --stat -- vendor`、`bash .claude/hooks/window-reminder.sh` の出力、`claude plugin list`、`git ls-files .claude | wc -l`・`git ls-files .agents .codex | wc -l`、`grep -rl "generated from" .agents .codex`(`plugins/superpowers` を除く)の件数(46 件の見込み)

---

## Phase 2: User Story 1 - 同期を廃止し、独立した正本にする (Priority: P1) 🎯 MVP

**Goal**: `.agents/` と `.codex/` が、`.claude/` から生成されない、独立した正本になる。

**Independent Test**: quickstart の 1。

- [X] T002 [US1] `.agents/` と `.codex/` の、「generated from … Do not edit; run scripts/sync-agent-env.py」というコメントを取り除く(46 ファイル。rules と Antigravity のエージェントは HTML コメントの 1 行、Codex の TOML は `#` の 1 行)。1 回限りの置換スクリプトで行い、置換の前後で、対象外のファイルが変わらないこと、rules の frontmatter(`trigger` など)、エージェントの frontmatter、TOML(`tomllib` で 9 件が読めること)が壊れていないことを確かめる。`.agents/plugins/superpowers/`(追跡されない派生物)は、触れない
- [X] T003 [US1] `scripts/sync-agent-env.py` を削除する。`AGENTS.md` の「他のツール(Codex・Antigravity CLI)との共有」の節(「生成物は手で直さない」「同期を実行する」)と、「このリポジトリ独自のルールとスキル」の表の 1 行を、独立した正本の説明に直す(`.claude/`・`.codex/`・`.agents/` を、それぞれ手で保守する。ツールの間でずれてよい)。`docs/共有環境/共有の一覧.md` と `docs/共有環境/環境構築.md` の、同期の記述も直す。`grep -rn "sync-agent-env" .` の残りが、過去の納品書と `specs/004`・`specs/005`・`specs/006` だけであることを確かめる
- [X] T004 [US1] quickstart の 1 を実行する(SC-001): `scripts/sync-agent-env.py` が存在しないこと、`grep -rl "generated from" .agents .codex`(`plugins/superpowers` を除く)が 0 件、`git diff --stat -- .claude vendor` が 0 件。出力を、納品書に貼る

**Checkpoint**: 独立した正本になった。

---

## Phase 3: User Story 2 - コマンド 1 つで、main に出す構成を組み立てる (Priority: P2)

**Goal**: `scripts/build-main.py` で、`main` に出す構成を、出力先に組み立てる。

**Independent Test**: quickstart の 2〜3。

- [X] T005 [P] [US2] `scripts/templates/` を作る: `main-AGENTS.md`(rules の案内のみ。`develop` の `AGENTS.md` の「rules の案内(Codex 向け)」の節と同じ内容。ツールの表、読み替え表、セキュリティの節、ブランチ運用は含めない)、`main-CLAUDE.md`(`@AGENTS.md` のみ)、`main-claude-settings.json`(data-model.md の内容。個人の設定を含めない)、`main-codex-marketplace.json`(superpowers、Unity、i-have-adhd を、Git の URL で指す)。README のひな形は T011 で作る
- [X] T006 [US2] `scripts/build-main.py` の骨組みを作る(contracts/build-main.md): 引数(`--out`、`--check`)、リポジトリのルートをスクリプトの位置から見つける、`git ls-files` を、`cwd` を指定して読む、許可リスト(data-model.md の「`main` の構成」)、LF で書く、順序と JSON の整形を固定する、終了コード 0・1・2、出力に個人のパス(`C:/Users`、`C:\Users`、ユーザー名)や `settings.local.json` が入っていないことの検査(入っていたら終了コード 2)
- [X] T007 [US2] 組み立てを足す: 追跡済みの `.claude/`(`settings.local.json` を除く)・`.codex/`・`.agents/`(`plugins/marketplace.json` を除く)・`.claude-plugin/marketplace.json`・`.gitattributes` の複製、テンプレートからの出力(`.claude/settings.json`、`.agents/plugins/marketplace.json`、`AGENTS.md`、`CLAUDE.md`、`README.md`)、Unreal の `.gitmodules`(Unreal のみ)。Unreal の submodule の中身(`vendor/unreal-engine-skills-for-claude-code-plugin`)は、出力先に、ファイルとして複製する(コミットでの gitlink 化は、T013)。submodule が空なら、終了コード 2
- [X] T008 [US2] 組み立てを実行し(出力先は、リポジトリの外)、quickstart の 2〜3 を実行する(SC-002、SC-003): 2 回の出力の `diff -r` が空、`--check` の終了コード 0、`specs/`・`docs/`・`scripts/`・`.specify/`・`vendor/` の superpowers・Unity・i-have-adhd が、出力にないこと、個人のパスが 0 件、`AGENTS.md` が `develop` の 134 行より大幅に短いこと。出力を、納品書に貼る

**Checkpoint**: `main` に出す構成が、組み立てられる。

---

## Phase 4: User Story 3 - 外部プラグインを、別に導入できる (Priority: P3)

**Goal**: `main` の利用者が、手順書どおりに、外部プラグインを別導入できる。

**Independent Test**: quickstart の 4。

- [X] T009 [US3] 外部プラグインの導入の設定の実在を確かめる: 各 `vendor/<名前>/.claude-plugin/marketplace.json` の `name`(`superpowers-dev`、`unity-agent-plugin`、`i-have-adhd`)と、テンプレートの `extraKnownMarketplaces` のキーが一致すること。`vendor/*/.codex-plugin/plugin.json` の `name`(Codex のマーケットプレイスの `plugins[].name` と一致)。リポジトリの URL(`.gitmodules`)と、テンプレートの `repo`・`url` の一致。ずれがあれば、テンプレートを直す
- [X] T010 [US3] `claude plugin install --help`、`claude plugin marketplace --help` で、README に書くコマンドとフラグ(`--scope project`、`marketplace add`)が、実在することを確かめる。Codex の `codex plugin marketplace add` と、Antigravity の `agy plugin install` は、このマシンに CLI がないため、公式の資料(https://developers.openai.com/codex/plugins/build.md、https://antigravity.google/docs/plugins)の記述として書く(実機では未確認と書く)
- [X] T011 [US3] `scripts/templates/main-README.md` を作る: `main` の概要、clone して開く方法(Claude Code・Codex・Antigravity)、外部プラグインの別導入の手順(Claude: 信頼ダイアログの後、`claude plugin install <名前>@<マーケットプレイス> --scope project` を、clone ごとに 1 回。Unreal は、ローカルのマーケットプレイスの相対パスのため、導入不要。Codex: `.agents/plugins/marketplace.json` のマーケットプレイスから、アプリで導入。Antigravity: `agy plugin install <URL>`、IDE は、手でフォルダを置く)、個人の設定の例(`.claude/settings.local.json` に足す `language` など。コピーできる形)、`bash` が要ること(Windows は Git for Windows か WSL)、制約と、確かめていないこと(T009・T010 の結果)。T007 の組み立てに、これを足す
- [X] T012 [US3] `claude plugin validate <出力先>` を実行し(マーケットプレイスの検証。エラーなし。警告の内容を記録)、`python -m json.tool` で、出力の `.claude/settings.json` と `.agents/plugins/marketplace.json` が、有効な JSON であることを確かめる。導入の試験は、**実行の前に、ユーザーに確認する**(外部の 3 つは、GitHub から取得するため、ネットワークが要る)。(結果: 検証は通った。導入の試験は、実施しなかった。理由: このマシンでは、外部 3 つのマーケットプレイスが、すでにユーザー設定に登録済みで、隔離したスコープで導入しても、005 の試験の繰り返しになり、`main` の `.claude/settings.json` の `extraKnownMarketplaces` と `enabledPlugins` の新しい動作(信頼ダイアログの後、プロジェクト単位)は、対話の操作が要るため、T017 のユーザー検収で確かめる。)確認が取れたら、隔離したスコープで、005 と同じ手順(`marketplace add`、`install --scope local`、`uninstall`、`prune`、`marketplace remove`)で行い、導入できた数を、SC-004 として、すべて報告し、後始末をして、ハーネスの `claude plugin list` が変わっていないことを確かめる

**Checkpoint**: 導入の設定と手順書が、確かめられた範囲で、そろう。

---

## Phase 5: User Story 4 - ローカルの変換ブランチにコミットできる (Priority: P4)

**Goal**: 組み立てた出力を、ローカルの変換ブランチ(`main-build`)に、コミットできる。

**Independent Test**: 使い捨てのブランチ名で試し、後始末する。

- [X] T013 [US4] `scripts/publish-main-branch.py` を作る(contracts/build-main.md): `git worktree` で、ローカルの変換ブランチを、リポジトリの外の作業フォルダに開き、中身を、`build-main.py` の出力に置き換えて、コミットする。**push しない。`main` に触れない。** 変更がなければコミットしない。`develop` に未コミットの変更があるときは、終了コード 2。Unreal の submodule は、gitlink(`git update-index --add --cacheinfo 160000,<`develop` の Unreal のコミット>,vendor/unreal-engine-skills-for-claude-code-plugin`)で入れる(`git worktree` との組み合わせが難しければ、手順を文書化して、報告する)。コミットの本文に、`develop` の短いハッシュを書く。試験は、使い捨てのブランチ名で行い、`git worktree remove` とブランチの削除で後始末する。ブランチの削除は、権限の確認が出るため、**実行の前に、ユーザーに確認する**
- [X] T014 [US4] `docs/共有環境/変換ブランチ.md` を作る: 流れ(`develop` → `main-build` → `main`)、組み立てとコミットの手順(`build-main.py`、`publish-main-branch.py`)、`main` に置くもの・置かないもの、`main` への PR・マージは、ユーザーの確認のもとで別に行うこと、確かめていないこと。`AGENTS.md` の「このリポジトリ独自のルールとスキル」の表に、新しいスクリプトと文書の行を足す

**Checkpoint**: ローカルの変換ブランチに、`main` に出す構成をコミットできる。

---

## Phase 6: Polish & Cross-Cutting

- [X] T015 変わっていないことを確かめる(SC-005): T001 の記録との比較。`.claude/` の SHA-256、`git diff --stat -- vendor .claude` が 0 件、`bash .claude/hooks/window-reminder.sh` の出力が同一、`claude plugin list` が同一
- [X] T016 納品書を `docs/納品書/006-plugin-conversion-branch.md` に、`docs/納品書/_template.md` から書く。完了の判定の各項目に 1 つの節を置き、3 つの欄(何をしたか、確認した方法=コマンドと出力の要点、確認していないこと)を埋める。続けて、`window-verifier` を呼ぶ(本件は必ず呼ぶ)。報告は、末尾に全文で追記し、状態は「確認待ち」にする
- [ ] T017 [ユーザー検収] 実機で確かめる(quickstart の 6): `main` 相当の出力を、別のフォルダで開き、Claude Code・Codex・Antigravity で、スキルと rules(窓口)が効くこと。README の手順どおりに、外部プラグインを導入できること。結果を、納品書に反映する
- [ ] T018 納品書の承認を、ユーザーが行う(状態を「確認待ち」から「承認済み」に)

---

## Dependencies & Execution Order

- T001 → US1(T002 → T003 → T004)→ US2。
- US2: T005 は並行できる。T006 → T007 → T008。T005 は T007 の前に終える。
- US3: T009・T010 は、T005 の後に並行できる。T011 は T009・T010 の後。T012 は T008・T011 の後。
- US4: T013 は T008 の後。T014 は T013 の後。
- Phase 6 は、すべての後。

## Implementation Strategy

1. **MVP**: T001〜T004(同期の廃止と、独立した正本)。`develop` の構成が、確定する。
2. US2(組み立て)、US3(外部プラグインの導入の設定と README)、US4(ローカルの変換ブランチ)を足す。
3. Phase 6 で、検証、納品書、検査。実機の確認(T017)は、ユーザー。

## Notes

- 外向きの操作(push、PR、`main` へのマージ)は、このタスクに含めない。
- 公式で確認できなかった点(Codex の `source.url` の動作、i-have-adhd の Antigravity 対応、`directory` の `path: "."` の基準、`git worktree` と submodule の組み合わせ)は、推測で埋めない。
- 正本が 3 か所に分かれるため、ツールの間で、同じ内容の文言がずれていく。今回は、ずれを検知する仕組みを作らない。
