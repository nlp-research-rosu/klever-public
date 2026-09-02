# Submitted-program construct and rule map

This map was reconstructed from `solution.mpy`, `spec.k`, the trusted supplied
semantics, and the fresh proof. Candidate build products and reports were not
used.

| Submitted construct | Declaration | Rules on the proof path | Audit result |
|---|---|---|---|
| `Module` / `FuncDef` / `Params` | `semantics/syntax.k:53,57,61` | A normal module run uses `core.k:125-127` and `functions.k:14-16`. The entry claim instead installs the exact translated closure and invokes it, so these load rules are not used by `kprove`. | Acceptable function-entry harness; body and binding are pinned exactly. |
| `Call` | `semantics/syntax.k:28` | `call.k:20-21,24,31,38-46,63-67,69-74`; shared argument loop `core.k:185-191`. | Callee before arguments; arguments left-to-right; closure frame/state effects preserved. |
| `Name` | `semantics/syntax.k:12` | `core.k:130-154`; builtins scope `core.k:157-181`. | Resolves the pinned function, parameter/local, and real supplied builtins binding. |
| `Assign(Name("order"), ...)` | `semantics/syntax.k:41` with strict RHS | `controls.k:9-11`. | Writes the fully evaluated tuple to the callee scope. |
| `TupleExpr` | `semantics/syntax.k:21` | `tuple.k:14-16` plus the shared argument loop. | Constructs the ten strings in source order. |
| `Str` | `semantics/syntax.k:13` | `str.k:13-17`. | All literals are ASCII and reduce to their exact code sequences. |
| `Attribute` | `semantics/syntax.k:29` with strict receiver | `call.k:16`; non-mutating heap-object dereference `call.k:56-67`. | Produces the exact bound `split`, tuple `index`, and string `join` methods. |
| `KwArg("key", ...)` | `semantics/syntax.k:25` | `core.k:95-102`. | Preserves the evaluated key as a tagged argument. |
| `numbers.split()` | `Call`/`Attribute` | `methods.k:72-86`, allocation `core.k:117-121`, helpers `list.k:18-20`. | Whitespace split is deterministic and allocates heap object 0. |
| `sorted(..., key=order.index)` | builtin entry in `core.k:172` | symbolic declaration `sort.k:49`; dispatch/allocation `sort.k:61-62`; allocation `core.k:117-121`. | The call and allocation execute, but the stable keyed sort is the supplied opaque `sortKeyVS` trust boundary. |
| `" ".join(...)` | `Call`/`Attribute` | dispatch `call.k:24`; method and equations `methods.k:26-31`. | Returns the join of the opaque sorted sequence; element-string preservation is not proved in K. |
| `Return` | `semantics/syntax.k:50` with strict expression | `functions.k:78-90`. | Constrains the returned value, restores the caller, deletes the callee scope, and resets stack/return state. |

The claim also fixes `<env>`, `<scopes>`, `<scopeLoc>`, `<heap>`, `<heapLoc>`,
`<stack>`, `<ret>`, `<exc>`, and `<exit-code>`. There are no loop/helper claims.
