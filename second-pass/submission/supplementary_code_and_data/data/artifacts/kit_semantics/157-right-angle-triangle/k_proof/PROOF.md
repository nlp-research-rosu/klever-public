VALIDATED

## What is proven

Under the supplied MPY semantics and the trust boundary below, the translated
`right_angle_triangle` function is partially correct for every symbolic
combination of MPY `Int` and `Float` arguments.  The function returns true
exactly when at least one of

```text
a*a == b*b + c*c
b*b == a*a + c*c
c*c == a*a + b*b
```

holds in MPY's numeric operations.  This covers all orders of the three sides.
The `Int` domain is unbounded.  The proof does not enumerate values, fix a
length, or use bounded unrolling.

For `Int`, the equality and arithmetic are K's interpreted integer operations.
For `Float` and mixed `Int`/`Float` cases, the theorem is structural and
conditional on the supplied opaque float-operation contracts and the explicit
`trustedFloatEq` contract described below.

## Formal claim

`spec.k` contains eight target reachability claims:

```text
right-angle-iii  right-angle-iif  right-angle-ifi  right-angle-iff
right-angle-fii  right-angle-fif  right-angle-ffi  right-angle-fff
```

Together they cover the Cartesian product `{Int, Float}^3`.  Each claim starts
with the normal MPY `Call(Name("right_angle_triangle"), ...)` computation.  The
module scope binds that name to `rightAngleTriangleClosure()`, whose sole
equation is the exact `solution.mpy` body.  Normal MPY rules perform name
lookup, left-to-right argument evaluation, parameter binding, frame creation,
body execution, return, frame pop, and restoration of the caller.

Each final result `?RESULT:Bool` is constrained by:

```k
ensures ?RESULT ==Bool ratExpected(A, B, C)
```

`ratExpected` is the three Pythagorean equalities joined by `orBool`.  No loop
claims are needed because the program is loop-free.

## Proof-extension inventory

### `rightAngleTriangleClosure()`

- Class: definitional summary.
- Role: names one constant closure value; it does not replace execution of the
  function body.
- Domain and context: nullary, unguarded, and exhaustive.  It is used only as
  the value bound to `right_angle_triangle` in the target call configuration.
- State footprint: none.
- Value influence: fixes the selected binding, parameter names, exact body, and
  defining environment location.
- Value justification: its right-hand side is the exact `FuncDef` body emitted
  in `solution.mpy`, converted to the closure representation used by MPY after
  module loading.
- Dependents: all eight target claims.
- Validation: `solution.mpy` is regenerated and byte-compared in `prove.sh`;
  `validation_tests.py` checks that the LLVM harness contains an AST-identical
  function.  `spec-body-mutation.k` replaces the body with `return False` and
  fails on `(3,4,5)`.

### `trustedFloatEq` and the Float `Compare` rule

- Class: trusted primitive representing the fixed external Float equality
  operation that is outside the program-defined code.
- Fixed-semantics gap: MPY routes Float equality to the `FLOAT.eq` hook.  LLVM
  implements that hook, but the Haskell backend aborts on symbolic Float
  equality with `Error: missing hook`.
- Complete matched context:

  ```k
  <k> Compare(F1:Float, CmpOp("==", F2:Float))
       => trustedFloatEq(F1, F2) ... </k>
  ```

  Both operands have already evaluated to `Float` values.  The continuation
  and every unmentioned cell are framed unchanged.
- Justification scope and context containment: the named external contract is
  universal over two MPY Float values and every continuation.  Float equality
  is a pure value operation in the supplied semantics, so it reads or writes no
  configuration cell, raises no modeled exception, and performs no control
  transfer.  The bridge has the same complete Float operand domain and
  preserves the same continuation.
- State footprint: reads no cells; writes no cells; returns one `Bool`.
- Value influence: its Boolean can select an `or` branch and can be the final
  result.
- Value justification: conditional assumption that `trustedFloatEq(F1,F2)`
  denotes MPY/Python Float equality.  The `[concrete]` equation evaluates it
  with `F1 ==Float F2` under LLVM.  This is an explicitly named external
  boundary, not a theorem about a program-derived oracle.
- Dependents: the seven target claims containing at least one `Float`.
- Control/value validation: fixed MPY LLVM and bridge-enabled LLVM produced
  byte-identical final configurations on the 10-case concrete harness,
  including Float and mixed numeric cases.

### `ratSquare`, `ratAdd`, `ratEq`, and `ratExpected`

- Class: definitional summaries.
- Role: occur only in postconditions; none replaces program execution.
- Domain: `ratSquare` has disjoint `Int` and `Float` cases; `ratAdd` and
  `ratEq` have the four disjoint ordered `Int`/`Float` cases.  These equations
  cover every use in the eight claims.  `ratExpected` composes those summaries.
- State footprint: none.
- Value influence: specify the required final Boolean.
- Value justification: every equation is the corresponding equation already
  used by MPY (`*Int`, `+Int`, `mulF`, `addF`, `intToF`, `eqIF`) or the named
  `trustedFloatEq` boundary.  Guards are implicit in disjoint K sorts, so there
  are no inconsistent overlaps.
- Dependents: all eight target claims.

There are no simplification lemmas, loop circularities, auxiliary execution
claims, return shortcuts, function-call intercepts, or program-result axioms.

## Exact commands and actual outputs

The complete reproducible command record is `./prove.sh`.  Its commands are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py solution.py | cmp - solution.mpy
python3 validation_tests.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete_tests.py > concrete-tests.mpy
krun concrete-tests.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kompile --backend llvm verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-runtime-kompiled
cmp \
  <(krun concrete-tests.mpy --definition runtime-kompiled) \
  <(krun concrete-tests.mpy --definition verification-runtime-kompiled)

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual final run:

- `validation_tests.py`: exit 0, output
  `validation: examples=10, positive_numeric_triples=35000, mismatches=0, concrete_harness_ast=identical`.
- Reference LLVM `kompile`: exit 0, with only warnings originating in the
  supplied semantics.
- Reference `krun`: exit 0; final `<k>` was `.K`, `<exc>` was `NoExc`, and
  `<exit-code>` was `0`.
- Haskell `kompile`: exit 0, with only unused-variable warnings from the
  supplied `str.k`.
- Positive target `kprove`: exit 0 and output `#Top`.
- Bridge-enabled LLVM `kompile`: exit 0.
- Fixed-versus-extended comparison: exit 0 and output
  `fixed-vs-extended LLVM outputs: identical`.
- False-postcondition probe: exit 1 with `WarnStuckClaimState`; its residual
  `<k>` contained `true ~> .K` while the mutation required false.
- Body-mutation probe: exit 1 with `WarnStuckClaimState`; its residual `<k>`
  contained `false ~> .K` while the retained postcondition required true.
- Overall `./prove.sh`: exit 0, ending with
  `EXPECTED FAILURE: false-postcondition mutation exited 1` and
  `EXPECTED FAILURE: body mutation exited 1`.

## Gate results

### Gate A — PASS

- A1: the exact program closure is selected by normal lookup and its body
  executes under fixed MPY call/return semantics.  The body-mutation probe
  demonstrates sensitivity to a material program change.
- A2: no program execution is summarized.  The one external Float equality
  bridge is pure and preserves every cell and the continuation; fixed and
  extended LLVM executions are identical on the recorded harness.
- A3: the bridge applies only after both operands are evaluated Floats and
  keeps the active continuation.  Its result-bearing value is explicitly
  conditional on the external Float equality contract.
- A4: the definitional equations are terminating, sort-disjoint, and cover all
  target uses.  No false or overlapping simplification rule is present.
- A5: `(3,4,5)` realizes the precondition.  The false-postcondition mutation
  and the distinct body mutation both fail with the expected concrete
  residuals.

### Gate B — PASS

- Domain: the eight symbolic claims cover every combination of MPY's two
  material side-length numeric classes, `Int` and `Float`.  The proof has no
  positivity restriction; therefore it includes the intended positive finite
  side-length inputs rather than silently narrowing them.
- Property: `ratExpected` checks the Pythagorean equality in every possible
  choice of hypotenuse, matching the prompt and both examples.
- Float meaning: the theorem describes exact MPY/Python floating operations,
  not ideal real arithmetic, and is conditional on the named supplied
  primitives.
- Model boundary: CPython numeric objects not represented by MPY, such as
  `Decimal`, `Fraction`, complex numbers, or user-defined operator overloads,
  are outside the fixed language model.  Python `bool` values are numeric at
  runtime but are not material side lengths.  These are model/contract
  boundaries, not finite-size restrictions introduced by the proof.

### Gate C — PASS

Every assumption and dependent claim is listed below; all cited artifacts and
commands exist in the workspace.  The concrete and differential evidence is
reported as finite evidence, not as a universal proof.

## Trust boundary

- Supplied `reference-semantics/`: trusted as the operational definition.
  Every target claim depends on it.
- K compiler, Haskell backend, LLVM backend, and their builtin integer/Float
  hooks: trusted toolchain.  Every execution/proof result depends on them.
- Supplied opaque Float functions `mulF`, `addF`, `intToF`, and `eqIF`: trusted
  to denote their documented Python numeric operations.  Claims containing a
  `Float` depend on the applicable functions.
- `trustedFloatEq`: trusted to denote MPY/Python Float equality for all Float
  values.  The seven Float-containing claims depend on it.  Its LLVM equation
  and fixed-versus-extended test provide finite concrete evidence.
- Pythagorean characterization: the standard geometric fact that positive
  side lengths form a right triangle exactly when one squared side equals the
  sum of the other two squared sides.

No conclusion about symbolic Float values is presented as unconditional on
these primitive contracts.

## Empirically supported facts

- `validation_tests.py` compares the candidate with the independently written
  sorted-side oracle `x*x + y*y == z*z`.
- Scope: the 10 named examples plus all 27,000 triples in `{1,...,30}^3` and
  all 8,000 triples in `{0.5,1.0,...,10.0}^3`.
- Result: 35,000 sampled triples, zero mismatches.
- `concrete_tests.py` supplies five integer cases and five Float/mixed cases to
  both LLVM definitions; all assertions terminate with `.K`, `NoExc`, and
  exit code 0.
- The fixed and bridge-enabled LLVM final configurations compare byte-for-byte
  equal.

These tests support implementation intent and the trusted Float boundary; they
do not replace the universal K reachability proof.

## Excluded behavior

- Inputs for which multiplication, addition, or equality is undefined are not
  side lengths and are outside the contract.
- Numeric classes absent from the supplied MPY model are an explicit fixed-model
  boundary.
- Non-finite Float values are not physical side lengths.  The formal claims
  remain structural and conditional for all MPY Float terms, but the finite
  differential evidence does not assert CPython fidelity for NaN or infinity.
- Reachability proves partial correctness.  It is not a separate total-
  correctness or resource-bound theorem.
