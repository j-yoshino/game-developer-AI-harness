# GameDeveloperAIHarness

ゲーム開発用の AI エージェントハーネス。

## 導入済みツール

| ツール | 置き場所 | 役割 |
|---|---|---|
| spec-kit | `.claude/skills/speckit-*`、`.specify/` | Spec-Driven Development の明示的フロー |
| superpowers | `vendor/superpowers`(submodule) | 開発方法論スキル群(自動発動) |
| SkillSpector | `uv tool`(リポジトリ外) | スキルのセキュリティスキャン |
| Unity CLI | MCP サーバー | Unity Editor 連携 |

## このリポジトリ独自のルールとスキル

| ファイル | 内容 |
|---|---|
| `.claude/rules/answer-policy.md` | 回答ポリシー(事実のみ / 未検証の明記 / 曖昧なら AskUserQuestion)。毎セッション読み込まれる |
| `.claude/skills/check-claude-docs/` | `/check-claude-docs` — Claude 自身の仕様を `claude-code-guide` エージェントに確認させる |
| `.claude/rules/<言語・エンジン>/` | 言語・エンジンごとのルール。`paths` で該当ファイルを開いたときだけ読み込まれる(毎セッション読み込まれるのは `answer-policy.md` だけ)。下表 |

### 言語・エンジン別のルール(`.claude/rules/`)

| ディレクトリ | ECC 由来 | コーディング規約の要約(追加分) | 対象(`paths`) |
|---|---|---|---|
| `cpp/` | `coding-style`・`hooks`・`patterns`・`security`・`testing` | `core-guidelines.md`(C++ Core Guidelines) | C/C++ のソース・ヘッダ |
| `csharp/` | 同上 | `dotnet-conventions.md`(.NET コーディング規則) | `**/*.cs` |
| `rust/` | 同上 | `api-guidelines-naming.md`(Rust API Guidelines の Naming) | `**/*.rs`、`**/Cargo.toml` |
| `unity/` | なし | `coding-style.md`(Unity の C# 命名規則とスタイル規則) | `Assets/**/*.cs` |
| `unreal-engine/` | なし | `coding-style.md`(Epic の C++ コーディング規約) | `Source/**`、`Plugins/**/Source/**` の `.h` `.cpp` `.cs` |

- `paths` に除外指定ができないため、重なるファイルでは両方が読み込まれる。**Unity は `unity/`、Unreal は `unreal-engine/` を優先**する(各ファイルの冒頭に明記)。
- コーディング規約の要約は、同じディレクトリの ECC 由来のルールより優先する。
- ECC 由来のルールは、`ecc/` の階層を外して `.claude/rules/<言語>/` に置いている。ECC の installer の記録(`.claude/ecc/install-state.json`、ローカル専用)は移動前のパスを指しており、ECC の更新・削除機能がこの配置で動くかは未検証。
- 各ファイルの末尾に、要約の範囲と未確認事項を書いてある。出典を読めていない部分を「規約どおり」と扱わない。

**Claude Code / Agent SDK / Claude API の仕様は記憶で答えない。** 設定キーやフラグは実在しないものを書いても黙って無視されるため、`/check-claude-docs` で裏を取る。

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
