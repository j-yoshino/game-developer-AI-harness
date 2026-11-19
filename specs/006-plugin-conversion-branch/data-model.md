# Data Model: `main` に出す構成

データベースはない。ファイル上の構成と対応である。

## `develop` の正本(ツールごとに独立。同期なし)

```text
.claude/                 # Claude の正本(変更しない)。settings.local.json は、個人の設定
.codex/                  # Codex の正本(agents/*.toml、hooks.json)。手で保守
.agents/                 # Codex・Antigravity の正本(skills/、agents/、rules/、hooks.json、hooks/)。手で保守
.agents/plugins/marketplace.json   # Codex の、リポジトリ単位のマーケットプレイス(develop では、vendor/superpowers を指す)
.claude-plugin/marketplace.json    # Claude の、Unreal 用マーケットプレイス
vendor/                  # 外部プラグイン(submodule 4 つ)
```

## `main` の構成(組み立てた出力)

```text
.claude/                 # develop の .claude/(追跡済みのもの。settings.local.json を除く 61 件前後)
  settings.json          #   新規(テンプレートから): 窓口のフックの登録、外部プラグインのマーケットプレイスと有効化
.codex/                  # develop の .codex/(追跡済みのもの)
.agents/                 # develop の .agents/(追跡済みのもの)。plugins/marketplace.json は、main 用に書き換える
  plugins/marketplace.json   # main 用: superpowers、Unity、i-have-adhd を、Git の URL で指す
.claude-plugin/marketplace.json   # Unreal 用(そのまま)
vendor/unreal-engine-skills-for-claude-code-plugin   # submodule(Unreal のみ)
.gitmodules              # Unreal のみ
AGENTS.md                # main 専用の最小版(rules の案内のみ)
CLAUDE.md                # @AGENTS.md のみ
README.md                # main 用: 導入の手順(3 つのツール、外部プラグインの別導入)
.gitattributes
```

## 置かないもの

`specs/`、`docs/`、`scripts/`、`.specify/`、`vendor/` の superpowers・Unity・i-have-adhd、`.claude/settings.local.json`、`.gitignore`、追跡されていないファイル(`.claude/ecc/`、`.agents/ecc-install-state.json`、`.agents/plugins/superpowers/`)。

## 組み立ての規則

| 項目 | 規則 |
|---|---|
| 元 | `git ls-files` の、追跡済みのファイル |
| 含める | 上の「`main` の構成」の一覧に当たるもの(許可リスト方式)。一覧にないものは、含めない |
| 書き換える | `.agents/plugins/marketplace.json`(main 用)、`.claude/settings.json`(新規)、`AGENTS.md`、`CLAUDE.md`、`README.md`(テンプレートから) |
| 決定性 | ファイルの順序、改行(LF)、JSON の整形を固定。時刻や乱数を入れない |
| 書き込まないもの | `develop` の正本、`vendor/` |
| 失敗する場合(終了コード 2) | Unreal の submodule が空、テンプレートがない、許可リストの項目が、実際のファイルにない |

## `main` 用の `.claude/settings.json`

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/window-reminder.sh\"", "timeout": 10 } ] }
    ]
  },
  "extraKnownMarketplaces": {
    "superpowers-dev": { "source": { "source": "github", "repo": "obra/superpowers" } },
    "unity-agent-plugin": { "source": { "source": "github", "repo": "Unity-Technologies/unity-agent-plugin" } },
    "i-have-adhd": { "source": { "source": "github", "repo": "ayghri/i-have-adhd" } },
    "game-developer-ai-harness": { "source": { "source": "directory", "path": "." } }
  },
  "enabledPlugins": {
    "superpowers@superpowers-dev": true,
    "unity@unity-agent-plugin": true,
    "i-have-adhd@i-have-adhd": true,
    "unreal-engine-skills-for-claude-code@game-developer-ai-harness": true
  }
}
```

(個人の設定 `env`・`model`・`effortLevel`・`advisorModel`・`teammateMode`・`language`・`enableWorkflows` は、含めない。)

## `main` 用の Codex のマーケットプレイス(`.agents/plugins/marketplace.json`)

名前 `game-developer-ai-harness-main`(仮)。`plugins` に、superpowers、Unity、i-have-adhd の 3 件。各 `source` は `{"source":"url","url":"<リポジトリの URL>"}`、`policy` は `{"installation":"AVAILABLE","authentication":"ON_INSTALL"}`、`category` は `"Developer Tools"`。

## `main` 専用の `AGENTS.md`(rules の案内のみ)

`develop` の `AGENTS.md` の「rules の案内(Codex 向け)」の節と同じ内容(毎回 `window.md`・`answer-policy.md`、作業の種類ごとに `cpp/`・`csharp/`・`rust/`・`unity/`・`unreal-engine/`)。ツールの表、読み替え表、セキュリティの節、ブランチ運用、このリポジトリ独自の表は、含めない。

## 状態の遷移

```text
develop(ツールごとの独立した正本)
  → scripts/build-main.py --out <dir>(同じ入力で、同じ出力)
  → scripts/publish-main-branch.py(ローカルの変換ブランチにコミット。push しない)
  → (ユーザーの確認のもとで)変換ブランチ → main の PR・マージ
```
