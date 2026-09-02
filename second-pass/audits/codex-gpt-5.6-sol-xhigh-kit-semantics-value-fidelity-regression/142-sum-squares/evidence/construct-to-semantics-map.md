# Construct-to-semantics map

This map is reviewer-authored. Line numbers refer to the clean scratch copy,
which is source-identical to the recursively checked candidate semantics.
The complete 949-record declaration inventory is in
`k-declaration-inventory.{jsonl,tsv}`.

| Submitted construct or proof term | Declaration | Operational rules used | Audit result |
|---|---|---|---|
| `Module(...)` | `reference-semantics/semantics/syntax.k:61` | `core.k:49-60,124-127` loads and sequences statements | Sound at supplied-semantics level. Used by the fresh LLVM run; the symbolic entry starts after module load. |
| `FuncDef("sum_squares", Params("lst"), BODY)` | `syntax.k:53,57,60` and `core.k:25-34` (`closureVal`) | `functions.k:14-16` installs the closure | Sound. The target claim preinstalls the exact closure instead of reproving module loading; the body/parent/binding are byte- and structure-pinned. |
| `Call(Name("sum_squares"), list(VS))` | `syntax.k:12,28`; `core.k:18-34,185-188`; `call.k:19` | `core.k:131-154,189-191`, `call.k:20-21,69-74`, `functions.k:63-66` | Callee lookup precedes left-to-right argument evaluation; the exact closure allocates a frame and binds `lst`. |
| `Assign(Name(...), Int(0))` | `syntax.k:9,12,41` with strict RHS | `core.k:194`, `controls.k:9-11` | Initializes `total`, `index`, and `value` in the current frame. Cell/ref priority alternatives are inapplicable because the exact frame has neither `$cells` nor refs. |
| `For(Name("value"), Name("lst"), BODY)` | `syntax.k:45` (`strict(2)`); `controls.k:65-67` | name lookup `core.k:131-154`; `controls.k:69,71-74,85`; list iterator `list.k:9-10`; target binding `tuple.k:31-34` | Iterable evaluated once. Each head is bound to `value`, then the exact body executes, then the remaining list loops. The invariant begins at the real `#loop` control point with the exact translated body. |
| `If(...)` | `syntax.k:49` (`strict(1)`) | `controls.k:51-54`; `core.k:199-205` | Condition evaluates before the selected branch. Integer-comparison results are `Bool` and truthiness is exact. |
| `BinOp("%", Name("index"), Int(3 or 4))` | `syntax.k:15` (`seqstrict(2,3)`); `core.k:209` | lookup/literal rules; `operators.k:12`; `int.k:15,19-20` | Left-to-right pure integer modulo using Python-style floored `pyMod`; divisors 3 and 4 are nonzero and positive. |
| `Compare(..., CmpOp("==", Int(0)))` | `syntax.k:30,32`; comparison contexts `operators.k:15-16` | `operators.k:17`; `int.k:26` | Both operands evaluate before integer equality. |
| `BinOp("*", value, value)` and nested cube | `syntax.k:15`; `core.k:209` | `operators.k:12`; fixed `int.k:14`; proof bridge `verification.k:33-35` | Bridge is pure and ground-sound under `isInt` operands; it agrees with fixed multiplication on all ground guarded cases. Exact symbolic guarded-domain connection does not close because K cannot cast from `isInt`, a recorded evidence limitation. |
| `AugAssign(total, "+", rhs)` and `AugAssign(index, "+", 1)` | `syntax.k:44` (`strict(3)`) | `controls.k:20-23`; fixed `int.k:9`; proof bridge `verification.k:30-32` | RHS is evaluated before the stored left value is combined. The bridge is pure and ground-sound under the guard, with the same symbolic connection limitation as multiplication. |
| `Return(Name("total"))` | `syntax.k:50` (`strict`) | lookup; `functions.k:78-90` | Evaluates the returned expression, discards the remaining callee computation, restores the caller environment, removes the frame, resets stack/return state, and returns the value. |
| `allInts` | `verification.k:7-10` | empty/cons equations | Total, structurally recursive, exhaustive. It is the formal domain predicate. |
| `contribution` | `verification.k:13-19` | three guarded equations | Total on `Int × Int`; guards are disjoint and exhaustive. They encode square precedence over cube at indices divisible by both 3 and 4. |
| `intVal` | `verification.k:23-25` | typed identity plus `[owise]` zero | Total and disjoint. Only identity cases influence the theorem because `allInts` holds. |
| `sumSquares` | `verification.k:38-48` | empty; integer-cons; noninteger-cons equations | Total, disjoint, and structurally descending. The noninteger case is unreachable from the entry precondition. |
| `advanceIndex` | `verification.k:51-54` | empty/cons equations | Total and structurally descending. |

## Configuration, effects, overlaps, and special attributes

- The supplied configuration is `core.k:49-60`: `<k>`, current environment,
  scope store/location, heap/location, call stack, return state, exception
  state, and exit code. The entry claim fixes every one of these cells. The
  loop claim rewrites only its named local bindings and `<k>`; configuration
  completion frames the remaining cells and arbitrary continuation.
- The function does not allocate user heap objects, mutate the input list,
  perform I/O, or raise an exception on the all-integer domain. The call frame
  is allocated and then removed by fixed semantics. The argument is a legal
  unboxed read-only `list(ValSeq)` in this semantics.
- Proof-local equation overlaps are benign: the three `contribution` guards
  are pairwise disjoint; `intVal(Int)` and its `owise` case are disjoint;
  `sumSquares` uses empty versus cons and `isInt` versus `notBool isInt`;
  `advanceIndex` uses empty versus cons. The two bridge rules overlap the
  fixed `MPY-INT` rules only on integers, where their right-hand sides reduce
  to the same integer operation. Their guards exclude every non-Int ground
  `Val`.
- All proof-local `[total]` declarations have constructor/guard coverage and
  structurally decreasing recursion. There are no proof-local priority,
  `[simplification]`, `[functional]`, `[concrete]`, `symbol`, or
  `no-evaluators` declarations.
- The trusted supplied tree contains 45 priority-bearing declarations, 35
  concrete declarations, 25 symbols, and 22 `no-evaluators` declarations.
  They are exhaustively inventoried. Every opaque/no-evaluator declaration is
  in float, sorting, or digest support and is unused by `solution.mpy`.
- LLVM warned about several non-exhaustive supplied total functions
  (`mapStrVS`, float conversion helpers, `joinCodes`, and `valSeqAt`); none is
  reachable from this submitted program or its claims.
