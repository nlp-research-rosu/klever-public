VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, the translated `search` function
is partially correct for every non-empty finite list of positive integers,
without a bound on list length or integer value.

The `search-program` claim loads the exact translated module, resolves
`search`, calls it with a heap-allocated list, executes both loops and the
function return/pop sequence, and proves that the result is:

```k
searchSummary(INPUT, INPUT, -1)
```

where:

- `frequencyOf(x, INPUT)` is the number of occurrences of `x`;
- `updateAnswer(a, x, n)` selects `x` exactly when `n >= x` and `x > a`;
- `searchSummary` folds that update over every input element.

Because every input element is positive, the initial accumulator `-1` is below
every qualifying value. Induction over the fold shows that the result is the
greatest input value whose frequency is at least its value, and remains `-1`
exactly when there is no such value. Repeated candidates do not change the
maximum.

The theorem observes the returned integer and preserves the input heap object,
heap location, call stack, return state, exception state, and exit code. The
final module binding of `search` is intentionally existential because the
contract does not observe a function object's internal representation.

## Formal claims

- `inner-loop`: for arbitrary finite `REM`, adds
  `frequencyOf(candidate, REM)` to the running frequency.
- `outer-loop`: for arbitrary finite `REM`, computes
  `searchSummary(REM, FULL, answer)`.
- `search-program`: proves the whole translated program for arbitrary non-empty
  `INPUT` satisfying `allPositive(INPUT)`.

The two loop claims are universal circularities, not bounded unrollings.

## Proof-extension inventory

### Guarded integer projection

- **Extension:** `isIntVal`, `definedProjectInt`, `projectIntTotal`, the
  `#Ceil` characterization, cast-orientation rules, collapse, and idempotence.
- **Class:** definitional summary and derived sort-refinement lemmas.
- **Semantic role:** exposes the existing `Int` subsort when a symbolic
  `Val` is constrained to be an integer; it does not skip a Python construct.
- **Domain/context:** projection contributes to the target only under
  `isIntVal(V)`. It matches pure terms, with no continuation, stack, binding,
  or state-cell context.
- **State footprint:** none.
- **Value influence:** projected integers feed equality, ordering, addition,
  frequency, branches, and the returned result.
- **Value justification:** the guarded projection is tied to K's partial
  `Val :> Int` cast; `projectIntTotal(I:Int) = I`. Outside the guard it has no
  evaluator and no target-dependent use.
- **Dependents:** all three claims.
- **Validation:** ground integers `1`, `2`, `3`, `4`, `5`, and `7` execute
  under the unchanged LLVM semantics; the projection collapse forbids an
  opposite interpretation on any actual `Int`.

### Guarded dispatch twins

- **Extension:** proof-local equations for `applyCmp("==", ...)`,
  `applyCmp(">=", ...)`, `applyCmp(">", ...)`, and `applyBin("+", ...)`.
- **Class:** derived lemmas.
- **Semantic role:** restates the corresponding frozen `MPY-INT` equation at
  the dynamic `Val` sort.
- **Domain/context:** both operands must satisfy `isIntVal`; these are pure
  function terms with no framed control or state.
- **State footprint:** none.
- **Value influence:** loop branches, frequency increments, and assignment of
  the answer.
- **Value justification:** after guarded projection, each right-hand side is
  textually the same integer operation as the existing `MPY-INT` rule. On the
  overlap where operands already have sort `Int`, both equations reduce to the
  same right-hand side.
- **Dependents:** `inner-loop`, `outer-loop`, and `search-program`.
- **Validation:** the unchanged LLVM definition executes the same operations
  in `concrete_tests.mpy`; the full symbolic proof closes with the guards
  implied by `allPositive`.

### Mathematical summaries

- **Extension:** `allPositive`, `frequencyOf`, `updateAnswer`, and
  `searchSummary`.
- **Class:** definitional summaries.
- **Semantic role:** name input-domain and result values without replacing
  program execution.
- **Domain/context:** all `ValSeq`/integer arguments. Empty/cons cases cover
  sequences; integer/non-integer guards are disjoint and exhaustive;
  `updateAnswer` partitions `N < X`, `N >= X and X <= A`, and
  `N >= X and X > A`.
- **State footprint:** none.
- **Value influence:** preconditions, loop postconditions, and the target
  result.
- **Value justification:** structurally recursive, descending equations over
  finite sequences. Their equations directly encode counting and maximum
  update.
- **Dependents:** all three claims.
- **Validation:** 20,030 independent CPython comparisons reported zero
  mismatches, and six translated assertion programs completed under LLVM.

### Loop circularities

- **Extension:** claims `inner-loop` and `outer-loop`.
- **Class:** machine-proved derived reachability lemmas.
- **Semantic role:** execute the exact fixed-semantics `#loop` configurations;
  they do not add operational rewrite rules.
- **Matched context:** arbitrary trailing `<k>` continuation, the active
  function environment and exact local bindings, a heap reference to the
  immutable input list, and framed unrelated configuration cells.
- **Justification scope/context containment:** the claims themselves prove the
  context-general reachability statements using the supplied semantics. The
  inner body contains no abrupt control. The outer claim reuses the proved
  inner claim and likewise preserves its continuation.
- **State footprint:** the inner loop writes only `frequency` and `item`; the
  outer loop writes only `answer`, `candidate`, `frequency`, and `item`. Both
  preserve `lst`, the referenced list, and all framed state.
- **Value influence:** their accumulator postconditions feed the returned
  result.
- **Dependents:** `outer-loop` depends on `inner-loop`;
  `search-program` depends on both.
- **Validation:** both are included in the successful all-claims `kprove`
  command. Changing the executed answer initialization from `-1` to `-2`
  makes the target proof fail.

There are no trusted primitives or operational bridges in the proof-local
theory.

## Reproducible commands and actual results

The complete runner is:

```sh
./prove.sh
```

It exited `0`. Its positive proof commands are:

```sh
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual `kprove` output: `#Top`; exit status: `0`. This single command proves
every claim in `spec.k`. The output is preserved in `kprove.log`.

Concrete execution used the required LLVM modules:

```sh
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy --definition runtime-kompiled
```

Actual final state: `<k> .K </k>`, `<exc> NoExc </exc>`, and exit code `0`.
This covers the three prompt examples and `[1]`, `[2]`, and
`[7,7,7,7,7,7,7,1]`. Output is preserved in `krun.log`.

Program identity:

```sh
python3 py2mpy.py solution.py > solution.mpy
python3 check_program_identity.py
```

Actual output: `program identity: PASS`. The checker compares the translated
module with the balanced `#loadAll` term embedded in `spec.k`, and also checks
that the concrete test artifact contains the same function AST.

Independent differential evidence:

```sh
python3 differential_test.py
```

Actual output: `cases=20030 mismatches=0`. The oracle directly filters distinct
values using Python's `list.count` and takes `max`, independently of the K fold
equations. The scope is every list of lengths 1 through 6 over values 1 through
5, plus 500 deterministic random lists of lengths 1 through 30 over values 1
through 30.

Negative validation probes:

```sh
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Both exited `1`, printed `WarnStuckClaimState`, and did not print `#Top`.
`spec-vacuity.k` requires the false off-by-one result and leaves
`searchSummary(...) +Int 1 = searchSummary(...)` unmet.
`spec-body-mutation.k` changes the executed initialization to `answer = -2`
while retaining the original postcondition and leaves
`searchSummary(...,-2) = searchSummary(...,-1)` unmet. Residuals are preserved
in `vacuity.log` and `body-mutation.log`.

The compiler warnings in the logs originate in unrelated portions of the
supplied read-only reference semantics; compilation and the selected execution
paths complete successfully.

## Gate results

- **Gate A — PASS.** The exact translated body is loaded, bound, called, and
  executed. No program-defined operation is replaced. State footprints and
  dynamic integer refinement are accounted for. The precondition is realizable
  (for example `[1]`). Both false-result and body-sensitivity mutations are
  rejected.
- **Gate B — PASS.** The formal domain is every non-empty finite list whose
  elements are positive integers, with no length or value bound. The recursive
  result definition is exactly the greatest qualifying value or `-1`, matching
  the prompt and all examples.
- **Gate C — PASS.** The proof, program-identity check, concrete semantics
  tests, differential oracle, mutation artifacts, logs, and exact commands are
  present and reproducible.

## Trust boundary and excluded behavior

Trusted components are the supplied unchanged `reference-semantics/`, K
v7.1.293 (including its Haskell backend and SMT reasoning), the fixed
`py2mpy.py` translator, and the host Python used only for finite testing.

The formal theorem is partial correctness under the supplied semantics. It does
not prove general CPython behavior outside that semantics, inputs outside the
prompt's non-empty positive-integer-list precondition, resource bounds, or a
separate liveness theorem. These are not restrictions within the HumanEval
contract proved here.
