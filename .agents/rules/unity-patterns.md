---
trigger: glob
description: "Unity Patterns"
globs: "Assets/**/*.cs, Assets/**/*.asmdef"
---
# Unity Patterns

> This file extends [common/patterns.md](../common/patterns.md) with Unity specific content.

Sources (read on 2026-11-15, docs.unity.com "current" manual):
- https://docs.unity.com/en-us/engine/current/manual/scripting/managing-update-order/execution-order
- https://docs.unity.com/en-us/engine/current/manual/scripting/get-started/fundamental-unity-types/class-scriptable-object
- https://docs.unity.com/en-us/engine/current/manual/programming-environment/script-compilation/assembly-definition-files
- https://docs.unity.com/en-us/engine/current/manual/analysis/performance-memory/managed-memory/optimizing-code-managed-memory

## Event function order
- Do not rely on the order of the same event function between different GameObjects or between instances of the same script, even in a parent/child relationship. To order different scripts, set Script Execution Order.
- Physics runs right after `FixedUpdate` when `Physics.simulationMode` (or `Physics2D.simulationMode`) is `FixedUpdate`, right after `Update` when it is `Update`, and only when you call `Physics.Simulate` when it is `Script`. Collision and trigger callbacks run inside the physics step.
- Coroutines resume at a point that depends on the yield instruction (`WaitForEndOfFrame` at frame end, `WaitForFixedUpdate` at the end of the fixed step). .NET `Task`/`async` methods resume in the Update phase; `Awaitable` resumes depending on the awaited method. Do not depend on the execution order of coroutines or async tasks.
- Render callbacks (`OnPreCull`, `OnPreRender`, `OnPostRender`, `OnRenderImage`) are Built-in Render Pipeline only and are called only on scripts on the same GameObject as an enabled Camera; use the camera delegates (`onPreCull`, ...) to receive them elsewhere.
- Not available from the page text: the per-function timing of `Awake`, `OnEnable`, `Start`, `Update`, `LateUpdate`, `OnDisable`, `OnDestroy` (it is shown only in a diagram). Check the Event functions page before relying on it.

## ScriptableObject
- A data asset that is not attached to a GameObject. Typical uses: shared immutable data (one asset instead of a copy per prefab saves memory), editor tool data, runtime data stored as an asset.
- Add `[CreateAssetMenu(...)]` to create assets from the editor; the script file name must match the class name.
- Changes made in the Inspector are saved automatically. Changes made from scripts in Edit mode are not: call `EditorUtility.SetDirty`, or values can revert after reopening the editor. In a built standalone Player the asset data is read-only.
- Not covered by the page: `CreateInstance`, `Awake`/`OnEnable`/`OnDestroy` behavior, and what happens to runtime changes after a build.

## Assembly definitions
- Splitting scripts into assemblies organizes dependencies, reduces unnecessary recompilation (finer control of references) and makes debugging easier. Dependencies are set per assembly; conditional inclusion uses scripting symbols.
- The overview page does not describe how to create them, the reference rules or test assemblies (sub-pages "Creating assembly assets" and "Referencing assemblies"); these were not read.
- Search-result summaries (not read on the official page, treat as unverified): edit asmdef files in the Inspector rather than by hand; reference assemblies by GUID; define explicit references; scripts without an asmdef recompile whenever any asmdef recompiles.

## Memory and pooling
Sub-pages read on 2026-11-15 (under `.../managed-memory/optimizing-code-managed-memory/`): `reference-types`, `reusable-code`, `arrays`; and `.../managed-memory/gc-avoid-reflection`. Unity's garbage collector is not generational, so many small temporary allocations are expensive.
- Strings: use `StringBuilder` for repeated concatenation; do not concatenate in loops or per-frame code; update text only when the value changes; keep static and dynamic text in separate UI objects; consider `TMP_Text.SetText(char[])`.
- Avoid closures and anonymous methods in per-frame code (capturing a variable allocates a class instance). Do not box value types (for example passing an `int` to an `object` parameter). Avoid `params` overloads in hot paths (they allocate an array). Boxing shows up as `Box(...)` in CPU traces or the `box` IL instruction.
- Arrays: reuse arrays by letting the caller allocate and pass them in; cache array-valued Unity API results (`mesh.vertices`, `Input.touches` copy on every access) before loops; use non-allocating variants (`Physics.RaycastNonAlloc`, `Animator.GetParameter`, `Renderer.GetSharedMaterials`, `Input.touchCount` + `Input.GetTouch`); return a shared zero-length array instead of allocating an empty one; use `NativeArray` for large arrays (more than about 10,000 elements).
- Pooling: pool frequently created objects with `UnityEngine.Pool` (not thread-safe, main thread only). `ObjectPool<T>` takes create/get/release/destroy callbacks, capacities and a collection check (Editor only, catches double release). `Get()` creates when empty; `Release()` destroys when the pool is full. Reset state when getting or releasing (stop coroutines, unsubscribe events, reset physics, animations and particles) and deactivate released GameObjects. A pool is destroyed with its scene unless its manager sits under a `DontDestroyOnLoad` root; release instances in `OnDisable`/`OnDestroy`; `Clear` destroys inactive instances. Collection pools (`List<T>`, `HashSet<T>`, `Dictionary<TKey, TValue>`) work the same way; `Clear()` on a collection keeps its memory, so hoist temporary lists into fields.
- Reflection: Mono and IL2CPP cache every `System.Reflection` object and never collect them, and the GC keeps scanning them. Avoid `Assembly.GetTypes` and `Type.GetMethods` at run time; scan in the Editor and store results in a ScriptableObject or JSON, or generate a C# file with a static type array; if reflection is unavoidable, limit `Activator.CreateInstance`/`Type.GetType` to a preselected list of types.
- Not covered by the pages read: LINQ, `foreach`, structs versus classes, `GetComponent` caching.

## Not filled from the C# patterns
The items in `.claude/rules/csharp/patterns.md` (API response envelope, repository, options pattern, dependency injection) target server applications, and none of the Unity pages read supports them for Unity, so they are not copied here.
