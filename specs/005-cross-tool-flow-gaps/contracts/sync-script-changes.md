# Contract: 同期スクリプトの変更(004 の契約への差分)

元の契約: `specs/004-cross-tool-claude-env/contracts/sync-script.md`。呼び出しと終了コードは変えない。

## 出力の変更

| 場所 | 変更 |
|---|---|
| `.agents/agents/<name>.md` | コピーから、Antigravity の frontmatter への変換(data-model.md)に変える |
| `.codex/agents/<name>.toml` | 読み取り専用のエージェントに、注意を足す |

## 規則

- `vendor/` は読むだけ。書かない。
- `--check` は、上の生成物のずれも検出する。
- frontmatter の `tools` に、未知の道具の名前があったら、変換を失敗(終了コード 2)にして、名前を報告する。
