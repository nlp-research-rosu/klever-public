# Used-construction and rule map

This map is for the parsed `solution.mpy` constructor tree whose SHA-256 is
`8be106732caecfcf1b9cc8782a2badbd792e1bd69fe1e5728356882640f600b4`
(`stage4/pinning-check-v2.log`). Exact text for every cited sentence is in
`inventory.json`.

| Used constructor/transition | Declaration | Operational rules | Audit finding |
|---|---|---|---|
| `Module`, `FuncDef`, `Params`, `Stmts` | `syntax.k:53-61`; `core.k:124` | `core.k:125-127`; `functions.k:14-16` | Module statements execute left-to-right. The definition stores the exact body as `closureVal(...,0)` and changes no unrelated cell. |
| `Call(Name("x_or_y"), N, X, Y)` | `syntax.k:28,37`; `core.k:185-188`; `call.k:19` | `call.k:20-21`; `core.k:189-191`; `call.k:69-74` | Callee lookup precedes left-to-right argument evaluation. Closure dispatch allocates scope 1, records the caller continuation and environment, and binds the exact stored body. No specific `Call` interception matches this callee. |
| `Name` lookup | `syntax.k:12`; `core.k:130` | `core.k:131-154` | The function binding is found in module scope 0; parameters and locals are found in scope 1. The priority-40 cell rule is inapplicable because the unannotated frame has no `"$cells"` binding. |
| Parameter binding | `functions.k:8-11` | `functions.k:63-75` | Three actuals bind in declared order. The cell-parameter priority rule is inapplicable for the same no-`"$cells"` reason. |
| `If` and `Return` | `syntax.k:49-50`; `controls.k:51`; `core.k:199` | `controls.k:52-54`; `functions.k:78-90`; `core.k:200` | The comparison is evaluated first; its Boolean result drives exactly one branch. Return sets `retV`, discards the remaining callee body, pops the exact top frame, restores env 0, deletes scope 1, and yields the value to the saved continuation. |
| `Assign(Name, Expr)` | `syntax.k:41` | strictness-generated RHS evaluation; `controls.k:9-18` | RHS evaluates before the write. The ordinary rule updates only the current scope. The cell-write priority rule is inapplicable. |
| `While` / `#while` | `syntax.k:46`; `controls.k:65-67` | `controls.k:77-85` | Each iteration reevaluates the guard, executes the complete body on true, and resumes via `#loopLbl`; false removes the loop. No abrupt loop control exists in the submitted body. |
| `Compare` | `syntax.k:30,32`; `operators.k:15-17` | `int.k:22` for `<`; `int.k:26` for `==` | Contexts impose left-then-right evaluation. The `[owise]` dispatch is not preempted: list/tuple membership, ref dereference, float/math, and other specialized rules do not match the integer terms. |
| `BinOp("%", n, i)` | `syntax.k:15`; `core.k:209`; `operators.k:12` | `int.k:15,19-20` | Sequential strictness evaluates `n` then `i`; `pyMod` is Python-style modulo. Every reachable divisor has `i >= 2`, so the unguarded helper is never applied at zero. |
| `BinOp("+", i, 1)` | same | `int.k:9` | Exact unbounded-integer increment. |
| Integer literals and values | `syntax.k:9`; `core.k:25,38-39` | `core.k:194` | K `Int` is unbounded and is a `Val`/`KResult`, matching the used Python arithmetic model. |
| Call frame/configuration | `core.k:49-60`; `functions.k:8-11` | `call.k:69-74`; `functions.k:78-90` | Initial scope, heap, allocation counters, stack, return state, exception state, and exit code are explicitly pinned by the entry claim. The call allocates and later removes only scope 1; heap and exit/exception state remain unchanged. |
| `trialChoice` | `verification.k:9` | `verification.k:17-26` | Definitional summary only. Its three guards are disjoint and exhaustive for every use (`I >= 2`); recursive cases increase `I` under `I < N`, and the base handles `I >= N`. |
| `xOrYSpec` | `verification.k:10` (`function,total`) | `verification.k:28-32` | Definitional summary only. `N < 2` and `N >= 2` are disjoint and exhaustive. It has no operational configuration match. |
| Loop circularity | `spec.k:6-38` | reachability claim, not a semantic rewrite in `verification.k` | The exact `#while`, exact local frame, exact stack, and no-return/no-exception states are proved. Arbitrary continuation, other scopes, heap, heap counter, and exit cell are framed on both sides. |
| Entry theorem | `spec.k:40-100` | reachability claim | Runs the exact parsed module and constrains the final value by equality to `xOrYSpec`; it also constrains the observable final cells. |

## Evaluation, overlap, and totality conclusions

- The only proof-path priority interactions are name/assignment cell handling.
  Their guards are false in the ordinary unannotated frame. Specialized call,
  comparison, reference, container, and math rules have constructor- or
  operator-disjoint heads.
- The proof-local file contains no priority, simplification, `[concrete]`,
  `[symbolic]`, `anywhere`, `owise`, hook, or opaque declaration.
- No supplied simplification rule or functional declaration exists in the
  inventoried sources. There are 45 supplied priority rules, 36 supplied
  `[concrete]` rules, and 22 `no-evaluators` declarations; none is on the task
  path. Their exact inventory/disposition is in `inventory.md` and
  `dispositions.csv`.
- The loop claim reads `n`, `i`, `result`, and `y`; writes only `i` and
  `result`; and preserves `x`, the enclosing scopes, heap, allocation cells,
  saved frame, return/exception states, exit status, and trailing continuation.
- `trialChoice` is intentionally partial outside `I >= 2`, but no theorem or
  execution produces an occurrence outside that guard. `xOrYSpec` is genuinely
  total over its declared `Int × Val × Val` domain.
