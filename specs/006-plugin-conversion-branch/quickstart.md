# Quickstart: 検証の手順

ルートで作業する。出力先は、スクラッチパッドなど、リポジトリの外にする。

## 1. 同期の廃止(SC-001)

```bash
ls scripts/sync-agent-env.py 2>&1               # 期待: 存在しない
git status --short .agents .codex               # 期待: 手の変更以外の差分なし
grep -rl "generated from" .agents .codex | grep -v "plugins/superpowers" | wc -l   # 期待: 0
```

## 2. 組み立てと決定性(SC-002)

```bash
python scripts/build-main.py --out "$OUT/a"
python scripts/build-main.py --out "$OUT/b"
diff -r "$OUT/a" "$OUT/b" && echo "同じ出力"        # 期待: 同じ出力
python scripts/build-main.py --out "$OUT/a" --check; echo $?   # 期待: 0
```

## 3. 含めるもの・含めないもの(SC-003)

```bash
(cd "$OUT/a" && find . -path ./.git -prune -o -type f -print | sort) | head -100
ls "$OUT/a"                                       # 期待: .claude .codex .agents .claude-plugin vendor AGENTS.md CLAUDE.md README.md …
ls "$OUT/a/specs" "$OUT/a/docs" "$OUT/a/scripts" "$OUT/a/.specify" 2>&1   # 期待: どれも存在しない
ls "$OUT/a/vendor"                                # 期待: unreal-engine-skills-for-claude-code-plugin のみ
test -f "$OUT/a/.claude/settings.local.json" && echo NG || echo OK   # 期待: OK
grep -rn "C:/Users\|C:\\Users\|Disas" "$OUT/a" | head   # 期待: 出力なし(個人のパスがない)
wc -l "$OUT/a/AGENTS.md"                           # 期待: develop の 134 行より、大幅に短い
```

## 4. 外部プラグインの導入の設定(SC-004)

```bash
python -m json.tool "$OUT/a/.claude/settings.json" > /dev/null && echo "settings OK"
python -m json.tool "$OUT/a/.agents/plugins/marketplace.json" > /dev/null && echo "codex mk OK"
grep -c "vendor/superpowers\|vendor/unity\|vendor/i-have-adhd" "$OUT/a/.agents/plugins/marketplace.json" "$OUT/a/.claude/settings.json"   # 期待: 0
claude plugin validate "$OUT/a"                    # マーケットプレイスの検証。エラーなし
```

導入の試験(隔離したスコープ。005 と同じ手順): `claude plugin marketplace add <出力先>` → `claude plugin install unreal-engine-skills-for-claude-code@game-developer-ai-harness --scope local` など → 後始末。外部の 3 つは、GitHub から取得するため、試験の導入は、ネットワークが要る。実行の前に、ユーザーに確認する。

## 5. 変わっていないこと(SC-005)

```bash
git diff --stat -- vendor .claude                  # 期待: 0 件(同期の廃止での .claude の変更はない)
bash .claude/hooks/window-reminder.sh < /dev/null | cmp - <変更前の記録>   # 期待: 一致
claude plugin list                                 # 期待: 変更前と同じ
```

## 6. 実機(ユーザー検収)

1. `main` 相当の出力を、別のフォルダで開き、Claude Code・Codex・Antigravity で、スキルと rules(窓口)が効くこと。
2. README の手順どおりに、外部プラグイン(superpowers、Unity、i-have-adhd)を、導入できること。
