VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, the reachability claim
`SPEC.bf-correct` proves partial correctness of the actual translated `bf`
body for every pair of string values represented by arbitrary
`P1:IntSeq` and `P2:IntSeq`.

The claim starts in the standard empty module configuration, loads the exact
`bf(planet1, planet2)` definition, looks up and calls `bf`, binds both
arguments, executes the function body, returns, and pops the call frame.  Its
result is:

```k
tuple(betweenPlanets(P1, P2))
```

`betweenPlanets` is the tuple sequence of the eight named planets whose
indices are strictly between the two supplied planet indices, in increasing
Sun-proximity order.  It is `.ValSeq` when either input is not one of the
eight names.  Equal and adjacent valid names also produce `.ValSeq`.

The result, restored environment, module binding, scope allocator, empty heap,
empty stack, cleared return state, `NoExc`, and exit code 0 are all constrained
by the claim.  The theorem is a partial-correctness theorem; it does not make a
separate liveness claim.

## Formal claim and scope

The positive target is the sole claim in `spec.k`:

```k
claim [bf-correct]:
  <k> #loadAll(bfModule) ~> bfCall(P1:IntSeq, P2:IntSeq)
      => tuple(betweenPlanets(P1, P2)) </k>
  ...
```

- Program boundary: module load, function binding, call lookup, argument
  evaluation/binding, every statement in `solution.mpy`, return, and frame pop.
- Input domain: two `str(IntSeq)` values.  Every finite `IntSeq` is admitted;
  there is no valid-name precondition.
- Observable final state: return tuple, control completion, restored scope
  state, heap, stack, return marker, exception cell, and exit code.
- Intended property: exclude both endpoint planets, order the intervening
  planets from nearest to farthest from the Sun, and return `()` for either
  invalid name.

There are no source loops, so no loop-invariant claim is required.

## Proof-extension inventory

Validation rebuilt this inventory from the final `verification.k` and
`spec.k`.

### `bfBody`, `bfModule`, and `bfCall`

- Class: compile-time syntactic definitions.
- Semantic role: abbreviate the exact translated body, module, and entry call;
  they do not summarize or replace an execution step.
- Domain and matched context: exact constructors only.  `bfCall` receives two
  `IntSeq` values and expands to the normal `Call(Name("bf"), ...)`.
- State footprint: none at macro expansion.  The expanded term is executed by
  the supplied `MPY` rules, including lookup, binding, control, tuple methods,
  slicing, return, and frame handling.
- Value influence: the expanded source body determines the result.
- Justification: direct constructor-by-constructor comparison with
  `solution.mpy`; `solution.mpy` is regenerated from `solution.py` by the fixed
  `py2mpy.py` in `prove.sh`.
- Dependents: `SPEC.bf-correct` and both validation probes.
- Validation: the positive proof executes the expansion; the material body
  mutation in `verification-mutant.k` is rejected.

### `planetValues`

- Class: definitional summary.
- Semantic role: names the fixed eight-element mathematical planet sequence;
  it does not rewrite a program term.
- Domain: the single nullary equation.
- State footprint: none.
- Value influence: supplies the ordered values in the postcondition.
- Value justification: its constructor order is exactly Mercury, Venus,
  Earth, Mars, Jupiter, Saturn, Uranus, Neptune, matching the prompt.
- Dependents: `betweenIndices` and `SPEC.bf-correct`.
- Validation: examples, all 64 valid-name pairs, and invalid-name boundary
  samples agree with an independent CPython oracle.

### `planetIndex`

- Class: definitional summary.
- Semantic role: maps a mathematical string code sequence to indices 0 through
  7, or `-1`; it does not intercept membership or `tuple.index` execution.
- Domain: eight singleton equality guards and one guard that is the
  conjunction of their negations.
- Context and state footprint: pure term evaluation; no continuation, binding,
  control, or state cells are matched.
- Value influence: selects invalid-name behavior and slice endpoints in the
  postcondition.
- Value justification: the singleton guards correspond one-to-one with the
  ordered names in `planetValues`.  The literals are pairwise distinct, and
  the final guard is their exact complement, so the equations are disjoint and
  exhaustive.
- Dependents: `betweenPlanets` and `SPEC.bf-correct`.
- Validation: the universal target proof connects real membership/index
  execution to this value for arbitrary inputs.  The finite differential test
  gives additional, non-universal evidence.

### `betweenPlanets` and `betweenIndices`

- Class: definitional summaries.
- Semantic role: state the mathematical postcondition; they do not replace
  Python execution.
- Domain: `betweenPlanets` is unguarded.  `betweenIndices` has three disjoint
  cases: either index negative; both nonnegative with `I < J`; and both
  nonnegative with `I >= J`.
- Context and state footprint: pure term evaluation only.
- Value influence: determines the entire returned tuple sequence.
- Value justification: invalid indices map to empty; valid indices select
  `I+1 .. J-1` or `J+1 .. I-1` from `planetValues` using the supplied
  `buildVS` slice definition.
- Dependents: `SPEC.bf-correct`.
- Validation: all guards are exhaustive and pairwise non-overlapping.  The
  actual source membership, index calls, comparison, and tuple slice execute
  under fixed semantics and the universal claim closes.

There are no proof-local simplification lemmas, operational bridges, priority
rules, opaque values, trusted primitives, or auxiliary reachability claims.
The imported opaque sort/float facilities are not exercised by this program.

## Exact commands and actual results

The complete reproducible command sequence is in `prove.sh`.  It was run as:

```bash
./prove.sh > prove.out 2>&1
```

Actual script exit: `0`.

### Translation and differential test

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py
python3 test_solution.py
python3 py2mpy.py krun_examples.py > krun_examples.mpy
```

Actual test output:

```text
pairs_checked=225
mismatches=0
krun_function_ast_matches_solution=True
```

### Concrete LLVM execution

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun krun_examples.mpy --definition runtime-kompiled
```

Actual build exit: `0`.  It printed only warnings from the supplied semantics.
Actual `krun` exit: `0`.  The exact final observable cells in `prove.out` were:

```text
<k>
  .K
</k>
<exc>
  NoExc
</exc>
<exit-code>
  0
</exit-code>
```

All nine assertions in `krun_examples.mpy` therefore completed.

### Positive symbolic proof

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.bf-correct
```

Actual build exit: `0`; only the four unused-variable warnings from the
supplied `semantics/str.k` were printed.  Actual target proof output and exit:

```text
#Top
```

Exit: `0`.

This is the only required positive target-proof command.

### A5 false-postcondition probe

Mutation: for the satisfiable witness `("Mercury", "Earth")`, require `()` even
though `"Venus"` is strictly between the endpoints.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual exit: `1`.  The stuck residual in `vacuity.out` contains:

```text
<k>
  tuple ( vCons ( str ( iCons ( 86 , iCons ( 101 , iCons ( 110 ,
  iCons ( 117 , iCons ( 115 , .IntSeq ) ) ) ) ) ) , .ValSeq ) ) ~> .K
</k>
```

This is the code sequence for the concrete result `("Venus",)`, which does not
unify with the mutated empty-tuple destination.

### A1 body-sensitivity probe

Mutation: preserve the name and two-argument signature but replace the function
body with an unconditional `return ()`.

```bash
kompile --backend haskell verification-mutant.k \
  --main-module MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition mutation-kompiled
kprove spec-body-mutation.k \
  --definition mutation-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual mutant build exit: `0`.  Actual mutation proof exit: `1`.  The residual
in `body-mutation.out` has `tuple(.ValSeq)` while the original property for
`("Mercury", "Earth")` requires `("Venus",)`.

## Gate A — PASS: real-program soundness

- A1: the translated program-defined body executes under fixed semantics.
  There is no helper interception.  The changed-body probe is rejected.
- A2: no operational bridge abstracts state.  The claim observes the result,
  environment, scopes, allocators, heap, stack, return state, exception, and
  exit code.
- A3: module binding, lookup, left-to-right argument evaluation, parameter
  binding, condition evaluation, return control, and frame pop all execute
  through supplied rules.  No abrupt control is added by proof-local theory.
- A4: every proof-local function equation is truthful on its complete guard;
  the guards described above are disjoint and exhaustive.  There is no
  recursive proof-local equation and no inconsistent totalization.
- A5: arbitrary `P1` and `P2` provide realizable inputs.  The returned tuple is
  constrained.  The concrete false-postcondition mutation is rejected with a
  meaningful stuck result.

## Gate B — PASS: intent adequacy

- The prompt requires string inputs; the theorem covers all two-string inputs
  in the reference model, not only the eight valid names.
- Invalid, equal, adjacent, forward, and reverse endpoint cases have the
  required results.
- The endpoints are excluded and `planetValues` fixes the returned order by
  proximity to the Sun.
- The supplied semantics represents strings as `IntSeq`.  The relevant names
  are ASCII, and this task only uses equality, finite tuple membership/index,
  and slicing.  No material CPython/reference-model difference affects the
  requested behavior.
- Non-string Python arguments are excluded, consistently with the prompt's
  stated string input contract.

## Gate C — PASS: trust and evidence auditability

### Trust ledger

- Supplied `reference-semantics/`: trusted as the task's fixed Python execution
  model.  It affects the target claim and concrete tests.  It was imported
  without modification.
- K v7.1.293 Haskell/LLVM backends: trusted to implement compilation,
  rewriting, and reachability checking.  They affect all K results.
- CPython 3 and the supplied `py2mpy.py`: trusted for parsing and exact
  transliteration of `solution.py` to `solution.mpy`.
- Natural-language astronomy ordering: fixed explicitly by the prompt and by
  `planetValues`; no external fact beyond that given order is assumed.

No proof-local trusted primitive or result-bearing opaque symbol contributes to
the theorem.

### Reproducible evidence

- `test_solution.py`: independent oracle using a position map and a filtered
  enumeration, not the implementation's tuple slicing.  Scope is the Cartesian
  product of 8 valid names and 7 invalid/boundary strings: 225 pairs.  Result:
  zero mismatches.
- `krun_examples.py` / `krun_examples.mpy`: three prompt examples plus adjacent,
  equal, full reverse, invalid-first, invalid-second, and both-empty cases.
  Result: all assertions complete with `.K`, `NoExc`, and exit code 0.
- `spec-vacuity.k`: false result mutation.  Result: rejected, exit 1.
- `verification-mutant.k` and `spec-body-mutation.k`: source-body sensitivity.
  Result: rejected, exit 1.
- `prove.out`, `vacuity.out`, and `body-mutation.out` contain the actual outputs.

Finite tests support intent/model alignment only; the universal connection from
actual MPY execution to the postcondition comes from `SPEC.bf-correct`.

## Excluded behavior

- Calls with non-string values are outside the theorem and the prompt's typed
  contract.
- Behavior under a Python implementation other than the supplied `MPY`
  reference semantics is not itself machine-proved; CPython testing is finite
  supporting evidence.
- The reachability theorem is reported as partial correctness, not as a
  separate termination theorem.
- Unused language facilities in the supplied semantics—including floats,
  mutable lists, sorting, I/O, and exceptions other than the observed `NoExc`
  result—are outside this program's behavior.
