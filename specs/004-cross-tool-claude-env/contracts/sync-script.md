# Contract: 同期スクリプト

正本(`.claude/`)から、参照側(`.agents/`、`.codex/`)を生成する、1 つのコマンドの契約。

## 呼び出し

```bash
python scripts/sync-agent-env.py            # 生成する(上書き)
python scripts/sync-agent-env.py --check    # 検査のみ。ファイルを書かない
```

- Python 3 を使う(このマシンで利用できることを、tasks で確認する)。
- 作業ディレクトリは、リポジトリのルート。それ以外から呼ばれたら、ルートを自分で見つける(スクリプトの位置から)。

## 入力

`.claude/skills/`、`.claude/agents/`、`.claude/rules/`、`.claude/hooks/`(フックは、呼ぶだけで、コピーしない)。

## 出力(生成するファイル)

| 場所 | 内容 |
|---|---|
| `.agents/skills/<name>/` | スキルのコピー |
| `.agents/agents/<name>.md` | エージェントのコピー |
| `.agents/rules/<name>.md` | rules(frontmatter 変換) |
| `.codex/agents/<name>.toml` | エージェント(TOML) |
| `.codex/hooks.json`、`.agents/hooks.json` | フックの設定 |
| `.agents/hooks/<変換スクリプト>` | Antigravity 向けの出力の変換 |

## 終了コード

| コード | 意味 |
|---|---|
| 0 | 生成が成功 / `--check` で一致 |
| 1 | `--check` で、ずれがある(ずれたファイルを一覧で出す) |
| 2 | 入力が不正(frontmatter が読めない、24,000 バイト超など) |

## 規則

- 生成するのは、上の表のファイルだけ。`.agents/workflows/`、`ecc-install-state.json`、`vendor/` には触らない。
- 正本に無くなったスキル・エージェント・rules は、参照側から削除する(生成物の孤児を残さない)。ただし、削除の対象は、同期が管理する場所(`.agents/skills`、`.agents/agents`、`.agents/rules`、`.codex/agents`)のうち、正本に対応するものがないファイルだけ。
- 同じ入力から、同じ出力を作る(順序と改行を固定する。改行は LF)。
