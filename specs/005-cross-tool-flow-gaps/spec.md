# Feature Specification: Codex・Antigravity での実装フローの穴を塞ぐ

**Feature Branch**: `feat/cross-tool-flow-gaps`

**Created**: 2026-11-15

**Status**: Draft

**Input**: User description: 「Codex と Antigravity CLI で、実装フロー(窓口、spec-kit、相談役、確かめる者、納品書)の『穴』を塞ぐ」(前回の `specs/004-cross-tool-claude-env` の続き)

## 依頼票

### ご要望(原文)

- 「codexとantigravity側で実装フローでできないことある?」(質問)
- 「穴を塞ぐ作業を進めて」

選択式の質問への回答(原文のまま):
- 塞ぐ穴は「道具名の読み替え」「相談役の読み取り専用の制限」「superpowers の両ツール向けプラグイン」。「Unity・Unreal のプラグインと MCP」は選ばれていない。
- Claude 側の正本(`.claude/rules`、エージェント)の文言は「変えない。AGENTS.md に読み替え表を足す」。

### こう理解した

- 前回の調査で見つかった、Codex と Antigravity CLI で実装フローが動かない 3 つの穴を塞ぐ。
  1. **道具名の読み替え**: 実装フローの rules とエージェントは、Claude Code の道具の名前(ユーザーに選択肢で聞く `AskUserQuestion`、サブエージェントを呼ぶ `Agent` ツールと `subagent_type`)で書いてある。両ツールでは、それが何の操作に当たるかを、読み替えられるようにする。
  2. **相談役の読み取り専用の制限**: 相談役は、Claude では `tools: Read, Grep, Glob` により、書き込めない。Codex 向けに生成した TOML には、この制限が移っていない。両ツールで、読み取り専用にできるかを確かめ、できる場合は設定し、できない場合は、そう明記する。
  3. **superpowers の両ツール向けプラグイン**: 実装フローは `brainstorming` から始まるが、superpowers は Claude にしか入っていない。両ツールで `brainstorming` を使える方法を、確かめて、文書にする(または、設定する)。
- 読み替えは、`AGENTS.md` に表として足す。`.claude/` の文言は、変えない(Claude 側の動作を変えない)。
- Unity・Unreal のプラグインと MCP は、今回は含めない。

### 誰のためか

このハーネスを使って、Claude Code・Codex・Antigravity CLI を切り替えながら、実装フロー(窓口→spec-kit→相談役→確かめる者→納品書)でゲームを開発する本人(ユーザー)。

### やらないこと

- `.claude/` 配下(rules、エージェント、スキル、フック)の文言の変更。読み替えは、`AGENTS.md` の表で行う。
- `vendor/` 配下のファイルの編集。
- Unity・Unreal のプラグインと MCP(Unity CLI を含む)の、両ツール向けの設定。
- Codex・Antigravity が対応していない機能を、別の仕組みで無理に作り込むこと。対応しない項目は、そう明記する。
- Codex・Antigravity 以外のツールへの対応。
- 実機(Codex・Antigravity)での動作の保証。このマシンには、どちらも入っていない。
- 外部のプラグインを、ユーザーの確認なしに、インストールすること(ダウンロードして実行する操作を含む)。

### 完了の判定

- [ ] `AGENTS.md` に「道具名の読み替え表」があり、実装フローで使う Claude 固有の道具(`AskUserQuestion`、`Agent` ツールと `subagent_type`、スキルの呼び出し、ほか調査で見つかったもの)のすべてについて、Codex と Antigravity での対応する操作、または「対応なし」(理由と出典つき)が書かれている。
- [ ] 相談役の読み取り専用の制限について、Codex と Antigravity のそれぞれで、「設定できる(設定した。公式の根拠つき)」か「できない(理由と出典つき。代わりの対策も)」かが、共有の一覧に明記されている。設定できる場合は、同期スクリプトの出力に反映され、`--check` が通る。
- [ ] superpowers(`brainstorming`)を、Codex と Antigravity で使う方法が、公式または submodule の記述に基づく手順として文書化されている(または、ユーザーの確認なしに行える範囲で設定されている)。確かめられなかったことは、そう書かれている。
- [ ] `.claude/` の差分が 0 件、`vendor/` の差分が 0 件、`python scripts/sync-agent-env.py --check` が成功する。
- [ ] [ユーザー検収] 実際の Codex と Antigravity CLI で、読み替え表のとおりに、実装フローの一部(例: 窓口の質問、相談役の呼び出し)が動くことを確かめる(このマシンには、どちらも入っていない)。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 道具名を読み替えて実装フローを進められる (Priority: P1)

開発者が Codex や Antigravity CLI で実装フローを進めるとき、rules に書かれた Claude の道具の名前を、そのツールの操作に読み替えられる。

**Why this priority**: 窓口(質問への選択肢)と、確かめる者・相談役の呼び出しが、この読み替えに依存している。穴の中心。

**Independent Test**: `AGENTS.md` の読み替え表を読み、`window.md` に出てくる Claude 固有の道具のすべてが、表に載っていることを確かめる。

**Acceptance Scenarios**:

1. **Given** `window.md` が `AskUserQuestion` を使うよう指示している、**When** Codex か Antigravity で、`AGENTS.md` の読み替え表を見る、**Then** 同じ目的(ユーザーへの選択肢の質問)の操作、または「対応なし」と代わりのやり方が書かれている。
2. **Given** `window.md` が `Agent` ツールで `window-verifier` を呼ぶよう指示している、**When** 読み替え表を見る、**Then** 各ツールでのエージェントの呼び方(または、対応しない旨)が書かれている。

---

### User Story 2 - 相談役が読み取り専用で動く (Priority: P2)

相談役を呼んだとき、Codex・Antigravity でも、ファイルを書き換えない。

**Why this priority**: 相談役は「決めて進まない」役。Claude の `tools` の制限が外れると、役割の安全弁が失われる。

**Independent Test**: 公式の資料で、両ツールの読み取り専用の設定を確認し、生成物(Codex の TOML など)に反映して、`--check` が通る。設定できない場合は、一覧に明記されている。

**Acceptance Scenarios**:

1. **Given** Codex の TOML に読み取り専用の設定の項目がある(公式で確認できた場合)、**When** 同期スクリプトを実行する、**Then** 相談役の TOML にその設定が出る。
2. **Given** 設定する手段が公式にない、**When** 一覧を見る、**Then** 「できない」と理由、代わりの対策(指示による制限であり、守られる保証は弱い)が書かれている。

---

### User Story 3 - 両ツールで brainstorming を使える (Priority: P3)

開発者が、Codex・Antigravity でも、実装フローの最初の `brainstorming` を使える。

**Why this priority**: 実装フローの入口だが、プラグインの導入は、外部のものの取り込みを伴い、ユーザーの確認が要る。

**Independent Test**: superpowers の submodule の記述(`.codex-plugin`、`.antigravity-plugin` と、README)を読み、導入の手順が書かれていることを確かめる。

**Acceptance Scenarios**:

1. **Given** superpowers に Codex 向けと Antigravity 向けの導入の仕組みがある、**When** 文書の手順を見る、**Then** 各ツールでの導入のコマンドと、確かめた範囲・確かめていない範囲が書かれている。

---

### Edge Cases

- 両ツールに、`AskUserQuestion` に相当する道具がない場合(代わりに、通常の文章で質問する)。
- Codex・Antigravity が、サブエージェントを名前では呼べない場合(前回の調査で、Codex は報告あり)。
- 読み取り専用の設定がエージェントごとではなく、セッション全体の設定である場合。
- superpowers の導入が、ネットワークからのダウンロードを伴う場合(ユーザーの確認が要る)。
- 読み替え表が、`AGENTS.md` を長くして、毎ターンの読み込みの量を増やす場合。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `AGENTS.md` に、Claude 固有の道具の読み替え表を足す。対象は、実装フロー(rules、エージェント、スキル)に出てくる Claude 固有の道具のすべて。
- **FR-002**: 表の各行に、Codex と Antigravity での対応する操作(または「対応なし」)と、出典(公式の URL)を書く。確認できなかったことは、そう書く。
- **FR-003**: 相談役の読み取り専用の制限を、公式で確かめた手段で、Codex・Antigravity の生成物に反映する。手段がなければ、できない旨と代わりの対策を、共有の一覧に書く。
- **FR-004**: superpowers(`brainstorming`)を両ツールで使う方法を、文書化する。外部のものの導入は、ユーザーの確認なしに行わない。
- **FR-005**: `.claude/` と `vendor/` を変更しない。
- **FR-006**: 共有の一覧(`docs/共有環境/共有の一覧.md`)を、この作業の結果で更新する。

### Key Entities

- **読み替え表**: Claude の道具の名前、Codex の対応、Antigravity の対応、出典、確認の状態を持つ、`AGENTS.md` の表。
- **共有の一覧**: 前回作った、項目ごとの共有の可否の表(`docs/共有環境/共有の一覧.md`)。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 実装フローの rules・エージェント・スキルに出てくる Claude 固有の道具のうち、読み替え表に載っているものの割合が 100%(grep で洗い出した一覧と突き合わせる)。
- **SC-002**: 読み替え表の「対応なし」と「未確認」の全行に、理由または確認できなかった旨が書かれている(空欄が 0 件)。
- **SC-003**: 相談役の読み取り専用の制限の可否が、両ツールとも、共有の一覧に書かれている(2/2)。
- **SC-004**: `.claude/` と `vendor/` の差分が 0 件。`--check` が成功する。
- **SC-005**: 両ツールで `brainstorming` を使う手順が、各ツールについて 1 つ以上、文書にある。確かめられなかった項目は、そう書かれている。

## Assumptions

- Codex と Antigravity は、このマシンに入っていない。実機の確認は、ユーザー検収とする。
- 読み替えの根拠は、公式ドキュメント(前回確認した `learn.chatgpt.com` と `antigravity.google` を含む)で確かめる。確認できない対応は、「未確認」と書く。
- 読み替え表の置き場は `AGENTS.md`(ユーザーの選択)。長くなりすぎる場合は、表だけを別のファイルに置き、`AGENTS.md` から案内する形も、計画で検討できる。
- 同期スクリプト(`scripts/sync-agent-env.py`)を、生成物の項目を足すために変更してよい(正本の `.claude/` は変えない)。
- 作業ブランチは `feat/cross-tool-flow-gaps`(`develop` から作成)。
