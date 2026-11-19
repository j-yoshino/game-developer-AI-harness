# game-developer-AI-harness

ゲーム開発用の AI エージェントハーネス。Claude Code・Codex・Antigravity で、同じ考え方(依頼の窓口、確かめる者、相談役、spec-kit の流れ)を使えるようにする。

このブランチ(`main`)は、`develop` から、スクリプトで組み立てた最小構成。手で直さない。作業は、`develop` で行う。

## 開き方

このリポジトリを clone して、フォルダを開く。

| ツール | 読み込まれるもの |
|---|---|
| Claude Code | `.claude/`(スキル、エージェント、rules、フック)。`.claude/settings.json` が、窓口のフックの登録と、外部プラグインの設定を持つ。フォルダの信頼ダイアログで、信頼する |
| Codex | `.agents/skills/`(スキル)、`.codex/`(エージェント、フック)。`AGENTS.md` の案内に従って、`.claude/rules/` を読む。プロジェクトの `.codex/` の信頼と、フックのレビューが要る |
| Antigravity | `.agents/`(スキル、エージェント、rules、フック)。プラグインの中のフックは、CLI のみ |

## 外部プラグインの別導入

superpowers、Unity、i-have-adhd、Unreal は、同梱していない。次のとおり、別に導入する。

### Claude Code

1. フォルダを開き、信頼ダイアログで、信頼する(信頼しないと、`.claude/settings.json` の `extraKnownMarketplaces` は、警告なしで無視される)。
2. 次を、リポジトリのルートで、1 回ずつ実行する(`enabledPlugins` の設定だけでは、導入されない)。

   ```bash
   claude plugin install superpowers@superpowers-dev --scope project
   claude plugin install unity@unity-agent-plugin --scope project
   claude plugin install i-have-adhd@i-have-adhd --scope project
   ```

3. Unreal(`unreal-engine-skills-for-claude-code`)は、このリポジトリの `vendor/` と、`.claude-plugin/marketplace.json` を使うため、導入の操作は、要らない。Windows では、Git for Windows(`bash`)か、WSL が要る(Unreal の README の注意)。

### Codex

- このリポジトリの `.agents/plugins/marketplace.json` が、superpowers、Unity、i-have-adhd を、Git の URL で指す。
- アプリで、このフォルダを開き、「Plugins」のマーケットプレイスの選択で、「Game Developer AI Harness (main)」を選んで、導入する。CLI では、`codex plugin marketplace add ./`。
- 導入の後、新しい会話を始める。

### Antigravity

- CLI: `agy plugin install https://github.com/obra/superpowers`、`agy plugin install https://github.com/Unity-Technologies/unity-agent-plugin`。
- IDE・App: 導入のコマンドは、公式にない。プラグインのフォルダを、`.agents/plugins/`(プロジェクト単位)か、`~/.gemini/config/plugins/`(全体)に、置く。
- i-have-adhd は、ルートに `plugin.json` があるが、Antigravity の書式に合うかは、未確認。

## 個人の設定の例

`.claude/settings.json` は、共有の設定で、個人の設定を含めない。自分の設定は、`.claude/settings.local.json` に書く。例(返答の言語を日本語にする):

```json
{
  "language": "japanese"
}
```

(`settings.json` は、コメントを受け付けないため、ここに、コピーできる例を置く。)

## 確かめていないこと

- Codex・Antigravity の外部プラグインの導入は、公式の資料に基づく手順。作者の環境では、Codex アプリで、superpowers を、ローカルのマーケットプレイス(`vendor/` を指す形)から導入できることを確かめた。Git の URL で指す形(この `.agents/plugins/marketplace.json`)、Unity と i-have-adhd、Antigravity の導入は、確かめていない。
- `.claude/settings.json` の `directory` の `path: "."` が、リポジトリのルートを指すか(公式で基準を確認できていない。作者の環境では、動いている)。
- 依存先のマーケットプレイスが、利用者の環境で、未登録のときの動作(Claude は、`extraKnownMarketplaces` が登録を担う見込み)。
