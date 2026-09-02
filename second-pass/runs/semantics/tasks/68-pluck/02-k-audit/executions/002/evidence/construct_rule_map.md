# Submitted-term construct map

All locations are in the scratch copy built from the trusted supplied
semantics. K-generated heating/cooling comes from the cited `strict` or
`seqstrict` attributes; those attributes are inventoried in
`rule_inventory.md`.

| Submitted constructor / effect | Declaration | Operational path used by the entry claim | Review |
|---|---|---|---|
| `Module` and statement sequence | `reference-semantics/semantics/syntax.k:56-61` | `core.k:124-127` (`#loadAll`, left-to-right statement sequence, empty sequence) | Exact module body executes. |
| `FuncDef`, `Params` | `syntax.k:53-60` | `functions.k:14-16` installs `closureVal(PNS,BODY,L)` in module scope | Binding and full body are retained. |
| `Call(Name("pluck"), list(VS))` | `syntax.k:28` | `call.k:20-21` evaluates the callee, `core.k:189-191` evaluates arguments left-to-right, `call.k:69-75` creates the frame | The call resolves the installed module binding; no name-based interception exists. |
| Parameter binding and frame return | `functions.k:8-11` | `functions.k:63-66`, `78-90`; `call.k:69-75` | `arr` is bound to the exact bare `list(VS)` value; return value, caller continuation, environment, frame map, and stack are handled. Heap allocation is monotone and therefore survives return. |
| `Assign(Name(...), rhs)` | `syntax.k:41 [strict(2)]` | `controls.k:9-11` after RHS evaluation | Writes only the current scope. Cell-specialized rule is guarded and cannot match this plain frame. |
| `Name` | `syntax.k:12` | `core.k:130-154` | Lookup begins at current environment and walks parents. Every used local is bound before lookup. |
| `Int`, unary `-` | `syntax.k:9,14 [strict(2)]` | `core.k:194`; `operators.k:10`; `int.k:7` | Produces mathematical K integers, including the `-1` sentinel. |
| `BinOp("%",...)` | `syntax.k:15 [seqstrict(2,3)]` | `operators.k:12`; `int.k:15,19-20` | Left-to-right operands; divisor is the fixed nonzero integer 2. |
| `BinOp("+",...)` from `AugAssign` | same declaration | `controls.k:20-23`; `int.k:9` | Reads the bound integer index and increments it by one. |
| `Compare`, `CmpOp("=="/"<")` | `syntax.k:30-32` | `operators.k:15-17`; `int.k:22-27` | Left operand then wrapped right operand; exact integer comparisons. |
| `If` | `syntax.k:49 [strict(1)]` | `controls.k:51-54`; `core.k:199-205` | Only the selected branch executes. Conditions here are Bool results. |
| `For` over `list(VS)` | `syntax.k:45 [strict(2)]` | `controls.k:69-74`; `list.k:9-10`; target binding in `tuple.k:31-41` | Iterable is evaluated once; each head binds `value`, body runs, then the loop continuation advances. The proof-local iterator specialization is reviewed separately. |
| `AugAssign(Name("index"),"+",Int(1))` | `syntax.k:44 [strict(3)]` | `controls.k:20-23` | Generic integer rule applies; ref-specialized rule is inapplicable. |
| `Return` | `syntax.k:50 [strict]` | `functions.k:78-90` | Abruptly discards the remaining function-body continuation, records the value, restores caller state, and leaves escaped heap objects allocated. |
| `ListExpr()` / `ListExpr(best,index)` | `syntax.k:17` | `list.k:13-15`; `core.k:183-191,117-121` | Elements evaluate left-to-right and the result is allocated at fresh heap location 0, exactly as constrained by the entry postcondition. |
| Configuration and observable cells | `core.k:44-60` | All entry-claim cells are explicit at `spec.k:93-145` | Entry proves `k=ref(0)`, exact module binding, heap result, heap counter, empty stack, `noRet`, `NoExc`, and exit code 0. |

No submitted constructor relies on float, string, dict, set, slice, sorting,
hashing, comprehension, assertion, or concrete-only rules. Sort-disjoint rules
in those modules cannot overlap the integer/list redexes above.
