# Submitted-program constructor and rule map

This map uses the trusted, byte-identical supplied semantics. Line references
are to `/reference/reference-semantics`.

| Submitted constructor/effect | Declaration | Fixed execution rules | Proof role / disposition |
|---|---|---|---|
| `Module(...)` and statement sequence | `semantics/syntax.k:61`; `semantics/core.k:124` | `core.k:125-127` | Loads the translated module and executes statements left-to-right. Entry claims may start after this inert setup because the exact generated closure is pinned separately. |
| `ImportFrom("typing","List")` | `syntax.k:41-44` | `controls.k:35-44`, especially the `owise` no-op at line 36 | Typing-only import is semantically inert under the selected semantics. |
| `FuncDef("rolling_max",...)` | `syntax.k:53-54` | `functions.k:14-16` | Binds `rolling_max` to `closureVal(params, exact body, 0)`. The constructor comparison in `stage4-program-pinning.log` proves the claims use those exact params/body. |
| Docstring `Expr(Str(...))` | `syntax.k:13,52` | `str.k:13-17`; `controls.k:46-48` | Evaluates the ASCII string and discards it; no state/result effect. |
| `Assign(Name("result"), ListExpr())` | `syntax.k:17,41`; `controls.k:9-18` | `list.k:13-15`; `core.k:117-121`; `controls.k:9-11` | Evaluates arguments left-to-right, allocates the fresh result list at heap location 0, and binds `result` to `ref(0)`. |
| `If(Name("numbers"),...)` | `syntax.k:49`; `core.k:130-154,198-205` | `controls.k:50-54,93-97` | Name lookup precedes truth testing. Empty `ValSeq` is false; a nonempty list is true. The ref rule preserves the same behavior for concrete heap-backed arguments. |
| `numbers[0]` | `syntax.k:22,38`; `subscript.k:11,21,27-40`; `core.k:223-225` | `subscript.k:31-40`, `valSeqAt` lines 12-14, `normIdx` lines 22-23 | Object then index evaluation, optional ref dereference, and index 0 of a nonempty list. The nonempty claim's `H:Int` makes access in-bounds. |
| Assignments to `current` and `number` | `syntax.k:41`; `controls.k:9-18` | `controls.k:9-11` on the plain callee frame | Updates only the current frame map. |
| `For(Name("number"), Name("numbers"), BODY)` | `syntax.k:45`; `controls.k:65-75`; `iter.k:8` | `controls.k:69-75,104-108`; `list.k:9-10`; `tuple.k:31-41` | Iterable is evaluated once, list iteration yields left-to-right, and each yielded value is target-bound before the exact body. The proof-local `#bindTgt` specialization has the same map update and a bridge-free universal connection proof. |
| `number > current` | `syntax.k:30-32`; `operators.k:14-17`; `core.k:210` | `operators.k:15-17`; `int.k:24` | Left operand then right operand; exact mathematical integer `>`. `stepMax` uses the disjoint/exhaustive `>` and `<=` partition. |
| Inner `If` and update | `syntax.k:49`; `controls.k:50-54` | `controls.k:52-54` | Selects the update exactly when the comparison is true. |
| `result.append(current)` | `syntax.k:28-29`; `call.k:15-24`; `core.k:183-191`; `list.k:18-20,52-55` | Attribute cooling, callee/argument left-to-right evaluation, mutator dispatch, and the priority-40 heap update | Appends one integer in place and returns `noneV`, which the surrounding `Expr` discards. `rollAcc` uses the identical `valSeqConcat` singleton append. |
| Loop recursion/control | `controls.k:65-75` | `#loop`, `#iterNext`, `#loopStep`, `#loopLbl` | The candidate loop bridge matches the exact target/body and exact `Return(...) ~> #endcall` suffix and cells. `LOOP-SPEC` proves the complete transition without importing that bridge. |
| `Return(Name("result"))` and call unwind | `syntax.k:50`; `functions.k:8-11` | `functions.k:78-90`; `call.k:69-75` | Stores the returned `ref(0)`, restores caller env/stack/scope location, deletes only the callee scope, and leaves the allocated result heap object live. |

Configuration review: all 11 selected-semantics cells are accounted for.
The entry poststates constrain the result reference, exact heap payload,
allocation counter, restored scope/environment/stack/return cells, exception,
and exit code. The loop connection constrains/preserves the active
continuation, module/callee/builtin scopes, scope and heap counters, result
heap, frame stack, return, exception, and exit-code cells.
