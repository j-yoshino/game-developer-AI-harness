> 日本語訳(参照用)。原文(英語): `.claude/rules/unity/patterns.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `Assets/**/*.{cs,asmdef}`

# Unity パターン

> このファイルは [common/patterns.md](../common/patterns.md) を Unity 固有の内容で拡張します。

出典(2026-11-15 に読んだ、docs.unity.com の「current」マニュアル):
- https://docs.unity.com/en-us/engine/current/manual/scripting/managing-update-order/execution-order
- https://docs.unity.com/en-us/engine/current/manual/scripting/get-started/fundamental-unity-types/class-scriptable-object
- https://docs.unity.com/en-us/engine/current/manual/programming-environment/script-compilation/assembly-definition-files
- https://docs.unity.com/en-us/engine/current/manual/analysis/performance-memory/managed-memory/optimizing-code-managed-memory

## イベント関数の実行順序
- 異なる GameObject 間、または同じスクリプトの異なるインスタンス間で、同じイベント関数の呼ばれる順序に頼らない。親子関係があっても同様。異なるスクリプトの順序を決めたいときは、Script Execution Order を設定する。
- 物理演算は、`Physics.simulationMode`(または `Physics2D.simulationMode`)が `FixedUpdate` なら `FixedUpdate` の直後、`Update` なら `Update` の直後に実行される。`Script` なら、`Physics.Simulate` を呼んだときだけ。衝突とトリガーのコールバックは物理ステップの中で呼ばれる。
- コルーチンは、yield 命令によって再開する位置が変わる(`WaitForEndOfFrame` はフレーム終端、`WaitForFixedUpdate` は固定ステップの終端)。.NET の `Task` / `async` メソッドは Update フェーズで再開する。`Awaitable` は待機するメソッドによって再開位置が変わる。コルーチンや非同期タスクの実行順序に頼らない。
- 描画のコールバック(`OnPreCull`、`OnPreRender`、`OnPostRender`、`OnRenderImage`)は Built-in Render Pipeline 専用で、有効な Camera と同じ GameObject 上のスクリプトでだけ呼ばれる。別の場所で受け取るには、カメラのデリゲート(`onPreCull` など)を使う。
- ページの本文から分からないこと: `Awake`、`OnEnable`、`Start`、`Update`、`LateUpdate`、`OnDisable`、`OnDestroy` それぞれの呼ばれるタイミング(図でしか示されていない)。頼る前に Event functions のページを確認する。

## ScriptableObject
- GameObject にアタッチされないデータアセット。代表的な用途: 共有する不変データ(Prefab ごとにコピーせず1つのアセットを参照することでメモリを節約する)、エディターツールのデータ、アセットとして保存するランタイムデータ。
- エディターからアセットを作るには `[CreateAssetMenu(...)]` を付ける。スクリプトのファイル名はクラス名と一致させる。
- Inspector での変更は自動的に保存される。Edit モードでスクリプトから行った変更は保存されない。`EditorUtility.SetDirty` を呼ばないと、エディターを開き直したときに値が元に戻ることがある。ビルド済みのスタンドアロン Player では、アセットのデータは読み取り専用。
- ページに書かれていないこと: `CreateInstance`、`Awake` / `OnEnable` / `OnDestroy` の挙動、ビルド後のランタイムでの変更がどうなるか。

## アセンブリ定義
- スクリプトをアセンブリに分けると、依存関係が整理され、不要な再コンパイルが減り(参照をきめ細かく制御できるため)、デバッグしやすくなる。依存はアセンブリごとに設定し、条件付きの組み込みはスクリプティングシンボルで行う。
- 概要のページは、作り方、参照のルール、テスト用アセンブリを説明していない(サブページの「Creating assembly assets」と「Referencing assemblies」)。これらは読んでいない。
- 検索結果の要約にあった内容(公式ページでは読んでいないため未検証として扱う): asmdef ファイルは手で編集せず Inspector で編集する、アセンブリは GUID で参照する、明示的な参照を定義する、asmdef のないスクリプトは、いずれかの asmdef が再コンパイルされるたびに再コンパイルされる。

## メモリとプーリング
2026-11-15 に読んだサブページ(`.../managed-memory/optimizing-code-managed-memory/` の下): `reference-types`、`reusable-code`、`arrays`、および `.../managed-memory/gc-avoid-reflection`。Unity のガベージコレクターは世代別ではないため、小さな一時的な確保が大量にあると高コストになる。
- 文字列: 繰り返しの連結には `StringBuilder` を使う。ループやフレームごとのコードで連結しない。値が変わったときだけテキストを更新する。静的なテキストと動的なテキストは別の UI オブジェクトに分ける。`TMP_Text.SetText(char[])` を検討する。
- フレームごとのコードでクロージャや匿名メソッドを避ける(変数をキャプチャするとクラスのインスタンスが確保される)。値型をボックス化しない(たとえば `int` を `object` 引数に渡す)。ホットパスで `params` のオーバーロードを避ける(配列が確保される)。ボックス化は、CPU トレースの `Box(...)` や IL の `box` 命令として現れる。
- 配列: 呼び出し側が確保して渡すことで配列を再利用する。配列を返す Unity API の結果(`mesh.vertices`、`Input.touches` はアクセスのたびにコピーされる)は、ループの前にキャッシュする。確保しない版を使う(`Physics.RaycastNonAlloc`、`Animator.GetParameter`、`Renderer.GetSharedMaterials`、`Input.touchCount` + `Input.GetTouch`)。空の結果には、確保せず共有の長さ0の配列を返す。大きな配列(約1万要素を超える)には `NativeArray` を使う。
- プーリング: 頻繁に作るオブジェクトは `UnityEngine.Pool` でプールする(スレッドセーフではなく、メインスレッド専用)。`ObjectPool<T>` は create / get / release / destroy のコールバック、容量、コレクションチェック(Editor のみ、二重解放を検出する)を受け取る。`Get()` は空なら作成し、`Release()` はプールが満杯なら破棄する。取得時・解放時に状態をリセットし(コルーチンの停止、イベントの購読解除、物理・アニメーション・パーティクルのリセット)、解放した GameObject は非アクティブにする。プールは、管理オブジェクトが `DontDestroyOnLoad` のルートの下にない限り、そのシーンと一緒に破棄される。インスタンスは `OnDisable` / `OnDestroy` で解放する。`Clear` は非アクティブなインスタンスを破棄する。コレクション用のプール(`List<T>`、`HashSet<T>`、`Dictionary<TKey, TValue>`)も同じように使う。コレクションの `Clear()` はメモリを保持するため、一時的なリストはフィールドに引き上げる。
- リフレクション: Mono と IL2CPP は、すべての `System.Reflection` オブジェクトをキャッシュして決して回収せず、GC はそれらをスキャンし続ける。実行時に `Assembly.GetTypes` や `Type.GetMethods` を使わない。エディターでスキャンして結果を ScriptableObject か JSON に保存するか、型の静的配列を持つ C# ファイルを生成する。リフレクションが避けられないなら、`Activator.CreateInstance` / `Type.GetType` は、あらかじめ選んだ型のリストに限る。
- 読んだページに書かれていないこと: LINQ、`foreach`、構造体とクラスの比較、`GetComponent` のキャッシュ。

## C# のパターンから埋めていない部分
`.claude/rules/csharp/patterns.md` の項目(API レスポンスのエンベロープ、リポジトリ、オプションパターン、依存性注入)はサーバーアプリケーション向けで、読んだ Unity のページのどれも、Unity での利用を裏付けていないため、ここにはコピーしない。
