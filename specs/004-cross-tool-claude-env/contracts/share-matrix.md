# Contract: 共有の一覧の書式

実装の後に、`docs/ゲーム制作/` ではなく、`docs/` の下(置き場は tasks で決める)へ置く表の書式。

| 項目 | ツール | 状態 | 理由(出典) | 確認 |
|---|---|---|---|---|
| スキル(18) | Codex | 共有 | `.agents/skills` を読む(https://learn.chatgpt.com/docs/build-skills) | 自動検査 + ユーザー検収 |
| スキル(18) | Antigravity | 共有 | 同上(https://antigravity.google/docs/customization-discovery/) | 自動検査 + ユーザー検収 |
| エージェント(9) | Antigravity | 一部 | frontmatter の仕様が未確認 | ユーザー検収 |
| エージェント(9) | Codex | 一部 | TOML に変換。`tools`・`model` は移せない。名前で呼べない不具合の報告あり(二次資料) | ユーザー検収 |
| rules(27) | Antigravity | 共有 | `trigger` を付けて生成。サブフォルダは使えないため平らにする | 自動検査 + ユーザー検収 |
| rules(27) | Codex | 一部 | 読み込み先がないため、`AGENTS.md` の案内の節で「読め」と指示する。自動では読み込まれない(推論) | ユーザー検収 |
| フック(1) | Codex | 共有 | `UserPromptSubmit` で同じスクリプトを呼ぶ。信頼のレビューが要る | ユーザー検収 |
| フック(1) | Antigravity | 一部 | `UserPromptSubmit` が無く、`PreInvocation` で近似。呼ばれる頻度が違う可能性 | ユーザー検収 |

- 状態は `共有` / `一部` / `不可` の 3 つ。`一部`・`不可` は、理由と出典が必須(SC-003)。
- 上の表は、現時点の見込み。実装の後に、実際の結果へ直す。
