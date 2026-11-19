# 設計: md を OKF(Open Knowledge Format)で統一する

日付: 2026-11-19 / 状態: ユーザーの確認待ち(読み手の確認を反映済み)

## 意図(なぜ)

- 文書管理を倍々にしないため。Anthropic は、確認しやすさのために HTML を足したが、HTML と md の2つを保守することになり、日本語訳まで含めると、さらに増える。このリポジトリは、md を正本の1つにして、md を読ませる形を主軸にする。
- OKF は、Markdown と YAML frontmatter の、ベンダー中立な書式(v0.2。凍結された `GoogleCloudPlatform/knowledge-catalog/okf` の `SPEC.md` で確認。現在の仕様は `GoogleCloudPlatform/open-knowledge-format` にあるが、まだ読んでいない)。`type` が必須で、`title`・`description`・`tags`・`status`・`sources`・`generated`・`verified`・`stale_after` が推奨。`index.md`(frontmatter なし、ルートだけ `okf_version` を持てる)と `log.md` は予約名。

## ユーザーが決めたこと(原文の要旨)

- md は、基本 OKF で統一したい。ツールが形式を決めているファイル(SKILL.md、エージェント、rules、AGENTS.md、CLAUDE.md、README.md)も含める(案 A)。
- 正本と訳の関係は、いまのまま(rules は英語が正本で、日本語訳を `docs/` に置く。Claude には読み込まれない)。
- 訳は、rules 以外にも広げる。置き場は、リポジトリの階層に沿ったファイル階層。訳す対象は、英語で書かれたものだけ(rules、ECC 由来のスキル・エージェント・コマンド、spec-kit のテンプレート)。
- 実装フローの HTML は、なるべくノンバーバル化したい。

## 範囲を分ける(独立した3つの作業)

| 順 | 作業 | 理由 |
|---|---|---|
| 1 | OKF の書式への統一(この設計の本体) | 2 の訳が、OKF の frontmatter を使う |
| 2 | 訳の拡張(`docs/ja/`。`docs/rules-ja/` を移す) | 1 の書式に依存する |
| 3 | `docs/実装フロー/*.html` のノンバーバル化 | OKF と独立 |

この設計は、1 だけを扱う。2 と 3 は、1 の後に、別の依頼票で始める。

## ゴールと、やらないこと

ゴール:
- 追跡している md(`vendor/` を除く)の、OKF の対象にしたものすべてが、パースできる frontmatter と空でない `type` を持つ。
- ディレクトリごとの `index.md` は、スクリプトで生成し、`--check` でずれを検出できる。手で書かない。
- ツールが frontmatter を読むファイルは、足したキーのせいで壊れない(確認した範囲で)。

やらないこと:
- HTML を足さない。
- `vendor/` と、外部から入れた md には触らない。
- `.specify/` の spec-kit 由来のファイルは、spec-kit の更新で上書きされるため、まず対象外にして、扱いを計画で決める。
- 訳(2)と HTML(3)は、この作業で行わない。

アンチゴール(技術的に動いても失敗):
- いずれかのツール(Claude Code、Codex、Antigravity)で、スキル・エージェント・rules が、読み込まれなくなる、または、`paths` などの既存のキーが効かなくなる。

## 制約

- 公式で確認できなかった点は、「未確認」と書き、推測で埋めない(`answer-policy.md`)。
- 正本は、ツールごとに独立している(006)。`.claude/`、`.codex/`、`.agents/` を、それぞれ直す。同期の仕組みは作らない。
- `main` に出す構成(`scripts/build-main.py`)の許可リストに、`index.md` などが、どう影響するかを確認する。

## 案(Approaches)

| 案 | 内容 | 判定 |
|---|---|---|
| A | 全 md に OKF の frontmatter を足す。ただし、先に、3つのツールで未知のキーが無視されるかを確かめる。壊れるカテゴリは、B に落とす。 | **ユーザーが選んだ** |
| B | 文書(`docs/`、`specs/`、訳)だけ OKF。ツール用のファイルは触らない。 | A の、壊れたときの退避先 |
| C | ツール用のファイルは、`index.md` に書く(frontmatter は足さない)。 | OKF の適合を満たさないため、選ばなかった |

選んだ理由: 「全 md を統一」という希望に、いちばん近い。確認を先にすることで、壊れるリスクを抑える。

## 設計(決めた形)

- **付ける項目**: `type`(必須)、`title`、`description`、`status`(`draft`・`stable`・`deprecated`)、`tags`。`sources` と `generated`・`verified`・`stale_after` は、訳(2)で使う。1 では、足さない(私の判断)。
- **`type` の値**: 種類ごとに決める(例: `Skill`、`Agent`、`Rule`、`Spec`、`DeliveryNote`、`Reference`)。値は OKF が登録を求めないため、このリポジトリで決める(私の判断)。
- **ツール用のファイル**: 既存の frontmatter に、キーを足す(例: `paths` を持つ rules に `type` を足す)。足す前に、各ツールで、未知のキーが無視されることを確かめる。確かめられなかったものは、足さない。
- **`index.md`**: 各ディレクトリに、`scripts/` のスクリプトで生成する。frontmatter は付けない(仕様)。ルートの `okf_version` は、ルートの `index.md` に置く。
- **`log.md`**: 作るかは、計画で決める(最初は作らない見込み。私の判断)。
- **既存の `README.md` / `index.md`**: ある場合の関係は、計画で決める。

## ビルダーに任せること

スクリプトの名前と置き場、`type` の値の一覧、`index.md` の見出し、どの md を除外するかの一覧、ツール確認の手順、移行の順序。

## 私の判断(読み手の質問への答え。確認してください)

1. **範囲**: `vendor/` を除く、追跡している md すべて。`specs/`、`docs/納品書/`、`docs/rules-ja/`、`_template.md`、ECC 由来の `.claude/` のファイル、`.agents/`・`.codex/` を含める。ECC の再導入で上書きされる可能性は、未確認(`AGENTS.md` に、ECC の更新・削除機能が未検証と書いてある)。`.specify/` は、計画で決める。
2. **ツールの確認**: ファイルの種類(SKILL.md、エージェント、rules、`AGENTS.md`・`CLAUDE.md`、README)× ツール(Claude Code、Codex、Antigravity)で確かめる。合格は「エラーも警告もなく、既存の挙動(`paths` の読み込みなど)が変わらない」こと。実機が要る確認(Codex・Antigravity)は、ユーザーの手が要るため、計画に「ユーザー検収」の手順として置く。確かめられなかった組み合わせの種類には、キーを足さない。
3. **`AGENTS.md` と `CLAUDE.md`**: 先頭の `---` の扱いが未確認で、`CLAUDE.md` は `@AGENTS.md` の読み込みだけのため、確認が取れるまで、frontmatter を足さない(B に落とした扱い)。
4. **`index.md` の置き場**: 文書のディレクトリ(`docs/`、`specs/`)だけに生成する。`.claude/skills/`・`.claude/agents/`・`.claude/rules/`、`.agents/`、`.codex/` には置かない(スキルやエージェントとして拾われる恐れと、frontmatter のない `index.md` が rules として毎回読み込まれてトークンを消費する恐れがあるため。後者は、rules の `paths` なしのファイルが常に読み込まれる挙動からの推論で、実機では未確認)。OKF は、`index.md` がなくても、消費側が拒否してはならないと定めている。
5. **`main` との関係**: `index.md` は `docs/`・`specs/` にだけあり、`main` には出ない(`build-main.py` の許可リストにない)。frontmatter は、ツール用のファイルの一部として `main` に出る。
6. **既存の `README.md` / `index.md`**: 生成する `index.md` は追加であり、`README.md` は置き換えない。
7. **`status`**: OKF の `status`(`draft`・`stable`・`deprecated`)として足す。納品書の「状態」は、別の項目として残す。
