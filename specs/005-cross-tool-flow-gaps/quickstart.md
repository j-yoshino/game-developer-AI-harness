# Quickstart: 検証の手順

ルートで作業する。実機は、ユーザーが操作する(Codex アプリ、Antigravity IDE)。

## 1. 同期と検査

```bash
python scripts/sync-agent-env.py
python scripts/sync-agent-env.py --check   # 期待: 終了コード 0
```

## 2. Antigravity のエージェントの変換(SC-003)

```bash
head -12 .agents/agents/game-advisor.md     # 期待: tools が view_file, grep_search のみ。model: inherit。Write/Bash 系がない
grep -L "tools:" .agents/agents/*.md        # tools を持たないエージェントがないこと
```

## 3. Codex のエージェントの注意(SC-003)

```bash
grep -c "read-only\|読み取り専用" .codex/agents/game-advisor.toml   # 期待: 1 以上
grep -c "read-only" .codex/agents/window-verifier.toml               # 期待: 0(Bash を持つため)
```

## 4. superpowers の導入(SC-005)

```bash
python scripts/setup-antigravity-plugins.py --dry-run   # 置く先と、置くファイルの一覧を表示するだけ。何も書かない
git diff --stat -- vendor                               # 期待: 0 件
```

置く操作(`--dry-run` なし)は、`.agents/plugins/superpowers/` を作る(プロジェクトの中。`git status` に出ないこと)。

## 5. 読み替え表(SC-001・SC-002)

```bash
grep -rnE "AskUserQuestion|subagent_type|\`Agent\`" .claude/rules .claude/agents .claude/skills   # 出現箇所
sed -n '/道具名の読み替え表/,/^## /p' AGENTS.md          # 全行に、Codex・Antigravity・出典の欄があること
```

## 6. 変わっていないこと(SC-004)

```bash
git diff --stat -- .claude vendor    # 期待: 0 件
```

## 7. 実機(ユーザー検収)

1. Antigravity IDE で、`game-advisor` を呼び、**書き込まないこと**(依頼に応じてファイルを作らせても、断ること)を確かめる。固まらないことも、確かめる。
2. Codex アプリで、`AGENTS.md` の読み替え表のとおりに、`window-verifier` を名前で頼めること。
3. 手順書(`docs/共有環境/環境構築.md`)のとおりに、Codex アプリと Antigravity IDE へ superpowers を導入し、両ツールで `brainstorming` が使えること。
