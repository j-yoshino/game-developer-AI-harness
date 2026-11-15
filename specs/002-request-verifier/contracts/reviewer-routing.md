# Contract: 言語・エンジン別のレビューの振り分け

確かめる者が、変更ファイルの一覧から、どのレビュー用エージェントを呼ぶかの規則。レビューは、`Agent` ツールで、`subagent_type` に名前を指定して、入れ子で呼ぶ(research.md R1)。

## 振り分けの表

| 変更ファイル | 呼ぶエージェント |
|---|---|
| `Assets/**` の `.cs` | `unity-reviewer`(新規) |
| `Source/**`、`Plugins/**/Source/**` の `.h` `.hpp` `.cpp` `.cc` `.cxx` `.cs` | `unreal-reviewer`(新規) |
| 上の2つに当たらない `.cpp` `.hpp` `.cc` `.hh` `.cxx` `.h` | `cpp-reviewer`(既存) |
| 上の2つに当たらない `.cs` | `csharp-reviewer`(既存) |
| `.rs` | `rust-reviewer`(既存) |
| 上のどれにも当たらない拡張子(`.py` `.js` `.shader` `.uasset` など) | 呼ばない。報告に「対象外」と書く |

## 規則

| 規則 | 内容 |
|---|---|
| 重なり | 特化側(Unity・Unreal)だけを呼ぶ。汎用側を重ねて呼ばない |
| 混在 | `Assets/` と `Source/` が混在する変更は、両方を呼ぶ。複数の言語が混在するときも、それぞれを呼ぶ |
| 並行 | 呼ぶレビューが複数あるときは、並行して呼んでよい(同時実行の既定の上限は20) |
| 渡すもの | 変更ファイルの一覧と、「納品書の完了の判定」。レビューは、自分で `git diff` を取る(既存のレビュー用エージェントの動き) |
| 返ってきた指摘 | CRITICAL と HIGH は、そのまま報告に含める。MEDIUM 以下とスタイルは、含めない |

## 新規のレビュー用エージェントの要件

`unity-reviewer` と `unreal-reviewer`:

| 項目 | 内容 |
|---|---|
| 置き場所 | `.claude/agents/` |
| 言語 | 英語(既存のレビュー用エージェントと同じ) |
| `tools` | `Read, Grep, Glob, Bash`(既存と同じ。`Edit` と `Write` は持たせない) |
| `model` | `sonnet` |
| rules の読み込み | `paths` 付きの rules は、サブエージェントに自動では届かない(research.md R2)。それぞれの rules(`unity-reviewer` は `.claude/rules/unity/`、`unreal-reviewer` は `.claude/rules/unreal-engine/` の5つのファイル)を、指示の中で、`Read` するよう書く |
| 重大度 | CRITICAL / HIGH / MEDIUM の3段階(既存のレビュー用エージェントと同じ形) |
| 変更の取り方 | `git diff` で、自分で取る |
