# Target-path semantic map and static assessment

This map supplements the 1,030-item exhaustive inventory. Line references are
to the clean copy under `/tmp/audit-work/reconstruction/reference-semantics`.

| Submitted constructor/operation | Declaration and rules | Static assessment |
|---|---|---|
| `Module`, `Stmts`, `FuncDef`, `Params` | `semantics/syntax.k:53,56-61`; `semantics/core.k:124-127`; `semantics/functions.k:14-16` | The module is sequenced left-to-right; the function body is stored unchanged in a closure bound in module scope 0. |
| Docstring `Expr(Str(...))` | `syntax.k:13,52`; `str.k:13-17`; `controls.k:48` | The ASCII source literal becomes its exact code sequence and is discarded as an expression statement. |
| `Assign(out,"")`, `Assign(c,"")` | `syntax.k:41`; `controls.k:9-11` | Strict RHS evaluation precedes a write to the current function scope. No cell/heap priority rule can match this plain frame. |
| `For(c,s,body)` | `syntax.k:45`; `controls.k:65,69-74`; `str.k:8-10`; `tuple.k:31-34` | The iterable is evaluated once, `#iterNext` removes one `iCons`, yields a one-code-point `str`, binds `c`, runs the body, and returns to the exact `#loop` continuation. |
| `If(and(...),then,else)` | `syntax.k:49`; `bool.k:27-36`; `controls.k:51-54`; `core.k:199-205` | `and` heats only the first operand and short-circuits; both comparisons yield Bool, and the branch selects exactly one body. |
| `Call(Name("ord"),c)` | `syntax.k:28`; `core.k:130-181,185-191`; `call.k:19-21,31`; `builtins.k:187` | Lookup selects the fixed builtin binding after local/module misses, evaluates the one argument left-to-right, and returns the sole code from the one-character string. No math/hashlib interception matches. |
| Integer literals/comparisons | `syntax.k:9,30-32`; `core.k:194,210`; `operators.k:15-17`; `int.k:31-34` | The guards compute `C>=97` and `C<=122` with ordinary mathematical integer order. |
| ROT4 arithmetic `((C-97+4)%26)+97` | `syntax.k:15`; `operators.k:12`; `int.k:9,22,24,28-29` | Evaluation is left-to-right. On the guarded domain, the modulo dividend is 4..29 and the result is 97..122. `pyMod` is therefore the CPython result. |
| `Call(Name("chr"),I)` | call path above; `builtins.k:188-189` | The only reachable `I` is 97..122, wholly inside the supplied model's ASCII guard, and yields the correct one-character string. |
| `AugAssign(out,"+",value)` | `syntax.k:44`; `controls.k:20-23`; `str.k:20-24` | The RHS evaluates first, scope lookup reads the existing `str`, and `seqConcat` appends exactly one code. The heap-ref priority leg is inapplicable. |
| `Return(out)` and call frame | `syntax.k:50`; `call.k:69-74`; `functions.k:63-66,78-90` | The actual closure body runs in a fresh scope, the argument is bound, return discards the remaining callee continuation, the frame is popped, and the value resumes at the caller assignment with normal `ret`/stack state restored. |
| Entry configuration/state | `core.k:49-60,157-181` | Module scope, builtins scope, allocator cells, stack, return state, exception state, and heap match the claim. String operations allocate neither heap nor scope entries beyond the call frame. |

## Proof-local extensions

`verification.k` has five `[function,total]` declarations and nine equations:

- `rot4Code`: one unguarded mathematical equation.
- `encryptedChar`: three pairwise-disjoint and exhaustive guards (`C<97`,
  `97<=C<=122`, `C>122`).
- `encryptFold`: empty/cons constructor partition, descending on its second
  `IntSeq`.
- `encryptResult`: one wrapper equation.
- `finalLoopChar`: empty/cons constructor partition, descending on its
  `IntSeq`.

None matches an operational `<k>` term. There is no priority, simplification,
`[concrete]`, `[owise]`, fresh variable, opaque/no-evaluator symbol, or oracle.
Their link to execution is established by `SPEC.encrypt-loop`, which takes one
fixed-semantics iteration before circular reuse. `SPEC.encrypt-entry` then
executes the exact loaded function and uses that loop claim.

## Priorities, overlaps, and opaque items

- The proof-local theory has no priority or overlapping equation.
- Fixed-semantics priority rules for heap refs, closure cells, math calls,
  hashlib calls, list mutation, sorting, and slicing have guards or constructor
  heads that do not match this target.
- The generic call rule is `[owise]`; for `encrypt`, `ord`, and `chr`, no
  syntactic interception rule matches, so ordinary lookup/call dispatch runs.
- The 30 opaque supplied-semantics inventory items are float, sorting, and MD5
  abstractions. No opaque symbol occurs in the submitted term, the two claims,
  a proof-local RHS, or a target residual.
- `MPY-CONCRETE` is not imported by `VERIFICATION`; its 32 inventoried items
  cannot contribute to `kprove`.

No inventoried rule enables a false conclusion for any intended string input
on this target path.
