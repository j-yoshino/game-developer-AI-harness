# Research: Codex・Antigravity を Claude と同じ環境で使えるようにする

調査日: 2026-11-15。ここに書く事実は、公式ドキュメントの本文で確認できたものだけ。二次資料の主張は、そう明記する。

## R1: 参照の方法(シンボリックリンクか、コピーか)

- **Decision**: 生成スクリプト(コピー)にする。`.claude/` を正本とし、`.agents/` と `.codex/` の内容を生成する。`--check` で、正本との一致を検査する。生成したファイルは、Git に含める。
- **Rationale**: このリポジトリの `core.symlinks` は `false`(`git config`、`C:/Program Files/Git/etc/gitconfig` と `.git/config` の両方)。Windows の Git は、シンボリックリンクを、リンク先のパスを書いた普通のファイルとして保存する。Codex は「シンボリックリンクされたスキルのフォルダを辿る」(https://learn.chatgpt.com/docs/build-skills)が、Git 経由で配る前提では使えない。
- **Alternatives considered**: (a) シンボリックリンク: 上の理由で却下。有効にするには、Windows の開発者モードと `core.symlinks=true` が要り、他の環境で壊れる。(b) ジャンクション: Git が追跡できない。(c) `.agents/` を正本にして `.claude/` を生成する: ユーザーが `.claude/` を正本と決めた(依頼票)。
- **残る注意**: 生成物が Git に入るため、`.claude/` を直したのに、スクリプトを実行し忘れると、ずれる。`--check` を、`AGENTS.md` の手順と、完了の判定で使う。自動で走らせる仕組み(pre-commit など)は、このリポジトリに無く、作らない(やらないことの範囲を超える)。

## R2: スキル

- Codex は、スキルを `.agents/skills`(作業ディレクトリからリポジトリのルートまでの各階層)、`$HOME/.agents/skills`、`/etc/codex/skills` から読む。`.claude/skills` は、公式ページに記載がない。同名のスキルは統合されず、両方表示される(https://learn.chatgpt.com/docs/build-skills)。
- Antigravity CLI は、`.agents/skills/<name>/SKILL.md` を読む(https://antigravity.google/docs/customization-discovery/)。
- **Decision**: `.claude/skills/<name>/` を、`.agents/skills/<name>/` へ、フォルダごとコピーする(18 件)。両ツールが同じ場所を読む。
- 既存の ECC 由来の 6 件は、`.claude/skills/` と内容が一致する(`diff -rq` で、cpp-coding-standards と cpp-testing の 2 件を確認済み。残りは tasks で確認する)。

## R3: エージェント

- Antigravity: `.agents/agents/<name>.md` または `.agents/agents/<name>/agent.md`(https://antigravity.google/docs/customization-discovery/)。frontmatter の項目(`tools`、`model` など)の仕様は、エージェントのページが 404 のため、**確認できなかった**。
- Codex: 標準のカスタムエージェントは、TOML ファイル(1 ファイル 1 エージェント)。個人用は `~/.codex/agents/`、プロジェクト用は `.codex/agents/`。必須項目は `name`、`description`、`developer_instructions`(https://developers.openai.com/codex/subagents、検索結果の要約から。ページ本文の取得は、していない)。コミュニティの報告(二次資料)に、`.codex/agents/*.toml` が、ツール経由のセッションで名前で呼べなかった、という不具合の記載がある。
- **Decision**: (a) Antigravity 向けに、`.claude/agents/<name>.md` を、`.agents/agents/<name>.md` へコピーする(9 件)。(b) Codex 向けに、`.codex/agents/<name>.toml` を生成する。`name` と `description` は frontmatter から、`developer_instructions` は本文から作る。`tools` と `model` は、Codex の項目に対応させず、落とす(Codex の項目名を確認できていない)。
- **Risk**: Antigravity が Claude 形式の frontmatter を受け付けるかは、未確認。既存の ECC 由来の 5 件(`.agents/agents/`)は Claude 形式のままだが、ECC の作りが正しい証拠にはならない。実機の確認は、ユーザー検収。

## R4: rules

- Antigravity: `.agents/rules/*.md`(直下のファイルのみ。サブフォルダは、`rules.json` に登録しない限り無視される)。frontmatter は `trigger`(`model_decision` / `always_on` / `glob` / `manual`)が必須で、`glob` のときは `globs`(カンマ区切り)を使う。**`paths` キーは、仕様にない。frontmatter が無い、または `trigger` が不明なファイルは、黙って捨てられる**。1 ファイル 24,000 バイトまで。`always_on` の合計に 20,000 トークンの予算がある(https://antigravity.google/docs/rules.md)。
- Codex: 指示は `AGENTS.md` のみ(`AGENTS.override.md` と、設定した別名も)。rules に相当する、Markdown の読み込み先は、確認できなかった。`@` による取り込みの記載も、公式ページにない(https://learn.chatgpt.com/docs/agent-configuration/agents-md)。
- **Decision**: (a) Antigravity 向けに、`.claude/rules/<dir>/<file>.md` を、`.agents/rules/<dir>-<file>.md` として、frontmatter を変換して生成する(`paths` あり→`trigger: glob` と `globs`、`paths` なし→`trigger: always_on`)。(b) Codex 向けには、生成せず、`AGENTS.md` に「案内の節」を足す(ユーザーの指示)。節には、毎回読む rules(`window.md`、`answer-policy.md`)と、作業の種類ごとに読む rules のフォルダ(C++、C#、Rust、Unity、Unreal)を、「読め」という文で書く。自動で読み込まれるわけではなく、モデルが指示に従って読みに行く形で、Claude の `paths` による読み込みより確実性が落ちる(推論。実機では未確認)。Antigravity にも、同じ `AGENTS.md` が読まれるが、`.agents/rules/` と重ねても、害はない(同じ内容を指す)。
- **発見**: 既存の ECC 由来の `.agents/rules/*.md`(15 件)は、`paths:` の frontmatter のままで、`trigger` が無い。上の仕様どおりなら、Antigravity に捨てられている(推論。実機では未確認)。生成で、この 15 件の内容が変わる。やらないことの「ECC 由来の既存 `.agents/` の内容を変えない」は、「重なる分の整理の方針は、計画で決める」と書いてあり、ここで決める: **生成物で置き換える**(ユーザーが、置き換えに同意済み)。`ecc-install-state.json` は、記録が古くなる(ECC の更新・削除の動作は、未検証)。
- `window.md` と `answer-policy.md` は、`paths` が無く `always_on` になる(合計 約 10.8 KB)。予算には収まる見込み。

## R5: フック

- Codex: `<repo>/.codex/hooks.json`(または `config.toml` の `[hooks]`)に書く。`UserPromptSubmit` がある。標準出力のテキスト、または `hookSpecificOutput.additionalContext` の JSON が、開発者コンテキストとして追加される。Windows 用の上書き `commandWindows` がある。**プロジェクトの `.codex/` が信頼されたときだけ読み込まれ、フックは、レビューして信頼するまで動かない**(`/hooks` で行う)(https://learn.chatgpt.com/docs/hooks)。Windows で動くことは、公式ページに明記がない。
- Antigravity: `.agents/hooks.json`。イベントは `SessionStart`、`PreToolUse`、`PostToolUse`、`PreInvocation`、`PostInvocation`、`Stop`。**ユーザーのプロンプト送信に当たるイベントはない**。近いのは `PreInvocation`(「モデルを呼ぶ前」)。`injectSteps` の `ephemeralMessage` で、一時的なメッセージを入れられる(https://antigravity.google/docs/hooks)。Windows での書式は、公式に記載なし。
- 既存の `window-reminder.sh` の出力は、`{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"..."}}`。Codex の JSON 形式と同じ形である。
- **Decision**: (a) Codex: `.codex/hooks.json` に `UserPromptSubmit` を書き、`.claude/hooks/window-reminder.sh` を、そのまま呼ぶ(コピーしない。正本は 1 つ)。(b) Antigravity: `.agents/hooks.json` に `PreInvocation` を書き、`window-reminder.sh` の出力を `injectSteps` の形に変える薄い変換スクリプトを呼ぶ。`PreInvocation` は、プロンプトごとではなく、モデル呼び出しごとに走る可能性があり(ツール実行のたびに注意が繰り返される)、Claude と動作が一致しない。この差を、一覧に書く。
- **Risk**: 両ツールの Windows での動作は、公式に記載がなく、ここでは実機で確かめられない(`codex`・`agy` が未導入)。ユーザー検収とする。

## R6: 直下の `.claude-plugin` を、vendor 側と同じ形に揃える

- vendor 側のプラグインは、`plugin.json` と `marketplace.json` を、`.claude-plugin/` に持つ(superpowers、i-have-adhd、unity)。Unreal だけは、`plugin.json` のみで、marketplace が無いため、直下の `marketplace.json` で代用している(`AGENTS.md` に記載)。
- `plugin.json` がある場合、それがプラグインの manifest になり、`strict` はデフォルトで `true`(https://code.claude.com/docs/en/plugins/marketplace-reference.md)。
- **Decision**: 直下に `.claude-plugin/plugin.json` を置く(名前と説明のみ。コンポーネントは持たない)。`marketplace.json` は残し、`unreal-engine-skills-for-claude-code` の項目も、そのままにする。`enabledPlugins` と `extraKnownMarketplaces`(`settings.local.json`)は変えない。
- **未確認**: 直下に `plugin.json` を置いたとき、直下がプラグインとして扱われ、何かが読み込まれるか(`.claude/` は、プラグインのコンポーネントの置き場ではない)。`claude plugin validate .` と `claude plugin list` で確かめる。問題があれば、`plugin.json` は置かず、その旨を報告する(spec の Assumptions に記載)。
- 前の調査で、`extraKnownMarketplaces` の `directory` の `path` の基準(相対パス)は、公式で確認できていない。現状は動いているため、触らない。

## R7: 共有しないもの

- `.claude/commands/`(6 件)、`.claude/settings.local.json`、`.claude/ecc/` は、対象外。`.agents/workflows/`(ECC 由来の 6 件)は、そのままにする。

## R8: 既存の `.agents/`(ECC 由来)との重なり(コマンドで確認済み)

| 種類 | 既存の件数 | `.claude/` との関係 |
|---|---|---|
| スキル | 6 | 6 件とも `diff -rq` で一致(同じ内容)。生成しても、差分は出ない |
| エージェント | 5 | 5 件とも `diff -q` で一致。生成しても、差分は出ない |
| rules | 15 | 15 件とも、frontmatter に `trigger` が無い。生成で、内容が変わる(R4) |
| workflows | 6 | 対象外。そのまま |
