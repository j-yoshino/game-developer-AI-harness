# 納品書: 初期化のルールを C++・Unreal と C#・Unity に加える

- 状態: 確認待ち
- 依頼: 
  - こう理解した:
    - C++・Unreal: 型の既定値(0・false・nullptr)にする変数は `{}` で、それ以外の値は `=` で初期化する(「プレース」は「ブレース」と読み、ユーザーが確認した)。
    - C#・Unity: 値型の既定値は `= default`。それ以外はユーザーが「提案して」と求め、提案(null が意味を持つ参照型は `T? = null`、`string` は `= string.Empty`、コレクションは `= []` か `= new()`、それ以外の値は `= 値`)に、ユーザーが合意した。
    - Unity の公式記事は、冗長な初期化子の削除を求める。ユーザーは理由(フィールドが自動で既定値になる)を聞いた上で、`= default` の明示を選んだ。
    - 作業分のコミットは、ユーザーが指示した(push はしない)。
  - やらないこと: push・PR。md の OKF への統一(別の作業として、ユーザーの確認の後に行う)。既存コードの書き換え(コードはまだない)。
- 納品日: 2026-11-19

> 状態は、置いた時点で「確認待ち」。承認はユーザーが行い、「承認済み」に変える。確認待ちの間は、完了とは言わない。

## 完了の判定ごとの報告

### C++・Unreal の初期化のルール

- 何をしたか: `.claude/rules/cpp/coding-style.md` に「Project Rules: Initialization」の節を足し、`.claude/rules/unreal-engine/coding-style.md` に、それを参照する「Initialization」の節を足した。
- 確認した方法: `git diff` で、追記が両ファイルにあることを確認した。`grep -c Initialization` が、両ファイルで 1 以上。
- 確認していないこと: Unreal の `UPROPERTY` で、UnrealHeaderTool がブレースの形を受け付けること(ルールに「未確認」と書いた)。

### C#・Unity の初期化のルール

- 何をしたか: `.claude/rules/csharp/coding-style.md` に「Project Rules: Initialization」の節を足した。`.claude/rules/unity/coding-style.md` の「フィールドを既定値で初期化しない」の行を、プロジェクトの規則(値型は `= default`)に置き換え、公式記事と異なることを明記した。
- 確認した方法: `git diff` で、両ファイルの変更を確認した。公式記事の該当の文を、WebFetch で確認した(「冗長な初期化子 … は削除してください」)。
- 確認していないこと: `= default` と、冗長な初期化子を指摘するアナライザー(IDE0034、CA1805)の関係(ルールに「未確認」と書いた)。

### 日本語訳と他ツールの複製

- 何をしたか: `docs/rules-ja/` の同じ 4 ファイルと、`.agents/rules/` の同じ 4 ファイルに、同じ変更を反映した。
- 確認した方法: `git diff --stat` で 12 ファイルの変更を確認した。
- 確認していないこと: `.codex/` 側には rules の複製がないため、変更していない(`.codex/agents/` が rules を指す方式のため。内容は未確認)。

## 追加した項目

- Unity の規約の食い違い(公式の理由)を、`unity/coding-style.md` の行に書き足した。

## 確かめる者の報告

検査不要: ドキュメント(rules)だけの変更で、ソースファイルもテストファイルも含まない。
