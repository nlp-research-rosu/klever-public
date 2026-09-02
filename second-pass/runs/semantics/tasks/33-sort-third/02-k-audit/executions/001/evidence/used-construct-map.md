# Used-construct map for `solution.mpy`

The submitted MPY AST uses only the constructs below. Line references are to
the fresh scratch copy, which is byte-identical to the trusted supplied
semantics tree.

| MPY construct | Declaration | Execution/value rules on this program's path |
|---|---|---|
| `Module`, statement sequencing | `semantics/syntax.k:61`, `core.k:124-127` | `#loadAll(Module(SS))` exposes the statements; `Stmt Stmts` sequences left-to-right; `.Stmts` terminates. |
| `FuncDef`, `Params` | `syntax.k:53-57` | `functions.k:14-16` stores `closureVal(PNS,BODY,L)` in the current scope. |
| `Expr(Str(...))` docstring | `syntax.k:13,52` | `str.k:14-16` constructs a string value; `controls.k:48` discards the expression value. |
| `Assign(Name(...), ...)` | `syntax.k:41` with strict RHS | `controls.k:9-11` updates the current scope after the RHS is a value. |
| `Name` | `syntax.k:12` | `core.k:131-155` starts lookup in `<env>`, returns a local binding when present, and otherwise follows the parent chain to builtins. |
| `Call` | `syntax.k:28` | `call.k:20-21` evaluates callee then arguments; `core.k:185-191` evaluates arguments left-to-right; `call.k:69-76` creates the function frame and executes the real body. |
| `sorted` | builtin binding in `core.k:157-184` | `call.k:38-46` dereferences the list argument; `sort.k:36-37` allocates a new `list(sortVS(VS))`. `sortVS` is opaque in Haskell and concretely insertion-sorted in LLVM (`sort.k:18-32`). |
| `Subscript` slice `l[::3]` | `syntax.k:22,38-39` | `subscript.k:27-28,54-65` evaluates object/bounds in order, computes CPython-style defaults, builds `buildVS(VS,0,vsLen(VS),3)`, and allocates the sliced list. |
| `ListExpr()` | `syntax.k:17` | `list.k:14-15` evaluates elements and allocates a fresh list; empty elements allocate `list(.ValSeq)`. |
| integer and `None` literals | `syntax.k:9,27` | `core.k:194-196` cools them to integer values and `noneV`. |
| `For(Name("value"), Name("l"), body)` | `syntax.k:45` with strict iterable | `controls.k:69-74`, `list.k:9-10`, and tuple target-binding rules iterate the input left-to-right, bind each element, execute the exact body, and recur on the remainder. |
| `If` | `syntax.k:49` with strict condition | `controls.k:52-54` computes `truthy` and selects exactly one branch. Here the condition is already Boolean. |
| `BinOp("%",...)`, `BinOp("//",...)` | `syntax.k:15` with sequentially strict operands | `operators.k:12`; `int.k:15-20` implements Python modulo and floor division. The actual divisor is the positive integer 3. |
| `Compare(..., CmpOp("==",...))` | `syntax.k:30`, `syntax.k:32` | `operators.k:15-17` evaluates left then wrapped right operand; `int.k:26` returns integer equality. |
| `Attribute(...,"append")`, method call | `syntax.k:29` with strict receiver | `call.k:16,20-24` constructs and dispatches a bound method; `list.k:53-55` writes one value at the end of the referenced result list and returns `noneV`. |
| `AugAssign(Name("i"),"+",Int(1))` | `syntax.k:44` with strict RHS | `controls.k:20-24` reads and writes the same local binding; `int.k:9` supplies integer addition. |
| indexed read of `thirds[i//3]` | `syntax.k:22` | `subscript.k:31-40` dereferences the list and uses `valSeqAt`; `valSeqAt` is total and reduces on concrete in-bounds sequences (`subscript.k:11-14`). |
| `Return(Name("result"))` | `syntax.k:50` with strict result | `functions.k:78-90` records the returned reference, pops/restores the exact saved continuation and caller environment, removes the callee scope, and leaves the allocated heap object live. |

The active configuration is `core.k:49-61`: `<k>`, `<env>`, `<scopes>`,
`<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and
`<exit-code>`. The entry claim explicitly fixes every one of those cells.
