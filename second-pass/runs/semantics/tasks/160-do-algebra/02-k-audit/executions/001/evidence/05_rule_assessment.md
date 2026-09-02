# Rule-by-rule assessment index

`05_rule_inventory.txt` is the exhaustive line-addressed inventory: 26 sources,
231 syntax declarations, 703 rules, 146 function declarations, 108 `total`
declarations, no `functional` declarations, 22 opaque declarations, 45
priority rules, no simplification rules, and ten reachability claims. The
following table gives the review decision for every rule in each source; the
eight candidate-local rules are then decided individually.

| Source | Rules | Decision for all inventoried rules in that source |
|---|---:|---|
| `semantics/assert.k` | 3 | Supplied baseline; unreachable in proof. Concrete assertions were used only in the independent LLVM smoke artifact. |
| `semantics/bool.k` | 13 | Supplied baseline; general BoolOp/ref rules unreachable. `truthy` consumers used by `If`/`While` are faithful on Bool comparison results. |
| `semantics/builtins.k` | 137 | Supplied baseline. Only `applyBuiltin("len")`, `seqLen(list)`, and `vsLen` are reachable; they exactly compute the operator-list length. Other rules, including opaque `md5hexCodes`, are unreachable and cannot affect closure. |
| `semantics/call.k` | 21 | Supplied baseline. Generic call routing, builtin dispatch, closure call, and frame creation are reachable and preserve callee binding, left-to-right argument evaluation, continuation, environment, stack, and scope allocation. Ref/method/annotated-closure paths are unreachable. |
| `semantics/comprehension.k` | 7 | Supplied baseline; unreachable. |
| `semantics/concrete.k` | 16 | Supplied LLVM-only baseline; absent from the Haskell proof definition. Its rules were used only by concrete reconstruction, with no proof dependency. |
| `semantics/controls.k` | 34 | Supplied baseline. Plain assignment, integer augmented assignment, `If`, and `While` paths are reachable and match the submitted control flow. Import, `For`, loop-control, ref, and cell paths are unreachable. |
| `semantics/core.k` | 46 | Supplied baseline. Configuration, module loading, sequencing, lexical lookup, literals, builtin scope, argument evaluation, and sequence-length helpers are reachable and preserve all claim-visible cells. Allocation/cell/keyword paths are unreachable. |
| `semantics/dict.k` | 28 | Supplied baseline; unreachable. |
| `semantics/float.k` | 121 | Supplied baseline; unreachable. All 19 float opaque symbols have zero influence on these claims. |
| `semantics/functions.k` | 15 | Supplied baseline. Plain definitions, parameter binding, return, and frame pop are reachable and execute the actual bodies. Annotated closure/cell paths are unreachable. |
| `semantics/int.k` | 16 | Supplied baseline and reachable. Integer arithmetic/comparison equations are ordinary mathematics. `pyMod`/floor division agrees with Python for every nonzero divisor; all floor-division claims force positive divisors. Exponent rules require nonnegative exponents, as supplied operands do. |
| `semantics/iter.k` | 0 | Declaration only; unreachable. |
| `semantics/list.k` | 27 | Supplied baseline. Bare `list(ValSeq)` inputs are used structurally; iteration, construction, mutation, membership, concat, and deep equality are unreachable. |
| `semantics/methods.k` | 75 | Supplied baseline; unreachable. |
| `semantics/operators.k` | 10 | Supplied baseline. Generic unary/binary/compare dispatch is reachable and uses declared strict/context evaluation. Heap-ref bridge rules are unreachable because claim inputs stay bare read-only lists. |
| `semantics/range.k` | 6 | Supplied baseline; unreachable. |
| `semantics/set.k` | 12 | Supplied baseline; unreachable. |
| `semantics/sort.k` | 19 | Supplied baseline; unreachable. Opaque `sortVS`/`sortKeyVS` cannot influence any branch, result, state, or postcondition here. |
| `semantics/str.k` | 28 | Supplied baseline. ASCII literal conversion and equality are reachable and exact for `+`, `-`, `*`, `//`, and `**`; other string rules are unreachable. |
| `semantics/subscript.k` | 40 | Supplied baseline. Object/index evaluation and in-bounds bare-list access are reachable. Valid list lengths and the recursive bounds maintain in-bounds indices. Slice/ref paths are unreachable. `valSeqAt` is over-broadly `total` for OOB indices but no false conclusion witness lies on a claim path. |
| `semantics/syntax.k` | 0 | Syntax declarations only; the used production map is in `05_used_construct_map.md`. |
| `semantics/tuple.k` | 21 | Supplied baseline; unreachable. |

Candidate-local `verification.k` decisions:

1. `solutionProgram` (`verification.k:7-82`) is a macro definition, not an
   execution shortcut. Fresh `kast --expand-macros` output is byte-identical to
   parsing `solution.mpy`.
2. `plusV`, `minusV`, `timesV`, `floorDivV`, and `powerV`
   (`verification.k:85-94`) are macro equations for the exact ASCII code
   sequences 43, 45, 42, 47/47, and 42/42. They are true and disjoint.
3. `floorQuot` (`verification.k:97-98`) is a definitional result summary, not an
   operational bridge. Its equation equals Python floor division for every
   divisor used by a claim. The unguarded `[total]` declaration includes
   divisor zero, where `pyMod`/division is undefined; this is an off-domain
   coverage defect, not a demonstrated false conclusion, and no claim admits
   zero at a floor-quotient use.
4. `runDoAlgebra` (`verification.k:100-104`) is a launcher: it expands to
   `#loadAll(solutionProgram)` followed by an ordinary call to the real
   `do_algebra`. It neither returns, pops a frame, fabricates state, nor
   summarizes `_evaluate`; every program body executes under fixed semantics.

There are no candidate-local opaque symbols, priority rules, simplification
rules, auxiliary claims, loop circularities, or program-execution bridges.
