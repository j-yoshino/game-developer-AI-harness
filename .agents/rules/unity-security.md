---
trigger: glob
description: "Unity Security"
globs: "Assets/**/*.cs"
---
<!-- generated from .claude/rules/unity/security.md. Do not edit; run scripts/sync-agent-env.py. -->
# Unity Security

> This file extends [common/security.md](../common/security.md) with Unity specific content.

Source (read on 2026-11-15): https://docs.unity.com/en-us/engine/current/script-reference/unityengine/playerprefs

## PlayerPrefs
- `PlayerPrefs` stores strings, floats and ints in the platform's local storage **without encryption**. Do not store sensitive data in it (official page).
- Locations: Android `SharedPreferences` (`/data/data/<pkg>/shared_prefs/<pkg>.v2.playerprefs.xml`); iOS `NSUserDefaults`; Linux `~/.config/unity3d/<Company>/<Product>`; macOS `~/Library/Preferences/<bundle id>.plist`; Windows registry `HKEY_CURRENT_USER\Software\<Company>\<Product>`; UWP `...\LocalState\playerprefs.dat`; Web IndexedDB, limited to 1 MB. In Play mode in the Editor the data goes to separate keys.
- Do not read or write secrets, tokens or authoritative game state through `PlayerPrefs`.

## What the official docs read do not cover
No official Unity page on game-code protection (IL2CPP, obfuscation, anti-cheat, protecting local save data, `global-metadata.dat`) was found in the searches run on 2026-11-15. Only secondary sources (vendor and community articles) turned up. They agree on a layered approach: keep authoritative game state and validation on a server, use integrity checks or encryption for local data, and treat IL2CPP and obfuscation as cost-raisers rather than guarantees. These are **unverified claims**; confirm against Unity's current manual before relying on them.

## Filled from the C# security rules
From `.claude/rules/csharp/security.md` (generic C#), the parts that are not tied to a web server:
- Never hardcode API keys, tokens or connection strings in source code, and keep real credentials out of committed configuration files.
- Validate input at the application boundary, and reject invalid data before running game logic.
- Never log raw tokens, passwords or personal data. Return safe messages to players and keep detailed errors in server-side logs.
- Inference, not from an official Unity page: because `PlayerPrefs` is unencrypted and a shipped build can be inspected, treat anything you ship in a client build as readable by the player.
- Not applicable: the SQL injection and ASP.NET authentication parts of `csharp/security.md`.
