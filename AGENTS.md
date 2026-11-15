# GameDeveloperAIHarness

ゲーム開発用の AI エージェントハーネス。

## 導入済みツール

| ツール | 置き場所 | 役割 |
|---|---|---|
| spec-kit | `.claude/skills/speckit-*`、`.specify/` | Spec-Driven Development の明示的フロー |
| superpowers | `vendor/superpowers`(submodule) | 開発方法論スキル群(自動発動) |
| Unity 公式プラグイン | `vendor/unity-agent-plugin`(submodule、`settings.local.json` で有効化) | Unity のスキル集(Unity-Technologies 製) |
| Unreal Engine プラグイン | `vendor/unreal-engine-skills-for-claude-code-plugin`(submodule、リポジトリ直下の `.claude-plugin/marketplace.json` 経由で有効化。Unreal 側に marketplace.json がないための代用) | MCP 経由の Unreal Editor 操作(Epic Games 製) |
| SkillSpector | `uv tool`(リポジトリ外) | スキルのセキュリティスキャン |
| Unity CLI | MCP サーバー | Unity Editor 連携 |

## このリポジトリ独自のルールとスキル

| ファイル | 内容 |
|---|---|
| `.claude/rules/answer-policy.md` | 回答ポリシー(事実のみ・確認の経緯は書かない / 事実でないことの明示 / 検証は自分で完結しユーザーの手が要るものだけ「やり残し」/ 曖昧さが残る間は進まず AskUserQuestion)。毎セッション読み込まれる |
| `.claude/rules/window.md` | 依頼の窓口。質問(作業を求めない発言)は `window-question` が答え、層は判定しない。作業の依頼は、軽作業・本件に判定し、経路に回す(迷ったら重い層を選び、層は下げない)。毎セッション読み込まれる。`.claude/hooks/window-reminder.sh`(UserPromptSubmit フック。`settings.local.json` で登録)が、毎ターン短い注意を注入する。遵守は保証されない |
| `.claude/skills/window-question/` | 質問(作業なし)への回答の手順。層を判定せず、依頼票・納品書・層の宣言を出さず、根拠付きで答える |
| `.claude/agents/window-verifier.md` | 確かめる者。作った者とは別の文脈で、納品書の主張を完了の判定に照合し、確認していないことの抜けを指摘し、確認方法を最大3つ再実行し、言語・エンジン別のレビューを入れ子で呼ぶ。本件は必ず、軽作業はコードかテストを変えたときだけ呼ぶ。報告は納品書の末尾に全文で追記する。第1版は、検査役の書き換えとメインによる報告の改変を検知しない |
| `.claude/agents/game-advisor.md` | 相談役。別の文脈で、抽象的な依頼やゲームの体験に関わる変更に、解釈案(推奨つき)と番号付きの補った点を返す。決めて進まず、ユーザーの合意を取ってから進む。補った点は依頼票(軽作業は納品書の依頼欄)に記録し、検収で1点ずつ覆せる。`tools` は Read・Grep・Glob だけ。窓口(`window.md` の Advisor 節)が呼ぶ。遵守は保証されない |
| `docs/ゲーム制作/` | 相談役の知識。8つの見方(`観点/`)、任天堂の記事の出典(`出典.md`)。任天堂の記事は出典付きの要約。桜井さんの動画の二次資料は「二次資料の複合結果」として扱い、個別のソースは書かない |
| `.claude/agents/unity-reviewer.md`、`unreal-reviewer.md` | Unity と Unreal のレビュー。`window-verifier` が名前で呼ぶ。`paths` 付きの rules はサブエージェントに自動では届かないため、指示の中で `.claude/rules/unity/`、`.claude/rules/unreal-engine/` を読む |
| `docs/納品書/` | 納品書(作業後の報告)の置き場。`_template.md` が書式。軽作業と本件の完了後に書き、ユーザーが確認する。状態は「確認待ち」から始まる |
| `.specify/templates/overrides/spec-template.md` | 依頼票(ご要望の原文・こう理解した・誰のためか・やらないこと・完了の判定)の節を足した spec テンプレート。spec-kit の更新で上書きされない |
| `scripts/sync-agent-env.py`、`docs/共有環境/共有の一覧.md` | `.claude/` を正本に、Codex・Antigravity CLI 向けの `.agents/`・`.codex/` を生成する(スキル・エージェント・rules・フック)。`--check` でずれを検査。共有の可否と、できない項目の理由は、一覧にある。実機(Codex・Antigravity)での動作は、ユーザーの検収待ち |
| `.claude/skills/check-claude-docs/` | `/check-claude-docs` — Claude 自身の仕様を `claude-code-guide` エージェントに確認させる |
| `.claude/rules/<言語・エンジン>/` | 言語・エンジンごとのルール。`paths` で該当ファイルを開いたときだけ読み込まれる(毎セッション読み込まれるのは `answer-policy.md` と `window.md` だけ)。下表 |
| `docs/rules-ja/` | `.claude/rules/` の日本語訳(同じ構成・同じファイル名)。**Claude には読み込まれない**。トークン量を抑えるため、rules は英語で書き、日本語は docs に置く |

### 言語・エンジン別のルール(`.claude/rules/`)

各ディレクトリに、`coding-style.md`・`hooks.md`・`patterns.md`・`security.md`・`testing.md` の5ファイルがある。**コーディング規約は、新しいファイルを作らず、各ディレクトリの `coding-style.md` に含めている。**

| ディレクトリ | 由来 | `coding-style.md` に含めた規約 | 対象(`paths`) |
|---|---|---|---|
| `cpp/` | ECC(5ファイル) | C++ Core Guidelines(全文を読了) | C/C++ のソース・ヘッダ |
| `csharp/` | ECC(5ファイル) | .NET コーディング規則(Microsoft Learn) | `**/*.cs` |
| `rust/` | ECC(5ファイル) | Rust API Guidelines の Naming | `**/*.rs`、`**/Cargo.toml` |
| `unity/` | 公式ドキュメントから作成 | Unity の C# 命名規則とスタイル規則 | `Assets/**/*.cs`(`patterns.md` と `testing.md` は `.asmdef` も) |
| `unreal-engine/` | 公式ドキュメントから作成 | Epic の C++ コーディング規約 | `Source/**`、`Plugins/**/Source/**` の `.h` `.cpp` `.cs` |

- ECC 由来のファイルは、`ecc/` の階層を外して `.claude/rules/<言語>/` に置いている。規約は、各 `coding-style.md` の末尾の「Project Conventions」の節に、ECC の記述を残したまま追記している。ECC の installer の記録(`.claude/ecc/install-state.json`、ローカル専用)は移動前のパスを指しており、ECC の更新・削除機能がこの配置で動くかは未検証。
- `paths` に除外指定ができないため、重なるファイルでは両方が読み込まれる。**Unity は `unity/`、Unreal は `unreal-engine/` を優先**する(各ファイルの冒頭に明記)。規約の節は、同じファイル内の汎用的な ECC の記述より優先する。
- `unity/` と `unreal-engine/` は公式ドキュメントで確認できた範囲だけを書いている。確認できなかったこと(Unity のセキュリティなど)は、各ファイルに「書かれていないこと」として明記してある。コマンド例は組み立てたもので、まだ実行していない。
- rules は英語で書く。`docs/rules-ja/` を更新するときは、rules の変更と同じ変更に含める。
- **コードを書くときの共通規則**(各 `coding-style.md` の「Project Rules: Comments and File Header」の節。`cpp/`・`csharp/`・`rust/` にある。`unity/` と `unreal-engine/` は、そこを参照する):
  - 新しいソースファイルは、先頭に Doxygen 形式のヘッダー(`@file`・`@brief`・`@date`・`@author`)を書く。C++ は `/** */`、C# は `//!` の行、Rust は `//!`(要約・Date・Author)。`@date` は作成日(`YYYY-MM-DD`)を1回だけ書き、`@author` は `git config user.name`。Unreal の著作権表示は1行目のまま。
  - すべてのコメント行の末尾にピリオドを付ける(値の行、URL、コード例などの例外は各ファイルに記載)。コメントは独立した行に書き、`//` の後に空白を1つ。

### 他のツール(Codex・Antigravity CLI)との共有

- **正本は `.claude/`**。スキル・エージェント・rules・フックは、`.claude/` だけを手で直す。
- `.agents/` と `.codex/` の中身は、`python scripts/sync-agent-env.py` で生成する。**生成物は手で直さない**(次の同期で上書きされる)。`--check` を付けると、正本とのずれを検査する(ファイルは書かない)。
- 共有できる範囲と、できない項目の理由は、`docs/共有環境/共有の一覧.md` にある。
- Windows の Git は、このリポジトリでシンボリックリンクを使えない(`core.symlinks=false`)ため、リンクではなく生成(コピー)にしている。

### rules の案内(Codex 向け)

Codex は `.claude/rules/` を自動では読み込まない。次のとおり、該当する rules を、作業の前に読む(Claude Code と Antigravity は、別の仕組みで読み込むため、重ねて読んでも害はない)。

- 毎回: `.claude/rules/window.md` と `.claude/rules/answer-policy.md`。
- C/C++ のソース・ヘッダ、`CMakeLists.txt` を触るとき: `.claude/rules/cpp/` の 5 ファイル。
- C#(`*.cs`、`*.csx`)を触るとき: `.claude/rules/csharp/` の 5 ファイル。
- Rust(`*.rs`、`Cargo.toml`)を触るとき: `.claude/rules/rust/` の 5 ファイル。
- Unity(`Assets/` 配下の `*.cs`、`*.asmdef`)を触るとき: `.claude/rules/unity/` の 5 ファイル。重なる `csharp/` よりも `unity/` を優先する。
- Unreal(`Source/` と `Plugins/**/Source/` の `.h` `.cpp` `.cs`)を触るとき: `.claude/rules/unreal-engine/` の 5 ファイル。重なる `cpp/` よりも `unreal-engine/` を優先する。

**Claude Code / Agent SDK / Claude API の仕様は記憶で答えない。** 設定キーやフラグは実在しないものを書いても黙って無視されるため、`/check-claude-docs` で裏を取る。

## 計画フェーズの使い分け

**依頼は、まず窓口(`.claude/rules/window.md`)を通る。** 質問は `window-question`、軽作業は brainstorming で規模を測って作業、本件(新規実装)は下の流れに進む。作業の完了後は、納品書を `docs/納品書/` に書き、本件と、コードやテストを変えた軽作業では、報告の前に `window-verifier`(確かめる者)に検査させる。

**計画と実装は spec-kit を正本とする。** superpowers と spec-kit は計画スキルの発動条件が重なるため、役割を以下に固定する。

```
brainstorming(何を作るか決める・design doc 作成)
  ↓ design doc のパスを引数で渡す
/speckit-specify → /speckit-plan → /speckit-tasks → /speckit-implement
```

- **計画を書くときは `/speckit-plan` を使う。** superpowers の `writing-plans` は使わない。
- **実装は `/speckit-implement` を使う。** superpowers の `executing-plans` と `subagent-driven-development` は使わない。
- 上記3スキルは **使わない**。superpowers はプラグインのスキルで、`skillOverrides` はプラグインのスキルに効かない(公式: 「Plugin skills are not affected by `skillOverrides`」、https://code.claude.com/docs/en/skills.md)ため、スキル一覧には残る。プラグインごと無効化すると brainstorming なども消えるので、無効化はしない。executing-plans と subagent-driven-development は、曖昧さや計画の欠陥を「判断して進め、台帳に記録する」(各スキルの「Rulings, not stalls」の段落)ため、「曖昧さが残る間は進まない」という `answer-policy.md` と食い違う。計画と実装は spec-kit で行う。
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
