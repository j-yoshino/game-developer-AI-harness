# GameDeveloperAIHarness

ゲーム開発用の AI エージェントハーネス(`main`)。このファイルは、`develop` から組み立てた最小版で、rules の案内だけを書く。

## rules の案内

rules は、`.claude/rules/` にある。Claude Code は、`.claude/rules/` を自動で読み込む(毎回: `window.md`・`answer-policy.md`、`paths` で絞ったものは、該当するファイルを触るとき)。Codex は、`.claude/rules/` を自動では読み込まない。次のとおり、該当する rules を、作業の前に読む(Claude Code と Antigravity は、別の仕組みで読み込むため、重ねて読んでも害はない)。

- 毎回: `.claude/rules/window.md` と `.claude/rules/answer-policy.md`。
- C/C++ のソース・ヘッダ、`CMakeLists.txt` を触るとき: `.claude/rules/cpp/` の 5 ファイル。
- C#(`*.cs`、`*.csx`)を触るとき: `.claude/rules/csharp/` の 5 ファイル。
- Rust(`*.rs`、`Cargo.toml`)を触るとき: `.claude/rules/rust/` の 5 ファイル。
- Unity(`Assets/` 配下の `*.cs`、`*.asmdef`)を触るとき: `.claude/rules/unity/` の 5 ファイル。重なる `csharp/` よりも `unity/` を優先する。
- Unreal(`Source/` と `Plugins/**/Source/` の `.h` `.cpp` `.cs`)を触るとき: `.claude/rules/unreal-engine/` の 5 ファイル。重なる `cpp/` よりも `unreal-engine/` を優先する。

## 置き場所

- Claude: `.claude/`(スキル、エージェント、rules、フック)。
- Codex: `.codex/`(エージェント、フック)と `.agents/`(スキル)。
- Antigravity: `.agents/`(スキル、エージェント、rules、フック)。
- 外部プラグイン(superpowers、Unity、i-have-adhd、Unreal)は、同梱せず、別に導入する。手順は `README.md`。
