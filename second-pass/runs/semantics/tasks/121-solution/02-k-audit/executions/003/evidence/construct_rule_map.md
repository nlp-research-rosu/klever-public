# Submitted-constructor to semantics map

This map is based on the byte-identical trusted-translator output
`/tmp/audit-work/reconstruction/solution.mpy`. Locations below refer to the
trusted supplied semantics copied into clean scratch.

| Submitted/proof constructor | Declaration/evaluation order | Operational rules exercised |
|---|---|---|
| `Module(Stmts)` and `FuncDef("solution", Params("lst"), Body)` | `semantics/syntax.k:53,56-61`; module sequencing in `semantics/core.k:124-127` | Concrete module loading binds the closure through `semantics/functions.k:14-16`. The entry proof instead starts from `solutionClosure`; expanded-KAST comparison proves that closure has the identical params/body/environment. |
| `Call(solutionClosure, (list(VS), .Exprs))` | `semantics/syntax.k:28`; callee before left-to-right args through `semantics/call.k:19-21` and `semantics/core.k:185-191` | Closure frame creation/call at `semantics/call.k:69-75`; param binding at `semantics/functions.k:63-66`. |
| `Assign(Name(...), RHS)` | `semantics/syntax.k:41 [strict(2)]` | Current-scope write at `semantics/controls.k:9-11`; cell rule `:12-18` is guard-disjoint and inactive. |
| `Name("lst"|"total"|"even_position"|"value")` | `semantics/syntax.k:12` | Lexical lookup at `semantics/core.k:130-154`; loop-target binding at `semantics/tuple.k:31-41`. |
| `Int(0|2)` | `semantics/syntax.k:9` | Literal cooling at `semantics/core.k:194`. K `Int` is unbounded, matching CPython integers for the used arithmetic. |
| `Bool(true)` | `semantics/syntax.k:11` | Literal cooling at `semantics/core.k:195`; truthiness at `semantics/core.k:200`. |
| `For(Name("value"), Name("lst"), Body)` | `semantics/syntax.k:45 [strict(2)]`, so the iterable is evaluated once | `semantics/controls.k:69-74`; list iterator cases `semantics/list.k:9-10`; target binding `semantics/tuple.k:31-41`; re-entry `semantics/controls.k:85`. |
| `If(Name("even_position"), Then, .Stmts)` | `semantics/syntax.k:49 [strict(1)]` | Truth-value dispatch at `semantics/controls.k:51-54` and Bool truthiness at `semantics/core.k:200`. |
| `BinOp("%", value, Int(2))` | `semantics/syntax.k:15 [seqstrict(2,3)]`, enforcing left-to-right operand evaluation | Generic dispatch `semantics/operators.k:12`; fixed Int case and Python modulo at `semantics/int.k:15,19-20`; proof-local exact bridge `verification.k:52-54`. |
| `BinOp("*", value, remainder)` | Same `seqstrict` declaration | Generic dispatch `semantics/operators.k:12`; fixed Int multiplication `semantics/int.k:14`; proof-local exact bridge `verification.k:58-60`. |
| `BinOp("+", total, product)` | Same `seqstrict` declaration | Generic dispatch `semantics/operators.k:12`; fixed Int addition `semantics/int.k:9`; proof-local exact bridge `verification.k:55-57`. |
| `UnaryOp("not", even_position)` | `semantics/syntax.k:14 [strict(2)]` | Generic dispatch `semantics/operators.k:10`; Bool/truthiness negation `semantics/bool.k:8`. |
| `Return(Name("total"))` | `semantics/syntax.k:50 [strict]` | Return records the value and discards only the callee suffix at `semantics/functions.k:78-81`; frame pop restores caller control/state at `:85-90`. |

No list allocation, mutation, I/O, exception, float, string, dictionary, sort,
opaque digest, or other supplied-semantics construct is reachable from the
entry claim. The input `list(VS)` is the explicitly supported unboxed,
read-only claim input described in `semantics/core.k:62-67`.
