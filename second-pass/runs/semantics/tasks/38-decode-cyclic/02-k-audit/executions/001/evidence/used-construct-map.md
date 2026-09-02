# Used construct and rule map

This map is based on the fresh trusted translation
`/tmp/audit-work/38-decode-cyclic/candidate/solution.regenerated.mpy`.
Line references are to the scratch copy of the byte-identical supplied
semantics.

| Submitted construct | Declaration | Operational rules used |
|---|---|---|
| `Module`, statement sequence, `FuncDef`, `Params` | `semantics/syntax.k:53-61` | `core.k:124-127` loads/sequences the module; `functions.k:14-16` installs the closure |
| `Call(Name("decode_cyclic"), ...)` | `syntax.k:9-30` | `core.k:130-181` name/builtin lookup; `call.k:20-21` evaluates callee/arguments; `call.k:69-75` creates a frame |
| Parameter `s` | `syntax.k:57-60`, `core.k:31` | `functions.k:63-66` binds it; `core.k:131-154` reads it |
| Docstring `Expr(Str(...))` | `syntax.k:13,52` | `str.k:13-17` creates the code sequence; `controls.k:48` discards the value |
| `If(len(s) < 3, ...)` | `syntax.k:23,28-30,49` | `call.k:20-32`; `builtins.k:17-24` computes `len`; `operators.k:15-17` and `int.k:22-27` compare; `controls.k:51-54` branches |
| `Return(...)` | `syntax.k:50` | strict evaluation from the generated heating rules; `functions.k:78-90` records the value and pops/restores the frame |
| String indexing `s[2]` | `syntax.k:22,38-39` | `subscript.k:27-41`; `intSeqAt` at `subscript.k:16-19` |
| String slices `s[:2]`, `s[3:]` | `syntax.k:22,38-39` | bound evaluation and slicing at `subscript.k:43-69`; slice normalization at `subscript.k:71-106`; `buildIS` at `subscript.k:116-121` |
| String `+` | `syntax.k:15` | `operators.k:12`; `str.k:20-24` and `seqConcat` |
| Recursive call | same call rules as entry | `call.k:69-75` pushes; `functions.k:85-90` pops; the helper reachability claim is applied at the exact `decodeBody ~> #endcall` recursive frame |
| Integer and string values | `core.k:13-39`, `syntax.k:9-15` | literal rules `core.k:193-196`, `str.k:14-17`; `isLen` at `core.k:227-229` |

The target performs no list construction, heap allocation, mutation, output,
sorting, hashing, floating-point work, exception raising, or loop control.
Accordingly the supplied rules for those constructs and all 22
`[no-evaluators]` declarations are unreachable from the two positive claims.

Relevant state footprint:

- Calls change `<env>`, `<scopes>`, `<scopeLoc>`, `<stack>`, and `<ret>`, then
  restore/deallocate the frame on `#pop`.
- The target leaves `<heap>`, `<heapLoc>`, `<exc>`, and `<exit-code>` unchanged.
- Argument and binary-expression evaluation is left-to-right under the
  supplied strictness/context rules.
