# Contract: 組み立てのスクリプト

## `scripts/build-main.py`

```bash
python scripts/build-main.py --out <出力先>           # 組み立てる(出力先は、空か、存在しない場所。既存の中身は消す)
python scripts/build-main.py --out <出力先> --check   # 出力先との一致を検査する(書かない)
```

- **入力**: `git ls-files`(追跡済みのファイル)、`scripts/templates/`(`main-AGENTS.md`、`main-CLAUDE.md`、`main-README.md`、`main-claude-settings.json`、`main-codex-marketplace.json`)、`vendor/unreal-engine-skills-for-claude-code-plugin`(submodule。読むだけ)。
- **出力**: data-model.md の `main` の構成。
- **終了コード**: 0 = 成功 / 一致、1 = `--check` でずれ、2 = 入力が不正(Unreal の submodule が空、テンプレートがない、許可リストの項目がない、など)。
- **規則**: `develop` の正本と `vendor/` を書かない。許可リスト方式で、一覧にないファイルは、出力に入れない。出力に、このマシンの絶対パスや、個人の設定が入らない(出力を `grep` で確かめる)。
- **外部コマンド**: 日本語を含む絶対パスを渡さない(相対パスと `cwd`)。

## `scripts/publish-main-branch.py`

```bash
python scripts/publish-main-branch.py [--branch main-build]
```

- `git worktree` で、ローカルの変換ブランチを開き、中身を、`build-main.py` の出力に置き換えて、コミットする。**push しない。`main` に触れない。** 変更がなければ、コミットしない。コミットの本文に、`develop` のコミットの短いハッシュを書く。
- 終了コード: 0 = 成功(変更なしを含む)、2 = `develop` に未コミットの変更がある、など。
- Unreal の submodule の扱い(gitlink を、`develop` と同じコミットにする)は、`git worktree` との組み合わせで難しい可能性がある(未確認)。実装で確かめ、難しければ、手順を文書化する。

## 同期の廃止(同じ作業の中)

- `scripts/sync-agent-env.py` を削除する。
- `.agents/`・`.codex/` の「generated from …」コメント(46 ファイル)を取り除く。
- `AGENTS.md`、`docs/共有環境/共有の一覧.md`、`docs/共有環境/環境構築.md` の、同期の記述を直す。
