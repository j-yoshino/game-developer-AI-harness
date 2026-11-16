# 納品書: Codex・Antigravity での実装フローの穴を塞ぐ

- 状態: 承認済み
- 依頼: [specs/005-cross-tool-flow-gaps/spec.md](../../specs/005-cross-tool-flow-gaps/spec.md)(依頼票は、spec の先頭)
- 納品日: 2026-11-16

> 状態は、置いた時点で「確認待ち」。承認はユーザーが行い、「承認済み」に変える。確認待ちの間は、完了とは言わない。

**この納品書の前提**: 作ったのは、`AGENTS.md` の読み替え表、同期スクリプトの拡張(エージェントの変換)、superpowers の配置スクリプトと手順書、共有の一覧の更新、生成物。**Codex と Antigravity で実際に動くことは、まだ確かめていない**(最後の節がユーザー検収)。計画の途中で、ユーザーの指示により、superpowers は「コピー」ではなく「環境構築方式(プラグインとして導入)」、Antigravity は「プロジェクト単位」に変えた(plan.md、research.md R5)。調査で、004 で生成した Antigravity 向けのエージェントが、Claude の `tools`・`model` の名前のままだった(Antigravity の公式は、対応しない道具名で「固まることがある」と警告)ことが分かり、同じ変更で直した。

## 完了の判定ごとの報告

### 1. `AGENTS.md` に読み替え表があり、実装フローの Claude 固有の道具のすべてに、両ツールの対応(または「対応なし」、理由と出典つき)が書かれている

- 何をしたか: `AGENTS.md` に「道具名の読み替え表(Codex・Antigravity 向け)」の節を足した。行は、`AskUserQuestion`、`Agent` ツールと `subagent_type`、エージェントの `tools:`、`model:`、`claude-code-guide`、スキルの呼び方(未確認)の 6 行。
- 確認した方法:
  - 洗い出し: `grep -rnE "AskUserQuestion|subagent_type|\`Agent\`|claude-code-guide" .claude/rules .claude/agents .claude/skills` → `window-verifier.md:49`、`answer-policy.md:24`、`window.md:30,48,49,82`、`check-claude-docs/SKILL.md:3,11,15,17,18`。`tools:`・`model:` は `.claude/agents/` の 9 件(計 18 行)。
  - 網羅: 表の節の中に、`AskUserQuestion`、`subagent_type`、`Agent`、`tools:`、`model:`、`claude-code-guide`、`speckit-plan` が、それぞれ 1 回以上出る(`awk` の範囲を `grep -c` で数えた)。
  - 「対応なし」「未確認」「二次資料」の各行に、理由または確認できなかった旨が書いてある(表を読んで確認)。
- 確認していないこと: 両ツールでの、スキルの呼び方(`/speckit-…` の記法)は、未確認と書いた。Codex の `request_user_input`(二次資料)と、Antigravity の質問の道具は、公式で確認できていない。`invoke_subagent` の引数の仕様は、公式に記載がない。表のとおりに読み替えて実装フローが動くかは、ユーザー検収。

### 2. 相談役の読み取り専用の可否が、Codex・Antigravity のそれぞれで、共有の一覧に明記されている(できる場合は、同期の出力に反映され、`--check` が通る)

- 何をしたか: `scripts/sync-agent-env.py` の `gen_agents` を書き換えた。Antigravity 向けは、frontmatter を変換して生成する(`Read`→`view_file`、`Grep`→`grep_search`、`Bash`→`run_command`、`Write`・`Edit`→`replace_file_content`。`model: inherit`、`subagent: true`、`mainAgent: false`。`Glob` と `Agent` は、対応する道具名を確認できず、入れない。未知の道具名は、終了コード 2 で失敗)。Codex 向けは、正本の `tools` が `Read`・`Grep`・`Glob` のみのエージェント(`game-advisor` のみ)の TOML の先頭に、読み取り専用の注意を足した。Codex は、エージェントごとの読み取り専用が、公式にできない(`sandbox_mode` は親の設定を上書きしない)ため、指示による制限になる。共有の一覧に、可否・理由・出典を書いた。
- 確認した方法:
  - `python scripts/sync-agent-env.py` → `65 generated files, 10 written, 0 orphans removed`。続けて `--check` → `65 generated files, 0 drifted`、終了コード 0。
  - `git status --short .agents .codex` → 変わったのは `.agents/agents/` の 9 件と `.codex/agents/game-advisor.toml` のみ(rules・skills・フックは差分なし)。
  - `.agents/agents/game-advisor.md` の frontmatter: `tools:` が `view_file`、`grep_search` のみ、`model: inherit`、`subagent: true`、`mainAgent: false`。`window-verifier.md`: `view_file`、`grep_search`、`run_command`。
  - `grep -L "^tools:" .agents/agents/*.md` → 0 件。frontmatter に `Glob`・`model: sonnet`・`model: opus` は残っていない(本文の 1 件、`game-advisor.md` 41 行目の言及を除く)。
  - Codex: `grep -c "Read-only: do not"` → `game-advisor.toml` のみ 1、ほか 8 件は 0。`tomllib` で 9 件が読め、キーは `name`、`description`、`developer_instructions` の 3 つのみ。
- 確認していないこと: 変換後の Antigravity のエージェントが、固まらず、`game-advisor` が書き込まないこと(ユーザー検収)。`Glob`・`Agent` の道具名は確認できていない。`window-verifier` が入れ子で Unity・Unreal のレビューを呼ぶことが、Antigravity で動くか。Codex の注意は、指示であり、強制ではない。ECC 由来のエージェント 5 件の内容が、変換で変わった(元は Claude 形式のコピー)。

### 3. superpowers(`brainstorming`)を両ツールで使う方法が、公式または submodule の記述に基づく手順として文書化されている

- 何をしたか: `docs/共有環境/環境構築.md` を作った(Codex アプリ・CLI の導入、Antigravity IDE の配置、注意、確かめていないこと)。`scripts/setup-antigravity-plugins.py` を作り(`--dry-run` あり)、`vendor/superpowers` から `.agents/plugins/superpowers/` へ 106 ファイルをコピーした(`.git`、`tests`、`docs`、他ツール向けの隠しフォルダなどを除く)。`.gitignore` を新規に作り、`.agents/plugins/superpowers/` を追跡しない。共有の一覧に、superpowers の 2 行を足した。
- 確認した方法:
  - `python scripts/setup-antigravity-plugins.py --dry-run` → `destination: .agents/plugins/superpowers`、`files: 106`、除外の一覧。何も書かれない。
  - 実行 → `copied 106 files`。`.agents/plugins/superpowers/.antigravity-plugin/plugin.json` と `skills/brainstorming/SKILL.md` があり、`skills` は 15 個。
  - `git check-ignore -v` → `.gitignore:2:.agents/plugins/superpowers/` で無視される。`git status --short .agents/plugins` → 0 件。
  - `git diff --stat -- vendor` → 0 件(`vendor/` は読むだけ)。
- 確認していないこと: Antigravity IDE が、`.agents/plugins/superpowers/` を読み込むこと(ユーザー検収)。プラグインの必須ファイルの範囲(公式に記載なし。除外した分が不足の可能性)。`using-superpowers` の自動読み込み。Codex の公式の一覧に superpowers が出ること、Codex の設定ファイルだけで有効にする方法(公式に記載なし)。プラグインに、方針で「使わない」と決めた `writing-plans` などが含まれること(手順書に注意を書いた。指示で守らせる形で、強制ではない)。

### 4. `.claude/` の差分が 0 件、`vendor/` の差分が 0 件、`--check` が成功する

- 何をしたか: `.claude/` と `vendor/` には、触れていない。
- 確認した方法: 変更前に `.claude/` のファイル(`settings.local.json` を除く 62 件)の SHA-256 を記録し、変更後と比較 → `.claude hashes identical`。`git diff --stat -- .claude vendor` → 出力なし。`git status --short vendor` → 0 件。`python scripts/sync-agent-env.py --check` → `65 generated files, 0 drifted`。
- 確認していないこと: `AGENTS.md` の追記(表と節)が、Claude の挙動に与える影響(指示が増える)は、新しいセッションでは確かめていない。

### 5. [ユーザー検収] 実機で、読み替え表のとおりに、実装フローの一部が動く

- 何をしたか: 確かめる手順を、`specs/005-cross-tool-flow-gaps/quickstart.md` の 7 に書いた。
- 確認した方法: Codex アプリと Antigravity IDE は、ユーザーのマシンにあるが、こちらでは、アプリを操作して確かめていない(ユーザーが操作する取り決め)。
- 確認していないこと: ユーザーが確かめる。(1) Antigravity IDE で `game-advisor` を呼び、書き込まず、固まらないこと。(2) Codex アプリで `window-verifier` を名前で頼めること。(3) 手順書のとおりに、両ツールへ superpowers を導入し、`brainstorming` が使えること。結果は、共有の一覧の「実機の結果」に反映する。

## 追加した項目

- `.gitignore`(新規): 完了の判定に明記はないが、配置したプラグインを Git で追跡しないために必要。
- `docs/共有環境/共有の一覧.md` に、Antigravity のエージェントの変換、Codex の読み取り専用の限界、superpowers の行と、「確認できていないこと」を追記した。
- `AGENTS.md` の表に、配置スクリプトと手順書の行を足した。
- 004 の納品書の状態を「承認済み」、004 の tasks.md の T025・T026 を完了にした(ユーザーの承認と実機の報告の反映。この作業とは別の変更)。
- 確かめる者の報告の後に、`.agents/plugins/marketplace.json`(Codex 向けのリポジトリ単位のマーケットプレイス。`vendor/superpowers` を指す)を追加した。Codex の公式の一覧に superpowers が出なかったため(ユーザーの確認)。あわせて、`docs/共有環境/環境構築.md` の Codex の節と、共有の一覧の該当行を直した。**この追加は、確かめる者の検査を通していない**(JSON とドキュメントのみ)。
- Antigravity 向けエージェントのモデル指定(`opus`→`pro`、`sonnet`→`flash`): 別の納品書(`docs/納品書/2026-11-16-antigravityのモデル指定.md`)。

## 確かめる者の報告

判定: 承認可

### 完了の判定との照合
- 基準1(AGENTS.md の読み替え表): 満たす。AGENTS.md:73-84 に 6 行の表がある。AskUserQuestion、Agent と subagent_type、tools:、model:、claude-code-guide、スキルの呼び方を扱う。「対応なし」「未確認」「二次資料」の行には、理由と出典(URL または SKILL.md)がある。
- 基準2(相談役の読み取り専用の可否): 満たす。
  - Antigravity: `.agents/agents/game-advisor.md` の frontmatter は、tools が view_file と grep_search のみ。subagent: true、mainAgent: false、model: inherit。
  - Codex: `.codex/agents/game-advisor.toml:5` に "Read-only: do not create, edit or delete files..." がある。強制できない理由(sandbox_mode は親の設定を上書きしない)と出典は、`docs/共有環境/共有の一覧.md:14` にある。
  - `python scripts/sync-agent-env.py --check` は成功した(下記)。
- 基準3(superpowers の手順の文書化): 満たす。`docs/共有環境/環境構築.md` が新規にある。`共有の一覧.md:19-20` に、Codex と Antigravity の行がある。`.agents/plugins/superpowers/skills` は 15 個。`brainstorming/SKILL.md` が実在する。`.gitignore:2` で追跡から外れている。公式に記載がない点は、「確認できていないこと」に明記されている。
- 基準4(.claude と vendor の差分 0 件、--check 成功): 満たす。`git diff --stat -- .claude vendor` は出力なし。`git status --short vendor .claude` も出力なし。--check は 0 drifted。
- 基準5([ユーザー検収] 実機の確認): 判定しない。「確かめる者が確認していないこと」に列挙した。

変更ファイル一覧は、私が導出したものと一致した(`.agents/plugins/superpowers/` は Git が無視するため、一覧に出ない)。

### 確認していないことの抜け
- なし

### 補足
- 基準1の網羅は、grep で数えた件数に基づく。表以外の箇所で Claude 固有の道具名が漏れていないかは、納品書の洗い出しコマンドの範囲内にとどまる。

### 再実行の結果
- `python scripts/sync-agent-env.py --check`: 成功。`65 generated files, 0 drifted`、終了コード 0。
- `git diff --stat -- .claude vendor`: 出力なし(差分 0 件)。
- `python scripts/setup-antigravity-plugins.py --dry-run`: 成功。`destination: .agents/plugins/superpowers`、`files: 106`。除外の一覧が出た。

### レビューの指摘
- 変更は `.py`、`.md`、`.toml`、`.gitignore` のみ: 対象外。言語・エンジン別レビューは呼んでいない。

### 確かめる者が確認していないこと
- [ユーザー検収] 基準5。Codex と Antigravity の実機で、読み替え表のとおりに実装フローが動くこと。納品書の「確認していないこと」欄に、ユーザーが確かめると書いてあることは確認した。
  - Antigravity で game-advisor が書き込まず、固まらないこと。
  - Codex で window-verifier を名前で呼べること。
  - 両ツールで superpowers が読み込まれ、brainstorming が使えること。
- 外部の URL(公式ドキュメント)の記述が、納品書の引用どおりか。ネットワークで確かめていない。
- AGENTS.md の追記が、新しい Claude セッションの挙動に与える影響。
- ファイルを書き換えていないかの確認は、していない。ただし、私は読み取りと実行系のコマンドしか使っていない。dry-run は何も書かない。
