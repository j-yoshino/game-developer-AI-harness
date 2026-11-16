# 納品書: Codex・Antigravity を Claude と同じ環境で使えるようにする

- 状態: 承認済み
- 依頼: [specs/004-cross-tool-claude-env/spec.md](../../specs/004-cross-tool-claude-env/spec.md)(依頼票は、spec の先頭)
- 納品日: 2026-11-15

> 状態は、置いた時点で「確認待ち」。承認はユーザーが行い、「承認済み」に変える。確認待ちの間は、完了とは言わない。

**この納品書の前提**: 作ったのは、同期スクリプト 1 つ、Antigravity 向けのフック変換 1 つ、生成物(`.agents/`・`.codex/`)、`.claude-plugin/plugin.json`、共有の一覧、`AGENTS.md` の追記。**Codex と Antigravity は、このマシンに入っておらず、実際に起動して動くことは、まだ確かめていない**(最後の節がユーザー検収)。計画の途中で、ユーザーの指示により、「Codex の rules は生成せず、`AGENTS.md` の案内の節で読ませる」に変えた(plan.md、research.md R4)。

## 完了の判定ごとの報告

### 1. スキル 18・エージェント 9・rules 27 が、Codex・Antigravity が読む場所から見える

- 何をしたか: `scripts/sync-agent-env.py` を作り、実行して、`.agents/skills/`(18)、`.agents/agents/`(9)、`.agents/rules/`(27)、`.codex/agents/`(9)を生成した。rules は、`paths` あり→`trigger: glob` と `globs`(`{h,cpp,cs}` は別々のパターンに展開)、`paths` なし→`trigger: always_on` に変換した。Codex 向けの rules は、生成せず、`AGENTS.md` の「rules の案内」の節に書いた。
- 確認した方法:
  - `python scripts/sync-agent-env.py` → `65 generated files, ... written, 0 orphans removed`、続けて `--check` → `65 generated files, 0 drifted`(終了コード 0)。
  - 件数: `skills 18 18`、`agents 9 9 9`(`.claude` / `.agents` / `.codex`)、`rules 27 27`。
  - `.agents/rules/cpp-coding-style.md` の先頭: `trigger: glob`、`globs: "**/*.cpp, **/*.hpp, ..., **/CMakeLists.txt"`。`window.md` の先頭: `trigger: always_on`。`unreal-engine-coding-style.md` の `globs` は、`Source/**/*.h, Source/**/*.cpp, ...` と展開されている。
  - `.codex/agents/*.toml` 9 件を `tomllib` で読み、キーが `name`、`description`、`developer_instructions` の 3 つだけであることを確認(`toml ok 9`)。
  - `git status --short .agents`: 既存のスキル 6 件とエージェント 5 件は差分なし。rules の既存 15 件が `M`(置き換え)、残りは新規。
- 確認していないこと: Codex・Antigravity が、実際にこれらを読み込むこと(ユーザー検収)。Antigravity が、Claude 形式のエージェントの frontmatter を受け付けるか(公式のページが取得できなかった)。Codex が `.codex/agents/*.toml` を名前で呼べるか。ECC の既存 rules 15 件が、元々 Antigravity に捨てられていたかは、公式の仕様からの推論で、実機では確かめていない。`.agents/ecc-install-state.json` の記録が古くなったため、ECC の更新・削除が動くかは、未検証。

### 2. `.claude/` を 1 つ書き換えたとき、1 つのコマンドで `.agents/` にも反映される

- 何をしたか: 上のスクリプトに、生成(上書き)と `--check`(検査のみ)を持たせた。正本から消えたファイルは、参照側から削除する(同期の管理下のフォルダのみ)。
- 確認した方法: `.claude/skills/window-question/SKILL.md` の末尾に `TMP-LINE` を足し、`--check` → `differs: .agents/skills/window-question/SKILL.md`、`1 drifted`、終了コード 1。同期 → 反映(`grep -c TMP-LINE` が 1)。元に戻して再同期 → `grep -c TMP-LINE` が正本・参照側とも 0、`--check` の終了コード 0。
- 孤児の削除の確認(確かめる者の報告の後に実施): `.agents/skills/zz-orphan/SKILL.md` と `.agents/rules/zz-orphan.md` を置き、`--check` → `orphan: ...` を 2 件報告、終了コード 1。同期 → `2 orphans removed`、2 件とも消えた。再度の `--check` は `0 drifted`。`.agents/workflows/`(6 件)と `.agents/ecc-install-state.json` は残った。
- 確認していないこと: 同期の実行し忘れを防ぐ仕組み(pre-commit など)は、作っていない。

### 3. フックの共有の可否が、一覧に明記されている

- 何をしたか: `.codex/hooks.json`(`UserPromptSubmit` から、`.claude/hooks/window-reminder.sh` をそのまま呼ぶ)と、`.agents/hooks.json`(`PreInvocation` から、`.agents/hooks/window-reminder-ag.py` を呼ぶ)を生成した。変換スクリプトは、Claude のフックの出力を `{"injectSteps":[{"ephemeralMessage":...}]}` に変える(失敗時は何も出さず終了コード 0)。可否と理由は、`docs/共有環境/共有の一覧.md` に書いた(Codex は共有、Antigravity は一部)。
- 確認した方法:
  - `bash .claude/hooks/window-reminder.sh < /dev/null | cmp - <変更前の記録>` → 一致(Claude のフックの出力は、変更前と同一)。
  - `echo '{"invocationNum":1}' | python .agents/hooks/window-reminder-ag.py | python -m json.tool` → `{"injectSteps":[{"ephemeralMessage":"Request window: if a USER message asks ..."}]}`。別のディレクトリ(`/tmp`)から実行しても、同じ形で出る。
  - `.codex/hooks.json` と `.agents/hooks.json` を `json.load` で読めることを確認。
  - 不具合を 1 件直した: 変換スクリプトが、日本語を含む絶対パスを Git Bash に渡すと失敗していた(出力が空になる)。相対パスと `cwd` で呼ぶ形に直し、再確認した。
- 確認していないこと: 両ツールで、フックが実際に動くこと(ユーザー検収)。Windows での動作は、両ツールとも公式に明記がない。Codex は、プロジェクトの `.codex/` を信頼し、フックを `/hooks` でレビューするまで動かない。Antigravity の `PreInvocation` が、プロンプトごとに 1 回なのか、モデル呼び出しごとなのか(Claude と同じ頻度かは、不明)。

### 4. 直下の `.claude-plugin` が vendor 側と同じ構成になり、validate が通り、4 つが有効のまま

- 何をしたか: `.claude-plugin/plugin.json`(`name`、`description`、`version` のみ。コンポーネントなし)を足した。`marketplace.json` と `settings.local.json` は、変えていない。
- 確認した方法: 変更前後の `claude plugin list` が同じ(`i-have-adhd@i-have-adhd` 0.4.1、`superpowers@superpowers-dev` 7.0.2、`unity@unity-agent-plugin` 0.1.9-beta、`unreal-engine-skills-for-claude-code@game-developer-ai-harness` 3.1.2、4 つとも `✔ enabled`)。`claude plugin validate .` → `✔ Validation passed`(マーケットプレイスの manifest)。`claude plugin validate .claude-plugin/plugin.json` → エラーなし、警告 1 件(`author` がない)。`.` を validate したときの別の出力に、「ルートの `CLAUDE.md` はプラグインのコンテキストとして読まれない」という警告が 1 件ある。
- 確認していないこと: 警告 2 件は、残した(`author` に、個人の名前を入れることは、依頼に無いため)。直下がプラグインとして実際にインストールされたときの動作は、見ていない(marketplace.json に、直下のプラグインを載せていないため、インストールされない見込み。推論)。

### 5. Claude 側の動作が変わっていない

- 何をしたか: `.claude/` の内容は、変えていない。`AGENTS.md` に節と表の行を足した(`CLAUDE.md` が `@AGENTS.md` で取り込むため、Claude にも届く追記)。
- 確認した方法: 変更前に、`.claude/` のファイル(`settings.local.json` を除く 62 件)の SHA-256 を記録し、変更後と比較 → 差分なし。スキル・エージェント・rules のファイル一覧も一致。`window-reminder.sh` の出力も同一(上の `cmp`)。`git diff --stat -- vendor` と `git status --short vendor` が 0 件。
- 確認していないこと: `.claude/settings.local.json` には、この作業の前から、`CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` の追加という未コミットの差分がある(この作業では触れていない。ハッシュの比較からも除いた)。`AGENTS.md` の追記が、Claude の挙動に与える影響(指示が増えたこと)は、新しいセッションで確かめていない。

### 6. [ユーザー検収] 実際の Codex と Antigravity CLI で、共有したものが使える

- 何をしたか: 確かめる手順を、`specs/004-cross-tool-claude-env/quickstart.md` の 7 に書いた。
- 確認した方法: このマシンには `codex` と `agy` がない(`which` で見つからない。`gemini` のみ)ため、こちらでは起動して確かめていない。
- 確認していないこと: ユーザーが、Codex(`/hooks` でフックを信頼し、スキルが使えること、窓口の注意が注入されること)と、Antigravity CLI(スキルと rules が読み込まれること、フックが動くこと)を起動して確認する。結果を、`docs/共有環境/共有の一覧.md` の「確認」欄に反映する。

## 追加した項目

- `.agents/hooks/window-reminder-ag.py`: Antigravity は `UserPromptSubmit` を持たず、出力の形式も違うため、完了の判定の「フックの共有の可否」を満たす手段として作った。依頼に明記はないが、計画で決めた範囲内。
- `docs/共有環境/共有の一覧.md`: 完了の判定の「一覧で明記」のために作った。
- `AGENTS.md` の 2 つの節(「他のツールとの共有」「rules の案内(Codex 向け)」)と、表の 1 行。

## 確かめる者の報告

判定: 承認可

### 完了の判定との照合
- スキル18・エージェント9・rules27が読む場所から見える: 満たす。根拠は次のとおり。
  - `.claude` と `.agents` の件数は skills 18/18、agents 9/9、rules 27/27。`.codex/agents` は 9 件。
  - `diff -rq .claude/skills .agents/skills` は差分なし。`diff -rq .claude/agents .agents/agents` も差分なし。
  - rules は frontmatter を変換している。内容の一致は `--check` の 0 drifted で確認した。
- `.claude/` を書き換えると 1 コマンドで反映される: 満たす(部分的な確認)。根拠は次のとおり。
  - `python scripts/sync-agent-env.py --check` は 65 generated files, 0 drifted、終了コード 0。
  - 書き換えて検知する流れは、納品書の記述のみで、私は再現していない。`--check` に drift と orphan の検出コードがあることは `scripts/sync-agent-env.py:248-250` で確認した。
- フックの共有可否が一覧に明記されている: 満たす。根拠は次のとおり。
  - `.codex/hooks.json` は `window-reminder.sh` を呼ぶ。
  - `echo '{"invocationNum":1}' | python .agents/hooks/window-reminder-ag.py` は `injectSteps`/`ephemeralMessage` の JSON を出した。
  - 「共有の一覧.md」の中身は読んでいない。納品書の記述のみで判断した。
- 直下の `.claude-plugin` が vendor 側と同じ構成で、validate が通り、4 つが有効のまま: 満たす。根拠は次のとおり。
  - `.claude-plugin/plugin.json` が存在する。
  - `claude plugin validate .` は ✔ Validation passed。
  - `claude plugin list` は 4 つとも ✔ enabled。
- Claude 側の動作が変わっていない: 満たす。根拠は次のとおり。
  - `git status --short vendor` は 0 件。
  - 差分に出る `.claude/` のファイルは `settings.local.json` のみで、納品書が申告した、作業前からの差分。
  - SHA-256 比較の再現はしていない。
- [ユーザー検収]: 判定しない(下記に列挙)。

### 確認していないことの抜け
- なし。

### 補足
- 変更ファイルの一覧は、私が導いたものと実質一致した。差分は、既存 15 rules、`.claude/settings.local.json`、`AGENTS.md` の `M` だった。
- `.claude-plugin/plugin.json` には `author` がなく、警告が出る。納品書に記載済み。

### 再実行の結果
- `python scripts/sync-agent-env.py --check`: 成功。65 generated files, 0 drifted。
- `claude plugin validate .` と `claude plugin list`: 成功。validate は通り、4 つとも enabled。
- `diff -rq` で skills・agents を比較し、`window-reminder-ag.py` を実行した: 差分なし。出力も期待どおりだった。

### レビューの指摘
- 変更は `.py`、`.json`、`.toml`、`.md` のみ。言語・エンジン別のレビューは対象外(呼んでいない)。

### 確かめる者が確認していないこと
- [ユーザー検収] 実際の Codex と Antigravity CLI を起動して、共有したものが使えること。納品書の「確認していないこと」に、ユーザーが確認すると明記されている。
- 孤児の削除を実際に試していない。納品書も未実施と明記している。
- 書き換えて反映する手順は、私は再現していない。
- フックが Windows と両ツールで実際に動くこと。
- 私はファイルを書き換えていない。ただし、書き換えていないことの機械的な確認はしていない。

(納品書の作成者の補足: 報告の「孤児の削除を実際に試していない」は、報告の後に、作成者が実施した。上の 2 を参照。)
