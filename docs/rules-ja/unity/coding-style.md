> 日本語訳(参照用)。原文(英語): `.claude/rules/unity/coding-style.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `Assets/**/*.cs`

# Unity C# コーディングスタイル

出典: https://unity.com/ja/how-to/naming-and-code-style-tips-c-scripting-unity(2026-11-15 に全文を読了)。Unity の記事は Microsoft の規約を土台にしており、最適なルールはチームで合意したものだと述べています。

## 優先順位

- `Assets/**/*.cs` では、このファイルが `.claude/rules/csharp/coding-style.md`(ECC の記述と .NET の節)より優先します。`paths` ではファイルを除外できないため、両方が読み込まれます。
- 記事はコメント、波かっこの位置、インデントを扱っていません。その空白は、C# のルールから埋めます(下の「C# のルールから埋めた部分」を参照)。

## 識別子
- 意味が分かる名前を使う。ハンガリー記法(`iCounter`、`strName`)は使わない。識別子に特殊文字・記号・Unicode 文字を使わない(Unity のコマンドラインツールと干渉することがある)。
- camelCase: ローカル変数とメソッドの引数。PascalCase: クラス、public フィールド、メソッド。snake_case と kebab-case は、記事では選択肢として挙げられているだけで、kebab-case は USS(UI Toolkit)で推奨されている。

## フィールドと変数
- `bool` 以外は名詞、`bool` は動詞の接頭辞を付ける(`isDead`、`hasDamageMultiplier`)。省略しない。1文字の名前はループと数式だけ。簡潔さより可読性を優先する。
- public フィールドは PascalCase、private フィールドは camelCase(記事の例では private フィールドに `_` を付けている。例: `_isDead`)。定数は `k_` 接頭辞 + PascalCase。`m_` と `s_` の接頭辞は選択肢として示されているだけで、最近の C# では一般的でないとされている。
- メンバーとローカル変数を区別するには `this` を使う。`private` を明示するかどうかはチームで決める(Microsoft は明示を推奨)。サブクラスが必要とするなら `protected`。
- フィールドを既定値で初期化しない(`= 0`、`= null`、`= false`)。1行に1つの変数。クラス名を繰り返さない(`Player.PlayerScore` ではなく `Player.Score`)。ふざけた名前を付けない。
- `var`: チームで決める。記事は、型が明らかなときだけ使い、型が不明確なときやループ外のプリミティブでは避ける流儀を説明している。

## 列挙型・クラス・インターフェース・メソッド
- 列挙型: 型もメンバーも PascalCase の単数名詞、接頭辞・接尾辞なし。`[Flags]` の列挙型は複数形でもよい。public の列挙型はクラスの外に置いてもよい。
- クラス: PascalCase の名詞または名詞句。`MonoBehaviour` のクラスは、クラス名と同じ名前のファイルに単独で置く。インターフェース: 大文字の `I` + 形容詞(`IKillable`、`IDamageable<T>`)。
- メソッド: 動詞で始める(`GetDirection`、`FindTarget`)。引数は camelCase。`bool` を返すメソッドは質問の形にする(`IsGameOver`、`HasStartedTurn`)。

## イベント
- 動詞句: 変化の前は現在進行形(`OpeningDoor`)、後は過去分詞(`DoorOpened`)。`System.Action` を優先し、`EventHandler` はチーム全体で選ぶ場合だけ使う。
- 発火するメソッドには `On` を付け(`OnDoorOpened`)、`?.Invoke` を使う。購読側のハンドラーには発生源の名前を含める(記事の例: `GameEvents_DoorOpened`)。カスタムの `EventArgs` は必要なときだけ(`System.EventArgs` を継承するか、読み取り専用の構造体にする)。

## 名前空間
- PascalCase、記号やアンダースコアは使わず、ドット区切りの階層(`MyApplication.AI`)にして、フォルダー構成に合わせる。ファイルの先頭で `using` ディレクティブを使う。同じクラス名が複数の名前空間にあるときは、接頭辞で修飾する。

## 読んだ範囲
記事の全体を読んだ。このリポジトリにはまだ Unity のプロジェクトがないため、`Assets/` の構成は標準的な構成の仮定である。

## C# のルールから埋めた部分
Unity の記事が扱っていない項目です。`.claude/rules/csharp/coding-style.md`(.NET の規約とプロジェクトルール)から取り、そこに書かれたとおりに適用します。
- フォーマット: スペース4つ(タブは使わない)、Allman 形式の波かっこ、1行に1つのステートメントと1つの宣言、メソッドとプロパティの定義の間に空行。
- `var`: 記事はチームの判断に任せている。右辺から型が明らかなときだけ `var` を使う。
- コメント、ファイルヘッダー、ピリオドの規則: `.claude/rules/csharp/coding-style.md` の「プロジェクトルール: コメントとファイルヘッダー」を参照。要点は、独立した行の `//` コメント、`//!` の行で書く Doxygen のファイルヘッダー、すべてのコメント行の末尾にピリオド。
