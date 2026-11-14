> 日本語訳(参照用)。原文(英語): `.claude/rules/unreal-engine/security.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `Source/**/*.{h,cpp,cs}`、`Plugins/**/Source/**/*.{h,cpp,cs}`

# Unreal Engine セキュリティ

> このファイルは [common/security.md](../common/security.md) を Unreal Engine 固有の内容で拡張します。

出典(2026-11-15 に読んだ):
- https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-procedure-calls-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine

## 信頼して検証する
- サーバーはクライアントから送られた情報を信頼してよいが、それがゲームのルールと制約に従っているかを、常に検証しなければならない。これが RPC の検証関数の目的(Epic の「trust and verify(信頼して検証する)」方針)。
- Server RPC には、`WithValidation` のメタデータを付けられる。検証関数の名前は `<RPCName>_Validate` で、`bool` を返し、RPC と同じパラメーターを取る。クライアントが Server RPC を呼ぶと、先にサーバーで検証関数が実行され、失敗すると呼び出したクライアントはサーバーから切断される。クライアントが制御するパラメーターは、すべて検証する。
- サーバー権威: サーバーが唯一のゲーム状態を持ち、クライアントは近似をシミュレートして、RPC でアクションを要求するだけ。権威ある状態を、クライアントに決めさせない。

## 安全のために重要な RPC の規則
- Server RPC は、その Actor を所有するクライアントが呼ばなければならない。別のクライアントが所有する Actor に対して呼ぶと、破棄される。RPC には、有効なオーナーと所有する接続を持つ、レプリケートされた Actor または ActorComponent が必要。
- RPC は一方向(戻り値なし)で、主に一時的な演出のイベント向け。状態にはレプリケートされたプロパティを使う。reliable な RPC は、確認応答があるまで後続の RPC を止め、帯域も使うので、控えめに使う。`ForceSend` は CPU と帯域を使う。
- Epic のネットワークの概要は、専用サーバー(dedicated server)が、セキュリティ、公平性、信頼性の面で望ましいと述べている。リッスンサーバー(listen server)は、ホストするプレイヤーに有利になる。

## 読んだページに書かれていないこと
ここで読んだ Epic の公式ページには、チート対策、アンチチート、シークレットの扱い、セーブデータの保護について、踏み込んだ説明はない。現行のエンジンバージョンで `WithValidation` が必須かどうかは、コミュニティの情報源の間で意見が分かれている。使うエンジンのバージョンで確認すること。検証が確かめるのは、クライアントが送る引数だけで、クライアントが自分の状態を操作することは防げない。

## C++ のセキュリティのルールから埋めた部分
`.claude/rules/cpp/security.md` と Core Guidelines の、言語レベルの安全性のルールは、Unreal の C++ にも適用される:
- 変数は必ず初期化する(ES.20)。符号付き整数のオーバーフローを避ける(ES.103)。null やダングリングポインターを決して参照外ししない(ES.65)。キャストを避け、避けられない場合を除き `reinterpret_cast` を使わない(ES.48、ES.49)。
- `strcpy`、`strcat`、`sprintf` を避ける(`cpp/security.md` より)。未検証: エンジンが推奨する代替手段。読んだページには書かれていない。
- UObject には、`cpp/security.md` のスマートポインターの助言ではなく、`patterns.md` のポインター型を使う。
- Unreal では未検証: `cpp/security.md` が挙げる AddressSanitizer/UBSan と、`clang-tidy` / `cppcheck` のコマンド。
