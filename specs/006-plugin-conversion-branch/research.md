# Research: main 用の構成を組み立てる変換ブランチ

調査日: 2026-11-17。ここに書く事実は、公式ドキュメントの本文か、このマシンでの実行結果で確認できたものだけ。二次資料は、そう明記する。旧版(自作を 3 つのプラグインに変換する計画)の調査のうち、使える事実を引き継いで、書き直した。

## R1: 外部プラグインを、ツールごとに別導入する仕組み

対象は、superpowers、Unity、i-have-adhd(外部の Git リポジトリ)と、Unreal(Epic の submodule)。

| プラグイン | リポジトリ | Claude | Codex | Antigravity |
|---|---|---|---|---|
| superpowers | `https://github.com/obra/superpowers.git` | `marketplace.json` あり(名前 `superpowers-dev`) | `.codex-plugin` あり | `.antigravity-plugin` あり |
| Unity | `https://github.com/Unity-Technologies/unity-agent-plugin.git` | `marketplace.json` あり(名前 `unity-agent-plugin`) | `.codex-plugin` あり | `.antigravity-plugin` あり |
| i-have-adhd | `https://github.com/ayghri/i-have-adhd.git` | `marketplace.json` あり(名前 `i-have-adhd`) | `.codex-plugin` あり | ルートの `plugin.json` あり(`.antigravity-plugin` はない。Antigravity が、ルートの `plugin.json` を、プラグインとして読むかは、公式の説明(「`plugin.json` はプラグインのルート、または `.antigravity-plugin/`」)からは読めるが、中身が、Antigravity の書式に合うかは、未確認) |
| Unreal | `https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin.git` | `.claude-plugin/plugin.json` のみ(`marketplace.json` なし)。README は、公式マーケットプレイス `claude-plugins-official` に公開されていると書くが、手元のキャッシュ(2025-12)には載っておらず、未確認 | なし | なし |

(各リポジトリの中の、隠しフォルダの有無は、`vendor/` の中を `ls` して確認。)

### Claude

- プロジェクトの `.claude/settings.json` に、`extraKnownMarketplaces` と `enabledPlugins` を書く。`extraKnownMarketplaces` は、フォルダの信頼ダイアログの後に有効になる(信頼しないと、警告なしで無視される)。`enabledPlugins` だけでは導入されず、利用者が、`claude plugin install <名前>@<マーケットプレイス> --scope project` を、clone ごとに 1 回実行する(公式。https://code.claude.com/docs/en/plugins/org.md)。ローカルの `directory` マーケットプレイスの、相対パスのプラグインは、例外(導入が不要)。
- マーケットプレイスの `source` の書式(公式の例): `{"source": "github", "repo": "owner/repo"}`。
- Unreal: 今の仕組み(リポジトリ直下の `.claude-plugin/marketplace.json` が、`./vendor/unreal-engine-skills-for-claude-code-plugin` を指し、`settings.local.json` の `extraKnownMarketplaces` が、`{"source":"directory","path":"."}` を指す)を、そのまま `main` に持っていく。これは、このマシンで動いている(`claude plugin list` で有効)。

### Codex

- リポジトリ単位のマーケットプレイス: `$REPO_ROOT/.agents/plugins/marketplace.json`。Git の外部プラグインは、`"source": {"source": "url", "url": "<リポジトリの URL>"}`(リポジトリのルートがプラグインの場合)で指す(公式の書式。https://developers.openai.com/codex/plugins/build.md)。CLI の追加: `codex plugin marketplace add ./local-marketplace-root`。アプリは、マーケットプレイスを選んで導入する。
- 導入後の有効化: プロジェクトの `.codex/config.toml` に `[plugins."名前@マーケットプレイス名"]` と `enabled = true`(公式。信頼したプロジェクトのみ)。
- **未確認**: `source.url` が、`.git` つきの URL を受け付けるか。リポジトリのルートが、`.codex-plugin` を持つプラグインのとき、ルートの指定が、`"url": "./"`(superpowers の `.agents/plugins/marketplace.json` の例)と、外部の URL で、同じ動作か。
- Codex には、プラグイン同士の依存の仕組みがない(公式のビルドの資料に記載なし)。

### Antigravity

- `agy plugin install https://github.com/<owner>/<repo>`(CLI)。IDE・App は、`.agents/plugins/`(プロジェクト単位)か、`~/.gemini/config/plugins/`(全体)に、プラグインのフォルダを置く(https://antigravity.google/docs/plugins)。IDE には、導入のコマンドも、マーケットプレイスの操作も、公式に記載がない。
- 外部プラグインの中身を、`main` に置くと、同梱になる(やらないこと)。そのため、`main` には、導入の手順(`agy plugin install <URL>`)だけを書く。IDE の利用者は、手順書に従って、手でフォルダを置く(005 の `scripts/setup-antigravity-plugins.py` と同じ。ただし、このスクリプトは `vendor/superpowers` から複製するため、`main` には含めない)。

## R2: `main` に置くもの・置かないもの(追跡されているファイルが基準)

- **基準**: `git ls-files`(追跡済みのファイル)を元にする。これにより、ローカルだけの状態(`.claude/ecc/install-state.json` は、`.git/info/exclude` で除外。`.agents/ecc-install-state.json` は、追跡されていない。中に、このマシンの絶対パスが 14 件ある)は、自然に含まれない。ユーザーの「ECC 由来を置く」は、追跡されているファイル(スキル・エージェント・コマンド・rules)に当たり、インストーラーの記録は、含めない(ローカルの状態で、パスが個人のため)。
- **件数(2026-11-17 時点)**: 追跡済みの `.claude/` は 62 件、`.agents/` と `.codex/` は 73 件。
- **置く**: `.claude/`(`settings.local.json` を除く)、`.codex/`、`.agents/`(`plugins/marketplace.json` は、`main` 用に、URL の外部プラグインへ書き換える)、`.claude-plugin/marketplace.json`(Unreal 用。そのまま)、`vendor/unreal-engine-skills-for-claude-code-plugin`(submodule)と、Unreal だけの `.gitmodules`、`main` 用の `.claude/settings.json`(新規)、最小の `AGENTS.md`、`CLAUDE.md`、`README.md`(導入の手順つき)、`.gitattributes`。
- **置かない**: `specs/`、`docs/`、`scripts/`、`.specify/`、`vendor/` の他の 3 つ(superpowers、Unity、i-have-adhd)、`.claude/settings.local.json`(個人の設定)、`.gitignore`(`develop` の派生物の除外のため)。
- **注意**: `.claude/settings.local.json` に、窓口のフック(`UserPromptSubmit`)の登録があり、個人の設定(`env`、`model`、`effort`、`advisorModel`、`teammateMode`、`language`)も入っている。`main` の利用者に、窓口のフックを効かせるには、共有の `.claude/settings.json` に、フックの登録を書く必要がある(R3)。

## R3: `main` 用の `.claude/settings.json`

- **内容**: `hooks`(`UserPromptSubmit` で、`bash "$CLAUDE_PROJECT_DIR/.claude/hooks/window-reminder.sh"`)、`extraKnownMarketplaces`(superpowers-dev=`github` の `obra/superpowers`、unity-agent-plugin=`github` の `Unity-Technologies/unity-agent-plugin`、i-have-adhd=`github` の `ayghri/i-have-adhd`、game-developer-ai-harness=`directory` の `.`(Unreal 用))、`enabledPlugins`(4 つ)。
- **含めない**: `env`、`model`、`effortLevel`、`advisorModel`、`teammateMode`、`language`、`enableWorkflows` などの個人の設定。
- **未確認**: `directory` の `path: "."` が、プロジェクトの設定の中で、リポジトリのルートを指すか(公式で基準を確認できなかった。`develop` の `settings.local.json` では、動いている)。マーケットプレイスの名前は、各リポジトリの `marketplace.json` の `name` と一致している必要があるか(公式で未確認。`develop` では、名前を一致させて、動いている)。

## R4: 004・005 の同期の廃止の影響(コマンドで確認)

- `scripts/sync-agent-env.py` を、廃止する。
- **直すもの**: (1) `.agents/` と `.codex/` の中の、「generated from … Do not edit; run scripts/sync-agent-env.py」というコメント(46 ファイル)を、取り除く(rules は HTML コメント、エージェントの `.md` は HTML コメント、TOML は `#` の行)。(2) `AGENTS.md` の「他のツールとの共有」の節(「生成物は手で直さない」「同期を実行する」の記述)と、表の 1 行。(3) `docs/共有環境/共有の一覧.md` の同期に関する記述。(4) `docs/共有環境/環境構築.md` の、`sync-agent-env.py` への言及。
- **直さない**: 過去の納品書(004・005 の記録は、その時点の事実)。`specs/004`・`specs/005`(過去の仕様)。
- **残すもの**: `scripts/setup-antigravity-plugins.py`(`vendor/superpowers` を `.agents/plugins/superpowers/` に複製する。`develop` での作業用)。ただし、`main` には含めない。

## R5: 変換ブランチと main

- **流れ**: `develop` →(スクリプトで組み立てる)→ 変換ブランチ →(PR)→ `main`。
- **スクリプト**: `scripts/build-main.py`(出力先に組み立てる。同じ入力で、同じ出力)と、`scripts/publish-main-branch.py`(`git worktree` で、ローカルの変換ブランチに、出力をコミットする。push しない。`main` には触れない)。ブランチ名は、`main-build`(仮)。
- **履歴**: 変換ブランチは、毎回、`develop` の内容から生成し直す(生成物のコミットが並ぶ)。
- **submodule**: Unreal の submodule を、変換ブランチに含めるには、`git submodule` の gitlink(コミットの指し先)を、`develop` と同じものにする。`git worktree` と submodule の組み合わせは、取り扱いが難しい可能性がある(未確認。実装で確かめる)。

## R6: Windows の注意

- 日本語を含む絶対パスを、外部コマンドに渡さない(004 で、Git Bash が失敗した)。相対パスと `cwd` で呼ぶ。
- フックのスクリプトは、`bash` が要る(Claude・Codex)。Windows で `bash` が無い環境では、動かない。README に書く。

## R7: 未確認のまま残るもの

- 依存先(外部プラグイン)のマーケットプレイスが、新しい利用者のマシンで、未登録のときの解決(Claude の `extraKnownMarketplaces` が、登録を担うため、解消する見込み。ただし、信頼ダイアログの後)。
- Codex の `source.url` の動作、i-have-adhd の Antigravity 対応。
- `directory` の `path: "."` の基準。
- Unreal が、公式マーケットプレイスにあるか。
