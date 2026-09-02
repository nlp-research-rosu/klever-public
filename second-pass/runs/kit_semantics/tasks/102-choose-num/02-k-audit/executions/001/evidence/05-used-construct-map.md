# Used-constructor and rule map

This map is for the byte-identical trusted supplied semantics copied to
`/tmp/audit-work/102-choose-num/reference-semantics`. The exhaustive lexical
inventory is `05-rule-inventory.tsv`; this document records the reachable slice
for `solution.mpy`.

| Submitted constructor | Declaration | Material fixed-semantics behavior | Review |
|---|---|---|---|
| `Module` | `semantics/syntax.k:61` | `core.k:124-127` turns `#loadAll(Module(SS))` into left-to-right statement execution and consumes `.Stmts`. | Exact `Module` KAST equals the load claim KAST. |
| `FuncDef`, `Params`, `ParamNames` | `syntax.k:53,57,60` | `functions.k:14-16` installs `closureVal(PNS,BODY,L)` in the current scope. | Load claim's target binding/body equals the translated KAST. |
| `Call` | `syntax.k:28` | `call.k:19-21` evaluates the callee, `core.k:185-191` evaluates arguments left-to-right, and `call.k:69-74` creates a frame for the exact closure body. | No call interception or proof-local operational rule exists. |
| `Name` | `syntax.k:12` | `core.k:130-154` searches the current scope and then parents. | `"choose_num"` resolves in scope 0; `"x"`/`"y"` resolve in the fresh call scope. The higher-priority cell lookup cannot match because the maps contain no `"$cells"` and the heap is empty. |
| `If` | `syntax.k:49 [strict(1)]` | `controls.k:51-54` applies `truthy` and chooses exactly one branch. | Conditions are integer comparison results (`Bool`); branch guards are exhaustive. Heap-ref priority rules cannot match integer/boolean conditions. |
| `Compare`, `CmpOp` | `syntax.k:30,32` | `operators.k:15-17` evaluates left then right and calls `applyCmp`; `int.k:22-27` implements integer `>`, `>=`, and `==`. | The generic `[owise]` dispatch is the applicable fixed rule; ref-deref priority rules cannot match `Int`. |
| `BinOp` | `syntax.k:15 [seqstrict(2,3)]` | `operators.k:12` dispatches after left-to-right operand evaluation; `int.k:13,15` implements subtraction and `%` via `pyMod`. | `pyMod(Y,2)` has a fixed nonzero divisor and agrees with Python parity for every integer. |
| `UnaryOp` | `syntax.k:14 [strict(2)]` | `operators.k:10` plus `int.k:7` computes `0 -Int I`. | This gives the literal return value `-1`; no heap dereference can match. |
| `Int` | `syntax.k:9` | `core.k:194` yields mathematical `Int`. | Unbounded K integers match the relevant Python integer model. |
| `Return` | `syntax.k:50 [strict]` | `functions.k:78-90` stores the value, discards the remaining body, pops the exact frame, restores `env`, deletes the temporary scope, and restores `scopeLoc`. | Correct abrupt return behavior; heap, heap counter, exception, and exit cells remain unchanged. |
| statement list | `syntax.k:56` | `core.k:126-127` schedules each statement with its suffix. | The three conditionals and final return execute in source order until a return discards the suffix. |

## Call-state footprint

Starting from the entry claim, scope 0 contains only the mechanically matched
`choose_num` closure and parent `-1`; `-1` is the fixed `builtinsScope`.
`scopeLoc=1`, the heap is empty, the stack is empty, `ret=noRet`,
`exc=NoExc`, and `exit-code=0`. The closure-call rule allocates temporary scope
1, binds `x` then `y`, pushes a frame containing the exact continuation, and
executes the exact body. `#pop` restores all stated cells. No used rule writes
the heap, exception, or exit code.

## Proof-local extensions

`verification.k` declares only `chooseNumSpec(Int,Int) [function,total]` and
four ordinary equations. There are no proof-local priority, simplification,
`functional`, `concrete`, opaque-symbol, or operational rules.

The guards partition `Int × Int`:

1. `X > Y`;
2. `X <= Y` and `pyMod(Y,2) == 0`;
3. `X <= Y`, nonzero parity, and `Y-1 >= X`;
4. `X <= Y`, nonzero parity, and `Y-1 < X`.

They are exhaustive and pairwise disjoint. Because the divisor is 2,
`pyMod(Y,2)` is 0 or 1, so the equations respectively yield `-1`, `Y`,
`Y-1`, and `-1`. This is both the program's branch result and the
greatest-even-in-`[X,Y]` result: an even `Y` is maximal; an odd `Y` has
immediate predecessor `Y-1`, which is the maximal possible even value when it
lies in the interval; otherwise the interval contains no even integer.

## Fixed but unreachable declarations

The other supplied modules are still enumerated row-by-row in the inventory.
They are part of the selected trusted semantics, are byte-identical to the
trusted mount, and are not candidate proof extensions. In particular, all 25
local `symbol(...)`/`no-evaluators` declarations are in float, sorting, or MD5
support and are unreachable from this integer-only, straight-line program.
No opaque value can influence its branch, result, state, exception, or
postcondition.
