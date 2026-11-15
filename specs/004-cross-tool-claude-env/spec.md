# Feature Specification: Codex・Antigravity を Claude と同じ環境で使えるようにする

**Feature Branch**: `feat/cross-tool-claude-env`

**Created**: 2026-11-15

**Status**: Draft

**Input**: User description: 「Codex と Antigravity CLI を、Claude Code とほぼ同じ環境で使えるようにする。`.claude/` を正本とし、`.agents/` から参照させる。共有する範囲は、スキル、エージェント、rules、フック。あわせて、リポジトリ直下の `.claude-plugin` を vendor 側のプラグインと同じ形(`plugin.json` も置く)に揃える」

## 依頼票

### ご要望(原文)

- 「.claude-plugin以下って、まとめられない?」
- 「codex, antigravity cliはclaudeのやつ参照して使用できるようにできない?」
- 「リポジトリ直下のやつを他と同じようにまとめられる?」
- 「なるべくclaudeと同環境にしたい。またなるべく.claudeを参照して使用できるようにしたい」

選択式の質問への回答(原文のまま):
- 直下の `.claude-plugin` は「vendor 側と同じ形(plugin.json も置く)に揃える」。
- 方針は「`.claude` を正本にし、`.agents` から参照させる」。
- 共有する範囲は「スキル、エージェント、rules(`.claude/rules/`)、フック(`window-reminder.sh`)」の全部。

### こう理解した

- Codex と Antigravity CLI で、Claude Code と同じ指示・スキル・エージェント・rules・フックを使えるようにしたい。
- 内容は 2 か所に書かず、`.claude/` を唯一の正本にする。`.agents/` 側は、そこを参照する形にして、手で二重に直さなくて済むようにする。
- リポジトリ直下の `.claude-plugin` は、vendor 側のプラグイン(`plugin.json` と `marketplace.json` を持つ形)と同じ構成に揃える。
- 「なるべく」とあるため、ツールが対応していない項目は無理に再現せず、「共有できない」と明記する(推測であり、確認が要る点は完了の判定で扱う)。

### 誰のためか

このハーネスを使って、Claude Code・Codex・Antigravity CLI を切り替えながらゲームを開発する本人(ユーザー)。

### やらないこと

- `vendor/` 配下のファイルの編集(submodule であり、`AGENTS.md` の規則で触らない)。
- Codex・Antigravity が対応していない機能(例: フックの仕組みが無いツールでのフック)を、別の仕組みで無理に作り込むこと。共有できない項目は、一覧で明記するだけにする。
- `.claude/` の内容の書き換え(正本の内容の変更)。この作業は、参照のしかたを足すだけで、スキル・エージェント・rules・フックの中身は変えない。
- Claude Code 側の動作を変えること。
- Codex・Antigravity 以外のツール(Cursor、Gemini CLI など)への対応。
- 既に `.agents/` にある ECC 由来のファイルの内容の変更(重なる分の整理の方針は、計画で決める)。

### 完了の判定

- [ ] `.claude/` にあるスキル 18 件、エージェント 9 件、rules 27 ファイルのそれぞれについて、Codex・Antigravity が読む場所に、同じ内容が見える(一覧と、内容が一致することをコマンドで確かめる)。
- [ ] `.claude/` のファイルを 1 つ書き換えたとき、手作業なしで、または 1 つのコマンドで、`.agents/` 側にも反映される(実際に書き換えて確かめる)。
- [ ] フック(`window-reminder.sh`)について、Codex・Antigravity のそれぞれで「共有できた」か「できない(理由つき)」かが、一覧で明記されている。
- [ ] リポジトリ直下の `.claude-plugin` が、vendor 側と同じ構成(`plugin.json` と `marketplace.json`)になり、`claude plugin validate .` が通り、`claude plugin list` で 4 つのプラグインの有効化が従来どおりに保たれている。
- [ ] Claude Code 側の動作が変わっていない(スキル・エージェントの一覧と、`window-reminder.sh` の動作が、変更前と一致する)。
- [ ] [ユーザー検収] 実際の Codex と Antigravity CLI を起動して、共有したスキルやエージェントが使えることを確かめる(このマシンには `codex` と `agy` が入っておらず、こちらでは起動して確かめられない)。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 1 か所を直せば 3 つのツールに反映される (Priority: P1)

開発者は、スキル・エージェント・rules を `.claude/` で直す。Codex と Antigravity でも、同じ内容が使える。

**Why this priority**: 「なるべく Claude と同環境」という依頼の中心であり、これが無いと他の項目に価値がない。

**Independent Test**: `.claude/` のスキル 1 件の本文を書き換え、`.agents/` 側から同じ書き換えが見えることを確かめる。

**Acceptance Scenarios**:

1. **Given** `.claude/skills/window-question/SKILL.md` がある、**When** `.agents/skills/window-question/SKILL.md` を開く、**Then** 同じ内容が見える。
2. **Given** `.claude/` のスキルを書き換えた、**When** 反映の手順(あれば)を行う、**Then** `.agents/` 側にも変更が出る。手順は 1 つのコマンド以内である。
3. **Given** 共有できない項目(対応していないツール機能)がある、**When** 一覧を見る、**Then** 共有できない理由と範囲が書かれている。

---

### User Story 2 - フックの働きを可能な範囲で揃える (Priority: P2)

開発者は、Claude の窓口フック(毎ターンの注意の注入)と同じ働きを、Codex・Antigravity でも得たい。

**Why this priority**: 窓口の遵守は、フックなしでは弱くなる(`AGENTS.md` に「遵守は保証されない」と書いてある)。ただし、ツールの対応状況が不明なため、P1 の後に扱う。

**Independent Test**: 各ツールのフック機能の有無を、公式ドキュメントで確かめ、対応するものは設定を書き、対応しないものは一覧に明記する。

**Acceptance Scenarios**:

1. **Given** ツールがフックに対応している、**When** 設定を足す、**Then** `window-reminder.sh` と同じ注意が、そのツールのプロンプト送信時に注入される。
2. **Given** ツールがフックに対応していない、**When** 一覧を見る、**Then** 対応していないことと、代わりに指示ファイル(`AGENTS.md`)に書いてある内容が一覧で明記されている。

---

### User Story 3 - 直下の `.claude-plugin` を vendor 側と同じ形に揃える (Priority: P3)

開発者は、直下の `.claude-plugin/` を、vendor 側のプラグインと同じ構成にしたい。

**Why this priority**: 依頼にあるが、Codex・Antigravity の対応とは独立している。

**Independent Test**: `claude plugin validate .` と `claude plugin list` で、構成が正しく、4 つのプラグインが有効のままであることを確かめる。

**Acceptance Scenarios**:

1. **Given** 直下に `plugin.json` と `marketplace.json` がある、**When** `claude plugin validate .` を実行する、**Then** エラーがない。
2. **Given** 構成を揃えた、**When** `claude plugin list` を実行する、**Then** 4 つのプラグイン(i-have-adhd、superpowers、unity、unreal-engine-skills-for-claude-code)が、従来どおり有効である。

---

### Edge Cases

- Windows で、シンボリックリンクが作れない、または Git が正しく扱えない場合(`core.symlinks`、権限)。
- `.claude/rules/` のうち、`paths` 付きの rules(特定のファイルを開いたときだけ読み込まれる)が、Antigravity の `.agents/rules/*.md`(フラットな走査のみ)で、条件なしに全部読み込まれる場合の影響(読み込みが増え、規則が衝突する)。
- `.claude/rules/` は階層(`cpp/`、`unity/` など)を持つが、Antigravity はサブフォルダを読まない。
- Claude 用のエージェント定義の frontmatter(`tools`、`model` など)が、Codex・Antigravity では解釈されない、または別の意味になる。
- 既に `.agents/` にある ECC 由来のファイル(スキル 6、エージェント 5、rules、workflows、`ecc-install-state.json`)と、名前が重なる。同名のスキルは、Codex で統合されず、両方表示される(公式に記載)。
- `.claude/` にあって、`.agents/` に対応する置き場がない項目(`commands`、`hooks`、`settings.local.json`)。
- スキャンや検証の最中に、`vendor/` を触ってしまう(作業は `vendor/` の外で行う)。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: スキル、エージェント、rules は、`.claude/` を正本とし、Codex・Antigravity が読む場所(`.agents/` 配下)から、同じ内容が見える。
- **FR-002**: 内容を 2 か所に手で書かない。`.claude/` を直したら、`.agents/` 側は、自動、または 1 つのコマンドで揃う。
- **FR-003**: 共有の対象は、スキル 18 件、エージェント 9 件、rules 27 ファイル、フック 1 件(`window-reminder.sh`)。対象の一覧と、共有の可否(可・不可・一部)を、ファイル(一覧表)に残す。
- **FR-004**: ツールが対応しない項目は、共有できないことと、その理由(出典つき)を、一覧に書く。別の仕組みで無理に再現しない。
- **FR-005**: `.claude/rules/` のうち、`paths` で読み込みを絞っている rules が、他のツールで条件なしに読み込まれる場合は、その影響を一覧に書く。
- **FR-006**: リポジトリ直下の `.claude-plugin/` に、`plugin.json` を置き、vendor 側のプラグインと同じ構成にする。`marketplace.json` は残し、4 つのプラグインの有効化は従来どおりに保つ。
- **FR-007**: `vendor/` 配下を、編集しない。
- **FR-008**: Claude Code 側の動作(スキル・エージェントの一覧、フックの動作、プラグインの有効化)を変えない。
- **FR-009**: 共有の方法と、新しく足したファイルの説明を、`AGENTS.md` に追記する。

### Key Entities

- **正本**: `.claude/` 配下のスキル・エージェント・rules・フック。ここだけを手で編集する。
- **参照側**: `.agents/` 配下の、Codex・Antigravity が読む場所。正本の内容が見える状態にする。
- **共有の一覧**: 項目ごとに、共有の可否、方法、理由、出典を書いた表。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 共有対象のスキル 18 件、エージェント 9 件、rules 27 ファイルのうち、参照側から正本と同じ内容が見える件数が、100%(コマンドで一致を確かめる)。
- **SC-002**: 正本を 1 つ書き換えてから、参照側に反映されるまでの手作業が、0 回、または 1 つのコマンドの実行のみ。
- **SC-003**: 共有の一覧に、共有できない項目がある場合、その全件に理由と出典が付いている(空欄が 0 件)。
- **SC-004**: `claude plugin validate .` が成功し、4 つのプラグインが有効のまま保たれている。
- **SC-005**: 変更の前後で、Claude 側のスキル・エージェントの一覧が一致する(差分 0 件)。
- **SC-006**: `vendor/` 配下の差分が 0 件。

## Assumptions

- Codex と Antigravity は、このマシンに入っていない(`codex`、`agy` は見つからない。`gemini` のみある)。そのため、実際に起動して確かめる項目は、ユーザー検収とする。
- 他のツールの読み込み先は、公式ドキュメントで確かめた範囲に従う: Codex はスキルを `.agents/skills`、指示を `AGENTS.md`(`CLAUDE.md` は読まない)。Antigravity CLI は `.agents/` 配下(`skills/`、`agents/`、`rules/*.md`)、`AGENTS.md`、`GEMINI.md`、フックは `hooks.json`。Codex のエージェントの置き場とフックの有無は、確認できていない。
- 共有の方法(シンボリックリンク、コピー、生成スクリプトなど)は、計画で決める。Windows でのシンボリックリンクの可否は、未検証である。
- 直下の `plugin.json` を置いたとき、直下のリポジトリがプラグインとしても読まれ、`marketplace.json` の `name` や既存の有効化(`enabledPlugins`)との関係に影響する可能性がある。影響の有無は、計画で確かめる。
- 作業ブランチは `feat/cross-tool-claude-env`(`develop` から作成)。
