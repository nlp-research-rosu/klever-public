# `solution.mpy` construct-to-semantics map

The declaration inventory for every supplied and proof-local K file is
`k-inventory.json`. This map narrows that exhaustive inventory to constructs
reachable from the submitted `solution.mpy`.

| Submitted construct | Declaration | Operational path used by the proof |
|---|---|---|
| `Module` / statement list | `semantics/syntax.k:56-61` | `core.k:124-127` expands `#loadAll` and sequences statements. |
| `FuncDef`, `Params` | `semantics/syntax.k:53-60` | `functions.k:14-16` installs `closureVal` in the current scope. |
| `Expr(Str(...))` | `semantics/syntax.k:13,52` | `str.k:13-17` converts the ASCII docstring; `controls.k:48` discards the value without effects. |
| `Assign(Name(...), ...)` | `semantics/syntax.k:12,41` | RHS strictness evaluates first; `controls.k:9-18` writes the active local scope (the cell-write priority case is inapplicable to this plain frame). |
| `Subscript(Name("nums"), Int(0))` | `semantics/syntax.k:9,12,22,38` | `core.k:131-154` looks up `nums`; `subscript.k:27-41` evaluates object then index and uses `valSeqAt`; proof-local `verification.k:24-25` supplies the exact symbolic head instance. |
| `For(Name("value"), Name("nums"), body)` | `semantics/syntax.k:45` | Strict iterable lookup; `controls.k:69-74` enters `#loop`; `list.k:9-10` provides iterator steps; target binding comes from `tuple.k`; proof-local iterator instances preserve the `IntSeq` witness. |
| `BinOp("+", ...)` | `semantics/syntax.k:15` | `seqstrict(2,3)` enforces left-to-right operand evaluation; `operators.k:12` dispatches; `int.k:9` performs mathematical integer addition. |
| `Compare(..., CmpOp("<", ...))` | `semantics/syntax.k:30-32` | `operators.k:15-17` evaluates left then right and dispatches; `int.k:22` returns the integer comparison Boolean. |
| `If` | `semantics/syntax.k:49` | Strict condition evaluation; `controls.k:51-54` applies `truthy`; comparison results are Boolean, so `core.k:200` is the applicable truthiness equation. |
| `Return(Name("smallest"))` | `semantics/syntax.k:50` | Name lookup, then `functions.k:78-90` stores the value, discards the remaining callee computation, pops the exact call frame, restores the caller, and yields the value to the saved continuation. |
| Direct closure invocation in `FUNCTION-SPEC` | proof-internal `#applyK` | `call.k:69-74` allocates a plain local frame, binds `nums`, executes the exact macro-expanded body, and restores the empty caller frame. |

Configuration cells relevant to this program are declared in `core.k:49-60`.
The function changes only its transient local scope and return/frame cells; it
does not mutate the supplied list, allocate objects, emit output, or raise a
modeled exception on the nonempty integer-list domain. The final claim pins all
configuration cells and therefore requires the local frame to be removed,
`ret` reset to `noRet`, the stack emptied, the heap unchanged, and the result
left in `<k>`.
