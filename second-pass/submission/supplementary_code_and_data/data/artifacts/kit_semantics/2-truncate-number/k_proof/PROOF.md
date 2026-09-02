VALIDATED

## What is proven

Relative to the supplied `MPY` semantics, for every symbolic `F:Float`, calling
the module binding `truncate_number` whose exact body is

```k
Return(BinOp("%", Name("number"), Float(1.0)))
```

returns `floatMod(F, 1.0)`. The proof executes name lookup, argument
evaluation, parameter binding, the program-defined body, return, and frame
cleanup using the fixed semantics. It also establishes that the environment,
scopes, heap, allocation counters, stack, return state, exception state, and
exit code have the values stated in the claim after the call.

This is a partial-correctness theorem. The value-level reading “fractional
part” is conditional on the supplied semantics' trusted interpretation of
`floatMod`; it is not derived from a symbolic IEEE-754 theory.

## Formal claim

`SPEC.truncate-number` in `spec.k` starts with:

```k
Call(Name("truncate_number"), (F:Float, .Exprs))
```

The module scope binds that exact name to a one-parameter closure containing
the exact translated function body. The destination is:

```k
floatMod(F, 1.0)
```

There is no `requires` clause beyond the K sort `F:Float`. Thus the operational
theorem is structurally quantified over all values represented by the supplied
semantics as `Float`. The source contract's human-facing decomposition is
claimed only for positive finite inputs.

## Proof-extension inventory

`verification.k` contains only `imports MPY`. It adds no syntax, equations,
lemmas, simplification rules, ordinary rewrites, priorities, auxiliary claims,
or operational bridges. `spec.k` adds only the target reachability claim.

The following fixed reference primitive is nevertheless material to the trust
boundary:

| Field | Record |
|---|---|
| Extension | Reference-semantics declaration `floatMod(Float, Float)` plus its `[concrete]` equation and `applyBin("%", Float, Float)` dispatch; this was supplied, not added locally |
| Class | Trusted primitive |
| Semantic role | The fixed dispatch executes the source `%`; symbolic proof leaves the result as the exact `floatMod` term, while LLVM evaluates its concrete equation |
| Domain | The fixed declaration is total over two K `Float` arguments; this theorem calls it only with divisor `1.0` |
| Matched context | `applyBin("%", F1:Float, F2:Float)` after both `BinOp` operands have evaluated; normal call and return continuations remain in the fixed semantics |
| Justification scope | The supplied semantics defines Python-style floor modulo as `F1 - floor(F1 / F2) * F2` in its concrete rule |
| Context containment | No local rule matches or widens this context; the exact fixed-semantics dispatch is used |
| State footprint | Produces one value; it reads or writes no configuration cells |
| Value influence | Its result is the function result and therefore the target postcondition |
| Value justification | Conditional trust in the supplied primitive's documented equation, supported by concrete LLVM and independent CPython tests below |
| Justification | Explicit trusted boundary in `reference-semantics/semantics/float.k`; no claim that K proved the IEEE-754 equation symbolically |
| Dependents | `SPEC.truncate-number` |
| Control validation | The target proof executes lookup, call, body, return, and cleanup; `spec-body-mutation.k` shows a changed body produces a changed residual |
| Value validation | Four LLVM examples and 1,521 CPython comparisons against `math.modf` have zero mismatches |
| Validation | Gate A body/postcondition mutations are rejected; Gates B and C record scope and finite evidence |

## Exact commands and actual outputs

The complete recorded workflow is:

```bash
./prove.sh
```

It exited `0`. `prove.sh` contains the individual commands actually used.
Their material outputs were:

```text
python3 py2mpy.py solution.py > solution.mpy
Exit: 0

python3 smoke.py
Exit: 0

python3 test_solution.py
inputs=1521 mismatches=0
Exit: 0

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
Exit: 0

krun solution.mpy --definition runtime-kompiled
Final: <k> .K </k>, <exc> NoExc </exc>, <exit-code> 0 </exit-code>
The module scope contains the exact translated truncate_number closure.
Exit: 0

krun smoke.mpy --definition runtime-kompiled
Final: <k> .K </k>, <exc> NoExc </exc>, <exit-code> 0 </exit-code>
All four in-semantics assertions passed.
Exit: 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
Exit: 0

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
#Top
Exit: 0

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kore-exec: [...] Warning (WarnStuckClaimState):
#Not ( { floatMod ( F , 1.0 ) #Equals floatMod ( F , 2.0 ) } )
[Error] Prover: backend terminated because the configuration cannot be
rewritten further.
EXPECTED_FAILURE: false postcondition exit=1

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
kore-exec: [...] Warning (WarnStuckClaimState):
<k> floatMod ( F , 2.0 ) ~> .K </k>
#Not ( { floatMod ( F , 1.0 ) #Equals floatMod ( F , 2.0 ) } )
[Error] Prover: backend terminated because the configuration cannot be
rewritten further.
EXPECTED_FAILURE: changed function body exit=1
```

Both `kompile` runs also printed warnings originating in the unchanged
reference semantics: unused `As`/`Bs` variables, and LLVM non-exhaustive-match
warnings for unrelated total functions. They did not change either compiler's
zero exit status.

## Gate results

### Gate A — PASS

- **A1:** The claim pins the function name, parameter list, body, defining
  environment, argument, and initial configuration. The program-defined body
  executes under fixed semantics. Changing `% 1.0` to `% 2.0` in
  `spec-body-mutation.k` changes the reached term and is rejected with exit 1.
- **A2:** No execution is skipped. Every configuration cell is present in the
  claim. The temporary call frame is created and removed by the fixed rules;
  state, heap, stack, return state, exception state, and exit code match the
  destination.
- **A3:** Name lookup selects the exact closure in module scope, the argument
  is evaluated and bound to `number`, and fixed return/pop rules preserve
  control.
- **A4:** There are no proof-local equations, summaries, lemmas, or bridges to
  audit for overlap, coverage, or false guards. The opaque fixed
  `floatMod` value is threaded parametrically rather than assigned an
  unproved symbolic interpretation.
- **A5:** `F = 3.5` is a realizable witness, exercised concretely by LLVM.
  `spec-vacuity.k` changes only the result to `floatMod(F, 2.0)` and is
  rejected with exit 1 and the expected unmet equality.

### Gate B — PASS

- The source contract concerns positive finite Python floats. The formal
  execution claim is broader—it returns the structural modulo term for every K
  `Float`—and therefore does not strengthen the requested input domain.
- On the intended positive finite subset, Python's `% 1.0` and the supplied
  floor-modulo primitive describe the requested fractional part.
- The implementation uses exactly that operation and agrees with the prompt
  example `truncate_number(3.5) == 0.5`.
- The mathematical meaning of the opaque symbolic primitive is explicitly
  conditional, rather than presented as a solver-proved IEEE-754 fact.

### Gate C — PASS

- The only value-level trust boundary is the supplied `floatMod` primitive,
  recorded above with its effect and dependent claim.
- Every evidence artifact exists, and every command is present in `prove.sh`.
- The positive proof, both negative probes, exact-module LLVM execution,
  in-semantics assertions, and independent differential test are reproducible.
- Finite testing is reported only as evidence, not as a universal proof.

## Trust boundary

The theorem is relative to the supplied Python semantics and the K
toolchain. In particular, symbolic `kprove` does not evaluate or axiomatize
`floatMod(F, 1.0)` for symbolic `F`; it proves that the actual program returns
that exact fixed-semantics term. Interpreting it as the Python fractional part
trusts the concrete equation in the supplied `MPY-FLOAT` module. This
primitive affects only the returned value, not binding, control, state,
exceptions, or termination behavior in this program.

## Empirically supported facts

`smoke.mpy` exercises `0.5`, `1.0`, `3.5`, and `123.875` on the required LLVM
backend; all assertions terminate with `.K`, `NoExc`, and exit code 0.

`test_solution.py` independently uses CPython's `math.modf` as its oracle. It
tests six named examples plus the grid
`whole + fraction / 16.0` for `whole = 0..100` and `fraction = 1..15`.
The recorded result is `inputs=1521 mismatches=0`.

These are finite adequacy checks for the trusted concrete primitive and the
implementation; they do not replace the symbolic reachability proof.

## Excluded behavior

- Total correctness and termination are not separately proved; the K theorem
  is a reachability/partial-correctness claim.
- The human-facing “fractional part” interpretation excludes negative and
  non-finite inputs, which are outside the prompt's decomposable positive
  number domain.
- No claim is made about CPython behaviors absent from the supplied subset,
  such as arbitrary exceptions, alternate numeric classes, Decimal, or
  user-defined `%`.
- The proof does not derive IEEE-754 floor modulo algebra inside the Haskell
  prover; that value-level operation is the named, tested trust boundary.
