# `solution.mpy` construct-to-semantics map

The submitted `solution.mpy` uses only the constructs listed below. Locations
refer to the byte-identical supplied semantics and the candidate-local proof
extensions.

| Program construct | Declaration | Fixed execution path | Candidate-local preemption |
|---|---|---|---|
| `Module`, statement and expression lists | `semantics/syntax.k:37,56,61` | `core.k:124-127` loads and sequences statements | `solutionProgram` macro, `verification.k:133-140`, expands to the exact parsed submitted module |
| `FuncDef`, `Params` | `syntax.k:53,57` | `functions.k:14-16` installs a closure; `call.k:69-75` creates a call frame and binds parameters | `solutionBody`, `verification.k:120-131`, is an exact AST macro only |
| `Assign(Name(...), ...)` | `syntax.k:41` with strict RHS | `controls.k:9-18` updates the current scope or closure cell | Existing `n` and `result` bindings are updated by priority-30 rules at `verification.k:178-218` |
| `Name` | `syntax.k:12` | `core.k:129-154` performs LEGB lookup through `<scopes>` | Direct `n`, `word`, and `result` lookup rules at `verification.k:237-280`; the `len` call bridge at `verification.k:220-235` bypasses this lookup |
| `Str`, `Int` | `syntax.k:9,13` | `str.k:13-17` converts ASCII literals to `IntSeq`; `core.k:193-196` evaluates integers | None |
| `Attribute` | `syntax.k:29`, strict receiver | `call.k:15-16` produces `boundMethodV` | None |
| `Call` and arguments | `syntax.k:28` | `call.k:18-32` evaluates callee, then arguments left-to-right, then dispatches | Symbolic `split` is replaced at `verification.k:144-152`; `Call(Name("len"), Name("word"))` is replaced before callee/argument evaluation at `verification.k:220-235` |
| no-argument `str.split()` | method dispatch through `call.k:24` | `methods.k:70-86` recursively scans concrete character codes and allocates a concrete list | `verification.k:144-152` maps opaque `sentenceCodes(W)` directly to opaque `wordsVals(W)` |
| `For` | `syntax.k:45`, strict iterable | `controls.k:62-74` evaluates iterable once and drives `#iterNext`; list iteration is `list.k:8-10` | `wordsVals` iterator cases at `verification.k:17-22`; direct plain-frame binding at `verification.k:157-176` |
| `len(word)` | generic `Call` | `core.k:129-191`, `call.k:18-32`, then `builtins.k:17-26` | `verification.k:220-235` returns `isLen(C)` without resolving `len` |
| `BoolOp("or", ...)` | `syntax.k:16` | `bool.k:13-46` evaluates left-to-right and short-circuits | `primeTest`, `verification.k:74-102`, is an exact AST macro only |
| `Compare(..., CmpOp("==", ...))` | `syntax.k:30,32` | `operators.k:14-17` dispatches after ordered evaluation; integer equality is `int.k:26`, string equality is `str.k:25` | Direct `Name` rules affect operand lookup |
| `If` | `syntax.k:49`, strict condition | `controls.k:50-54` selects by `truthy` | None |
| string `BinOp("+", ...)` | `syntax.k:15`, left-to-right strict | `operators.k:10-12`, then `str.k:20-26` concatenates code sequences | Direct `Name` rules affect operand lookup |
| `Return` | `syntax.k:50`, strict expression | `functions.k:77-90` stores the value, pops the frame, restores caller state | None |

The fixed configuration is `core.k:49-60`: `<k>`, `<env>`, `<scopes>`,
`<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and
`<exit-code>`. The entry claim pins all observable cells. The loop claim frames
cells other than `<k>`, `<env>`, and `<scopes>`.
