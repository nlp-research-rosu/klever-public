VALIDATED

# What is proven

`spec.k` proves partial correctness of the exact translated `exchange` body in
`solution.mpy`.  For arbitrary non-empty finite lists whose elements are any
mixture of the numeric values represented by the supplied model (`Int`, `Bool`,
and `Float`), normal termination returns:

- `"YES"` iff the combined lists contain at least `len(lst1)` even values;
- `"NO"` otherwise.

The theorem is symbolic in both list lengths and every element.  It is not a
fixed-size proof or a bounded unrolling.  The entry claim starts from the
reference initial configuration, loads the exact function body, resolves and
calls `exchange`, executes both loops, and observes the returned string, empty
heap, restored environment/stack/return state, `NoExc`, and exit code 0.
Module-scope contents after loading the definition are intentionally
unobserved.

Unlimited element exchanges preserve the length of `lst1` and allow its final
contents to be any size-`len(lst1)` selection from the combined pool.  Such a
selection is all-even exactly when the pool contains at least `len(lst1)` even
values.  This is the mathematical bridge from the formal count theorem to the
HumanEval contract.

# Formal claims

## Program boundary

`SPEC.exchange` begins with:

```k
#loadAll(exchangeProgram)
~> Call(Name("exchange"), list(VS1), list(VS2))
```

`exchangeProgram`, `exchangeBody`, and `countBody` are compile-time macros
whose expansions reproduce `solution.mpy`, including the function definition,
docstring expression, assignments, both `for` loops, `len(lst1)`, and both
returns.  They do not replace runtime execution.

## Input domain

```k
requires allNumbers(VS1) andBool allNumbers(VS2)
  andBool vsLen(VS1) >Int 0 andBool vsLen(VS2) >Int 0
```

`allNumbers` recursively admits every finite heterogeneous `ValSeq` made from
`Int`, `Bool`, and `Float`.  There is no length bound.

## Observable final state

The result is `exchangeResult(VS1, VS2)`.  The claim additionally fixes:

- `<env> 0 </env>`;
- `<heap> .Map </heap>` and `<heapLoc> 0 </heapLoc>`;
- `<stack> .List </stack>` and `<ret> noRet </ret>`;
- `<exc> NoExc </exc>` and `<exit-code> 0 </exit-code>`.

The final module scope is existential because definition installation is not an
observable part of the HumanEval result.

## Loop invariant

`SPEC.count-loop` applies to both syntactically identical loops.  Starting with
an accumulator `C` and any numeric suffix `VS`, it executes the actual fixed
loop machinery and ends with:

```k
"even_count" |-> C +Int evenCount(VS)
```

The invariant keeps the exact ordinary function-frame keys (`lst1`, `lst2`,
`even_count`, `value`), the parent scope, and an empty heap.  `value` is
existential only after the loop because its final value is not observed.

The three proof obligations close as follows:

1. Empty suffix: `evenCount(.ValSeq) = 0`.
2. Step: the source condition produces `numberEven(V)`; the recursive
   circularity gives `evenCount(R)`, and the guarded defining equations fold
   this to `evenCount(vCons(V, R))`.
3. Entry: the first invariant adds `evenCount(VS1)`, the second adds
   `evenCount(VS2)`, and the final source comparison selects
   `exchangeResult`.

# Proof-extension inventory

## Syntax macros

- **Extensions:** `countBody`, `exchangeBody`, `exchangeProgram`.
- **Class:** compile-time syntax abbreviations.
- **Semantic role:** none after macro expansion.
- **Domain/context:** only their literal occurrences in the claims.
- **State/value/control:** none is abstracted.
- **Justification:** direct transcription of `solution.mpy`; the body mutation
  probe demonstrates sensitivity to a material source change.
- **Dependents:** `SPEC.exchange`, `SPEC.count-loop`.

## Guarded numeric projections

- **Extensions:** `definedProjectInt`, `definedProjectBool`,
  `definedProjectFloat`; `projectIntTotal`, `projectBoolTotal`,
  `projectFloatTotal`; their `#Ceil`, cast-orientation, collapse, and
  idempotence rules.
- **Class:** derived lemmas/definitional total projections.
- **Semantic role:** refine the dynamic `Val` sort under an exact generated
  sort predicate; they do not choose a value without that predicate.
- **Domain:** all `Val`; cast orientation is guarded by the matching
  `definedProject*` predicate.
- **Matched context:** pure projection or partial-cast terms only; no
  continuation or operational cells are matched.
- **Justification scope/context containment:** the guarded-total-projection
  construction is exactly the partial subsort cast on its defined domain.
- **State footprint:** none.
- **Value influence:** only the pure `numberEven` formula.
- **Value justification:** collapse on the matching static subsort; off-sort
  projections remain total opaque terms underneath a false Boolean conjunct.
- **Dependents:** `numberEven`, `isNumberVal`, `allNumbers`, both target claims.
- **Validation:** all six bridge-free connection claims close, and concrete
  Int/Bool/Float tests exercise both parity outcomes.

## Missing numeric primitive cases

- **Extensions:** `boolToInt`; `applyBin("%", B:Bool, 2)`;
  `applyBin("%", F:Float, 2)`; priority-40
  `applyCmp("==", F:Float, 0)`.
- **Class:** definitional summary (`boolToInt`) plus trusted primitive
  language-model extensions for exact Python numeric promotion.
- **Semantic role:** model only the unmodeled literal operations exercised by
  the source.  The Bool and Float modulo cases are sort-disjoint from the
  supplied Int modulo rule.  The Float comparison specialization agrees with
  promotion of integer zero to literal `0.0`.
- **Domain:** exactly Bool `% 2`, Float `% 2`, and Float `== 0`.
- **Matched context:** pure `applyBin`/`applyCmp` function terms; no state or
  continuation.
- **Justification scope/context containment:** the match domain is no wider
  than the stated Python primitive operations.
- **State footprint/control:** none.
- **Value influence:** parity, loop branches, count, and final result.
- **Value justification:** Bool maps to 0/1; Float maps to the supplied opaque
  `floatMod` and `eqF` primitives with literal `2.0`/`0.0`.
- **Dependents:** Float/Bool connection claims, `numberEven`, loop and entry
  claims.
- **Validation:** the frozen runtime demonstrably stops on Float `% Int`
  (`krun-numeric-reference.out`); the extended LLVM definition completes all
  ten mixed numeric assertions; Python differential testing has zero
  mismatches over 5,007 cases.

## Domain and mathematical summaries

- **Extensions:** `isNumberVal`, `allNumbers`, `numberEven`, `evenCount`,
  `exchangeResult`.
- **Class:** definitional summaries.
- **Semantic role:** name mathematical values without replacing name lookup,
  function calls, loops, frame control, or state transitions.
- **Domain:** `isNumberVal` is the exact union of Int/Bool/Float;
  `allNumbers` is structural recursion over all finite `ValSeq`;
  `numberEven` is total on `Val`; `evenCount` is total on `ValSeq`;
  `exchangeResult` is total on two `ValSeq`.
- **Matched context/state footprint:** pure terms only; no operational cells.
- **Guard coverage/overlap:** `evenCount` uses `numberEven(V)` and its exact
  negation; `exchangeResult` uses complementary integer guards `>=` and `<`.
  The guards cover all inputs and do not disagree on overlap.
- **Value influence:** these summaries state the loop accumulator and final
  returned string.
- **Value justification:** exhaustive equations; `numberEven` is the
  per-subsort formula established by `CONNECTION-SPEC`; `evenCount` is a
  structural fold; `exchangeResult` is the contract criterion.
- **Dependents:** `SPEC.count-loop`, `SPEC.exchange`.
- **Validation:** bridge-free universal connection proof, positive target
  proof, two opposite-value probes, false-result probe, body mutation, LLVM
  tests, and independent combinatorial oracle.

## Connected parity composition

- **Extension:** simplification
  `applyCmp("==", applyBin("%", V, 2), 0) => numberEven(V)`
  under `isNumberVal(V)`.
- **Class:** operational bridge over a pure function composition.
- **Semantic role:** replaces only the symbolic `% 2 == 0` function
  composition after name and literal evaluation; it does not skip lookup,
  argument binding, loop control, frame control, state, or exceptions.
- **Complete matched context:** the exact `applyCmp` term in any pure
  continuation; guard `isNumberVal(V)`.  No operational cell is read or
  changed.
- **Justification scope:** `CONNECTION-SPEC` imports `VERIFICATION-BASE`, not
  `VERIFICATION`, so this bridge is unavailable.  Its Int, Bool, and Float
  composition claims universally prove the exact match value.  Three
  additional execution claims start at the corresponding source expression.
- **Context containment:** the three disjoint numeric subsorts exhaust
  `isNumberVal`; the claims frame an arbitrary `<k>` continuation, and the
  connected term is pure and state-free.
- **State footprint/control:** reads/writes no cell and introduces no control
  effect.
- **Value influence:** selects the source `if` branch, accumulator increment,
  and final result.
- **Value justification:** the six bridge-free claims in
  `connection-spec.k`.
- **Dependents:** `SPEC.count-loop`, hence `SPEC.exchange`.
- **Control/value validation:** source-body mutation is rejected; the ground
  opposite interpretations for even `2` and odd `1` are both rejected.

## Definedness lemma

- **Extension:** `#Ceil(applyBin("%", V, 2)) => #Top` under
  `isNumberVal(V)`.
- **Class:** derived lemma.
- **Semantic role:** records that modulo by the nonzero literal 2 is defined
  for every represented numeric subsort.
- **Context/domain/state:** pure logical term, same numeric union as the
  connected composition, no cells.
- **Justification:** the bridge-free Int/Bool/Float execution claims all reach
  a Boolean result; the Float and Bool cases use the exact primitive extensions
  listed above.
- **Dependents:** symbolic loop definedness.
- **Validation:** connection proof and both numeric LLVM/Python evidence sets.

## Reachability claims

- **Extensions:** `CONNECTION-SPEC.parity-*` and `SPEC.count-loop`.
- **Class:** auxiliary reachability claims/circularity.
- **Semantic role:** the connection claims prove the bridge value without the
  bridge; `count-loop` executes the real loop body and supplies the coinductive
  invariant.
- **Domain/context:** connection claims quantify universally over each numeric
  subsort and frame arbitrary continuation/state.  `count-loop` accepts every
  finite all-numeric suffix with the exact function-local map and empty heap.
- **State/control:** connection claims preserve all cells; `count-loop`
  changes only `even_count` and the unobserved loop target, using fixed loop
  control.
- **Dependents:** connection claims justify the bridge; `SPEC.exchange`
  depends on `count-loop`.
- **Validation:** both positive `kprove` commands print `#Top`; the body,
  result, and value mutations fail.

# Commands and actual outputs

The complete reproducible command sequence is in `prove.sh`.  The final run was:

```bash
./prove.sh > prove.out 2> prove.err
```

Actual exit: `0`.

The required positive proof commands were:

```bash
kprove connection-spec.k \
  --definition verification-base-kompiled \
  --spec-module CONNECTION-SPEC
# stdout: #Top
# exit: 0

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
# stdout: #Top
# exit: 0
```

`prove.out` begins:

```text
#Top
#Top
cases=5007 mismatches=0
```

Concrete frozen-semantics command:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled > krun-reference.out
```

Actual exit: `0`; `krun-reference.out` has `<k> .K </k>`.

Extended numeric concrete command:

```bash
kompile verification.k \
  --backend llvm \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-runtime-kompiled
krun k-numeric-tests.mpy \
  --definition verification-runtime-kompiled \
  > krun-numeric-extended.out
```

Actual exit: `0`; all ten assertions completed with `<k> .K </k>`.

Negative probes:

```text
kprove spec-vacuity.k ...             exit 1 (expected)
  residual result: "YES"; mutated destination: "NO"
kprove spec-body-mutation.k ...        exit 1 (expected)
  residual result: "NO"; original destination: "YES"
kprove connection-wrong-spec.k ...     exit 1 (expected)
  residual value: true; destination: false
kprove connection-wrong-odd-spec.k ... exit 1 (expected)
  residual value: false; destination: true
```

The exact residuals and expected-failure markers are in `prove.out` and
`prove.err`.

# Gate results

## Gate A — PASS

- A1: `exchangeProgram` is the exact body, and the odd-count body mutation is
  rejected.
- A2: the only operational bridge is pure and has no state footprint.  The
  loop theorem executes fixed bindings, assignments, iterator control, frame
  control, and state transitions.
- A3: the bridge applies after lookup/literal evaluation to the exact pure
  composition.  Six bridge-free universal claims cover its complete
  Int/Bool/Float domain and arbitrary continuation.
- A4: projection guards are exact; Bool equations are exhaustive; numeric
  guards are disjoint; `evenCount` and `exchangeResult` use complementary
  cases; recursive definitions descend structurally.
- A5: `[2], [1]` is a realizable precondition witness.  The false-result,
  mutated-body, wrong-even, and wrong-odd probes all fail.

## Gate B — PASS

- B1: the theorem covers arbitrary non-empty finite numeric lists, including
  heterogeneous Int/Bool/Float elements and unbounded lengths.
- B2: these are every numeric class represented by the supplied model.
  Numeric classes absent from the model are an explicit model boundary, not a
  candidate-added restriction.  Complex modulo is undefined in Python and is
  outside the source computation.
- B3: K formally connects execution to combined even count; the selection
  argument above establishes that this count criterion is equivalent to
  possible exchanges.  The independent enumeration oracle supports this
  intent bridge on 5,007 finite cases.
- B4: the implementation and contract agree on all examples, boundary cases,
  and the formal domain.

## Gate C — PASS

- Every non-derived component and dependent claim is listed below.
- All cited artifacts and commands exist in the current directory.
- Formal results, trusted primitive behavior, mathematical intent reasoning,
  and finite evidence are separated explicitly.

# Trust boundary

| Component | Effect and dependents | Status and evidence |
|---|---|---|
| Supplied `MPY` semantics | All execution, control, state, and base primitives | Trusted reference input; concrete LLVM smoke tests |
| K compiler/Haskell prover/LLVM runtime | All machine-checked results | K v7.1.293; exact commands in `prove.sh` |
| `floatMod` and `eqF` | Float parity, loop branch, final result | Supplied intentionally opaque primitives under `kprove`; concrete under LLVM; 10 K assertions and 5,007 Python differential cases |
| Bool/Float literal promotion rules in `VERIFICATION-BASE` | Fill the exact operations absent from the frozen subset | Conditional on Python numeric semantics; bridge-free K connection claims plus LLVM/Python evidence |
| Exchange-count equivalence | Human-facing meaning of `exchangeResult` | Mathematical selection argument; independently enumerated differential oracle |
| Termination | K claims establish partial correctness | Inputs are finite lists and each source loop consumes one element, but termination is not a separate K liveness theorem |

# Empirically supported facts

`differential.py` uses an independent oracle: it enumerates every size-
`len(lst1)` combination from the combined pool and checks whether any selected
combination is all-even.  It does not call `evenCount` or reuse K equations.

```bash
python3 differential.py
# cases=5007 mismatches=0
```

The cases include both prompt examples, boundary length-one lists, negative
integers, integral and fractional floats, booleans, heterogeneous lists, and
5,000 deterministic random pairs with lengths 1 through 4.  This is finite
evidence, not a universal proof.

# Excluded behavior

- Empty input lists are excluded exactly as stated by the prompt.
- Non-numeric list elements are outside the contract.
- Numeric classes not represented by `MPY` (for example custom numeric
  objects) are a recorded fixed-model boundary.
- Inputs on which Python `% 2` itself is undefined are outside the specified
  computation.
- The proof is partial correctness; it does not independently prove liveness.
