# Target construct-to-semantics map

This map was rebuilt from the trusted semantics and the scratch source copy.
Line references identify the complete rule groups in
`/reference/reference-semantics`.

| Submitted constructor/operation | Declaration and fixed rules | Static assessment |
|---|---|---|
| `Module`, statement lists | `semantics/syntax.k:61`; `semantics/core.k:124-127` | `#loadAll` exposes the exact statement sequence; sequencing is left-to-right and consumes `.Stmts`. |
| `Import("math")` | `semantics/syntax.k:42`; `semantics/float.k:58-67` | Imports are a no-op in the reduced semantics. For this program that is observationally contained: the only use, `math.ceil`, is intercepted syntactically before `math` lookup. |
| `FuncDef`, `Params` | `semantics/syntax.k:53-60`; `semantics/functions.k:14-16` | Binds the exact body and parameter list in module scope as `closureVal`. |
| Function call/return | `semantics/call.k:18-32,69-75`; `semantics/functions.k:62-90` | Callee lookup precedes left-to-right arguments; a fresh local frame is pushed, the parameter is bound, and `Return` restores the saved caller continuation and state. |
| `Assign` and `Int` literals | `semantics/syntax.k:9,41`; `semantics/core.k:194`; `semantics/controls.k:8-31` | RHS strictness precedes writes. The higher-priority cell/ref variants are inapplicable to this plain four-key local frame. |
| `Name` | `semantics/syntax.k:12`; `semantics/core.k:129-181` | Lookup starts at the current local scope and walks to module/builtins. Every target local is bound before use. |
| `For(Name("number"), Name("lst"), ...)` | `semantics/syntax.k:45`; `semantics/controls.k:62-74`; `semantics/list.k:8-10`; `semantics/tuple.k:30-41` | The input list is evaluated once; each head is bound to `number`; the tail is retained in `#loop`. The submitted body does not mutate the iterated list, so the reduced semantics' snapshot limitation is irrelevant. |
| `Call(Attribute(Name("math"),"ceil"), number)` | `semantics/syntax.k:28-29`; `semantics/float.k:58-67,90-95`; generic route `semantics/call.k:18-21` | Priority 40 preempts generic attribute lookup, evaluates the one argument once, then returns fixed primitive `ceilF(V)`. On intended `Int`/finite-`Float` inputs its concrete equations are `I` and `Float2Int(ceilFloat(F))`. Symbolically the theorem is interpretation-parametric in this supplied external primitive. |
| `BinOp("*", rounded, rounded)` | `semantics/syntax.k:15`; `semantics/operators.k:10-17`; `semantics/int.k:9-17` | Sequential strictness evaluates both reads; both are the same integer written by `math.ceil`; integer multiplication is exact and unbounded. |
| `AugAssign(total,"+",...)` | `semantics/syntax.k:44`; `semantics/controls.k:20-31`; `semantics/int.k:9-17` | RHS evaluates first; the current integer accumulator and integer square are added and written to the same local map. |
| `Return(total)` | `semantics/syntax.k:50`; `semantics/functions.k:77-90` | Strict evaluation yields the local integer, then `#pop` returns it to the saved entry continuation. |
| `solutionProgram` | scratch `program.k:7-24` | Nullary, total definitional constant. Independent 122-token constructor comparison equals trusted regenerated `solution.mpy`. |
| `sumCeilSquares` | scratch `verification.k:10-14` | Structural, disjoint, exhaustive recursion over `ValSeq`; it names the postcondition and does not replace operational execution. |

The target uses no allocation, list mutation, exception, output, sort, digest,
dictionary, string, comprehension, slicing, or closure-cell behavior. The
proof configuration nevertheless keeps every fixed cell, so these cells cannot
be silently fabricated by a local proof rule.
