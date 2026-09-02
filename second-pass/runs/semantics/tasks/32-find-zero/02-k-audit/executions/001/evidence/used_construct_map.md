# `solution.mpy` construct map

All line references below are to the exact supplied-semantics copy under
`/candidate/reference-semantics/semantics/`.

| Submitted construct | Declaration | Fixed-semantics route |
|---|---|---|
| `Module(...)` | `syntax.k:61` | `core.k:124-127` loads and sequences statements. |
| `Import("math")` | `syntax.k:42` | `float.k:61` treats imports as no-ops; supported `math` calls are intercepted syntactically. |
| Annotated `FuncDef`, `Params`, `CellVars`, `FreeVars` | `syntax.k:53-60` | `functions.k:33-45` creates and binds `closureValC`; ordinary defs use `functions.k:14-16`. |
| `Return` | `syntax.k:50` | Strict expression evaluation plus `functions.k:78-91` sets `<ret>`, pops the frame, restores `<env>`, removes the scope, and resumes the saved continuation. |
| `Call` | `syntax.k:28` | `call.k:20-32` evaluates callee then arguments and dispatches; `call.k:69-76` allocates the ordinary closure call frame. |
| `Name` | `syntax.k:12` | `core.k:131-155` walks local/parent scopes and the builtins scope. |
| `Int`, `Float`, `Bool` | `syntax.k:9-11` | `core.k:195-197` and `float.k:20-21` produce `Val`s. |
| `UnaryOp` | `syntax.k:14` | Strict operand evaluation, `operators.k:10`, then integer minus in `int.k:7` or float minus in `float.k:99`. |
| `BinOp` | `syntax.k:15` | `seqstrict(2,3)` gives left-to-right operands; `operators.k:12` dispatches. Integer cases are `int.k:9-17`; relevant float/mixed cases and opaque proof-domain primitives are `float.k:101-151,189-206`. |
| `Compare` / `CmpOp` | `syntax.k:30-32` | Left then right evaluation via `operators.k:15-17`; integer `>` is `int.k:24`, float/mixed `>` is `float.k:123-151`. |
| `Assign`, `AugAssign` | `syntax.k:41,44` | Current-scope writes are `controls.k:9-31`; the normal numeric `AugAssign` uses `applyBin`. |
| `While` | `syntax.k:46` | `controls.k:77-82` repeatedly evaluates the condition and executes the body according to `truthy`. |
| `If` | `syntax.k:49` | Strict condition evaluation and `controls.k:51-54` select exactly one branch. |
| `ListComp`, `CompFor` | `syntax.k:19,35-36` | `comprehension.k:11-26` expands to a closure with an allocated accumulator, nested `For`, and return. |
| `TupleExpr` target `(i, coeff)` | `syntax.k:21` | `tuple.k:15-16` constructs tuples; `tuple.k:31-57` binds/unpacks iteration targets. |
| `enumerate(xs)` | Builtin binding in `core.k:176`; generic call syntax above | `builtins.k:123-129` materializes indexed tuples in a fresh list. |
| `math.pow(x, i)` / `Attribute` | `syntax.k:29` | Priority-40 interception in `float.k:81-88` evaluates both args then applies opaque `powF` (`float.k:119-120` has the concrete rule). |
| `sum(...)` | Builtin binding in `core.k:162`; generic call syntax above | `call.k:26` enters the fold; `builtins.k:47-56` handles integer values and `float.k:257-273` handles float/mixed values. |

The candidate proof does not traverse the important routes above. It executes
the two initial `Assign`s, then its priority-40 rules replace each complete
`While` before the guard is evaluated. Consequently no `poly` lookup, `Call`,
comprehension, `enumerate`, `math.pow`, `sum`, arithmetic guard, `If`, or loop
body runs in either positive proof.
