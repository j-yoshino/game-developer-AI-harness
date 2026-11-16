# Research: Codex・Antigravity での実装フローの穴を塞ぐ

調査日: 2026-11-16。ここに書く事実は、公式ドキュメントの本文で確認できたものだけ。二次資料は、そう明記する。

## R1: Claude 固有の道具の洗い出し(SC-001 の母集団)

`grep` で、`.claude/rules`、`.claude/agents`、`.claude/skills`、`AGENTS.md` を調べた結果。

| 道具・項目 | 出現箇所 |
|---|---|
| `AskUserQuestion`(ユーザーへの選択肢の質問) | `.claude/rules/answer-policy.md:24`、`.claude/rules/window.md:49`、`.claude/rules/window.md:82` |
| `Agent` ツールと `subagent_type`(サブエージェントの呼び出し) | `.claude/rules/window.md:30`(確かめる者)、`:48`(相談役)、`.claude/agents/window-verifier.md:49`(Unity・Unreal のレビュー)、`.claude/skills/check-claude-docs/SKILL.md:15-18`(`claude-code-guide`) |
| エージェントの `tools:`(`Read`、`Grep`、`Glob`、`Bash`、`Write`、`Edit`、`Agent`) | `.claude/agents/` の 9 ファイルの frontmatter(4 行目) |
| エージェントの `model:`(`sonnet`、`opus`) | 同 9 ファイルの frontmatter(5 行目) |
| `claude-code-guide`(Claude 専用の組み込みエージェント) | `.claude/skills/check-claude-docs/SKILL.md` |

- `Skill` ツール、`TodoWrite`、`Task` ツールの出現は、0 件だった。
- 「スキルを `/speckit-plan` のように呼ぶ」書き方は、`AGENTS.md` と各スキルにある。Codex・Antigravity での呼び方は、公式で確認していない(「未確認」とする)。

## R2: `AskUserQuestion` の対応

- **Codex**: 公式ドキュメントでは確認できなかった。二次資料(コミュニティの投稿とミラーされたコミット)では、`request_user_input` という道具がある。Plan モード限定で、Default モードでは、機能フラグ `default_mode_request_user_input` が要る(開発中の表示)。出典: https://community.openai.com/t/let-a-codex-skill-raise-a-modal-request-user-input-in-default-mode-and-an-enterplanmode-exitplanmode-tool/1381866(二次資料)。
- **Antigravity**: 対応する道具名を、公式で確認できなかった。
- **Decision**: 読み替え表では、両ツールとも「通常の文章で、番号つきの選択肢を書いて質問し、返事を待つ」を、共通の読み替えにする。Codex の `request_user_input` は、「二次資料。Plan モードなら使える見込み」と添える。

## R3: サブエージェントの呼び出し(`Agent` ツール)

- **Codex**: 専用の道具やコマンドは、公式に記載がない。自然な文章で、エージェントの名前を指して頼む(例: 「`pr_explorer` に、影響する経路を調べさせて」)。`AGENTS.md` やスキルの指示で、委任させることもできる。エージェントの定義は、TOML(`name`、`description`、`developer_instructions` が必須)。出典: https://learn.chatgpt.com/docs/agent-configuration/subagents.md。
- **Antigravity**: `subagent: true`(既定)のエージェントを、主エージェントが `invoke_subagent` ツールで呼ぶ。引数の仕様は、公式に記載がない。実行中のサブエージェントには、プロンプトを `@名前` で始めて指示する。出典: https://antigravity.google/docs/subagents.md。
- **Decision**: 読み替え表に、上の 2 行を書く。呼び出し方の動作は、前回の実機確認(Codex・Antigravity IDE とも「全部成功」。内訳は未確認)に基づく。

## R4: 相談役の読み取り専用の制限

- **Codex**: エージェントごとの読み取り専用は、**できない**。公式: 「`sandbox_mode`、`approval_policy`、`model_provider`、`mcp_servers` などは、カスタムエージェントのファイルに書いても、親の設定を上書きしない」。サブエージェントは、親のサンドボックスを引き継ぐ。指示で「編集しない」と頼めるが、「別の読み取り専用のサンドボックスは作られない」。読み取り専用にしたければ、親のセッションのサンドボックスを設定する(https://learn.chatgpt.com/docs/agent-configuration/subagents.md)。
- **Antigravity**: frontmatter に `tools`(使える道具の明示リスト)があり、これが、最も近い制御。ただし、**道具の名前が、Claude と違う**。公式の例に出てくる名前は `view_file`、`replace_file_content`、`grep_search`、`run_command` の 4 つのみ。「対応しない・綴りを誤った道具の名前は、サブエージェントを固まらせることがある」と書いてある(https://antigravity.google/docs/subagents.md)。`Glob` や、ファイルの一覧に当たる道具の名前は、確認できなかった。`model` は `inherit` / `flash` / `pro` で、Claude の `sonnet` / `opus` とは別。
- **発見(前回の生成の不具合の可能性)**: 現在、`.agents/agents/<name>.md` は、`.claude/agents/` のコピー(`tools: Read, Grep, Glob`、`model: opus` など)。Antigravity の仕様では、これらの名前は対応せず、「固まる」可能性がある(推論。前回の実機確認は、この点を見ていない可能性がある)。
- **Decision**:
  - Antigravity: 生成時に、frontmatter を Antigravity の形に変換する。`tools` は、`Read`→`view_file`、`Grep`→`grep_search`、`Bash`→`run_command`、`Write`・`Edit`→`replace_file_content`。`Glob` と `Agent` は、対応が確認できないため、リストに入れず、変換の注記に書く。`model` は、`inherit`(Claude の `sonnet`・`opus` は、対応しない)。`subagent: true`、`mainAgent: false`。
  - 相談役の `tools` は `Read, Grep, Glob`(書き込み・コマンドなし)なので、変換後は `view_file`、`grep_search` のみ。書き込めない(公式: `tools` は「許可する道具の明示リスト」)。
  - Codex: 制限できない。生成する TOML の `developer_instructions` の先頭に、「読み取り専用: ファイルの作成・編集・削除や、状態を変えるコマンドをしない」という注意を足す(正本の `tools` が読み取り専用の道具だけのエージェントに限る)。指示による制限で、強制ではない。親のセッションを読み取り専用にする手順を、共有の一覧に書く。

## R5: superpowers の導入(環境構築方式。ユーザーの指示: コピーではなく環境構築)

- 公式の導入(`vendor/superpowers/README.md:84-112`):
  - Antigravity: `agy plugin install https://github.com/obra/superpowers`(CLI)。
  - Codex: 公式のプラグイン一覧(CLI は `/plugins`、ChatGPT デスクトップアプリはサイドバーの Plugins タブのプラス ボタン)。導入の後、新しいセッションを始める(https://learn.chatgpt.com/docs/plugins)。Codex のプラグインを、設定ファイルで有効にする方法は、この公式ページに記載がない(`~/.codex/config.toml` に `[plugins."名前@マーケット"]` の項目があるが、書式の公式の説明は未確認)。IDE 拡張は、プラグインに対応しない。
- **Antigravity IDE**(ユーザーが導入済み): IDE には、導入のコマンドも、マーケットプレイスの操作も、公式に記載がない。プラグインのフォルダを、次のどちらかに置く(https://antigravity.google/docs/plugins)。
  - プロジェクト単位: `.agents/plugins/` (プロジェクトのルート)。そのプロジェクトでだけ有効。
  - 全体: `~/.gemini/config/plugins/`。すべての IDE のウィンドウで有効。
  - 読み込まれた項目は、エージェントのサイドパネルの「Customizations」のドロップダウンで確かめる。
  - `plugin.json` は、プラグインのルートか `.antigravity-plugin/plugin.json`(superpowers には、後者がある)。
- **Decision**: 手順書と、Antigravity IDE 用の配置スクリプトを作る。
  - `docs/共有環境/環境構築.md`(新規): Codex(アプリのサイドバーの操作。ユーザーが行う)と、Antigravity IDE(配置の手順)。確かめた範囲と、確かめていない範囲を書く。
  - Antigravity IDE の配置は、**プロジェクト単位**(ユーザーの指示): `vendor/superpowers` から、必要なファイルを `.agents/plugins/superpowers/` へ置く。そのプロジェクトでだけ有効になる(公式)。ホーム(`~/.gemini/`)は変えない。スクリプトは `scripts/setup-antigravity-plugins.py`(`--dry-run` で、置く先と中身を表示するだけ)。
  - 置くもの: `vendor/superpowers` のうち、`.git`、`tests/`、`docs/`、ほかのツール向けの隠しフォルダ(`.codex-plugin`、`.cursor-plugin`、`.devin-plugin`、`.hermes-plugin`、`.kimi-plugin`、`.muse-plugin`、`.opencode`、`.pi`、`.github`)を除いたもの。`.antigravity-plugin/plugin.json` とスキルを含める。**どのファイルが必須かは、公式に記載がなく、未確認**。足りなければ、実機の結果で直す。
  - **Git で追跡しない**(私の判断): 置いたものは、`vendor/superpowers`(submodule)から作れる派生物で、約 106 ファイルになる。`.gitignore` に `.agents/plugins/superpowers/` を足す。新しく clone したら、スクリプトを実行する。
  - 同期スクリプトには、superpowers のコピーを足さない。
- **注意**: プラグインとして入れると、`writing-plans`、`executing-plans`、`subagent-driven-development` も入る。`AGENTS.md` の「使わない」方針は、Claude と同じく、指示で守らせる(強制ではない)。この点を、手順書に書く。
- **未確認**: Antigravity IDE が、`~/.gemini/config/plugins/superpowers/` を読み込んで、`using-superpowers` を会話の最初に読み込むか(README の記述は、`agy plugin install` で入れた場合)。Codex のアプリで、superpowers が公式の一覧に出るか(README の記述のみ)。

## R6: 読み替え表の置き場

- **Decision**: `AGENTS.md` に節を足す(ユーザーの選択)。ただし、表は 8 行前後なので、`AGENTS.md` の読み込み量は、わずかに増える。長くなりすぎる場合に、表だけを別ファイルにする判断は、実装時に行う(今回は、`AGENTS.md` の中)。
