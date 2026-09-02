# Used constructor-to-semantics map

This map is for the trusted-regenerated `solution.mpy` and the entry execution
in `SPEC.make-palindrome-entry`. Every cited fixed-semantics file below was
recursively byte-identical in `/candidate/reference-semantics` and
`/reference/reference-semantics`.

| Program constructor/effect | Declaration | Rules or evaluation mechanism used | Audit conclusion |
|---|---|---|---|
| `Module`, statement lists | `semantics/syntax.k:56,61` | `semantics/core.k:124-127` loads the module and sequences statements left-to-right | Exact module body is loaded; no statement is bypassed. |
| `FuncDef`, `Params` | `semantics/syntax.k:53,57` | `semantics/functions.k:14-16` stores a closure in the current scope | The two submitted bindings are installed at module location 0. |
| `Call(Name("make_palindrome"), ...)` | `semantics/syntax.k:28` | `semantics/call.k:20-21`, `core.k:189-191`, and `call.k:69-74` evaluate callee then arguments, allocate a frame, and execute its body | Binding, argument order, body, continuation, frame, and environment are preserved. |
| Parameter binding and return | `semantics/functions.k:8-11` | `functions.k:63-66,78-90` binds `string`, records `retV`, pops exactly one frame, restores continuation/environment, and removes the local scope | Entry post-state correctly requires an empty stack, `env=0`, `scopeLoc=1`, and no return marker. |
| `Name` reads | `semantics/syntax.k:12` | `semantics/core.k:130-154` performs lexical lookup through the local then module scope | All locals and the function binding resolve through the fixed scope maps; cell-specific priority rules are disabled because these are plain frames. |
| `Str`, `Bool` | `semantics/syntax.k:11,13` | `semantics/str.k:13-17` and `core.k:194-196` produce values | All source literals are ASCII; arbitrary input is already `str(S:IntSeq)`, so the ASCII literal parser does not narrow the input domain. |
| `Expr` docstrings | `semantics/syntax.k:52` | strict evaluation plus `semantics/controls.k:46-48` discards the resulting string | Docstrings are semantically inert and still execute. |
| `Assign` | `semantics/syntax.k:41` with strict RHS | `semantics/controls.k:9-18` updates the active local map | The plain-frame rule is selected; no heap or cell write occurs. |
| `For` and string iteration | `semantics/syntax.k:45`; loop protocol in `controls.k:65-74` | `semantics/str.k:8-10` yields one-code strings and a strictly shorter remainder | Each loop consumes the exact input once and binds `char` before the exact body. |
| `If` | `semantics/syntax.k:49` with strict condition | `semantics/controls.k:51-54` applies `truthy` and selects exactly one branch | `found` is Boolean, so the condition is exact. |
| `IfExp` | `semantics/syntax.k:23` with strict condition | `semantics/controls.k:57-60` selects one expression | The initial result is `string` iff `found`, otherwise `string + reverse_string`. |
| `Return` | `semantics/syntax.k:50` with strict result | `semantics/functions.k:78-90` discards the remaining function continuation and returns through the saved frame | This matches Python return control for this body. |
| `UnaryOp("not", ...)` | `semantics/syntax.k:14` with strict operand | `semantics/operators.k:10` and `semantics/bool.k:8` | Exact Boolean negation of `found`. |
| `BinOp("+", ...)` | `semantics/syntax.k:15` with left-to-right `seqstrict(2,3)` | `operators.k:12`, `str.k:20-24` and structural `seqConcat` | String concatenation preserves Python code-point sequence order. |
| `Compare(..., "==", ...)` | `semantics/syntax.k:30,32` | left/right contexts at `operators.k:15-17`, then `str.k:25` | Both operands are evaluated left-to-right and compared by structural `IntSeq` equality. |

Reachable priority rules were also checked. Ref/cell rules in `core.k`,
`controls.k`, `functions.k`, `operators.k`, and `call.k` require heap references
or a `"$cells"` marker absent from these states, so they do not overlap the
plain-string/plain-frame execution. No proof-local priority, simplification,
`owise`, `anywhere`, opaque, or operational `<k>` rule exists.
