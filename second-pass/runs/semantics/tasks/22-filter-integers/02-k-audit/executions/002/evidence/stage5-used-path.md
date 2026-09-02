# Material constructor/rule map

This map was reconstructed from the submitted `solution.mpy`, the
macro-expanded `FILTER-PROGRAM`, and the supplied semantics. Line references
are to the scratch copy rooted at `/tmp/audit-work/22-filter-integers`.

| Program construct/effect | Declaration and material rules | Audit result |
|---|---|---|
| Module and sequential statements | `syntax.k:56-61`; `core.k:124-127` | `#loadAll` exposes the submitted statement sequence in order. |
| `from typing import List, Any` | `syntax.k:43`; `controls.k:35-44` | The non-`math` import is discarded. This is inert because annotations were removed only by the trusted translator and the imported names are never used at runtime. |
| Function definition/binding | `syntax.k:53`; `functions.k:14-16` | Binds the exact parameter/body closure in module scope 0. |
| Function call/frame | `call.k:19-21,69-75`; `functions.k:63-66,78-90` | Callee and arguments evaluate left-to-right, a scope is allocated, `values` is bound, return stores the ref, and pop restores every relevant control cell. |
| Docstring expression | `str.k:13-17`; `controls.k:48` | The submitted ASCII docstring evaluates to `str(...)` and is discarded without state effects. |
| `result = []` | `list.k:13-15`; `core.k:117-121,186-191,217-219`; `controls.k:9-11` | Empty list construction allocates the fresh result object at heap location 0 and binds its ref. |
| `for value in values` | `controls.k:65,69-74,85`; `list.k:9-10`; `tuple.k:31-34` | The input bare-list value is iterated in order, each item is bound, and the loop continuation preserves execution order. The program never mutates the iterated input. |
| `if ...` | `syntax.k:49`; `controls.k:51-54`; `core.k:199-205` | The condition is evaluated before exactly one branch. The resulting K Bool is used directly by `truthy`. |
| `isinstance(value, int)` | `call.k:20-21,31`; `core.k:130-181`; `builtins.k:291-297` | Binding lookup is real and selects builtin `isinstance` and type object `int`. Direct K `Int` values are accepted, but K `Bool` values are rejected by `isIntV`—a material contradiction with CPython/canonical where `bool` subclasses `int`. |
| `result.append(value)` | `call.k:16,20-24,52-60`; `list.k:18-20,53-55`; `controls.k:48` | The mutator keeps the receiver ref, updates exactly its heap list by appending the selected value, returns `noneV`, and the expression statement discards it. Priority 40 preempts generic method dispatch. |
| `return result` | `syntax.k:50`; `core.k:130-154`; `functions.k:78-90` | Lookup yields the exact result ref; return removes the remaining body continuation and frame and exposes that ref to the caller. |
| Candidate proof extensions | `verification.k:6-28` | Four syntax macros only. They expand to the actual submitted program/closure/body and introduce no semantic shortcut, oracle, lemma, totality assertion, simplification, or operational bridge. |

The fixed-shape claims fully unroll. There is no loop circularity or auxiliary
claim capable of generalizing over an arbitrary `ValSeq`.
