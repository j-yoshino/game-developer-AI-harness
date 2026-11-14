# GameDeveloperAIHarness

ゲーム開発用の AI エージェントハーネス。

## 導入済みツール

| ツール | 置き場所 | 役割 |
|---|---|---|
| spec-kit | `.claude/skills/speckit-*`、`.specify/` | Spec-Driven Development の明示的フロー |
| superpowers | `vendor/superpowers`(submodule) | 開発方法論スキル群(自動発動) |
| SkillSpector | `uv tool`(リポジトリ外) | スキルのセキュリティスキャン |
| Unity CLI | MCP サーバー | Unity Editor 連携 |

## 計画フェーズの使い分け

**計画と実装は spec-kit を正本とする。** superpowers と spec-kit は計画スキルの発動条件が重なるため、役割を以下に固定する。

```
brainstorming(何を作るか決める・design doc 作成)
  ↓ design doc のパスを引数で渡す
/speckit-specify → /speckit-plan → /speckit-tasks → /speckit-implement
```

- **計画を書くときは `/speckit-plan` を使う。** superpowers の `writing-plans` は使わない。
- **実装は `/speckit-implement` を使う。** superpowers の `executing-plans` と `subagent-driven-development` は使わない。
- 上記3スキルは `.claude/settings.local.json` の `skillOverrides` で `user-invocable-only` にしてあり、明示的に呼ばれた場合のみ動く。
- 計画の成果物は `specs/<NNN-feature>/plan.md` に置く。`docs/superpowers/plans/` は使わない。**計画書の正本を2つ作らない。**

### superpowers 側で積極的に使うスキル

spec-kit と競合しないため、自動発動のまま活用する。

- `brainstorming` — 作る前の要件掘り起こし(spec-kit に相当機能がない)
- `test-driven-development`
- `systematic-debugging`
- `requesting-code-review` / `receiving-code-review`
- `using-git-worktrees`
- `verification-before-completion`

## セキュリティ

スキルやプラグインをリポジトリに取り込む前に SkillSpector でスキャンする。

```bash
skillspector scan <対象> --recursive --no-llm
```

- 判定が CRITICAL でも、ドキュメント内のサンプルコードを拾った誤検知が大半を占める。**検出の所在(`docs/` か実行されるスクリプトか)を確認してから判断する。**
- `--output` は Windows では使えないため `> file.json` でリダイレクトする。
- LLM 解析を使う場合は `SKILLSPECTOR_PROVIDER=claude_cli`(API キー不要)。

## ブランチ運用

- 作業ブランチは `develop` から切り、`develop` 向けの PR を作る。
- `main` には直接コミットしない。
