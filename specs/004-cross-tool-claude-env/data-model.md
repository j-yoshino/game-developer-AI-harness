# Data Model: 共有の対応表

データベースはない。ファイル上の対応と書式である。

## 共有の対応(正本 → 参照側)

| 種類 | 正本(件数) | Antigravity が読む場所 | Codex が読む場所 | 変換 |
|---|---|---|---|---|
| スキル | `.claude/skills/<name>/`(18) | `.agents/skills/<name>/` | `.agents/skills/<name>/`(同じ) | フォルダごとコピー。変換なし |
| エージェント | `.claude/agents/<name>.md`(9) | `.agents/agents/<name>.md` | `.codex/agents/<name>.toml` | Antigravity: コピー。Codex: TOML を生成(下) |
| rules | `.claude/rules/**/*.md`(27) | `.agents/rules/<dir>-<file>.md`(直下のみ。`window.md` と `answer-policy.md` は `<file>.md`) | `AGENTS.md` の案内の節から `.claude/rules/` を読ませる(生成しない) | Antigravity: frontmatter を変換(下)。Codex: 変換なし |
| フック | `.claude/hooks/window-reminder.sh`(1) | `.agents/hooks.json` の `PreInvocation` と変換スクリプト | `.codex/hooks.json` の `UserPromptSubmit` | 正本のスクリプトを呼ぶ。コピーしない |
| 指示 | `AGENTS.md` | 同じファイルを読む | 同じファイルを読む | 「rules の案内」の節を足す(Codex 向け) |

## 変換規則

### rules(Antigravity 向け)

| 正本の frontmatter | 生成する frontmatter |
|---|---|
| `paths:` のリスト(例: `**/*.cpp`) | `trigger: glob` と `globs: "<パターンをカンマ区切り>"` |
| `paths` なし | `trigger: always_on` |

- 本文は、そのままコピーする。
- 生成物の先頭の frontmatter の後に、`<!-- generated from .claude/rules/... -->` の 1 行を入れる(手で直さないための印)。
- 1 ファイル 24,000 バイトを超えたら、スクリプトは失敗にする(Antigravity が切り捨てるため)。

### エージェント(Codex 向け TOML)

| 項目 | 元 |
|---|---|
| `name` | frontmatter の `name` |
| `description` | frontmatter の `description` |
| `developer_instructions` | frontmatter を除いた本文 |

- `tools` と `model` は、TOML に移さない(Codex の項目名を確認できていない。research R3)。
- 先頭に、`# generated from .claude/agents/<name>.md` のコメントを入れる。

### フック

| ツール | 設定の場所 | イベント | 呼ぶもの |
|---|---|---|---|
| Codex | `.codex/hooks.json` | `UserPromptSubmit` | `bash .claude/hooks/window-reminder.sh`(Windows 用の上書きは、必要なら `commandWindows`) |
| Antigravity | `.agents/hooks.json` | `PreInvocation` | `window-reminder.sh` の出力を `injectSteps`(`ephemeralMessage`)の形に変える変換スクリプト |

## 共有の一覧(各項目の状態)

| 欄 | 規則 |
|---|---|
| 項目 | 種類と名前(スキル 18、エージェント 9、rules 27、フック 1) |
| ツール | Codex / Antigravity |
| 状態 | `共有` / `一部` / `不可` |
| 理由 | `一部`・`不可` のとき、必須。出典(URL)を付ける |
| 確認 | `自動検査` / `未確認(ユーザー検収)` |

## 状態の遷移

```text
.claude/ を編集 → sync スクリプトを実行 → .agents/・.codex/ が更新される
                → --check が、正本との一致を検査する(ずれたら失敗)
```
