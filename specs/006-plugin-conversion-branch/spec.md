# Feature Specification: main 用の構成を組み立てる変換ブランチ

**Feature Branch**: `feat/plugin-conversion`

**Created**: 2026-11-17

**Status**: Draft(2026-11-17 に、構成の方針が変わった。旧版の spec・計画・タスクは、破棄した。下の「経緯」を参照)

**Input**: User description: 「develop と main の間に、変換用のブランチを置き、Claude と同じ構成で、`main` に出せるようにする。自作したものは `.claude/`・`.codex/`・`.agents/` 配下に置き、外部から入れたプラグインは、プラグインとして別に入れる」

## 経緯

- 当初は、「自作のスキル・エージェント・フックを、Claude・Codex・Antigravity の 3 つのプラグインに、変換する」計画だった。
- 2026-11-17 に、ユーザーが、「Claude と同じ構成に近しい形でやりたい。自作したものは、`.codex`・`.agents` 配下に置く。外部から入れてきたプラグインは、プラグイン(plugins)でいい」と方針を示し、私の整理(案 A)に「yes」と答えた。
- そのため、**自作のものを、プラグインに変換することは、やらない**。旧版の、3 つのプラグインへの組み立て(`plugins/claude`・`plugins/codex`・`plugins/antigravity`)は、取りやめた。
- 調査の結果(旧 research.md)は、残す(外部プラグインの導入の仕組みなどで、使う)。

## 依頼票

### ご要望(原文)

- 「プラグイン化して、mainにマージすることは可能?」
- 「developとmainの間にプラグインに変換させるブランチ欲しいな」
- 「基本プラグインにまとめるんじゃないの?」
- 「プラグイン化したときの最適解は?」
- 「含める形で」
- 「別導入、何とかして使えるか調べて欲しい」
- 「ちょっと思ってるのと違うかも。コーデックスとアンチグラビティは、プラグインズだけの想定?ドットエージェンツも含んでる?」
- 「2に近いかな。黒堂と同じ構成に近しい形でやりたくて、自作したものはコーデックスやエージェンツ配下に置く想定なんだけど、外部から入れてきたプラグインはプラグインズでいいかな。」(音声入力。「黒堂」は「Claude」、「コーデックス」は「`.codex`」、「エージェンツ」は「`.agents`」、「プラグインズ」は「plugins」と読んだ)
- 私の整理(案 A)への返事: 「yes」

メモ(ユーザーの指示、原文):
- 「ecc、skillspectorは読み込ませるプラグインに含めない」
- 「mainブランチに上げるのは、AGENTS.mdのみで最小(rulesの記載ぐらい?)を上げる形で」
- 「rulesは上げるまま + その案内ぐらい?」「別に用意」(`main` 専用の最小版の `AGENTS.md` を、別に用意する)
- 「developも個別で」「ツールごとに、独立した正本を持つ」(`develop` に、ツールごとに独立した正本を持つ)

### こう理解した(案 A)

| 種類 | 置き場所 |
|---|---|
| 自作(Claude) | `.claude/`(今のまま) |
| 自作(Codex) | `.codex/` と `.agents/`(リポジトリ直下。スキル、エージェント、フック) |
| 自作(Antigravity) | `.agents/`(リポジトリ直下。スキル、エージェント、rules、フック) |
| 外部から入れたもの(superpowers、Unity、i-have-adhd、Unreal) | プラグインとして別に導入する。`vendor/` に同梱せず、導入の設定(マーケットプレイス、有効化)と、手順書だけを置く |

- **`develop` の正本は、ツールごとに独立**する。Claude は `.claude/`、Codex は `.codex/`(と `.agents/` の Codex 向け部分)、Antigravity は `.agents/` の Antigravity 向け部分。互いを、生成の元にしない(004・005 の「`.claude/` から `.agents/`・`.codex/` を生成する同期」は、やめる)。
- **変換ブランチ**(`develop` と `main` の間)の役割は、`develop` から、`main` に出す構成を、スクリプトで組み立てること(手で直さない)。`main` は、最小構成にする。
- **`main` に置くもの**: `.claude/`、`.codex/`、`.agents/`(いずれも自作。ECC と SkillSpector に関わるものの扱いは、下の前提)、`main` 専用の最小の `AGENTS.md`(rules の案内)、外部プラグインの導入の設定、`README.md`。
- **`main` に置かないもの**: `specs/`、`docs/`、`scripts/`、`.specify/`、`vendor/`(Unreal を除く)。

### 誰のためか

次の 2 者。

- このハーネスの作者(ユーザー本人): `develop` で作業し、変換ブランチ経由で `main` に出す。
- `main` を clone して、Claude Code・Codex・Antigravity で開く人(利用者)。

### やらないこと

- 自作のスキル・エージェント・rules・フックを、プラグインに変換すること(旧版の、3 つのプラグインへの組み立ては、取りやめた)。
- `.claude/` の変更(Claude の正本は、そのまま)。Claude 側の動作を変えること。
- `.claude/` から、`.agents/`・`.codex/` を自動で生成し続けること(独立した正本にするため、004・005 の同期は、廃止する。最初の状態は、004・005 の生成物が、そのまま引き継がれる)。
- 外部プラグイン(superpowers、Unity、i-have-adhd)の `vendor/` への同梱。
- `main` への実際のマージ・push(この作業は、仕組みを作るまで。マージは外向きの操作で、実行の前に、ユーザーに確認する)。
- 公式ディレクトリへの申請。
- 変換ブランチの手での編集(生成物は、手で直さない)。
- ツールの間で、同じ内容の文言を、そろえ続ける仕組み(独立した正本のため、ずれてよい。ずれを検知する仕組みも、今回は作らない)。

### 完了の判定

- [ ] `develop` の `.agents/` と `.codex/` が、`.claude/` から生成されない、独立した正本になっている(同期スクリプトが、これらを上書きしない。上書きしないことを、実行して確かめる)。
- [ ] 1 つのコマンドで、`develop` から、`main` に出す構成を、出力先に組み立てられる。同じ入力で 2 回実行すると、同じ出力になる。
- [ ] 組み立てた出力が、「`main` に置くもの」を含み、「`main` に置かないもの」を含まない(ファイル一覧で確かめる)。
- [ ] `main` 専用の最小の `AGENTS.md` が出力に含まれ、rules の案内だけを書いている。`develop` の `AGENTS.md`(約 134 行)との差が、一覧で説明されている。
- [ ] 外部プラグイン(superpowers、Unity、i-have-adhd、Unreal)が、同梱ではなく、導入の設定と手順書で扱われている。Claude は、導入の設定(マーケットプレイスの登録、有効化)を、`main` の `.claude/settings.json` に置き、Codex・Antigravity は、それぞれの仕組みの設定と手順書を置く。公式で確認できなかった点は、「未確認」と書く。
- [ ] ECC と SkillSpector の扱いが、決まった内容(下の前提)どおりに、出力に反映されている。
- [ ] `vendor/` と `.claude/` に差分がない。Claude 側のスキル・エージェント・rules・フックの一覧と、窓口のフックの出力が、変更前と同じである。
- [ ] [ユーザー検収] `main` 相当の出力を、別のフォルダで開き、Claude Code・Codex・Antigravity のそれぞれで、スキルと rules(窓口)が効くことを確かめる。外部プラグインを、手順書どおりに、導入できることを確かめる。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - develop の独立した正本を整える (Priority: P1)

作者が、`develop` で、Claude は `.claude/`、Codex・Antigravity は `.codex/`・`.agents/` を、それぞれ独立して、手で保守する。

**Why this priority**: 「ツールごとに独立した正本」が、すべての前提。

**Independent Test**: 同期スクリプトを実行しても、`.agents/`・`.codex/` が、書き換わらないことを確かめる。

**Acceptance Scenarios**:

1. **Given** `.claude/` のスキルを直した、**When** 何もせず(同期もせず)、**Then** `.agents/`・`.codex/` は、変わらない。
2. **Given** `.agents/` のスキルを直した、**When** `.claude/` を見る、**Then** `.claude/` は、変わらない。

---

### User Story 2 - コマンド 1 つで、main に出す構成を組み立てる (Priority: P2)

作者が、スクリプトを 1 つ実行すると、`main` に出す構成が、出力先に組み立てられる。

**Why this priority**: 変換ブランチの中心。

**Independent Test**: 実行して、ファイル一覧を確かめ、2 回実行して差分がないことを確かめる。

**Acceptance Scenarios**:

1. **Given** `develop` の最新がある、**When** スクリプトを実行する、**Then** `.claude/`、`.codex/`、`.agents/`、最小の `AGENTS.md`、外部プラグインの導入の設定、`README.md` を持つ出力ができ、`specs/`・`docs/`・`scripts/`・`.specify/` は含まれない。
2. **Given** 組み立て済みの状態、**When** もう一度、同じ入力で実行する、**Then** 差分が出ない。

---

### User Story 3 - 外部プラグインを、別に導入できる (Priority: P3)

利用者が、手順書(または、導入の設定)に従って、外部プラグイン(superpowers、Unity、i-have-adhd、Unreal)を、別に導入できる。

**Why this priority**: `vendor/` の同梱を避けるため。ただし、導入先のマーケットプレイスが、利用者の側で、登録済みかに依存し、未確認の点がある。

**Independent Test**: 手順書の手順を、隔離した環境で試し、導入できる範囲を、すべて報告する。

**Acceptance Scenarios**:

1. **Given** 手順書、**When** Claude の導入の設定(`.claude/settings.json`)を使う、**Then** マーケットプレイスが登録され、有効化の設定が入る(公式: `enabledPlugins` だけでは導入されず、利用者が、`claude plugin install … --scope project` を 1 回実行する必要がある。ローカルのマーケットプレイスの相対パスは、例外)。
2. **Given** 手順書、**When** Codex・Antigravity の手順を使う、**Then** 各ツールの仕組みで、導入できる(Codex は、`.agents/plugins/marketplace.json` の、リポジトリ単位のマーケットプレイス。Antigravity は、`agy plugin install` か、`.agents/plugins/` への配置)。

---

### Edge Cases

- 利用者が、`.claude/settings.json` を信頼しない場合(`extraKnownMarketplaces` が、警告なしで無視される。公式)。
- 依存先のマーケットプレイスが、利用者の環境で、未登録の場合。
- `.agents/skills` を、Codex と Antigravity の両方が読むため、どちらかだけの内容を置けない(`.agents/` の共有)。
- `develop` で、`.claude/` のスキルを直したのに、`.agents/`・`.codex/` を直し忘れて、ツールの間でずれる(受け入れる)。
- ECC 由来のものが、`.claude/`・`.agents/`・`.codex/` に混ざっている(扱いは、前提)。
- Windows の Git Bash で、日本語を含むパスをスクリプトが扱う場合(004 で、外部コマンドへの絶対パスが失敗した)。
- Unreal の submodule が、未取得(空)の場合。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `develop` の `.agents/` と `.codex/` を、`.claude/` から生成しない、独立した正本にする。004・005 の同期(`scripts/sync-agent-env.py`)は、**廃止する**(ユーザーの回答)。`AGENTS.md`・共有の一覧の、同期に関する記述(「生成物は手で直さない」など)も、直す。
- **FR-002**: 1 つのコマンドで、`develop` から、`main` に出す構成を、出力先に組み立てる。同じ入力で、同じ出力。
- **FR-003**: 出力は、`.claude/`、`.codex/`、`.agents/`、最小の `AGENTS.md`、外部プラグインの導入の設定、`README.md` を含み、`specs/`、`docs/`、`scripts/`、`.specify/`、`vendor/`(Unreal を除く)を含まない。
- **FR-004**: `main` 専用の最小の `AGENTS.md` を、`develop` の `AGENTS.md` とは別に用意する。rules の案内だけを書く。
- **FR-005**: 外部プラグイン(superpowers、Unity、i-have-adhd)は、`vendor/` に同梱せず、導入の設定と手順書で扱う。Unreal は、Epic の submodule(Unreal 側に `marketplace.json` がない)で、同梱を許可されているため、`vendor/` に残す。
- **FR-006**: 組み立てのスクリプトは、`develop` の正本と `vendor/` を書き換えない。
- **FR-007**: `main` への実際のマージ・push は、スクリプトに含めない。
- **FR-008**: 導入の手順書を、`docs/共有環境/` に書く。確認できなかった点は、「未確認」と書く。

### Key Entities

- **独立した正本**: `develop` の `.claude/`(Claude)、`.codex/`・`.agents/`(Codex・Antigravity)。互いを、生成の元にしない。
- **変換ブランチ**: `develop` から組み立てた、`main` に出す構成だけを持つブランチ。手で直さない。
- **外部プラグインの導入の設定**: Claude は `.claude/settings.json` の `extraKnownMarketplaces` と `enabledPlugins`。Codex は `.agents/plugins/marketplace.json`。Antigravity は、手順書(`agy plugin install`、または `.agents/plugins/` への配置)。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 同期スクリプトを実行しても、`develop` の `.agents/`・`.codex/` の差分が 0 件。
- **SC-002**: 組み立てを実行するコマンドの数が 1 つで、同じ入力で 2 回実行したとき、出力の差分が 0 件。
- **SC-003**: 出力に、「`main` に置かないもの」が 0 件。
- **SC-004**: 外部プラグイン(superpowers、Unity、i-have-adhd、Unreal)のうち、手順書どおりに導入できたものの数を、すべて報告する(導入できないものは、理由を書く)。
- **SC-005**: `vendor/` と `.claude/` の差分が 0 件。

## Assumptions

- 変換ブランチの名前は、実態に合わせて `main-build`(仮)とする(計画で決める。変えられる)。
- **ECC と SkillSpector の扱い(ユーザーの回答で、確定)**: 自作のものを、プラグインにしなくなったため、ECC 由来のもの(`.claude/skills/` の 6、`.claude/agents/` の 5、`.claude/commands/` の 6、`.claude/rules/` の `cpp/`・`csharp/`・`rust/`、`.agents/` の ECC 由来、`.agents/ecc-install-state.json`、`.claude/ecc/`)は、**`main` の `.claude/`・`.agents/`・`.codex/` に置く**(ユーザーが「置く」と回答)。「ECC と SkillSpector は、読み込ませるプラグインに含めない」というメモは、自作をプラグインにしなくなったことで、「ECC を、プラグインとして配布しない」という意味に、読み替える。SkillSpector は、`AGENTS.md` のセキュリティの節に記述があるだけで、ファイルとしては、`main` に含まれない。`main` 専用の `AGENTS.md` には、セキュリティの節を含めない。
- 外部プラグインの導入: Claude は、`dependencies` を使わない(自作のプラグインがないため)。代わりに、プロジェクトの `.claude/settings.json` に、`extraKnownMarketplaces` と `enabledPlugins` を書く(信頼ダイアログの後に有効)。ただし、`enabledPlugins` だけでは導入されないため、利用者が、`claude plugin install` を 1 回実行する(公式)。
- Codex の外部プラグイン: リポジトリ単位のマーケットプレイス(`.agents/plugins/marketplace.json`)に、`source: "url"` などで、外部の Git の URL を指す(公式の書式。superpowers の README の記述では、`https://github.com/obra/superpowers`)。Codex は、プラグイン同士の依存の仕組みがない。
- Antigravity の外部プラグイン: `agy plugin install <GitHub の URL>`、または `.agents/plugins/` への配置。IDE では、導入のコマンドが公式にない。
- 外部プラグインのうち、Unity と i-have-adhd が、Codex・Antigravity で使えるか(`.codex-plugin`・`.antigravity-plugin` を持つか)は、未確認。計画で調べる。Unreal は、Claude 専用(`.claude-plugin` のみ)。
- 前回までの調査結果(旧 research.md)のうち、Antigravity のプラグインの部品(`rules/`、`agents/`、ルートの `hooks.json`)、Codex のフック(`SessionStart`、`UserPromptSubmit`)、`dependencies` の動作は、外部プラグインの導入の設定に、必要な範囲で使う。
- Claude Code の最小バージョン: 手元は `2.1.233`。
- 作業ブランチは `feat/plugin-conversion`(`develop` から作成)。
