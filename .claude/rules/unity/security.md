---
paths:
  - "Assets/**/*.cs"
---
# Unity Security

> This file extends [common/security.md](../common/security.md) with Unity specific content.

Source (read on 2026-11-15): https://docs.unity.com/en-us/engine/current/script-reference/unityengine/playerprefs

## PlayerPrefs
- `PlayerPrefs` stores strings, floats and ints in the platform's local storage **without encryption**. Do not store sensitive data in it (official page).
- Locations: Android `SharedPreferences` (`/data/data/<pkg>/shared_prefs/<pkg>.v2.playerprefs.xml`); iOS `NSUserDefaults`; Linux `~/.config/unity3d/<Company>/<Product>`; macOS `~/Library/Preferences/<bundle id>.plist`; Windows registry `HKEY_CURRENT_USER\Software\<Company>\<Product>`; UWP `...\LocalState\playerprefs.dat`; Web IndexedDB, limited to 1 MB. In Play mode in the Editor the data goes to separate keys.
- Do not read or write secrets, tokens or authoritative game state through `PlayerPrefs`.

## What the official docs read do not cover
No official Unity page on game-code protection (IL2CPP, obfuscation, anti-cheat, protecting local save data, `global-metadata.dat`) was found in the searches run on 2026-11-15. Only secondary sources (vendor and community articles) turned up. They agree on a layered approach: keep authoritative game state and validation on a server, use integrity checks or encryption for local data, and treat IL2CPP and obfuscation as cost-raisers rather than guarantees. These are **unverified claims**; confirm against Unity's current manual before relying on them.
