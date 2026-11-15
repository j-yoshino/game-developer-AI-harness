---
name: check-claude-docs
description: Claude Code / Claude Agent SDK / Claude API / Claude Tag の公式情報を claude-code-guide エージェントに確認させる。設定キー、hooks、slash command、MCP、plugin、skill、モデルID、料金、API の仕様を調べるときに使う。
when_to_use: 「Claude Code は〜できる?」「この設定キーは実在する?」「hooks の書き方」「モデルIDは?」のように Claude 自身の仕様を確かめたいとき。記憶や推測で答える前に必ず使う。
argument-hint: 確認したいこと
allowed-tools: Agent
---

# Claude 公式情報の確認

Claude 自身の仕様(Claude Code、Claude Agent SDK、Claude API、Claude Tag)は記憶で答えず、**必ず `claude-code-guide` エージェントに確認させる**。設定キー名やフラグ名は実在しないものを書くと黙って無視されるため、裏取りが必須。

## 手順

1. **既存のエージェントを確認する。** このセッションで `claude-code-guide` を起動済みなら、`Agent` を新規に呼ばず `SendMessage` でそのエージェントに追加質問する。

2. **未起動なら `Agent` ツールで起動する。**
   - `subagent_type`: `claude-code-guide`
   - `description`: 3〜5語
   - `prompt`: 下の「プロンプトに含める内容」を満たすもの

3. **結果を検証する。** エージェントの報告は鵜呑みにしない。
   - 設定キーやフラグが返ってきたら、**公式ドキュメントの URL が付いているか**を見る。付いていなければ未検証として扱う。
   - 二次情報(ブログ、まとめサイト)だけが根拠のものは、二次情報であることを明記する。
   - このマシンで確認できるもの(インストール済みバージョン、キャッシュされたカタログ、実際のファイル)は自分で確認して突き合わせる。

4. **回答する。** 確認できた事実と、確認できなかったことを分けて書く。`.claude/rules/answer-policy.md` に従う。

## プロンプトに含める内容

- 調べたい具体的な質問($ARGUMENTS)
- **一次情報で裏を取り、ソースの URL を必ず返すこと**
- **確認できなかった項目は「未検証」と明記して返すこと。推測で埋めないこと**
- 設定キー・環境変数・CLI フラグは**正確な綴り**で返すこと
- そのキーがどの設定ファイル(user / project / local / managed)で有効かも返すこと
- 機能にバージョン要件がある場合は**最小バージョン**を返すこと

## このプロジェクトでの注意

- インストール済みの Claude Code のバージョンを `claude --version` で確認し、**調べた機能の最小バージョン要件を満たしているか**を必ず突き合わせる。要件を満たさない機能は「このマシンでは使えない」と明記する。
- バージョンを上げる提案をするときは、既存設定への影響(`.claude/settings.local.json` の `env` など)も併せて確認する。
