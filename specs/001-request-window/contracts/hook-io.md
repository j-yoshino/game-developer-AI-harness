# Contract: 窓口のフック(UserPromptSubmit)

## 入力(標準入力の JSON)

2.1.233 で実際に渡されたもの(research.md R1)。

```json
{
  "session_id": "...",
  "transcript_path": "...",
  "cwd": "...",
  "prompt_id": "...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "<ユーザーの入力文>"
}
```

スクリプトは、標準入力を読み捨ててよい(第1版は、`prompt` の内容で分岐しない。R2)。

## 出力

標準出力に、次の JSON だけを出す。他の文字を混ぜない。終了コードは 0。

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "<注入文>"
  }
}
```

## 注入文の要件

| 要件 | 値 |
|---|---|
| 言語 | 英語 |
| 長さ | 400 文字以内(`additionalContext` の上限は 10,000 文字だが、毎ターン届くため短くする) |
| 内容 | (1) ユーザーの発言ごとに、質問・軽作業・本件を判定する。(2) 迷ったら層を上げる。(3) 手順は `window.md` を見る。(4) システムの通知は対象外 |
| 禁止 | 出力に、層の宣言や依頼票を、質問のたびに出させる指示を含めない(SC-006) |

## 登録

`.claude/settings.local.json` の `hooks` に、UserPromptSubmit のハンドラーとして登録する。`type` は `command`、`timeout` は 10 秒。command のパスの書き方は、research.md R3(未検証)に従う。

## 失敗時の挙動

スクリプトが失敗しても、ユーザーの入力はブロックしない(終了コード 2 を返さない)。注意が届かないだけで、通常の会話は続く。
