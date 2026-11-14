> 日本語訳(参照用)。原文(英語): `.claude/rules/unity/security.md`。この訳は Claude には読み込まれません。
> 適用パス(`paths`): `Assets/**/*.cs`

# Unity セキュリティ

> このファイルは [common/security.md](../common/security.md) を Unity 固有の内容で拡張します。

出典(2026-11-15 に読んだ): https://docs.unity.com/en-us/engine/current/script-reference/unityengine/playerprefs

## PlayerPrefs
- `PlayerPrefs` は、文字列・float・int を、プラットフォームのローカルストレージに**暗号化せずに**保存する。機密データを保存しない(公式ページ)。
- 保存場所: Android は `SharedPreferences`(`/data/data/<pkg>/shared_prefs/<pkg>.v2.playerprefs.xml`)、iOS は `NSUserDefaults`、Linux は `~/.config/unity3d/<Company>/<Product>`、macOS は `~/Library/Preferences/<bundle id>.plist`、Windows はレジストリ `HKEY_CURRENT_USER\Software\<Company>\<Product>`、UWP は `...\LocalState\playerprefs.dat`、Web は IndexedDB で上限 1 MB。Editor の Play モードでは、データは別のキーに保存される。
- `PlayerPrefs` を通して、シークレット、トークン、権威ある(信頼できる)ゲーム状態を読み書きしない。

## 読んだ公式ドキュメントに書かれていないこと
2026-11-15 に行った検索では、ゲームコードの保護(IL2CPP、難読化、チート対策、ローカルのセーブデータの保護、`global-metadata.dat`)に関する Unity の公式ページは見つからなかった。出てきたのは二次情報(ベンダーやコミュニティの記事)だけだった。それらは、多層防御で考えることで一致している: 権威あるゲーム状態と検証はサーバーに置く、ローカルのデータには整合性チェックや暗号化を使う、IL2CPP と難読化は保証ではなくコストを上げる手段として扱う。これらは**未検証の主張**であり、頼る前に Unity の最新のマニュアルで確認する。

## C# のセキュリティのルールから埋めた部分
`.claude/rules/csharp/security.md`(一般的な C#)から、Web サーバーに依存しない部分:
- API キー、トークン、接続文字列をソースコードにハードコードしない。本物の認証情報を、コミットされる設定ファイルに入れない。
- アプリケーションの境界で入力を検証し、不正なデータは、ゲームロジックを実行する前に拒否する。
- 生のトークン、パスワード、個人データをログに出さない。プレイヤーには安全なメッセージを返し、詳細なエラーはサーバー側のログに残す。
- 推測(Unity の公式ページにはない): `PlayerPrefs` は暗号化されず、配布したビルドは調べられるため、クライアントのビルドに含めたものは、プレイヤーが読めると考える。
- 適用しない: `csharp/security.md` の SQL インジェクションと ASP.NET の認証の部分。
