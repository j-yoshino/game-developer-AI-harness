# 納品書: main 用の構成を組み立てる変換ブランチ

- 状態: 確認待ち
- 依頼: [specs/006-plugin-conversion-branch/spec.md](../../specs/006-plugin-conversion-branch/spec.md)(依頼票は、spec の先頭)
- 納品日: 2026-11-17

> 状態は、置いた時点で「確認待ち」。承認はユーザーが行い、「承認済み」に変える。確認待ちの間は、完了とは言わない。

**この納品書の前提**: 当初の「自作のものを 3 つのプラグインに変換する」計画は、ユーザーの方針変更(「Claude と同じ構成で、自作したものは `.codex`・`.agents` 配下、外部から入れたプラグインはプラグイン」。案 A への「yes」)で、取りやめた。作ったのは、`main` に出す構成を組み立てるスクリプト(`scripts/build-main.py`)、ローカルの変換ブランチにコミットするスクリプト(`scripts/publish-main-branch.py`)、テンプレート 5 つ、手順書、同期の廃止。**`main` 相当の出力を、実際の Claude Code・Codex・Antigravity で開いて確かめることは、まだしていない**(最後の節がユーザー検収)。

## 完了の判定ごとの報告

### 1. `develop` の `.agents/` と `.codex/` が、`.claude/` から生成されない独立した正本になっている

- 何をしたか: `scripts/sync-agent-env.py` を削除した(`git rm`)。`.agents/` と `.codex/` の「generated from … run scripts/sync-agent-env.py」コメント 45 件(Antigravity のエージェントと rules の HTML コメント 36 件、Codex の TOML の `#` の行 9 件)を、1 回限りの置換で取り除いた。`AGENTS.md` の「他のツールとの共有」の節と表の行、`docs/共有環境/共有の一覧.md` の同期の記述を、独立した正本の説明に直した。
- 確認した方法:
  - 置換の出力: `changed 45`、`toml ok 9`、`frontmatter ok`。`git diff --stat` は、`45 files changed, 45 deletions(-)`(各ファイル 1 行の削除のみ)。
  - `ls scripts/sync-agent-env.py` → `No such file or directory`。`grep -rl 'sync-agent-env' .agents .codex`(`plugins/superpowers` を除く)→ 0 件。
  - `.agents/rules/window.md` の先頭 6 行(frontmatter の `trigger: always_on` が残る)、`.agents/agents/game-advisor.md` の frontmatter、`.codex/agents/game-advisor.toml` の先頭を目で確認した。
- 確認していないこと: 変更前に、「generated from」の検索で 46 件が出たが、うち 1 件は、`speckit-*` のスキルの文言(「Be generated from the user's phrasing…」)で、マーカーではない(変更していない)。`docs/共有環境/環境構築.md` には、同期への言及がなかった。過去の納品書、`specs/004`・`specs/005` の、同期への言及は、記録として残した。`.agents/plugins/superpowers/`(追跡されない派生物)は、触れていない。

### 2. 1 つのコマンドで、`main` に出す構成を組み立てられ、同じ入力で 2 回実行すると、同じ出力になる

- 何をしたか: `scripts/build-main.py`(`--out`、`--check`)を作った。`git ls-files` の追跡済みのファイルから、許可リスト方式で、出力先に組み立てる。テキストは LF に正規化する。
- 確認した方法: `python scripts/build-main.py --out <a>` → `153 files written`。もう一度 `<b>` に → `153 files written`。`diff -r a b` → `same output`。`--check` → `153 files, 0 differences`、終了コード 0。
- 確認していないこと: 別のマシン・別の OS での出力の同一性。

### 3. 組み立てた出力が、「`main` に置くもの」を含み、「`main` に置かないもの」を含まない

- 何をしたか: 許可リスト(`.claude/`、`.codex/`、`.agents/`、`.claude-plugin/marketplace.json`、`.gitattributes`、Unreal)と、除外(`.claude/settings.local.json`、`.agents/plugins/marketplace.json` の元のもの)を定めた。
- 確認した方法(出力 `a`):
  - 最上位: `.agents .claude .claude-plugin .codex .gitattributes .gitmodules AGENTS.md CLAUDE.md README.md vendor`。
  - `specs`・`docs`・`scripts`・`.specify`・`.gitignore`・`.claude/settings.local.json` がない(`test -e` で確認)。`vendor/` は `unreal-engine-skills-for-claude-code-plugin` のみ。
  - ファイル数: `.claude` 62、`.codex` 10、`.agents` 63、`vendor`(Unreal)12。`.gitmodules` は Unreal の 1 件のみ。
  - 個人のパス(`Disas`、`C:/Users`、`デスクトップ`)を `grep -rIl` で検索 → 0 件(スクリプトにも、出力に入ると失敗する検査がある)。
- 確認していないこと: 追跡されていないファイル(`.claude/ecc/install-state.json`、`.agents/ecc-install-state.json`、`.agents/plugins/superpowers/`)が出力にないことは、`git ls-files` を元にする作りで確かめた(個別のファイルの有無は、出力に対して、`grep` の個人のパスの検索で間接的に確認した)。

### 4. `main` 専用の最小の `AGENTS.md` が出力に含まれ、rules の案内だけを書いている

- 何をしたか: `scripts/templates/main-AGENTS.md` を作った(rules の案内、置き場所の一覧、外部プラグインは `README.md` へ)。`CLAUDE.md` は `@AGENTS.md` のみ。
- 確認した方法: 出力の `AGENTS.md` は 21 行(`develop` は 134 行)。内容は、`develop` の「rules の案内(Codex 向け)」の節と同じ案内(毎回 `window.md`・`answer-policy.md`、作業の種類ごとに `cpp/`・`csharp/`・`rust/`・`unity/`・`unreal-engine/`)と、置き場所の 4 行。ツールの表、読み替え表、セキュリティの節(SkillSpector)、ブランチ運用は含まない。
- 確認していないこと: `develop` の `AGENTS.md` と、`main` の `AGENTS.md` の差の一覧を、ファイルとして作っていない(上の説明で代えた)。

### 5. 外部プラグインが、同梱ではなく、導入の設定と手順書で扱われている

- 何をしたか: `.claude/settings.json`(テンプレートから。窓口のフックの登録、`extraKnownMarketplaces` の 4 件、`enabledPlugins` の 4 件。個人の設定は含めない)、`.agents/plugins/marketplace.json`(Codex 用。superpowers、Unity、i-have-adhd を Git の URL で指す)、`README.md`(Claude・Codex・Antigravity の導入の手順、個人の設定の例、制約)を作った。
- 確認した方法:
  - 名前と URL の一致: `vendor/*/.claude-plugin/marketplace.json` の `name`(`superpowers-dev`、`unity-agent-plugin`、`i-have-adhd`)、`vendor/*/.codex-plugin/plugin.json` の `name`(`superpowers`、`unity`、`i-have-adhd`)、`.gitmodules` の URL が、テンプレートと一致。3 つのリポジトリの既定のブランチが `main` であることを `git ls-remote --symref` で確認(読み取りのみ)。
  - `claude plugin validate`(出力 `a`)→ `Validation passed`。Unreal の `plugin.json` も `Validation passed`。`python -m json.tool` で、`.claude/settings.json`、`.agents/plugins/marketplace.json`、`.claude-plugin/marketplace.json` が有効な JSON。`vendor/superpowers`・`vendor/unity`・`vendor/i-have-adhd` への参照は、0 件。
  - README に書いたコマンドとフラグ(`claude plugin install <名前>@<マーケットプレイス> --scope project`、`claude plugin marketplace add`)は、`claude plugin install --help` と `claude plugin marketplace --help` で実在を確認。
  - i-have-adhd の自前の Codex のマーケットプレイス(`vendor/i-have-adhd/.agents/plugins/marketplace.json`)が、`{"source":"url","url":"https://github.com/ayghri/i-have-adhd.git","ref":"main"}` の形を使っていることを確認し、同じ形を、外部プラグインに使った。
- 確認していないこと: **導入の試験は、実施しなかった**(隔離したスコープで、外部 3 つを導入する試験。このマシンでは、3 つのマーケットプレイスが、ユーザー設定に登録済みで、005 の試験の繰り返しになるため。新しいクローンでの、信頼ダイアログの後の、プロジェクト単位の動作は、対話の操作が要るため、ユーザー検収)。Codex の `source.url`(Git の URL、`ref`)が公式の書式として受け付けられるか(i-have-adhd の自前の例のみが根拠。公式の資料の例は、`source: "url"` を、リポジトリのルートの指定に使う)。Unity・i-have-adhd・Antigravity の導入。i-have-adhd の Antigravity 対応(ルートの `plugin.json` の書式)。`directory` の `path: "."` の基準(公式に記載なし)。

### 6. ECC と SkillSpector の扱いが、決まった内容どおりに、出力に反映されている

- 何をしたか: ユーザーの回答(「置く」)に従い、ECC 由来のスキル・エージェント・コマンド・rules を、`main` に含めた。ECC のインストーラーの記録は、追跡されておらず(個人のパスを含む)、出力に含めていない。SkillSpector は、`develop` の `AGENTS.md` のセキュリティの節にしか記述がなく、`main` 専用の `AGENTS.md` に含めていない。
- 確認した方法: 出力の `.claude/skills` に、ECC 由来の 6 件(`cpp-coding-standards`、`cpp-testing`、`csharp-testing`、`dotnet-patterns`、`rust-patterns`、`rust-testing`)、`.claude/agents` に 9 件(ECC 由来の `cpp-build-resolver`、`cpp-reviewer`、`csharp-reviewer`、`rust-build-resolver`、`rust-reviewer` を含む)、`.claude/commands` に 6 件、`.claude/rules` に `cpp/`・`csharp/`・`rust/`・`unity/`・`unreal-engine/`・`window.md`・`answer-policy.md` が含まれる(一覧で確認)。`grep -rIil skillspector <出力>` → 0 件。
- 確認していないこと: ECC のインストーラーの記録が、`main` にないことで、ECC の更新・削除の機能が、`main` で動くかは、未検証。

### 7. `vendor/` と `.claude/` に差分がなく、Claude 側の動作が変わっていない

- 何をしたか: `.claude/` と `vendor/` には、触れていない。
- 確認した方法: 作業の前に記録した `.claude/` の SHA-256(62 件、`settings.local.json` を除く)と、作業の後を比較 → `.claude hashes identical`。`git diff --stat -- vendor .claude` → 0 件。`bash .claude/hooks/window-reminder.sh` の出力が、記録と `cmp` で一致(`hook identical`)。`claude plugin list` が、記録と一致(`plugin list identical`)。
- 確認していないこと: 新しい Claude のセッションでの挙動(`AGENTS.md` の変更が、指示として届くこと)。

### 8. [ユーザー検収] `main` 相当の出力を、別のフォルダで開き、3 つのツールで、スキルと rules が効く。外部プラグインを、手順書どおりに導入できる

- 何をしたか: 確かめる手順を、`specs/006-plugin-conversion-branch/quickstart.md` の 6 に書いた。出力の `README.md` に、導入の手順がある。
- 確認した方法: こちらでは、`main` 相当の出力を、実際の Claude Code・Codex・Antigravity で開いて確かめていない(ユーザーが操作する取り決め)。
- 確認していないこと: ユーザーが確かめる。(1) 出力(または、ローカルの `main-build` ブランチを clone した場所)を、Claude Code で開き、信頼ダイアログの後、窓口のフックが効き、`claude plugin install … --scope project` で、外部プラグインを導入できること。(2) Codex アプリで開き、`.agents/plugins/marketplace.json` のマーケットプレイスから、外部プラグインを導入できること、フックを信頼して、窓口の注意が効くこと。(3) Antigravity で開き、スキルと rules が読み込まれること。結果を、納品書に反映する。

## 追加した項目

- `scripts/publish-main-branch.py`: 依頼の「develop と main の間に、変換用のブランチ」に対する手段。`git worktree` で、ローカルの変換ブランチ(`main-build`)に、組み立てた出力を、orphan 履歴の 1 コミットとしてコミットする。`main`・`develop`・`master` には書かない。push しない。Unreal の submodule は、gitlink として入れる。試験(`--branch main-build-test --allow-dirty`)で、コミット(`a28d48e`)、gitlink(`160000 commit 0e27bde…`)、`.gitmodules`、再実行での `no change on main-build-test` を確認した。**試験用のブランチ `main-build-test` が、ローカルに残っている**(ブランチの削除は、権限の確認が要るため、ユーザーの確認を待つ)。
- `docs/共有環境/変換ブランチ.md`: 流れ、手順、置くもの・置かないもの、制約。`AGENTS.md` の表に行を足した。
- `scripts/templates/main-README.md`: `main` の README(導入の手順、個人の設定の例)。

## 確かめる者の報告

判定: 承認可

### 完了の判定との照合
- 1 同期廃止・独立した正本: 満たす — `ls scripts/sync-agent-env.py` は存在せず。`git diff --stat -- .agents .codex` は `45 files changed, 45 deletions(-)`(各1行削除のみ)。AGENTS.md・docs/共有環境・.claude に `sync-agent-env` への言及なし(grep 0件)。
- 2 1コマンドで組み立て・再現性: 満たす — `build-main.py --out a` と `--out b` を各実行(153 files written)、`diff -r` で `same`。`--out a --check` は `153 files, 0 differences`、rc=0。(`--check` だけ単独では usage エラー。`--out` が必須で、納品書の記述と矛盾はない)
- 3 置くもの・置かないもの: 満たす — 出力の最上位は `.agents .claude .claude-plugin .codex .gitattributes .gitmodules AGENTS.md CLAUDE.md README.md vendor`。`specs docs scripts .specify .gitignore .claude/settings.local.json` は存在せず。`vendor/` は Unreal のみ。`Disas` を含むファイルは 0 件。
- 4 最小の AGENTS.md: 満たす — 出力の AGENTS.md は 21 行(develop は約134行)。差の一覧ファイルは作られていないが、納品書が説明で代えたと明記している。基準は「一覧で説明」なので、ここは弱いが許容範囲。
- 5 外部プラグインの扱い: 満たす — 出力の `.claude/settings.json` に `extraKnownMarketplaces` 4件と `enabledPlugins` 4件、窓口フックの登録がある。外部3つは github 参照で同梱なし。Codex の `source.url` が公式書式かどうかは「未確認」と納品書に明記されている。
- 6 ECC・SkillSpector: 満たす — `grep -rIil skillspector` は出力内 0 件。ECC 由来ファイルは、出力の元が `git ls-files` の追跡ファイルなので含まれる。個別の件数は再確認していない。
- 7 vendor・.claude に差分なし: 満たす — `git diff --stat -- vendor .claude` は 0 件。`git status` でも `.claude`・`vendor` の変更は出ていない。変更前後の SHA-256 比較は、こちらでは再現できない(変更前の記録がない)。
- 8 [ユーザー検収]: 判定せず(下記)。

### 確認していないことの抜け
- なし

### 補足
- 試験用ブランチ `main-build-test` がローカルに残っている(納品書に明記済み)。
- 納品書の変更ファイル一覧と、こちらで導出した一覧(AGENTS.md、docs/共有環境の2件、納品書、scripts の3つ、scripts/templates、specs/006、.agents・.codex の45件)は一致した。

### 再実行の結果
- `python scripts/build-main.py --out <a>` と `--out <b>` の後、`diff -r a b`: 成功。153ファイル、同一出力。
- `python scripts/build-main.py --out <a> --check`: 成功。`153 files, 0 differences`。
- 除外物の `test -e`、`grep` で skillspector と `Disas` を検索、`git diff --stat -- vendor .claude`: 成功。除外物は出力になく、skillspector と個人名は 0 件、vendor と .claude の差分は 0 件。

### レビューの指摘
- 変更は `.py`・`.md`・`.json` のみ(`.cs`・`.cpp`・`.rs` なし): 対象外(レビュー担当は呼んでいない)。

### 確かめる者が確認していないこと
- [ユーザー検収] 完了の判定の最後の項目(Claude Code・Codex・Antigravity で出力を開き、スキルと rules が効くこと。外部プラグインを手順書どおりに導入できること): 判定していない。納品書の「確認していないこと」に、ユーザーが確かめると書かれていることは確認した。
- 外部プラグインの導入の実機の試験、Codex の `source.url` が公式書式かどうか、Antigravity での動作: 実行も判定もしていない。
- 変更前の `.claude` SHA-256 とフック出力の一致: 変更前の記録がないため再現していない。
- Windows 以外の OS での出力の同一性。
- ファイルを書き換えていないかの確認は、していない。再実行の出力先は scratchpad のみで、リポジトリには書いていない。
