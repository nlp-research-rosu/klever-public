# Proof-local extension review

The exhaustive machine inventory is `rule-inventory.tsv`. This file records the
manual disposition of all 24 `verification.k` items and both `spec.k` claims.

## Closed AST macros

`GRADE-STEP` (`verification.k:8-46`) and `GRADE-PROGRAM`
(`verification.k:48-57`) are syntax macros with closed right-hand sides. They
have no runtime cell match, guard, state footprint, fresh value, priority, or
opaque symbol. Their class is a definitional AST abbreviation. Fresh `kast
--expand-macros` output for `GRADE-PROGRAM` is byte-identical to the trusted
regeneration of `solution.mpy` (see `stage4/program-identity.log`). The
reviewer body mutation changes this executed module term, the constructor terms
then differ, and the ground entry proof rejects the old result
(`stage5/body-mutation-run.log`).

## Domain functions

`isGradeNumber` (`verification.k:60-61`) has one universal equation:
`isInt(V) orBool isFloat(V)`. It is total and does not touch execution state.
On this `Val` algebra, the two tests denote disjoint `Int` and `Float`
injections.

`allGradeNumbers` (`verification.k:63-66`) has exactly the empty and `vCons`
constructor cases. They are disjoint and exhaustive, and recursion strictly
descends through the tail. It affects only claim admissibility and the guards
of the two derived comparison lemmas.

## Numeric twins

`gradeEq` (`verification.k:71-75`) and `gradeGt`
(`verification.k:77-81`) are total definitional summaries.

- The `Int` equations exactly reproduce fixed
  `applyCmp("==", Int, Float)` and `applyCmp(">", Int, Float)` from
  `semantics/float.k:142-150`.
- The `Float` equations exactly reproduce fixed
  `applyCmp("==", Float, Float)` and `applyCmp(">", Float, Float)` from
  `semantics/float.k:41-44,125-127`.
- The nonnumeric equations are guarded by
  `notBool isGradeNumber(V)`, so they do not overlap either numeric case.

The three domains are exhaustive and pairwise disjoint. `eqF`, `gtF`, and
`intToF` are fixed, result-bearing opaque primitives in the supplied semantics,
not proof-local inventions. Both execution and postcondition depend on the
same fixed primitive interpretation; the proof is parametric in it. LLVM
concrete execution and Python differential testing support—but do not
universally prove—the intended IEEE/Python interpretation.

## Derived comparison simplifications

The only `[simplification]` rules in the entire proof source are
`verification.k:84-91`.

Their complete match domains are the pure function terms
`applyCmp("==", V, F)` and `applyCmp(">", V, F)` under
`isGradeNumber(V)`. They have no continuation, binding, stack, heap, or other
cell context. For the only two satisfying constructors, their right-hand sides
reduce to the exact fixed right-hand sides listed above. No other constructor
satisfies the guard. The fixed rules and simplifications therefore agree on
every overlap; there is no result-bearing oracle or operational bridge.

## Result definitions

`gradeValue` (`verification.k:95-133`) is a one-equation total function. Its
thirteen outcomes use the same equality/strict-greater atoms and ordering as
the submitted branch chain. It does not rewrite a program term.

`gradeAcc` (`verification.k:137-143`) has exactly the empty and `vCons` cases,
which are disjoint and exhaustive. Each step appends one `gradeValue` through
fixed `valSeqConcat` and strictly descends through the input tail. It does not
read or write any cell.

Both are result-bearing definitions, but neither replaces execution. The
machine-checked loop circularity connects actual per-iteration comparison,
branch, string construction, and heap append behavior to these definitions.
The body mutation produces `"Z"` (code 90) and gets stuck against the expected
`"A+"`, demonstrating this connection is body-sensitive.

## Claims

`SPEC.loop-invariant` (`spec.k:6-29`) is a circularity, not a compiled
ordinary rule. Its domain is any finite numeric `VS`, any `ACC`, a real
`#loop(list(VS), Name("grade"), GRADE-STEP)` redex, the named local bindings,
and a heap list at `H`. It preserves the arbitrary following continuation and
all framed cells, changes only the loop variable and heap list as fixed
execution does, and constrains the result to `gradeAcc(ACC, VS)`.

`SPEC.entry` (`spec.k:31-55`) starts from the complete initial configuration,
loads the exact submitted module, calls the exact bound function on
`list(VS)`, and requires arbitrary finite `Int`/`Float` elements. It constrains
the returned value to `ref(0)`, the exact output heap list, allocation
counters, caller environment, stack, return state, exception state, and exit
code. Only the final scope map is existential because it is not part of the
requested returned list property.

No proof-local operational bridge, priority rule, opaque symbol,
`no-evaluators` declaration, fresh result oracle, or ordinary `<k>` rewrite
exists. No local item is classified unsound, so no false-conclusion witness is
applicable.

