VALIDATED

## What is proven

Relative to the supplied `reference-semantics/`, `spec.k` proves partial
correctness of the exact `double_the_difference` body in `solution.mpy` for an
arbitrary finite list whose elements are any mixture of the fixed model's
`Int` and `Float` values.  There is no length bound.

The whole-function claim starts with ordinary lookup of
`double_the_difference`, executes parameter binding and the source body, and
finishes after return and call-frame cleanup:

```k
Call(Name("double_the_difference"), (list(VS:ValSeq), .Exprs))
  => dtd(VS)
requires numericVals(VS)
```

`numericVals` recursively accepts exactly finite `ValSeq`s of model `Int` and
`Float` values.  `dtd` recursively adds `I *Int I` exactly when an integer
`I` is positive and `pyMod(I, 2) == 1`; floats contribute zero.  Thus the
formal result is the sum of squares of the positive odd integers, with
negative integers, even integers, zero, and non-integer numeric values ignored.

This is a partial-correctness result, as required by the Kit workflow.  It does
not separately prove a liveness theorem.

## Formal claims and obligations

`SPEC.loop-invariant` is the single-loop circularity.  At a loop head with
accumulator `S` and remaining suffix `VS`, it establishes final accumulator
`S +Int dtd(VS)` and the exact final local loop-target value
`lastNumber(VS, OLD)`.  Its obligations are:

- Base: `.ValSeq` takes the fixed `#iterDone` path; `dtd(.ValSeq) = 0`.
- Integer step: fixed semantics executes binding, `isinstance`, positivity,
  modulo, multiplication, and accumulator update; the remaining state is the
  circularity instantiated on the tail.
- Float step: fixed semantics makes `isinstance(_, int)` false and reuses the
  circularity on the tail without changing the accumulator.
- Whole-program discharge: the source initializes `result` and `number`, the
  `For` rule reaches the stable loop head, the circularity supplies the result,
  and fixed return/pop rules restore the caller configuration.

`SPEC.double-the-difference` is the target theorem.  It observes the returned
value and pins `env`, scopes, scope allocator, heap, heap allocator, stack,
return state, exception state, and exit code at the ordinary initial/final
function-call boundary.

## Rebuilt proof-extension inventory

No rule in `verification.k` rewrites a `<k>` program configuration.  There is
no operational bridge and no proof-local trusted primitive.

### `numericVals`, `dtd`, `oddIntSquare`, and `lastNumber`

- **Class:** definitional summaries.
- **Semantic role:** describe the input domain, mathematical result, and exact
  final local target; they do not replace source execution.
- **Domain:** all `ValSeq`/`Int`/`Val` arguments declared by their sorts.
  Empty and cons equations cover `ValSeq`; the `dtd` head cases are
  Int, Float, and a disjoint `[owise]` remainder.
- **Matched context / containment:** pure terms only; no continuation, stack,
  binding, or cell is matched.  Context-containment obligations for an
  operational bridge are not applicable.
- **State footprint:** none.
- **Value influence:** `numericVals` is the target precondition; `dtd` is the
  returned postcondition; `lastNumber` constrains the loop-local `number`.
- **Value justification:** their exhaustive structural equations.
  `oddIntSquare` uses the supplied `pyMod` equation and K integer arithmetic.
- **Dependents:** both claims depend on `numericVals` and `dtd`; the loop claim
  also depends on `lastNumber`.
- **Control/value validation:** prompt examples and mixed concrete tests
  terminate with `.K`, `NoExc`, exit code 0; 12,111 independent differential
  cases have zero mismatches; the false-postcondition mutation is rejected.

The two guarded `[simplification]` equations for `dtd` restate its static
Int/Float equations over a dynamic `Val`.  Their guards are disjoint
(`isInt` versus `isFloat`) and their right-hand sides agree with the original
static equations after projection collapse.

### Guarded integer projection family

Exact symbols/rules:

- `definedProjectInt(V) => isInt(V)`
- the `#Ceil({V}:>Int)` characterization
- `projectIntTotal(V) => {V}:>Int` under `definedProjectInt(V)`
- the reverse symbolic orientation under the same guard
- Int collapse and projection idempotence

Record:

- **Class:** guarded total projection plus derived cast lemmas.
- **Semantic role:** refine a dynamic `Val` only on paths already known to be
  in the fixed `Int` subsort; no source computation is bypassed.
- **Domain:** every use that can affect a result is guarded by `isInt(V)`.
  Off-domain projection values are not used by any branch, state update, or
  postcondition.
- **Matched context:** projection/cast terms only; no `<k>` continuation,
  control stack, bindings, or framed state.
- **Justification scope / containment:** the guard is exactly the built-in
  subsort-cast definedness domain.  The `#Ceil` equation and two guarded
  orientations connect the total projection to `{V}:>Int`; collapse fixes its
  value on an actual `Int`.
- **State footprint:** none.
- **Value influence:** supplies integer operands to the guarded summary and
  dispatch twins.
- **Value justification:** the fixed K subsort cast, not a fresh result oracle.
- **Dependents:** `dtd`, integer comparison/modulo/multiplication dispatch, and
  therefore both claims.
- **Control validation:** not applicable; no control term is rewritten.
- **Value validation:** static Int collapse, concrete LLVM Int/Float tests, the
  changed-body rejection, and the off-by-one rejection.

### `isIntV` and integer dispatch twins

Exact equations:

- `isIntV(V) => isInt(V)`
- guarded dynamic `applyCmp(">", V, I)`
- guarded dynamic `applyBin("%", V, I)`
- guarded dynamic `applyBin("*", V1, V2)`

Record:

- **Class:** derived lemmas.
- **Semantic role:** restate existing fixed `MPY-BUILTINS`/`MPY-INT`
  equations over dynamically sorted operands after normal source evaluation.
- **Domain:** exactly `isInt` for every operand that the corresponding fixed
  rule statically matches.
- **Matched context:** the fixed pure dispatch-function applications only.
  There is no `<k>` frame, wildcard continuation, binding, heap, stack, return,
  exception, output, or abrupt control.
- **Justification scope / containment:** identical operator names, operand
  order, guards, and right-hand-side operations as the fixed static rules;
  projection is connected to the partial Int cast as recorded above.
- **State footprint:** none.
- **Value influence:** source branches and the accumulator update.
- **Value justification:** fixed `isIntV` cases and fixed `MPY-INT`
  `applyCmp`/`applyBin` equations.
- **Dependents:** loop circularity and target claim.
- **Control validation:** fixed semantics still performs lookup, call,
  argument evaluation, `If`, comparison, arithmetic, assignment, and loop
  control.  No control-affecting bridge exists.
- **Value validation:** concrete prompt/mixed cases, a source-body mutation
  that reaches `2` instead of required `1`, and the false-result mutation.

The Int and Float guards are disjoint.  On static Int terms, projection
collapse makes each twin identical to the fixed rule.  No new equation has
overlapping guards with a different result.

### `dtdLoopBody` and `dtdBody`

These are `[macro]` source-term abbreviations, not runtime proof rules.  They
expand to the exact constructors in `solution.mpy`, including the
behavior-preserving local `number = 0` initialization.  They read/write no
state themselves; the expanded terms execute entirely through fixed MPY
rules.  Both claims depend on these exact expansions.

### Reachability claims

- `SPEC.loop-invariant` is the proved circularity, not an assumed result
  equation.  It reads the remaining iterable and local accumulator, updates
  only the exact local `number` and `result` bindings, preserves `lst`, module
  and builtins scopes, and frames the continuation and all other cells.
- `SPEC.double-the-difference` is the required target theorem.  It executes the
  program-defined closure through fixed call/binding/body/return/pop rules.

Both claims print `#Top`.  Neither is marked trusted.

## Exact reproducible commands and actual outputs

The complete recorded run is `prove-run.log`; `./prove.sh` exited 0.

Generation:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 py2mpy.py model-boundary-bool.py > model-boundary-bool.mpy
```

Concrete LLVM build and runs:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled
krun model-boundary-bool.mpy --definition runtime-kompiled
```

Actual: build exit 0 with warnings originating in supplied semantics.  Both
`krun` commands exit 0 with final `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`.

Differential evidence:

```bash
python3 test_solution.py
```

Actual output and exit:

```text
cases=12111 mismatches=0
Exit: 0
```

Symbolic build:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Actual: exit 0 with only supplied-`str.k` unused-variable warnings.

Focused circularity proof:

```bash
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant
```

Actual:

```text
#Top
Exit: 0
```

All claims, including the required target:

```bash
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Actual:

```text
#Top
Exit: 0
```

False-postcondition probe:

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual: exit 1 with `WarnStuckClaimState`; the residual implication is:

```text
dtd ( VS ) +Int 1 #Equals dtd ( VS )
```

Changed-body probe:

```bash
kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual: exit 1 with `WarnStuckClaimState`; the mutated execution reaches:

```text
<k> 2 ~> .K </k>
```

while the claim requires `1`.

## Gate results

### Gate A — PASS

- A1: the exact program closure executes under fixed semantics.  The target
  pins its module binding and full body.  Changing multiplication to addition
  is rejected on `[1]`.
- A2/A3: there is no operational bridge.  Fixed semantics handles lookup,
  argument order, parameter binding, loop control, return, frame cleanup, heap,
  stack, exception, and exit cells.
- A4: summary equations are exhaustive/disjoint; dynamic twins use exact
  static-rule domains; projection use is guarded and connected to the built-in
  partial cast.
- A5: the empty list is a realizable precondition witness, and the prompt
  examples are realizable witnesses.  The off-by-one postcondition exits 1.

### Gate B — PASS

- The theorem covers arbitrary finite lists over every numeric class represented
  as numeric by the fixed semantics: unbounded K `Int` and K `Float`.
- It does not replace the domain with examples, fixed sizes, or bounded
  unrollings.
- `dtd` definition is the requested human-facing sum, and the implementation
  executes exactly that test and update.
- Model boundary: the supplied semantics makes `Bool` disjoint from `Int`.
  `model-boundary-bool.mpy` therefore verifies model result 0 for `[True]`,
  while CPython prints `1` because `isinstance(True, int)` is true.  This is the
  fixed model's numeric-identification boundary, not a candidate-added bound.
  Python complex and other numeric classes are not represented by the supplied
  semantics.

### Gate C — PASS

The proof-local trust ledger has no result-bearing oracle, operational bridge,
or unproved program-defined helper.  Trusted foundations are the supplied
reference semantics, K's Int/Float/sort predicates and subsort cast, the
Haskell backend/solver, and the K proof checker.  The Bool/Int and unavailable
numeric-class model boundaries are explicit above.  All concrete,
differential, mutation, and positive-proof evidence names an existing artifact,
exact command, scope, result, and exit behavior.  Finite tests are reported
only as evidence; the universal result comes from the unbounded symbolic claims.

## Trust boundary and excluded behavior

- Trusted: unchanged supplied semantics, K toolchain/backend, and their
  built-in integer/float/sort theories.
- Formally established: partial correctness for all arbitrary finite
  fixed-model numeric lists satisfying `numericVals`.
- Empirically supported: concrete execution examples and the 12,111 CPython
  differential cases.
- Model boundary: CPython Bool-as-Int and numeric classes absent from the fixed
  semantics.
- Contract-excluded: nonnumeric list elements.  The prompt states a list of
  numbers; the target theorem does not silently claim arbitrary `Val` lists.
- Not established: a separate termination/liveness theorem or equivalence to
  full CPython beyond the supplied subset.
