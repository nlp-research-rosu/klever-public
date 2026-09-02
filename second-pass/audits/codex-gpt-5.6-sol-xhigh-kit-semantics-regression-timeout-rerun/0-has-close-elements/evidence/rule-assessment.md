# Rule-by-rule assessment key

The exhaustive line-addressed population is `rule-inventory.md` (26 files,
725 rules, 239 syntax declarations, 116 `total` declarations, no `functional`
declarations). This document records the decision applied to every population
segment and expands every candidate-authored segment.

## Supplied-semantics population

Every declaration and rule under `reference-semantics/` is byte-identical to
the trusted SUPPLIED_SEMANTICS tree. Accordingly:

- every one of its 695 rules (725 total minus 30 in `verification.k`) is
  classified `ACCEPTED_FIXED_SEMANTICS`, not a candidate proof extension;
- all used generic rules and operator-specific rules were additionally checked
  against the actual constructor path in `used-construct-map.md`;
- declarations/rules for unused constructors (dicts, sets, strings, sorting,
  comprehensions, ranges, subscripting, methods, unrelated builtins, and
  unrelated numeric operations) cannot match the reachable program terms
  because their constructor, operation string, or callable guard is disjoint;
- supplied opaque symbols are accounted for in REVIEW stage 7. Only `subF`,
  `absF`, and `floatLt` occur in the theorem's result path.

This is the semantics level selected by the rendered mode. It is an explicit
trust boundary rather than a candidate lemma. No supplied rule was found to
conflict with the used execution slice.

## Candidate `verification.k` population

| Lines / exact population | Count | Decision | Coverage, overlap, descent, and truth check |
|---|---:|---|---|
| 8-33, `HC-INNER-BODY`, `HC-OUTER-BODY`, `HC-FUNCTION-BODY` declarations and macro rules | 3 rules | `SOUND_MACRO` | Exact nested constructor subtrees of byte-identical `solution.mpy`; no executing term is summarized. Fresh module execution expands to the entry closure body. |
| 37-40, `allFloatVS` | 2 | `SOUND_DEFINITION` | Empty/cons cases are disjoint and exhaustive; cons recursion strictly descends. |
| 46-49, guarded `applyBin("-")` simplification | 1 | `SOUND_DERIVED` | `isFloat(X) ∧ isFloat(Y)` makes both downcasts defined. RHS is identical to supplied `applyBin("-", F1:Float, F2:Float) => subF(F1,F2)`; overlap agrees exactly. |
| 53-58, `closeVals` and its simplification | 1 | `SOUND_CONSERVATIVE_DEFINITION` | Fresh total uninterpreted Bool symbol. On every target-reachable use, both Val arguments satisfy `isFloat`, and the equation identifies it with exactly `floatLt(absF(subF(X,Y)),T)`. It asserts neither truth nor falsity and does not encode pair scanning. Off-domain interpretations are irrelevant and unconstrained without inconsistency. |
| 62-85, `rowClose` | 5 | `SOUND_DEFINITION` | Empty versus cons is exhaustive. On cons, `I<J` versus its negation partitions the index guard; when true, Float/non-Float cases partition both operands. Recursive cases descend on the sequence tail. Intended claims use only the both-Float branch. |
| 89-100, `closeRows` | 3 | `SOUND_DEFINITION` | Empty/cons and `isFloat(F)`/negation are exhaustive and disjoint; recursion descends on the outer tail. |
| 102-104, `hasClose` | 1 | `SOUND_DEFINITION` | Universal one-step wrapper instantiating `closeRows(VS,VS,T,0)`. |
| 108-115, `lastV` | 3 | `SOUND_DEFINITION_AND_LEMMA` | Empty/cons base equations are exhaustive and descending. Idempotence is true: empty yields the default twice; nonempty yields the same final element. Overlaps normalize to identical RHS values. |
| 117-121, `advance` | 2 | `SOUND_DEFINITION` | Empty/cons exhaustive; recursion descends and adds one per element. |
| 123-130, `outerJ` | 3 | `SOUND_DEFINITION_AND_LEMMA` | Empty preserves incoming `j`; nonempty records the completed inner-scan length. Absorption overlaps both base cases only at the same `advance(0,ALL)` value. |
| 132-139, `outerOther` | 3 | `SOUND_DEFINITION_AND_LEMMA` | Empty preserves incoming `other`; nonempty gives the last inner element. Absorption overlaps at the same `lastV` value. |
| 141-143, `orBool` associativity | 1 | `SOUND_MATHEMATICS` | Boolean truth-table identity; orientation only reassociates rightward. |
| 153-185, inner operational bridge | 1 | `SOUND_DERIVED_BRIDGE` | Same arbitrary suffix, complete nine-cell context, bindings, exact caller frame, and guard as `SPEC-INNER.inner-loop`, which closes without this rule. It changes only `result`, `j`, and `other`. Fixed and extended observable-continuation claims both close; changed-body increment is rejected. |
| 195-225, outer operational bridge | 1 | `SOUND_DERIVED_BRIDGE` | Exact `REM=ALL`, `RB=false`, `I=J=0`, dummy-Float instance of `SPEC-OUTER-STATE.outer-loop-state`, which closes without this bridge. It changes the five loop locals only; Return and frame cleanup remain fixed-semantics steps. Fixed and extended observable-continuation claims both close. |

Total candidate rules assessed above: 30. The 12 candidate syntax declarations
are the three exact macros, eight structural/function declarations, and the
fresh `closeVals` declaration. All nine `total` declarations have either
exhaustive constructor equations or, for `closeVals`, an explicit total
uninterpreted interpretation with a guarded definition on every theorem use.
There are 11 simplification rules and two priority rules, all listed above.
There are no candidate `functional` declarations.

## Claim population

All four claims in `spec.k` were separately selected and reconstructed:

- `SPEC-INNER.inner-loop`: exact inner body under `VERIFICATION-BASE`;
- `SPEC-OUTER-STATE.outer-loop-state`: exact outer body under
  `VERIFICATION-INNER`;
- `SPEC-OUTER.outer-loop`: outer body plus exact Return/frame-pop continuation
  under `VERIFICATION-INNER`;
- `SPEC.target`: exact closure call under `VERIFICATION`.

Each exited zero and printed exact `#Top`. Their adequacy is stated in REVIEW
stage 4. No inventoried rule is labeled unsound, so there is no unsound-rule
false-conclusion witness to report.
