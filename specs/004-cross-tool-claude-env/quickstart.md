# Quickstart: 検証の手順

前提: ルートで作業する。`codex` と `agy` はこのマシンに無いため、自動で検査できるのは、ファイルの内容までである。

## 1. 同期と検査

```bash
python scripts/sync-agent-env.py
python scripts/sync-agent-env.py --check   # 期待: 終了コード 0
```

## 2. 件数の一致(SC-001)

```bash
ls .claude/skills | wc -l; ls .agents/skills | wc -l     # 期待: 18 と 18
ls .claude/agents | wc -l; ls .agents/agents | wc -l; ls .codex/agents | wc -l   # 期待: 9 / 9 / 9
find .claude/rules -name "*.md" | wc -l; ls .agents/rules | wc -l                # 期待: 27 / 27
```

## 3. 正本を書き換えたときの反映(SC-002)

1. `.claude/skills/window-question/SKILL.md` の末尾に、一時的な 1 行を足す。
2. `--check` が、終了コード 1 で、そのファイルを報告することを確かめる。
3. 同期を実行し、`.agents/skills/window-question/SKILL.md` にも同じ行が出ることを確かめる。
4. 1 行を消し、同期をもう一度実行する。

## 4. rules の frontmatter

```bash
head -8 .agents/rules/cpp-coding-style.md   # 期待: trigger: glob と globs
head -5 .agents/rules/window.md             # 期待: trigger: always_on
```

## 5. プラグイン(SC-004)

```bash
claude plugin validate .
claude plugin list    # 期待: 4 つが有効
```

## 6. Claude 側が変わっていないこと(SC-005、SC-006)

```bash
git diff --stat -- .claude vendor   # 期待: .claude/ は、生成物の追加以外の差分なし。vendor は 0 件
bash .claude/hooks/window-reminder.sh < /dev/null | head -c 120   # 期待: 変更前と同じ出力
```

## 7. 実機(ユーザー検収)

1. Codex を、このリポジトリで起動し、`/hooks` でフックを信頼する。スキル(例: `window-question`)が使えることを確かめる。
2. Antigravity CLI(`agy`)を起動し、同じスキルと、`.agents/rules/` の rules が読み込まれることを確かめる。
