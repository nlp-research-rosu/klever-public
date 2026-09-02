# Material constructor-to-rule map

This map is for the constructors in the trusted-regenerated `solution.mpy`.
Line numbers refer to the scratch copy under
`/tmp/audit-work/candidate-scratch/reference-semantics/`.

| Constructor/value | Declaration | Material rules |
|---|---|---|
| `Module(Stmts)` | `semantics/syntax.k:61` | `core.k:124-127` loads and sequences statements |
| `ImportFrom("typing","List")` | `syntax.k:43,60` | `controls.k:35-36`; the non-`math` import is an inert no-op |
| `FuncDef`, `Params` | `syntax.k:53,57,60` | `functions.k:14-16` binds `closureVal(params,body,current-env)` |
| `Assign(Name(...), ...)` | `syntax.k:41` | strict RHS evaluation, then `controls.k:9-18` updates the local scope |
| `Name` | `syntax.k:12` | `core.k:130-154` follows the scope chain |
| `ListExpr(.Exprs)` | `syntax.k:17,37` | `list.k:13-15`, `core.k:117-121,183-191,217-219` evaluate elements and allocate a fresh list |
| `For` | `syntax.k:45` | `controls.k:62-74,104-108`, `list.k:8-10`, and `tuple.k:30-41` evaluate the iterable once, iterate its snapshot, and bind the target |
| `If` | `syntax.k:49` | strict condition plus `controls.k:50-54`; `core.k:198-205` defines Bool truth |
| `Compare(... CmpOp("==", Int(1)))` | `syntax.k:30,32` | `operators.k:14-17`, `core.k:193-195`, and `int.k:22-27` preserve operand order and integer equality |
| `Call` | `syntax.k:28` | `call.k:18-32` and `core.k:183-191` evaluate callee then arguments left-to-right |
| `Attribute(...,"count")` | `syntax.k:29` | `call.k:15-16,24` creates and dispatches a bound method |
| `list.count` | method dispatch | `methods.k:63-68`; a terminating occurrence count with complementary equality guards |
| `Attribute(...,"append")` | `syntax.k:29` | `call.k:52-67` preserves mutating receivers as refs |
| `list.append` | method dispatch | `list.k:18-20,52-55`; in-place heap update and `noneV` result |
| `Expr(Call(...))` | `syntax.k:52` | strict call evaluation, then `controls.k:46-48` discards only the value |
| `Return(Name(...))` | `syntax.k:50` | strict expression evaluation and `functions.k:77-90` return/pop the call frame while preserving the heap |
| statement and expression list units | `syntax.k:37,56` | `core.k:123-127,183-191` sequences statements and arguments |

The proof definition imports `MPY`, not `MPY-CONCRETE`; therefore none of the
LLVM-only concrete rules contribute to symbolic closure.
