> 日本語訳(参照用)。原文(英語): `.claude/rules/unreal-engine/patterns.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `Source/**/*.{h,cpp,cs}`、`Plugins/**/Source/**/*.{h,cpp,cs}`

# Unreal Engine パターン

> このファイルは [common/patterns.md](../common/patterns.md) を Unreal Engine 固有の内容で拡張します。

出典(2026-11-15 に読んだ):
- https://dev.epicgames.com/documentation/unreal-engine/unreal-object-handling-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine

## リフレクションとガベージコレクション
- `UCLASS` / `UPROPERTY` / `UFUNCTION` は、クラス・プロパティ・関数をエンジンに登録し、自動初期化、参照の更新、シリアル化、エディター連携、レプリケーションを可能にする。
- ガベージコレクターは、ルートセットから参照をたどり、到達できない UObject を削除する。UObject を生かしておくには、`UPROPERTY` の参照(または `UPROPERTY` のコンテナ内の参照)で保持する。
- `UPROPERTY` のない生ポインターはエンジンから見えない。回収を防がず、自動で null にもならない。オブジェクトを生かさずに有効性を確認するには `TWeakObjectPtr` を使う。
- Actor とコンポーネントは、通常レベルや親から参照されているため、特別に振る舞う。Actor は `Destroy`、コンポーネントは `DestroyComponent` で破棄する。`UPROPERTY` やコンテナで保持された参照は、破棄されると null になる。アセットの強制削除も `UPROPERTY` の参照を null にするので、アセットを扱うコードは null を許容しなければならない。
- GC の挙動(クラスタリング、実行間隔)はプロジェクト設定で構成し、ヒッチ(一時的な停止)に影響する。
- 読んだページに書かれていないこと: `NewObject`、`CreateDefaultSubobject`、`SpawnActor`、`AddToRoot`、`MarkAsGarbage` / `IsValid`、`USTRUCT`、Outer による所有。

## オブジェクトポインター
- `TObjectPtr<T>` は、生の `UObject*` メンバーの代わりに置ける型。`UPROPERTY` 付きの `TObjectPtr` は強い GC 参照になり、`UPROPERTY` がなければ GC に対して安全ではない。クック時の依存関係の追跡、GC バリア(インクリメンタルマーキング)、レプリケーションに対応する。生ポインターは、ローカル変数と一時的なものだけに使い、`UPROPERTY` 付きの生ポインターは `UPROPERTY` 付きの `TObjectPtr` に移行する。
- `TWeakObjectPtr`: 所有しない参照やキャッシュ。破棄されると null になるので、使う前に有効性を確認する。`TMap` のキーには使えない(`TObjectKey` を使う)。`TSoftObjectPtr`: パスによる参照で、アセットをロードせず、GC に影響しない。アセット参照に推奨される選択。`TStrongObjectPtr`: UObject を保持しなければならない、UObject 以外のクラスと構造体専用。GC に影響しコストも高いので、避ける。`TLazyObjectPtr` は非推奨。
- ワーカースレッドは、オブジェクトがルートされていない限り、`TObjectPtr` に直接触れてはいけない。`TWeakObjectPtr` を `Pin` して `TStrongObjectPtr` にし、有効なときだけ使う。

## レプリケーション
- サーバー権威: サーバーが唯一のゲーム状態を持ち、クライアントはその近似をシミュレートして、ローカルの Pawn から RPC でアクションを要求する。ネットワークモード: Standalone、Dedicated Server、Listen Server、Client。
- Actor(と、Actor にアタッチされたサブオブジェクト)は、`bReplicates` を設定するとレプリケートされる。生成・破棄・移動は自動でレプリケートされるが、プロパティ、コンポーネント、サブオブジェクト、RPC は自動ではなく、明示的に指定しなければならない。
- RPC より RepNotify プロパティを優先する。マルチキャストは控えめに。頻繁に呼ぶ RPC は unreliable にする。プレイヤー入力に結び付いた reliable な RPC は、キューがあふれないようにレート制限する。サーバーとクライアントの両方で動くコードを絞るには、Actor のネットワークロールと `IsLocallyControlled` を使う。ローカル専用の映像・音声を駆動する変数をレプリケートする。
- ここで扱っていないこと: Net Role と `HasAuthority` の詳細(Actor Role のドキュメントにあるが、読んでいない)、Gameplay Framework、Subsystem、デリゲート。

## C++ のパターンから埋めた部分
- UObject ではない通常の C++ の型には、`.claude/rules/cpp/coding-style.md` の言語レベルの指針(RAII、Rule of Zero、Rule of Five)が引き続き適用される。UObject の寿命は、上で説明したとおり、代わりにガベージコレクションが扱う。
- 未検証: Unreal 独自のスマートポインター(`TSharedPtr`、`TUniquePtr`)と、`cpp/patterns.md` の標準ライブラリに関する助言との関係。読んだページには書かれていない。
