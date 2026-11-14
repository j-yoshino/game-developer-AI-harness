---
paths:
  - "Assets/**/*.cs"
---

# Unity の C# 命名規則とスタイル規則

- 出典: https://unity.com/ja/how-to/naming-and-code-style-tips-c-scripting-unity (2026-11-15 取得)
- 位置づけ: Unity 公式の記事。Microsoft の規約を土台に、最適なルールはチームの必要に合わせて決めるという立場。
- 要約であり原文の転載ではない。

## 優先順位

- `Assets/**/*.cs` では **この規約を `dotnet-csharp.md` より優先**する。食い違ったらこちらに従う。
- この記事が扱わない項目(コメント、波かっこ、インデント)は `dotnet-csharp.md` のスタイル節に従う(判断。原文は別記事を案内している)。
- `.claude/rules/ecc/csharp/` の ECC のルールと食い違う場合も、このディレクトリの規約を優先する。

## 識別子全般

- 意味が分かる名前を付ける。ハンガリー記法(`iCounter`、`strName`)は使わない。
- 識別子に特殊文字・記号・Unicode 文字を使わない(Unity のコマンドラインツールと干渉する可能性がある)。
- 大文字小文字: **camelCase** はローカル変数とメソッドの引数、**PascalCase** はクラス・public フィールド・メソッド。
- snake_case と kebab-case は、記事では選択肢として紹介されているだけ。kebab-case は USS(UI Toolkit)で推奨。

## フィールドと変数

- `bool` 以外は名詞。`bool` は動詞の接頭辞を付ける(`isDead`、`hasDamageMultiplier`)。
- 省略せず、意図が分かる名前にする。1文字の名前はループや数式だけ。簡潔さより可読性を優先する(例: `CanScrollHorizontally`)。
- public フィールドは PascalCase、private フィールドは camelCase。記事の例では private に `_` 接頭辞を付けている(`_isDead`)。
- **定数は `k_` 接頭辞 + PascalCase。**
- `m_`(メンバー)や `s_`(static)の接頭辞は、記事では選択肢として紹介されているだけで、最近の C# では一般的でないとされている。
- メンバーとローカル変数を区別したいときは `this` を使う。
- アクセス修飾子を省略するかどうかはチーム内で統一する(Microsoft の指針は private の明示を推奨)。サブクラスで使う可能性があるなら `protected`。
- フィールドを既定値で初期化しない(`= 0`、`= null`、`= false` は冗長)。
- 1行に1つの変数を宣言する。クラス名を繰り返さない(`Player` クラスの `PlayerScore` ではなく `Score`)。言葉遊びの名前を付けない。
- `var` の使い方はチームで決める。記事は、型が明らかなときだけ使い、不明確なときやループ外のプリミティブ型では避ける流儀を紹介している。

## 列挙型・クラス・インターフェース・メソッド

- 列挙型: 型名もメンバーも PascalCase、単数形の名詞。接頭辞・接尾辞は付けない。`[Flags]` のビット列挙は複数形でよい。
- クラス: PascalCase の名詞(句)。**`MonoBehaviour` 派生は1ファイルに1クラス、ファイル名をクラス名に合わせる。**
- インターフェース: 大文字の `I` + 機能を表す形容詞(`IKillable`、`IDamageable<T>`)。
- メソッド: 動詞または動詞句で始める(`GetDirection`、`FindTarget`)。引数は camelCase。`bool` を返すメソッドは問いの形にする(`IsGameOver`、`HasStartedTurn`)。

## イベント

- 名前は動詞句。状態変化の前は進行形(`OpeningDoor`)、後は過去分詞(`DoorOpened`)。
- ほとんどの場合は `System.Action`。`EventHandler` を使うかどうかはチームで統一する。
- イベントを発火するメソッドは `On` 接頭辞(`OnDoorOpened`)。購読者の有無を確認して発火する(`?.Invoke`)。
- 購読側のハンドラーは、購読対象の名前を含める(記事の例: `GameEvents_DoorOpened`)。
- カスタムの `EventArgs` は必要なときだけ。作るなら `System.EventArgs` を継承するか、読み取り専用の構造体にする。

## 名前空間

- PascalCase。記号やアンダースコアを使わない。ドット区切りで階層化する(`MyApplication.AI`、`MyApplication.UI`)。
- プロジェクトのフォルダ構成に合わせる。ファイル先頭で `using` を使い、接頭辞の繰り返しを避ける。
- 複数の名前空間に同名のクラスがあるときは、接頭辞で明示して衝突を避ける。

## 要約の範囲と未確認事項

- 日本語版の記事の全文を読んだ(Web 取得の要約を経由しており、原文の細部は未確認)。
- 記事は、コメント・波かっこの位置・インデント・EditorConfig を扱っていない。
- このリポジトリには Unity のプロジェクトがまだ無い。`Assets/` の構成は**標準的な構成の仮定**で、実際のフォルダ構成は未確認。
