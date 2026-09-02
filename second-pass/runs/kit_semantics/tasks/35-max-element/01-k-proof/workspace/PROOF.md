VALIDATED

## What is proven

`solution.py` implements:

```python
def max_element(l: list):
    return max(l)
```

The K claims prove partial correctness of the exact translated body.  They
start from module loading, bind `max_element`, call it through MPY's ordinary
name lookup and function-frame rules, evaluate the program-defined body, look
up the fixed `max` builtin, and execute MPY's iterator folds.  The final result
is the corresponding recursive maximum summary, and the claims also require
the final environment, scope allocation counter, heap, heap counter, stack,
return cell, exception cell, and exit code to have their stated values.

The required target is unbounded.  Four entry claims collectively cover every
nonempty list for which the supplied MPY semantics defines `max`:

- `SPEC.max-element-int-head`: an integer head and an arbitrary finite
  numeric tail;
- `SPEC.max-element-float-head`: a float head and an arbitrary finite numeric
  tail;
- `SPEC.max-element-bool-head`: a Boolean head and an arbitrary finite
  numeric tail;
- `SPEC-STR.max-element-str-head`: a string head and an arbitrary finite
  string tail.

Here numeric means any mixture of MPY `Int`, `Bool`, and `Float`.  The recursive
`allNumericVS` and `allStrVS` preconditions do not bound list length.

The companion circularities are
`SPEC.max-int-numeric-acc`, `SPEC.max-float-numeric-acc`,
`SPEC.max-general-numeric-acc`, and `SPEC-STR.max-general-str-acc`.  Their base
case consumes an empty remainder, their step case consumes one constructor,
and the entry claims instantiate them after the first element seeds MPY's
fold.

## Formal postcondition

The numeric claims return `maxIntNumericVS`, `maxFloatNumericVS`, or
`maxNumericGeneralVS` according to MPY's accumulator state.  The string claim
returns `maxStrGeneralVS`.  Each summary recursively keeps the old candidate
unless the next value is strictly greater, so ties retain the first maximal
element, matching Python and the supplied MPY builtin.

This is a partial-correctness result under the supplied semantics and the
float trust boundary below.  It does not separately prove termination.

## Proof-extension inventory

No rule intercepts `Call`, function lookup, argument evaluation, return,
`#maxAcc0`, or any program-defined body.

### Guarded projections

- Extensions: `projectIntTotal`, `projectFloatTotal`,
  `projectBoolTotal`, and `projectStrTotal`, including their `#Ceil`
  characterizations, guarded cast orientations, and static-sort collapses.
- Class: derived lemmas/guarded total projections.
- Domain: each orientation is guarded by the matching generated sort
  predicate; collapse applies only to a value already in the target sort.
- Matched context and state footprint: pure value terms in arbitrary pure
  contexts; no configuration cell, continuation, binding, control, exception,
  or state is read or changed.
- Value influence and justification: they expose exactly the fixed partial
  subsort cast under its definedness guard.  They cannot manufacture an
  off-sort value.  The `#Ceil` equations and `preserves-definedness`
  orientations are the guarded-total-projection construction.
- Dependents: all symbolic accumulator claims.
- Validation: ground collapse is exercised throughout `smoke.mpy`; the
  false-result mutation rejects the opposite numeric result.

### Domain and view definitions

- Extensions: `isNumericV`, `allNumericVS`, `allStrVS`, `codesOf`, and
  `numericView` with constructors `nInt`, `nBool`, `nFloat`, and `nOther`.
- Class: definitional summaries.
- Domain and coverage: `allNumericVS` and `allStrVS` have disjoint
  empty/cons equations and structurally descend.  `numericView` covers the
  three mutually exclusive numeric sorts plus the exact negation
  `notBool isNumericV(V)`.
- Matched context/state footprint: pure values and raw `ValSeq`
  constructors only; no operational context or state.
- Value influence and justification: the view only tags an existing value
  and each tag contains the guarded exact projection.
- Dependents: comparison dispatch, summary functions, and every positive
  claim.

### Comparison lemmas

- Extensions: the eleven equations of total `numericGt`; the numeric and
  string simplifications of `applyCmp(">")`; and the three sort-disjointness
  simplifications.
- Class: derived lemmas.
- Domain: all `NumericView` pairs (the two overlapping `nOther` cases both
  return `false`), numeric `Val` pairs, string `Val` pairs, and the exact
  generated-sort guards.
- Matched context/state footprint: only pure comparison terms; no
  continuation, frame, binding, heap, exception, or control state.
- Value influence: these Booleans select whether the general fold replaces
  its candidate.
- Value justification: the nine numeric equations are exactly MPY's static
  int/bool/float `applyCmp(">")` equations, including the fixed `gtF`,
  `ltFI`, and `ltIF` primitives.  The string equation is exactly
  `strLt(codes(M), codes(V))`, MPY's existing string `>` equation.  Guards do
  not widen those static match domains.
- Dependents: both general-accumulator claims and all four entry claims.
- Validation: LLVM and CPython both pass increasing, decreasing, Boolean,
  mixed numeric, float, string, and greater-than-2^53 cases.  The
  false-result claim forces `[1, 2]` to return the wrong branch value `1`;
  fixed execution reaches `2` and `kprove` rejects it.  A second probe forces
  `[2, 1]` to take the wrong replacement branch and is likewise rejected
  after fixed execution reaches `2`.

### Fold summaries and circularities

- Extensions: `maxNumericGeneralVS`, `maxStrGeneralVS`,
  `maxIntNumericVS`, and `maxFloatNumericVS`; the four accumulator claims.
- Class: definitional summaries and reachability circularities.
- Domain: exactly the recursive numeric or string preconditions recorded in
  the claims.
- Matched context: the circularities match only the fixed accumulator
  configurations `#maxAcc`, `#maxAccF`, and `#maxAccV`, with an arbitrary
  framed continuation.  Their conclusions preserve that same continuation
  and every framed configuration cell.
- State footprint: the fixed folds and summaries read only the iterable and
  accumulator; no state cell is written.
- Value influence and justification: every summary equation mirrors the
  corresponding fixed empty, same-sort step, or general-fold handoff.
  Recursive descent is on the tail constructor.
- Dependents: the four whole-program entry claims.
- Validation: each circularity is proved in the same module as its dependent
  entry claim.  Numeric and string circularities are separated into two proof
  modules so one domain cannot be applied as the other's invariant.

### Float primitive wrapper

- Extensions: `maxFOpaque`; concrete
  `maxFOpaque(F1,F2) => maxFloat(F1,F2)`; symbolic
  `maxFloat(F1,F2) => maxFOpaque(F1,F2)`.
- Class: trusted primitive wrapper.
- Semantic role: only K's fixed `FLOAT.max` hook is isolated; no Python or
  MPY program region is skipped.
- Domain and matched context: every symbolic pair of `Float` values in a
  pure term context.  The symbolic rule has no configuration-cell pattern,
  continuation, binding, or control effect.  The concrete rule covers every
  ground pair.
- Context containment/state footprint: `FLOAT.max` is a pure fixed hook, so
  arbitrary pure-term context is its complete context and it reads/writes no
  MPY state cell.
- Value influence: the returned `Float` may be the result or may participate
  in a later fixed float comparison.
- Value justification: conclusions involving it are conditional on the named
  contract `maxFOpaque(F1,F2) = FLOAT.max(F1,F2)`.  The proof only threads the
  term; it does not assert a different value or reuse it as an unconstrained
  postcondition oracle.
- Dependents: `max-float-numeric-acc`, the float-headed entry claim, and
  mixed numeric paths reached after a float accumulator.
- Validation: the Haskell backend's missing `FLOAT.max` evaluator is the
  reason for the wrapper.  LLVM executes the supplied hook on the recorded
  homogeneous and mixed-float smoke cases with no assertion failure.

## Exact commands and actual results

The complete reproducible command sequence is in `prove.sh`.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 smoke.py
```

All exited 0.  Regenerating `solution.mpy` and comparing it with the delivered
file succeeded.

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Both exited 0.  `krun` ended with `<k> .K </k>`, `NoExc`, and exit code 0.
Compiler warnings are from the read-only reference definition.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC
kprove spec.k --definition verification-kompiled --spec-module SPEC-STR
```

Compilation exited 0.  Each positive `kprove` command printed the success line
`#Top` (plus warnings originating in the read-only reference definition) and
exited 0.  The full `prove.sh` run exited 0 and contains two positive `#Top`
lines in `prove-run.out`.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Expected result: exit 1.  Actual result: exit 1 with
`WarnStuckClaimState`; fixed execution reached `<k> 2 ~> .K </k>` while the
mutated destination required `1`.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-KEEP
```

Expected result: exit 1.  Actual result: exit 1 with
`WarnStuckClaimState`; fixed execution of the decreasing input also reached
`<k> 2 ~> .K </k>` while the opposite branch mutation required `1`.

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Expected result: exit 1.  Actual result: exit 1 with
`WarnStuckClaimState`; the mutated body reached `<k> 0 ~> .K </k>` while the
original behavior witness required `1`.

## Gate results

- Gate A — PASS.  The exact source body executes.  Extensions are pure
  definitions/derived lemmas except for the explicitly trusted fixed float
  hook wrapper.  Equations have complete guarded coverage, overlaps agree,
  recursive summaries descend, a satisfiable witness exists, the wrong
  result is rejected, and a material body mutation is rejected.
- Gate B — PASS.  The four symbolic entry claims cover arbitrary finite
  nonempty numeric lists (including all int/bool/float mixtures) and arbitrary
  finite nonempty string lists, which is the full domain on which the supplied
  MPY `max` fold defines ordering.  The implementation directly calls Python's
  `max`, and the formal summaries implement strict replacement with first-tie
  retention.  Float conclusions are conditional on the supplied fixed
  primitives, not on a candidate-added assumption.
- Gate C — PASS.  The trust ledger is explicit; every reported test and
  mutation has an artifact, exact command, scope, oracle, and actual result.
  Formal, conditional, empirical, and excluded conclusions are separated.

## Trust ledger

| Component | Effect | Dependents | Evidence/status |
|---|---|---|---|
| Supplied MPY semantics and K reachability engine | Defines execution, cells, builtins, and proof calculus | All claims | Fixed task input; concrete and symbolic commands above |
| `FLOAT.max` via `maxFOpaque` | Float value, later comparisons, result | Float and mixed numeric claims | Explicit conditional contract; LLVM float smoke cases |
| Supplied opaque `gtF`, `ltFI`, `ltIF` | Numeric comparison branches | Mixed/float general fold | Exact reuse in `numericGt`; LLVM homogeneous, mixed, and 2^53-boundary cases |
| `py2mpy.py` | Source-to-constructor boundary | Program identity | Fixed task input; regenerated delivered `solution.mpy` matches |
| Partial-correctness interpretation | Termination is not established separately | All reachability claims | Stated limitation of the proof calculus |

## Empirical evidence

`smoke.py` is an executable CPython oracle with explicit expected results.
The same file is translated to `smoke.mpy` and executed under LLVM MPY.
Both runs exit 0 with zero assertion failures on:

- the two prompt examples;
- a negative singleton;
- lexicographically ordered strings;
- Booleans;
- mixed int/float/bool values;
- homogeneous floats; and
- an exact mixed int/float comparison above `2^53`.

This finite evidence supports the fixed primitive boundary; it is not used as
a universal proof.

## Excluded behavior and model boundaries

- Empty lists are excluded because there is no maximum; CPython raises
  `ValueError`, and the supplied MPY fold has no successful empty seed.
- Lists mixing strings with numeric values are excluded because Python's
  ordering is undefined and raises `TypeError`.
- CPython orderings not modeled by the supplied fixed semantics, such as
  lexicographic ordering of nested lists/tuples and user-defined comparison
  methods, are a language-model boundary.  The candidate does not replace
  those behaviors; the K theorem makes no claim about them.
- The formal float claims cover MPY `Float` values, but value-level alignment
  for exotic IEEE cases (NaN, infinities, and signed zero) is conditional on
  the supplied fixed float primitives.  No unchecked claim of CPython
  equivalence for those edges is made.
