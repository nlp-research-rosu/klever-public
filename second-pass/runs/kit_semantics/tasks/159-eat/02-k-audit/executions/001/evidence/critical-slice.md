# Target execution dependency slice

This is the manually reconstructed rule path from each claim's initial redex.
It is a supplement to the 930-block exhaustive inventory in
`rule-inventory.md`.

| Program construct / effect | Declaration and rules | Audit decision |
|---|---|---|
| `Call(Name("eat"), Int(...), Int(...), Int(...))` | `syntax.k:9-30`; `call.k:19-21` | The callee is evaluated before arguments. `Name("eat")` is looked up from the pinned environment, then the shared argument loop evaluates all three integer expressions left-to-right. |
| Name lookup | `core.k:130-154` | Every lookup used here is present in the pinned current scope: `eat` at scope 0 and the three parameters at the fresh callee scope. No fallback, builtin, cell, or opaque lookup rule is reached. |
| Integer literal arguments | `core.k:193-196` | `Int(I)` rewrites exactly to mathematical `I`; K `Int` is unbounded, matching Python integers on this domain. |
| Argument/list-element ordering | `core.k:183-191`, `core.k:213-219` | `#evalArgs` evaluates the head, appends its value, and recurs; it preserves left-to-right order and exact arity. |
| Closure invocation and parameter binding | `call.k:69-74`; `functions.k:63-66` | The exact pinned `closureVal` body is installed in a fresh scope 1 with parent 0. The three names receive the three values in order. The caller continuation/environment are saved. |
| `need <= remaining` | `operators.k:14-17`; `int.k:23` | The left operand is evaluated before the wrapped right operand, then the result is exactly K's `<=Int`. Neither operand is a heap reference. |
| `If` | `syntax.k:41-54`; `controls.k:50-54`; `core.k:199-205` | Strictness evaluates the condition first. Since it is already a `Bool`, `truthy` is identity and exactly one of the disjoint branches is selected. |
| Integer `+` and `-` | `syntax.k:9-30`; `operators.k:12`; `int.k:9,13` | Sequential strictness evaluates operands left-to-right; dispatch performs mathematical addition/subtraction. No overflow or coercion is present. |
| Returned list literal | `list.k:12-15`; `core.k:117-121`, `core.k:183-191`, `core.k:217-219` | Both result elements are evaluated, converted to the same ordered `ValSeq`, and allocated at fresh heap location 0. The returned value is exactly `ref(0)` and `heapLoc` advances to 1. |
| Abrupt `Return` and cleanup | `functions.k:77-90` | `Return(V)` discards the remaining body (thereby skipping the fallback return on the enough branch), records `V`, pops the sole frame, restores environment 0, removes callee scope 1, and restores `scopeLoc` to 1. |
| Exceptions and exit status | No exercised rule writes either cell | The initial/post `NoExc` and exit code 0 are preserved. Arithmetic is only `+`, `-`, and `<=`, so no modeled exceptional operation is possible. |

The only source attributes that synthesize evaluation rules on this path are
`strict(1)` for `If`, `strict` for `Return`, and `seqstrict(2,3)` for `BinOp`.
`Compare` uses the two explicit contexts in `operators.k`. The inventory found
no local `simplification` or `functional` declarations and no proof-local rule
at all.
