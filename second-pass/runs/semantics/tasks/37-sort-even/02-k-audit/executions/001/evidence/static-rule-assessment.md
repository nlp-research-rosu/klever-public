# Static rule assessment

This assessment is keyed to the exhaustive machine-generated inventory in
`k-rule-inventory.txt` / `k-rule-inventory.json`.  The inventory covers all 26
K source files used in the clean reconstruction: 956 top-level records
(236 syntax declarations, 712 rules, five contexts, one configuration, and two
claims).  It also indexes every occurrence of `function`, `total`, `symbol`,
`no-evaluators`, `priority`, `simplification`, `concrete`, `owise`, and
strictness attributes.  There are no `functional` declarations.

## Supplied-semantics module decisions

The top-level `reference-semantics/semantics.k` has no local rules: it assembles
the fixed `MPY` proof module and the `MPY-KRUN` concrete module.  The following
table accounts for every declaration/rule record in its helper files.

| File | Inventory | Reachability and decision |
|---|---:|---|
| `syntax.k` | 16 syntax | All submitted `.mpy` constructors parse through these declarations. `BinOp` is left-to-right `seqstrict`; assignment RHS, `For` iterable, `Return`, and expression statements have the strictness needed by this program. Accepted at the supplied-semantics level. |
| `core.k` | 37 syntax, 46 rules, 1 configuration | Reached rules cover initial cells, module loading, sequencing, name lookup, builtins scope, left-to-right call arguments, literals, list helpers, length, and allocation. They preserve the cells used by the theorem. Cell/keyword/truthiness/write helpers are either guarded and non-overlapping or not reached. Accepted. |
| `iter.k` | 1 syntax | Declares the iterator protocol used by `For`; behavior is supplied by type modules. Accepted. |
| `list.k` | 5 syntax, 27 rules | Reached rules implement list iteration, list literal allocation, concatenation/allocation, and in-place `append`. `append` changes only the addressed heap list, returns `noneV`, and appends exactly one value. Other comparison/membership rules are not reached. Accepted. |
| `subscript.k` | 15 syntax, 40 rules, 2 contexts | Reached rules dereference a list, evaluate slice bounds in order, normalize positive-step slices, build the even/odd/suffix subsequences, and read list indices. For this program every concrete index is in bounds if `sortVS` has its named permutation/length contract. The total but intentionally underspecified `valSeqAt` on opaque/OOB sequences is a trust limitation, not a proof of bounds. Accepted conditionally on the fixed sort contract. |
| `controls.k` | 3 syntax, 34 rules | Reached rules implement local assignment, integer `AugAssign`, expression discard, one-time list dereference for `For`, iterator stepping, and loop continuation. The loop does not mutate its iterated `odds` list. Import/branch/while/break rules are inert. Accepted. |
| `tuple.k` | 4 syntax, 21 rules | Only `#bindTgt(Name(...), V)` is reached by `For`; it updates the current local map and preserves other cells. Tuple behavior is inert. Accepted. |
| `functions.k` | 4 syntax, 15 rules | Reached rules load the function closure, bind one plain parameter, handle `Return`, restore the caller, and deallocate only the local frame. The submitted function creates no escaping closure. Accepted. |
| `call.k` | 3 syntax, 21 rules | Reached rules evaluate callee then arguments, dereference list arguments for `sorted`/`len`, preserve references for mutating `append`, dispatch the closure, and push its frame. Priorities select structural dereference without changing observable state. Accepted. |
| `builtins.k` | 38 syntax, 137 rules | Only the ordinary `len(list(VS)) = vsLen(VS)` path is reached. All other builtin names/helpers are syntactically disjoint from this program and cannot encode its answer. The inactive `md5hexCodes` is opaque but has no dependent path. Accepted/inert. |
| `sort.k` | 6 syntax, 19 rules | The reached `sorted(list(VS))` rule allocates `list(sortVS(VS))`. `sortVS` is the supplied semantics' explicit result-bearing opaque primitive; its concrete insertion-sort equations handle integer/string ground lists, while symbolic proof uses the named contract. No candidate rule defines its value. Accepted as an external trust boundary, with an intent-validation concern because ascending/permutation/length are not proved in this K theorem. Keyed/reverse/in-place sort paths are inert. |
| `operators.k` | 10 rules, 2 contexts | Reached rules dereference the two list operands of final `+` in left-to-right order; the list-specific priority rule then allocates the result. Comparison/unary paths are inert. Accepted. |
| `int.k` | 1 syntax, 16 rules | Integer literal and `i += 1` use the ordinary `+Int` equation. Other integer operators are inert. Accepted. |
| `assert.k` | 3 rules | Not reached by `solution.mpy`; reached only by reviewer concrete-test programs, where failed assertions set the exit cell. Inert for the proof. |
| `concrete.k` | 5 syntax, 16 rules | Imported only by the LLVM `MPY-KRUN` build. Its keyed-sort and deep-equality rules do not match this program's unkeyed integer sort. Inert for symbolic proof. |
| `bool.k` | 13 rules, 1 context | No boolean operation occurs in the submitted body. Inert. |
| `comprehension.k` | 3 syntax, 7 rules | No comprehension occurs. Inert. |
| `dict.k` | 12 syntax, 28 rules | No dictionary syntax/value occurs. Inert. |
| `float.k` | 34 syntax, 121 rules | No float or intercepted math call occurs. Its 20 float-related opaque symbols are outside every submitted redex/postcondition. Inert. |
| `methods.k` | 27 syntax, 75 rules | Declares generic method dispatch, but none of its string/list-count methods matches `append`; list `append` is handled in `list.k`. All local method equations are inert. |
| `range.k` | 2 syntax, 6 rules | No range occurs. Inert. |
| `set.k` | 6 syntax, 12 rules | No set occurs. Inert. |
| `str.k` | 5 syntax, 28 rules | No program string value/operator occurs. `strLt` is used only by the concrete string-sort branch, not the intended integer domain. Inert for the theorem. |

Unused subset rules were checked for generic left-hand sides that could overlap
the reached syntax. Their dispatch is constructor-, value-sort-, builtin-name-,
operator-, or method-name-specific; none can rewrite the submitted path or the
postcondition. They are therefore accepted at the supplied-semantics boundary
without claiming that this deliberately small language is a complete model of
all Python behavior.

## `verification.k` decisions (all 26 records)

| Lines | Records | Class and decision |
|---|---|---|
| 7–14 | `loopBody` syntax/equation | Definitional expansion. It is exactly the three statements in `solution.mpy`'s `For` body. Total, one equation, no overlap. Accepted. |
| 16–36 | `sortEvenBody` syntax/equation | Definitional expansion of all statements in the submitted function body, including `loopBody`. Total, one equation. Accepted. |
| 38–39 | `sortEvenClosure` syntax/equation | Definitional closure with the submitted singleton parameter, exact body, and module environment 0. Accepted. |
| 44–47 | singleton `#bindP` priority rule | Administrative operational bridge. Its match requires the current scope map to be exactly empty. Fixed rules `functions.k:64–66` then `functions.k:63` instantiate to the same singleton binding and preserve continuation/all other cells; the higher-priority cell-binding guard is false on `.Map`. No binding, value, control, state, or exception difference exists over the match domain. A bridge-free Haskell connection attempt remains stuck at the known narrowing ambiguity this rule resolves; the exact static two-step derivation and LLVM function calls support soundness, but absence of a closing universal connection artifact is an evidence concern. |
| 51–64 | `evenIndices`, `oddIndices` declarations/equations | Definitional summaries using the same `slStart/slStop/slStep/buildVS` functions used by real `Subscript`. Each has one total equation. For positive step 2 they denote indices 0,2,… and 1,3,… respectively. Accepted. |
| 67–72 | `pairedVS` declaration/two equations | Structural recursion over the unconsumed odd sequence, appending the corresponding sorted-even value and unchanged odd value. Cases are constructor-disjoint, exhaustive for `ValSeq`, and recursive descent is strict. Accepted. |
| 74–77 | `advancedIndex` declaration/two equations | Structural length accumulator over the same odd suffix. Constructor-disjoint, exhaustive, descending. Accepted. |
| 81–87 | `evenSuffix` declaration/equation | Reuses supplied slice helpers for `EVS[len(OVS):]`, exactly the source's final slice. Accepted. |
| 89–91 | `assembledEvenSort` declaration/equation | Transparent name for `pairedVS(...,0)` concatenated with the remaining even suffix. It does not replace execution or assert ordering. Accepted. |
| 96 | right identity of `valSeqConcat` | Mathematical simplification. It agrees with both fixed concat equations on their overlaps. Accepted. |
| 97–101 | associativity of `valSeqConcat` | Mathematical simplification oriented from left- to right-nesting; agrees with fixed concat, does not create values, and reduces left nesting. Accepted. |
| 106–114 | `"$cells" in_keys(...)` simplification | The five explicit keys are concrete strings different from `"$cells"`; well-formed map concatenation makes them disjoint from the framed remainder. The rule simply strips impossible keys and descends to `M`. Accepted. |
| 118 | `#observeResult` syntax | Fresh specification-only observer, not a Python construct. Accepted. |
| 119–124 | two observer rules | Fully split by total `isRefV`: a reference is read from the heap without mutation; a non-reference is unchanged. They run only after the real call and cannot fabricate a value. Accepted. |

There are no candidate-local opaque symbols, `no-evaluators` declarations, or
answer-encoding priority rules.  The only result-bearing opaque symbol reached
is the fixed supplied `sortVS`.

## Claims

- `loop-correct` executes the actual fixed iterator/binding/body rules for any
  odd suffix.  It changes only `i`, `odd`, and the `result` heap entry as the
  real loop does; it preserves `evens`, `odds`, the rest of the heap, and the
  arbitrary continuation `K`.
- `sort-even-correct` executes `sortEvenClosure`, which expands to the submitted
  body.  The result is forced through `#observeResult` to the structural list
  `assembledEvenSort(sortVS(evenIndices(VS)), oddIndices(VS))`; it is not an
  existential result, implication-only property, or tautology.

No inventoried candidate rule has a false-conclusion witness on the intended
integer-list domain.  Accordingly, none is labeled unsound.  The two narrower
evidence gaps are the non-closing bridge-free Haskell connection attempt for the
administrative bind specialization and the external `sortVS` meaning/length
contract.
