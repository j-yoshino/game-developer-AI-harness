# Data Model: 読み替え表と変換規則

## 読み替え表(`AGENTS.md` に書く)

| 欄 | 規則 |
|---|---|
| Claude の道具・項目 | R1 の洗い出しの 1 行につき 1 行 |
| Codex | 対応する操作。なければ「対応なし」。確認できなければ「未確認」 |
| Antigravity | 同上 |
| 出典 | URL。二次資料のときは、「二次資料」と書く |

書く行(見込み): `AskUserQuestion` / `Agent` ツールと `subagent_type` / エージェントの `tools:` / エージェントの `model:` / `claude-code-guide`(Claude 専用の組み込みエージェント)/ スキルの呼び方(`/speckit-…`)。

## Antigravity 向けエージェントの変換規則(同期スクリプト)

| Claude の frontmatter | Antigravity の frontmatter |
|---|---|
| `name` | `name`(同じ) |
| `description` | `description`(同じ) |
| `tools: Read, Grep, Glob, Bash, Write, Edit, Agent` | `tools:` のリスト。`Read`→`view_file`、`Grep`→`grep_search`、`Bash`→`run_command`、`Write`・`Edit`→`replace_file_content`。`Glob`・`Agent` は、対応を確認できないため、リストに入れない |
| `model: sonnet / opus` | `model: inherit` |
| (なし) | `subagent: true`、`mainAgent: false` |
| 本文 | 本文(同じ) |

- 先頭の frontmatter の後に、`<!-- generated from .claude/agents/<name>.md. ... -->` を入れる。
- 変換できなかった項目(`Glob`・`Agent`)は、生成物のコメントではなく、共有の一覧に書く。

## Codex 向けエージェントの注意(同期スクリプト)

- 正本の `tools` が、`Read`・`Grep`・`Glob` のみ(書き込み・コマンドなし)のエージェントに限り、TOML の `developer_instructions` の先頭に、読み取り専用の注意を足す。

## superpowers の導入(環境構築)

| 項目 | 規則 |
|---|---|
| Codex | アプリのサイドバーの Plugins タブから、ユーザーが導入する(手順書に書く)。同期の対象外 |
| Antigravity IDE | `vendor/superpowers` の必要なファイルを、`.agents/plugins/superpowers/` へ置く(`scripts/setup-antigravity-plugins.py`)。プロジェクト単位。Git では追跡しない(`.gitignore`) |
| 手順書 | `docs/共有環境/環境構築.md`。確かめた範囲と、未確認の範囲を書く |
