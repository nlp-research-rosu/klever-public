VALIDATED

## What is proven

Under the supplied MPY semantics, the exact translated body of
`rescale_to_unit` is partially correct for every symbolic finite list

```k
vCons(FIRST:Float, vCons(SECOND:Float, REST:ValSeq))
```

where `allFloatVS(REST)` holds and the supplied opaque float equality says that
the computed extrema differ.  `REST` is symbolic and unbounded; the theorem is
not a collection of fixed-size unrollings.

Starting from the initial MPY configuration, the theorem executes the module
load, import, function definition, name and builtin lookup, argument binding,
both extrema traversals, result-list allocation, source `for` loop, every
`append`, return, and frame pop.  It returns `ref(0)`.  Heap location `0`
contains, in input order, exactly

```k
scaleAcc(.ValSeq, INPUT, minVF(INPUT), maxVF(INPUT))
```

whose defining step appends

```k
divF(subF(element, minVF(INPUT)),
     subF(maxVF(INPUT), minVF(INPUT)))
```

for each input element.  The final stack is empty, `<ret>` is `noRet`,
`<exc>` is `NoExc`, and `<exit-code>` is `0`.

This is a K reachability proof of partial correctness.  It does not separately
claim a liveness theorem.

## Formal claims

`spec.k` contains four mutually supporting claims:

1. `SPEC.min-float-loop` proves the supplied float-min iterator fold for an
   arbitrary all-float tail using `minTailF`.
2. `SPEC.max-float-loop` proves the analogous float-max fold using `maxTailF`.
3. `SPEC.scale-loop` proves the exact source loop over an arbitrary all-float
   tail.  It records both observable heap growth and Python's final loop-target
   binding.
4. `SPEC.rescale-to-unit` loads and calls the exact program and establishes the
   caller-visible result and final configuration.

The positive command proves all four together so the three circularities are
available to the entry claim:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual output: `#Top`.  Actual exit status: `0`.

## Proof-extension inventory

This inventory was rebuilt from the final `verification.k` and `spec.k`.

### `allFloatVS`

- Class: definitional summary.
- Role and domain: a total recursive predicate over every `ValSeq`; the empty
  and constructor equations are exhaustive and disjoint.
- Matched context and justification scope: pure terms only; it neither matches
  nor replaces a computation or configuration.
- State footprint: none.
- Value influence and justification: restricts the claims to `List[float]`;
  its two constructor equations define that restriction.
- Dependents: all three loop claims and the entry claim.
- Validation: symbolic `REST` remains unbounded, and both constructor cases are
  exercised by the circularities.

### `definedProjectFloat`, `projectFloatTotal`, and the cast rules

- Class: derived guarded total projection.
- Role and domain: `definedProjectFloat(V) = isFloat(V)` characterizes the
  built-in partial cast.  `projectFloatTotal` is used only under that guard.
  Its collapse, two guarded orientation rules, and `#Ceil` characterization are
  the standard guarded-total projection equations.
- Matched context and justification scope: pure `Val`/`Float` terms.  On the
  guard, the value is already in the fixed semantics' `Float` subsort, so the
  total projection and partial cast denote that same value.
- Context containment: every use is beneath `isFloat(V)` or
  `allFloatVS(vCons(V, ...))`; no off-domain value is used.
- State footprint: none.
- Value influence and justification: exposes the already-existing float value
  to float-domain equations; it cannot manufacture a different guarded value.
- Dependents: extrema summaries, `scaleAcc`, and the dynamic subtraction twin.
- Validation: the static-sort collapse reduces `projectFloatTotal(F:Float)` to
  `F`; final `kprove` closes without any unguarded projection.

### Dynamic `applyBin("-")` twin

- Class: derived lemma.
- Role and domain: restates the supplied MPY-FLOAT equation
  `applyBin("-", F1:Float, F2:Float) = subF(F1,F2)` over a dynamic first
  operand, guarded by exactly `isFloat(V)`.
- Matched context and justification scope: only the pure dispatch term; no
  continuation, scope, heap, control, or exception cell is matched or skipped.
- Context containment: after guarded projection, its right-hand side is
  identical to the fixed static-sort equation.  On the overlap where `V` is
  already statically `Float`, the projection collapses and both equations agree.
- State footprint: none.
- Value influence and justification: affects each returned element, with value
  fixed by the supplied `subF` primitive.
- Dependents: `SPEC.scale-loop` and `SPEC.rescale-to-unit`.
- Validation: the complete source loop executes through fixed call, lookup,
  arithmetic dispatch, and append rules; the twin only repairs backend sort
  refinement.

### `minFOpaque`/`maxFOpaque` and the `minFloat`/`maxFloat` aliases

- Class: trusted primitive.
- Role and domain: isolates exactly the supplied `FLOAT.min` and `FLOAT.max`
  value operations, whose hooks are unavailable in the Haskell backend.
  The aliases accept every pair of `Float` terms.
- Matched context and justification scope: pure `minFloat(F1,F2)` or
  `maxFloat(F1,F2)` terms.  They do not match `#minAccF`, `#maxAccF`,
  `#iterNext`, a continuation, a binding, or any state cell.
- Context containment: the wrappers have the same complete two-float domain as
  the supplied primitives.  No broader configuration is accepted.
- State footprint: none; only a float value is abstracted.
- Value influence: extrema, the non-degeneracy precondition, and every result
  element.
- Value justification: conditional trust contract:
  `minFOpaque(F1,F2)` denotes the supplied `FLOAT.min(F1,F2)`, and
  `maxFOpaque(F1,F2)` denotes the supplied `FLOAT.max(F1,F2)`.
- Dependents: both extrema-loop claims and the entry claim.
- Control validation: not control-affecting; iterator seeding, traversal, and
  termination remain fixed-semantics execution.
- Value validation: the reference LLVM semantics executes the real primitives
  in seven hard-coded oracle cases, while `evidence.py` reports zero mismatches
  over 1,001 deterministic CPython cases.  This finite evidence supports but
  does not prove the primitive contract.

### `minTailF`, `maxTailF`, `minVF`, and `maxVF`

- Class: definitional summaries.
- Role and domain: exact accumulator descriptions of the supplied float folds.
  Empty, float-head, and non-float-head cases are exhaustive; the latter two
  have disjoint guards.  Recursive calls consume one constructor.
- Matched context and justification scope: pure summary terms; they do not
  replace source or fixed-semantics computation.
- State footprint: none.
- Value influence and justification: determine the extrema terms.  The float
  cases use exactly the trusted primitive aliases applied in the same order as
  the fixed folds.
- Dependents: extrema-loop claims, `scaleAcc`, the entry postcondition, and the
  non-degeneracy guard.
- Validation: `SPEC.min-float-loop` and `SPEC.max-float-loop` each print
  `#Top` as part of the full proof.

### `scaleAcc`

- Class: definitional summary.
- Role and domain: total accumulator definition over every `ValSeq`.  Empty,
  float-head, and non-float-head equations cover the full domain with disjoint
  guards and consume one constructor.
- Matched context and justification scope: pure summary terms only.
- State footprint: none in the definition; the corresponding reachability
  claim connects it to the actual heap update.
- Value influence and justification: characterizes the complete returned list.
  Its float step is definitionally the exact expression evaluated by the source
  followed by the exact `list.append` accumulator update.
- Dependents: scale-loop and entry claims.
- Validation: the false-result mutation reaches the correct `ref(0)` and
  `scaleAcc` heap yet fails against `noneV`.

### `lastVal`

- Class: definitional summary.
- Role and domain: total constructor recursion that records the final Python
  loop-target binding.
- Matched context and state footprint: pure definition; the scale-loop claim
  uses it to describe the one local scope entry actually written by
  `#bindTgt`.
- Value influence: local callee state only; the frame is later popped.
- Dependents: scale-loop.
- Validation: the closed plain function-frame shape eliminates the semantics'
  inapplicable closure-cell branch, and the loop claim prints `#Top`.

### Three circularity claims

- Class: derived reachability lemmas.
- Role and matched context:
  - min/max claims match the exact `#minAccF`/`#maxAccF` computation and frame
    every other cell unchanged;
  - the scale claim matches the exact `#loop`, exact body, plain function scope,
    result heap object, and arbitrary continuation.
- Justification scope and context containment: each claim's complete match
  domain is its stated symbolic configuration and precondition; there is no
  operational rewrite with a broader wildcard or continuation.
- State footprint: extrema claims change no state; the scale claim updates only
  `"number"` and heap object `H`, preserving all other configuration cells.
- Value influence and justification: their RHS summaries are fixed by the
  definitions above.
- Dependents: the entry claim.
- Validation: all close in the single successful `kprove` run.

There is no proof-local rule that returns from the user function, pops a frame,
intercepts the source call, replaces `min(numbers)` or `max(numbers)` as a
whole, or constructs the final list without executing the source body.

## Exact commands and actual outputs

The complete reproducible command sequence is `./prove.sh`.  The final run is
recorded in `prove-run.log` and exited `0`.

Key commands and observed results:

```bash
python3 py2mpy.py solution.py > solution.mpy
```

Exit `0`; the generated module contains the same body used by the entry claim.

```bash
python3 evidence.py
```

Output:

```text
ast-body-match: yes
cpython-differential: 1001 cases, 0 mismatches
```

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete_test.py > concrete_test.mpy
krun concrete_test.mpy --definition runtime-kompiled
```

All commands exited `0`.  `concrete-test.log` ends with `<k> .K </k>`,
`<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`.  LLVM compilation emits
the supplied semantics' existing non-exhaustiveness warnings for unrelated
helpers; none is on a reachable operation in these tests or claims.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Both exited `0`; `target-proof.log` contains exactly:

```text
#Top
```

False-return mutation:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual exit `1`.  `vacuity.log` contains `WarnStuckClaimState`; its residual
`<k>` is `ref ( 0 ) ~> .K`, which rejects the mutated `noneV` result.

Body-sensitivity mutation:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual exit `1`.  The mutation changes both copies of the exact function body
from `Return(Name("result"))` to `Return(Name("numbers"))`.
`body-mutation.log` contains `WarnStuckClaimState`; its residual returns the
symbolic input list instead of `ref(0)`.

## Gate results

### Gate A — PASS

- A1 program identity/body sensitivity: the entry claim contains the exact
  module AST from `solution.mpy`; `evidence.py` also confirms that the LLVM test
  body and solution body have identical CPython AST statement bodies.  The
  changed-return mutation fails with the expected list-valued residual.
- A2 operational state: no operational bridge skips a source or iterator
  region.  The entry claim observes result, scopes, scope allocator, heap, heap
  allocator, stack, return state, exception state, and exit code.
- A3 binding/evaluation/control: fixed semantics performs import, definition
  binding, builtin lookup, left-to-right call evaluation, frame push/pop,
  loop control, target binding, append dispatch, and return.
- A4 consistency: definitional cases are exhaustive, disjoint where guarded,
  and structurally recursive.  The subtraction twin agrees with the fixed rule
  on its overlap.  The only intentionally opaque proof-local values are the
  explicitly trusted aliases of supplied float primitives.
- A5 non-vacuity/result constraint: `[-3.0, 7.0]` is a concrete satisfying
  witness and finishes in the LLVM semantics with `[0.0, 1.0]`.  The
  false-return mutation exits `1` on the computed `ref(0)`.

### Gate B — PASS

- B1 domain: the structural first two floats plus arbitrary
  `REST:ValSeq`/`allFloatVS(REST)` cover arbitrary finite `List[float]` sizes
  from two upward.  The only value restriction is unequal computed extrema.
  Equal extrema are contract-inherently undefined: no linear function can map
  one identical value simultaneously to both `0` and `1`, and the Python
  formula divides by zero.
- B2 language model: collection, scope, heap, and control behavior are supplied
  MPY behavior.  Float extrema, subtraction, division, and equality are the
  supplied semantics' intentionally opaque numeric primitives; the theorem is
  complete relative to their named contracts, not a proof of IEEE-754 or real
  analysis.
- B3 summary/property: the connection from source execution to the exact
  elementwise formula is formally proved.  Interpreting that formula as
  sending the numerical minimum to `0` and maximum to `1` is conditional on the
  named float-primitive contracts and ordinary non-degenerate arithmetic.
- B4 implementation: the implementation computes that exact formula in input
  order and agrees with the prompt example.

### Gate C — PASS

- Every unproved primitive and dependent claim is listed below.
- Every claimed proof, mutation, concrete run, AST comparison, and
  differential test has an existing artifact and exact command in `prove.sh`.
- Formal, conditional, empirical, and excluded conclusions are separated in
  this report.

## Trust boundary

- The read-only reference MPY semantics, K compiler/prover, and supplied
  `py2mpy.py` translator are trusted infrastructure.
- `minFOpaque` and `maxFOpaque` are conditional aliases for the supplied
  `FLOAT.min` and `FLOAT.max` values.  They affect extrema, the domain guard,
  and the returned values, but no state or control.
- Supplied `subF` and `divF` determine each output float.  Supplied `eqF`
  determines the non-degeneracy precondition.  These affect values; `eqF` also
  determines theorem membership.  They do not bypass program-defined code.
- The theorem does not assume a program-derived oracle and has no trusted
  operational bridge.

## Empirically supported facts

- `concrete_test.py` is an LLVM/K artifact with seven hard-coded,
  independently stated expected lists, including the prompt example,
  two-element orderings, negative values, duplicates, and descending input.
  It has zero assertion failures and reaches `.K`, `NoExc`, exit-code `0`.
- `evidence.py` uses `sorted` endpoints as an independently written oracle,
  seed `20260729`, list lengths `2..20`, quarter-valued inputs in
  `[-50.0, 50.0]`, and excludes only equal-extrema samples.  Including the
  prompt example, all 1,001 cases match.
- These are finite adequacy checks, not universal proofs of the float
  primitives.

## Excluded behavior

- Lists shorter than two elements.
- Heterogeneous lists or lists whose elements are not MPY `Float` values.
- Equal-extrema inputs, for which the requested linear transform is
  mathematically inconsistent and the Python formula divides by zero.
- Any stronger claim about NaN, infinities, rounding error, or bit-level
  IEEE-754 behavior beyond the supplied named primitive contracts.
- Total-correctness/termination as a separate theorem.
