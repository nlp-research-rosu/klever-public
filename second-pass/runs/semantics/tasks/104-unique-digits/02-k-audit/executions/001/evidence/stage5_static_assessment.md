# Static assessment and used-construct map

The exhaustive, source-quoted inventory is `stage5-rule-inventory.md`. It
contains all 709 `rule` blocks, 235 `syntax` declarations, five `context`
declarations, the one configuration, the submitted claim, and all attributes
attached to those blocks. No `[functional]` or `[simplification]` declaration
occurs. `stage5-special-attributes.log` separately indexes `total`,
`no-evaluators`, priority, and related declarations.

## Per-file disposition

The semantics tree is byte/type-identical to the trusted supplied tree. For the
selected `SUPPLIED_SEMANTICS` level, the baseline rules are therefore not
candidate proof extensions. Every baseline block in the exhaustive inventory
was reviewed for whether it can contribute to this program. The used subset is
mapped below; unused groups are inert on `solution.mpy` and do not support a
claim about full Python.

| Source | Inventory | Disposition for this proof |
|---|---:|---|
| `semantics.k` | assembly only | Imports the trusted `MPY` modules; proof does not import `MPY-CONCRETE`. |
| `semantics/syntax.k` | 16 syntax | Used AST constructors are declared; strict/seqstrict attributes give the required evaluation order. |
| `semantics/core.k` | 1 configuration, 37 syntax, 46 rules | Used: initial cells, module load, statement sequencing, literals, lookup, builtins scope, argument evaluation, and allocation. No task answer is encoded. |
| `semantics/iter.k` | 1 syntax | Iterator protocol declaration used by the real `For`. |
| `semantics/list.k` | 5 syntax, 27 rules | Used: list iterator, list allocation, concatenation, and in-place `append`. |
| `semantics/operators.k` | 2 contexts, 10 rules | Used dispatch/evaluation for comparisons and binary operations. |
| `semantics/int.k` | 1 syntax, 16 rules | Used `%`, `//`, `>`, and `==`; rules are ordinary unbounded-integer arithmetic and Python-style floored remainder/division for positive divisors. |
| `semantics/bool.k` | 1 context, 13 rules | Boolean/truthiness support; only ordinary Boolean results are used here. |
| `semantics/controls.k` | 3 syntax, 34 rules | Used assignment, augmented assignment, `If`, `For`, `While`, `Break`, and loop continuations. |
| `semantics/functions.k` | 4 syntax, 15 rules | Used definition loading, parameter binding, return, and frame pop. |
| `semantics/call.k` | 3 syntax, 21 rules | Used callee lookup, left-to-right arguments, closure dispatch, method dispatch, and builtin dispatch. |
| `semantics/methods.k` | 27 syntax, 75 rules | `append` is dispatched through the call layer but implemented in `list.k`; the method helpers here are otherwise unused. |
| `semantics/builtins.k` | 38 syntax, 137 rules | Supplies the builtin registry targets; task execution uses only dispatch onward to `sorted`. Other builtin rules are unused. |
| `semantics/sort.k` | 6 syntax, 19 rules | Used `sorted`: allocates a fresh list containing opaque `sortVS`. `sortVS` is an explicit supplied trusted primitive in proofs; its concrete insertion-sort equations are `[concrete]`. |
| `semantics/assert.k` | 3 rules | Used only by concrete test harnesses, not by the proof claim. |
| `semantics/concrete.k` | 5 syntax, 16 rules | LLVM-only and absent from the Haskell proof definition. |
| `semantics/{comprehension,dict,float,range,set,str,subscript,tuple}.k` | fully inventoried | Their AST forms never occur in `solution.mpy`; no rule can contribute to the target path. Opaque float/keyed-sort/digest symbols are correspondingly inert. |
| `verification.k` | 8 syntax, 14 rules | Individually assessed below. |
| `spec.k` | 1 claim | Individually assessed below. |

The compiler's non-exhaustiveness warnings concern baseline helpers
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None is
reachable from this program. `sortVS` is deliberately opaque in the Haskell
definition and is recorded as a trust boundary, not as a proved ordering
theorem.

## Mapping every submitted construct to execution rules

| Submitted construct | Declaration and operative rules |
|---|---|
| `Module`, `FuncDef`, `Params`, statement lists | `syntax.k:41-61`; `core.k:124-127`; `functions.k:14-16` |
| `Name`, `Int`, `Bool` | `syntax.k:9-13`; `core.k:130-154,194-196` |
| `Assign`, `AugAssign` | `syntax.k:41-45`; `controls.k:9-31` |
| `ListExpr` | `syntax.k:17`; `list.k:13-15`; allocation is `core.k:117-121` |
| `While`, `Break` | `syntax.k:46-48`; `controls.k:76-91` |
| `For` over the unboxed input list | `syntax.k:45`; `controls.k:62-74`; `list.k:9-10`; target binding is `tuple.k:31-41` |
| `If` and truthiness | `syntax.k:49`; `controls.k:50-54`; `core.k:198-205` |
| `%`, `//`, `>`, `==` | `syntax.k:14-16,30-32`; strictness/contexts in `operators.k:10-17`; integer equations in `int.k:15-27` |
| helper and builtin calls | `syntax.k:28`; `core.k:183-191`; `call.k:18-32,69-75`; frames/returns in `functions.k:62-90` |
| `result.append(n)` | `syntax.k:29`; attribute/method routing in `call.k:15-24`; heap mutation in `list.k:52-55` |
| `sorted(result)` | builtin lookup in `core.k:156-181`; heap argument dereference in `call.k:34-50`; fresh sorted allocation in `sort.k:34-37` |
| `Return` and `Expr` | `syntax.k:50,52`; `functions.k:77-90`; `controls.k:46-48` |

Under fixed supplied semantics, the program allocates the mutable result list
at heap location 0, mutates it in place during the loop, allocates the sorted
return list at location 1, and returns `ref(1)`. The submitted claim's cell and
allocation shape matches that control flow.

## Every proof-local declaration and rule

1. `oddDigits(Int)` (`verification.k:9-10`) is a total, opaque,
   no-evaluators Boolean with no equation. It is result-bearing: it controls
   the helper's returned Boolean, every filter branch, heap 0, `sortVS`'s
   argument, heap 1, and the claimed result. It has no bridge-free connection
   theorem. Disposition: **illegitimate program-derived oracle**.

2. `filterOddAcc` plus its three rules (`verification.k:14-23`) is terminating
   and guard-complete for Int sequences, with disjoint true/false guards.
   Mathematically it filters according to `oddDigits`; it does not establish
   that this predicate means “all decimal digits odd.” Disposition:
   **sound only as an oracle-parameterized definitional summary; inadequate as
   the task's filter**.

3. `lastInput` plus two rules (`verification.k:25-28`) is terminating, total,
   and equals the old loop variable on empty input or the last list element.
   Disposition: **sound**.

4. `positiveInts` plus three rules (`verification.k:30-35`) is terminating;
   the Int and non-Int heads are disjoint, and it exactly expresses a finite
   sequence of integers greater than zero. Disposition: **sound**.

5. `digitLoopBody`, `oddDigitsBody`, `filterLoopBody`, and
   `uniqueDigitsBody`, with their macro rules (`verification.k:37-64`), expand
   exactly to the four corresponding AST regions in submitted
   `solution.mpy`. Disposition: **sound syntactic aliases**.

6. The priority-40 helper rule (`verification.k:76-82`) is an operational
   bridge. It preempts fixed closure dispatch for the exact submitted helper
   and produces `oddDigits(N)` without executing the helper body, parameter
   binding, loop, return, or frame lifecycle. Its match omits every cell other
   than `<k>` and accepts an arbitrary continuation. There is no bridge-free
   universal execution theorem or equation fixing its value. Disposition:
   **unsound/illegitimate**.

7. The priority-40 loop rule (`verification.k:90-109`) is an operational
   bridge. It preempts the real iterator loop and all helper calls, rewrites
   the loop variable and accumulator using the same unconnected oracle, and
   omits any guard fixing the `_all_digits_odd` binding in parent `P`.
   There is no exact auxiliary loop theorem. Disposition:
   **unsound/illegitimate**.

8. The entry claim (`spec.k:9-50`) has a satisfiable pristine
   configuration and the correct submitted module syntax. It constrains the
   return reference and heap, so it is not syntactically a free-result
   tautology. Its substantive postcondition is nevertheless only
   `sortVS(filterOddAcc(...))`, where the filter predicate is the same
   unconnected oracle that replaced execution. Disposition:
   **oracle-relative, not the requested correctness theorem**.

## False-conclusion witnesses

For the helper bridge and the loop summary, use the intended-domain input
`[2]`. Fixed Python execution and fresh LLVM/K execution return `[]` because
the helper computes false. The candidate places no equation on
`oddDigits(2)`, so `oddDigits(2) = true` is an admissible interpretation.
`stage4_wrong_oracle_verification.k` supplies exactly that ground
interpretation; `stage4_wrong_result_spec.k` then proves `#Top` for the false
heap result containing `2`. The command and zero exit are in
`stage4-kprove-wrong-result.log`.

Conversely, `stage4_correct_result_spec.k` asks the unmodified candidate
theory for the genuine empty filtered result on `[2]`. It fails with a
`WarnStuckClaimState` residual containing
`filterOddAcc(.ValSeq, vCons(2, .ValSeq))`; see
`stage4-kprove-correct-ground-result.log`.

The loop bridge also has an independent binding-sensitivity witness over the
same positive input: at its matched loop-head state, let parent `P` bind
`_all_digits_odd` to a closure returning false while interpret
`oddDigits(1)` as true. Fixed lookup/call execution leaves the accumulator
empty; the bridge, which never inspects `P`, appends `1`. Thus its complete
match domain is broader than any justification supplied by the entry claim.
