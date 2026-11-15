# Quickstart: 窓口の検証

窓口が動くことを確かめる手順。遵守は保証されないため、**新しい対話セッション**で、実際に発言を入力して確認する。自動テストは作らない。

## 前提

- すべての成果物(`window.md`、フック、`window-question`、spec テンプレートの override、納品書のテンプレート)が、リポジトリにある。
- リポジトリのルートで、新しいセッションを開始する(フックと rules は、起動時に読み込まれる)。
- 設計: [contracts/hook-io.md](contracts/hook-io.md)、[contracts/request-form.md](contracts/request-form.md)、[contracts/delivery-note.md](contracts/delivery-note.md)、[data-model.md](data-model.md)。

## 準備: スクリプトの単体確認(セッション不要)

1. フックのスクリプトに、サンプルの JSON を標準入力で流す。
2. 標準出力が、1つの JSON であり、`hookSpecificOutput.additionalContext` が 400 文字以内であることを確認する。
3. 終了コードが 0 であることを確認する。

## シナリオ

検証用の発言は、各層で3件以上を用意する(SC-001)。次は、各層の例である。

| # | 層 | 入力する発言(例) | 期待する結果 |
|---|---|---|---|
| 1 | 質問 | 「この rules はいつ読み込まれる?」 | 層の判定も、依頼票も納品書も層の宣言も出ない。根拠が path:line や URL で示される。**注入文が届いたことの確認も兼ねる** |
| 2 | 軽作業 | 「README の誤字を直して」 | 規模が伝えられる。設計メモや計画に進まない。完了後、`docs/納品書/<日付>-<題名>.md` ができ、3欄が埋まり、状態は「確認待ち」。完了とは言わない |
| 3 | 本件 | 「新しい機能を作りたい」 | brainstorming から spec へ進む。spec の依頼票の5欄が埋まる。合意前に実装に入らない。完了後、`docs/納品書/<NNN-feature>.md` ができる |
| 4 | 迷う例 | 「直して push して」 | 外向きの操作を含むため、本件の確認を取る。層は上がる方向にだけ動く |
| 5 | 混在 | 「これは何?あと直しておいて」 | 作業の層で扱う |

## 確認する未検証の項目

research.md の未検証3点を、この検証で確かめる。

1. `additionalContext` がモデルに届き、従われるか(シナリオ 1〜4 の挙動で判断)。
2. フックの command で、プロジェクトのルートを指す環境変数が使えるか(リポジトリの外から起動して確認)。
3. `speckit-specify` が override のテンプレートを使うか(シナリオ 3 の spec に、依頼票の節があるか。`.specify/scripts/powershell/resolve-template.ps1` の出力でも確認)。

## 合否

- SC-001: 判定が期待どおりに出るものが、全体の90%以上。
- SC-002〜SC-006: spec の Success Criteria のとおり。
- 従わない場合は、注入文を直す。それでも従わなければ、設計書の案 B(メインを窓口エージェントにする)への移行を検討する。
