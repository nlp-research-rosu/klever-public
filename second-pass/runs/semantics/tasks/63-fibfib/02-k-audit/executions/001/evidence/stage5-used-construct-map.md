# Used-construct and proof-extension map

The numeric IDs refer to `stage5-rule-inventory.tsv` and
`stage5-rule-decisions.tsv`.

| Submitted construct / obligation | Declaration | Fixed rules on the path | Audit result |
|---|---:|---:|---|
| `Module` / module load | 903, 297 | 324–326, 565 | Concrete `smoke.mpy` loads the translated function into module scope. The entry claim starts from the equivalent post-load closure binding. |
| `FuncDef("fibfib", Params("n"), BODY)` | 897, 899 | 565 | Creates `closureVal("n", .ParamNames, BODY, 0)` in scope 0. The pinning script proves `BODY` is token-identical to the submitted MPY body. |
| `Call(Name("fibfib"), Int(N))` | 888 | 195–196, 328–329, 334–339, 352–354, 212 | Callee is looked up, the integer argument is evaluated left-to-right, a new scope/frame is allocated, and `n` is bound. No problem-local call interception exists. |
| `Int`, `Name` | 888 | 328–329, 339 | Integers evaluate to mathematical K `Int`; names read the current scope map. Every used name is bound. |
| `Assign(Name(X), RHS)` | 897 (`strict(2)`) | 248 | The RHS evaluates first, then the current local scope is updated. The cell-write priority rule is pruned because this plain closure has no `$cells` binding. |
| `BinOp("+", L, R)` | 888 (`seqstrict(2,3)`) | 736, 350, 584 | Operands evaluate left-to-right and integer addition becomes `+Int`. Values on this path are integers, so float/list/ref cases do not overlap. |
| `Compare(L, CmpOp("<", R))` | 888–889 | 737–739, 351, 594 | Explicit contexts evaluate left then right; integer `<` becomes `<Int`. |
| `While(C, BODY)` / `#while` | 897 | 270–274, 342, 345 | The condition is reevaluated each iteration; integer truth is nonzero; true executes the exact body then loops, false consumes only the loop. The helper claim’s `#while` body exactly matches the submitted `While`. |
| `Return(Name("a"))` | 897 (`strict`) | 580, 582 | The return expression evaluates, the result is stored, the exact call frame is popped, and caller cells/continuation are restored. Body sensitivity (`a` changed to `b`) makes the proof fail. |
| `fibFrom` summary | 929 | 930–931 | Definitional, not operational. Guards `N <= 0` and `N > 0` are disjoint and exhaustive; recursion descends for the positive case. It is the first tuple component after `N` shifts. |
| Index normalization lemma | — | 932 | Globally true integer identity `N-(I+1)=(N-I)+(-1)`; it changes no program cell and only normalizes the loop proof. |

The 22 fixed opaque primitives (float operations, sorting, and MD5) are listed
in the TSV inventory. None is referenced or constructible by `solution.mpy`,
`spec.k`, or `verification.k`; none can influence these claims.
