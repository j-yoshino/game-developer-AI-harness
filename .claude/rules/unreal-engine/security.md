---
paths:
  - "Source/**/*.{h,cpp,cs}"
  - "Plugins/**/Source/**/*.{h,cpp,cs}"
---
# Unreal Engine Security

> This file extends [common/security.md](../common/security.md) with Unreal Engine specific content.

Sources (read on 2026-11-15):
- https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-procedure-calls-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine

## Trust and verify
- The server may trust what clients send, but must always verify that it follows the game's rules and constraints. This is the purpose of RPC validation functions (Epic's "trust and verify" policy).
- Server RPCs can carry `WithValidation` metadata. The validation function is named `<RPCName>_Validate`, returns `bool`, and takes the same parameters as the RPC. When a client calls a Server RPC, the validation function runs on the server first; if it fails, the calling client is disconnected from the server. Validate every parameter a client controls.
- Server authority: the server holds the single game state; clients only simulate an approximation and request actions through RPCs. Do not let a client decide authoritative state.

## RPC rules that matter for safety
- A Server RPC must be called by the client that owns the Actor; calling it on an Actor owned by another client is dropped. RPCs need a replicated Actor or ActorComponent with a valid owner and owning connection.
- RPCs are one-way (no return value) and mainly meant for transient, cosmetic events; use replicated properties for state. Reliable RPCs block later RPCs until acknowledged and cost bandwidth; use them sparingly. `ForceSend` costs CPU and bandwidth.
- Epic's networking overview says dedicated servers are preferable for security, fairness and reliability; a listen server gives the hosting player an advantage.

## Not covered by the pages read
No official Epic page read here describes cheat prevention, anti-cheat, secret handling or save-data protection in depth. Community sources disagree on whether `WithValidation` is mandatory in current engine versions; confirm against your engine version. Validation checks only the arguments a client sends; it does not stop a client from manipulating its own state.
