# 納品書: Antigravity 向けエージェントのモデル指定

- 状態: 承認済み
- 依頼: 「Antigravity は Opus 枠が Argon、Sonnet 枠が Hydrogen」と「公式の段階(pro / flash)」(ユーザーの回答)。こう理解した: Antigravity 向けに生成するエージェントの `model` を、Claude の `opus`→`pro`、`sonnet`→`flash` に変える。やらないこと: Codex 側のモデルの変更(ユーザーは Antigravity だけ指定した)、`.claude/` の変更、Argon・Hydrogen のモデル名の直接指定(`model` に書ける値が、公式で確認できなかったため、ユーザーが公式の段階を選んだ)。
- 納品日: 2026-11-16

> 状態は、置いた時点で「確認待ち」。承認はユーザーが行い、「承認済み」に変える。確認待ちの間は、完了とは言わない。

## 完了の判定ごとの報告

### Antigravity 向けエージェントの `model` が、`opus`→`pro`、`sonnet`→`flash` になる

- 何をしたか: `scripts/sync-agent-env.py` に `AG_MODELS`(`opus`→`pro`、`sonnet`→`flash`、`haiku`→`flash`)を足し、`model` を変換するようにした。未知のモデル名は、終了コード 2 で失敗する。`AGENTS.md` の読み替え表と、`docs/共有環境/共有の一覧.md` の該当行を直した。
- 確認した方法: `python scripts/sync-agent-env.py` → `65 generated files, 9 written, 0 orphans removed`。続けて `--check` → `65 generated files, 0 drifted`、終了コード 0。`grep -H "^model:" .agents/agents/*.md` → `game-advisor.md: model: pro`、残り 8 件は `model: flash`。
- 確認していないこと: `pro` と `flash` が、実際に Argon と Hydrogen に当たるかは、公式に対応表がなく、未確認。Antigravity IDE が、`model: pro` / `flash` を受け付けること(ユーザー検収)。Argon は「Antigravity IDE では使えない」という要約があった(二次的な確認のみ)。`haiku`→`flash` は、ユーザーの指定ではなく、私の補い(現在 `haiku` を使うエージェントはない)。

## 追加した項目

- `haiku`→`flash` の対応(現在は使われない。未知のモデル名で失敗しないための補い)。

## 確かめる者の報告

検査不要: 差分に、窓口の規則が挙げるソースファイル(`.cpp` `.hpp` `.cc` `.hh` `.cxx` `.h` `.cs` `.rs`)とテストファイルがない(変更は Python のスクリプトと、ドキュメント、生成物のみ)。
