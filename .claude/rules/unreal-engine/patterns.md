---
paths:
  - "Source/**/*.{h,cpp,cs}"
  - "Plugins/**/Source/**/*.{h,cpp,cs}"
---
# Unreal Engine Patterns

> This file extends [common/patterns.md](../common/patterns.md) with Unreal Engine specific content.

Sources (read on 2026-11-15):
- https://dev.epicgames.com/documentation/unreal-engine/unreal-object-handling-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine

## Reflection and garbage collection
- `UCLASS`/`UPROPERTY`/`UFUNCTION` register classes, properties and functions with the engine, enabling automatic initialization, reference updates, serialization, editor integration and replication.
- The garbage collector walks references from the root set and deletes unreachable UObjects. Keep a UObject alive with a `UPROPERTY` reference (or a reference inside a `UPROPERTY` container).
- A raw pointer without `UPROPERTY` is invisible to the engine: it does not prevent collection and is not nulled automatically. Use `TWeakObjectPtr` to check validity without keeping the object alive.
- Actors and components are usually referenced by the level or a parent, so they behave specially. Destroy an actor with `Destroy` and a component with `DestroyComponent`. References held through `UPROPERTY` or containers become null when they are destroyed; asset force-deletes null `UPROPERTY` references too, so asset-handling code must tolerate null.
- GC behavior (clustering, run interval) is configured in Project Settings and affects hitches.
- Not covered by the page read: `NewObject`, `CreateDefaultSubobject`, `SpawnActor`, `AddToRoot`, `MarkAsGarbage`/`IsValid`, `USTRUCT`, and Outer ownership.

## Object pointers
- `TObjectPtr<T>` is the drop-in replacement for raw `UObject*` members. A `UPROPERTY` `TObjectPtr` is a strong GC reference; without `UPROPERTY` it is not GC-safe. It supports cook dependency tracking, GC barriers (incremental marking) and replication. Use raw pointers only for locals and temporaries; migrate `UPROPERTY` raw pointers to `UPROPERTY` `TObjectPtr`.
- `TWeakObjectPtr`: non-owning reference or cache, becomes null on destruction, check validity before use; not a `TMap` key (use `TObjectKey`). `TSoftObjectPtr`: path-based reference that does not load the asset and does not affect GC; the recommended choice for asset references. `TStrongObjectPtr`: only for non-UObject classes and structs that must hold a UObject; it affects GC and is costly, so avoid it. `TLazyObjectPtr` is deprecated.
- Worker threads must not touch a `TObjectPtr` directly unless the object is rooted; pin a `TWeakObjectPtr` into a `TStrongObjectPtr` and use it only if valid.

## Replication
- Server-authoritative: the server holds the one game state, clients simulate an approximation and request actions through RPCs from their local pawn. Network modes: Standalone, Dedicated Server, Listen Server, Client.
- Actors (and subobjects attached to actors) replicate when `bReplicates` is set. Creation, destruction and movement replicate automatically; properties, components, subobjects and RPCs do not and must be marked.
- Prefer RepNotify properties over RPCs; use multicast sparingly; make frequently called RPCs unreliable; rate-limit reliable RPCs tied to player input so the queue does not overflow. Use the actor's network role and `IsLocallyControlled` to filter code that runs on both server and client; replicate the variables that drive local-only visuals and audio.
- Not covered here: Net Role and `HasAuthority` details (they are in the Actor Role documentation, not read), Gameplay Framework, Subsystems and delegates.
