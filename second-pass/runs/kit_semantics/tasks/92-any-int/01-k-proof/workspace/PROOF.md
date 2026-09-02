VALIDATED

## What is proven

Under the supplied `MPY` semantics, calling the loaded module binding
`any_int(x, y, z)` is partially correct for every numeric value representable
by that semantics:

- `Int` inputs range over unbounded symbolic integers.
- `Bool` inputs range over both booleans and follow Python's rule that
  `bool` is an `int` subtype, with `False`/`True` contributing `0`/`1`.
- `Float` inputs range symbolically over the full K `Float` sort and cause the
  function to return `false` before arithmetic is evaluated.

If all three inputs pass `isinstance(_, int)`, the return value is true exactly
when one input equals the sum of the other two. If any input is a `Float`, the
return value is false. The final configuration also requires the module and
builtin scopes, environment, scope allocator, heap, heap allocator, stack,
return state, exception state, and exit code to equal their initial values.

This is a partial-correctness theorem. The submitted function is loop-free, but
termination is not a separate reachability claim.

## Formal claim

`spec.k` contains 15 claims:

- Eight claims cover all symbolic `Int`/`Bool` sort combinations.
- Seven claims partition all cases containing at least one `Float` by the first
  failing `isinstance` check. Later arguments are left at sort `Val` where
  short-circuiting makes them unreachable.

Together these claims cover all 27 combinations of the reference model's three
numeric sorts without fixing integer values, float values, or sizes.

For integer interpretations `X`, `Y`, and `Z`, the postcondition is:

```text
anySum(X, Y, Z)
  = (X + Y == Z) or (X + Z == Y) or (Y + Z == X)
```

The initial module scope binds `"any_int"` to the exact parameters and body in
`solution.mpy`. `AnyIntCall` expands to `Call(Name("any_int"), ...)`, so ordinary
name lookup selects that binding and fixed semantics executes parameter
binding, the function body, return, frame pop, and short-circuit control.

## Proof-extension inventory

`AnyIntCall` and `anyIntModuleScope` are parse-time syntax macros, not semantic
rewrites. They disappear during macro expansion and merely place the exact
entry call and loaded program binding into each claim.

### `anySum(Int, Int, Int)`

- Extension/class: `anySum` and its single equation; definitional summary.
- Semantic role: names the mathematical contract in the postcondition; it
  never replaces or accelerates program execution.
- Domain: every triple in `Int × Int × Int`; one unguarded equation covers the
  entire declared domain.
- Matched context: pure `anySum(X, Y, Z)` terms in the eight integer/boolean
  postconditions. It matches no `<k>` computation or configuration cell.
- Justification scope/context containment: exactly the declared integer
  domain; the equation is the prompt's three sum arrangements.
- State footprint: none.
- Value influence: only the expected Boolean in the postcondition.
- Value justification: an explicit, terminating expression using K integer
  addition, equality, and Boolean disjunction.
- Dependents: the eight `Int`/`Bool` claims.
- Control validation: not applicable; no control or execution is replaced.
- Value validation: target proof is `#Top`; the false-postcondition probe is
  rejected; the independent differential test reports zero mismatches.
- Equation audit: total coverage, no recursion, no overlaps.

### `boolAsInt(B) => #if B #then 1 #else 0 #fi`

- Extension/class: one `[simplification]` rule; derived lemma.
- Semantic role: normalizes two equivalent representations already used by
  the fixed semantics. It does not rewrite a program construct.
- Domain: the complete `Bool` sort.
- Matched context: pure `boolAsInt(B)` terms during proof simplification; no
  configuration cell, continuation, binding, or state is matched.
- Justification scope/context containment: `Bool` has exactly `true` and
  `false`. The supplied rules give `boolAsInt(true) = 1` and
  `boolAsInt(false) = 0`; the conditional has those same two results.
- State footprint: none.
- Value influence: integer normalization inside the seven mixed-boolean
  postconditions.
- Value justification: exhaustive constructor analysis against the two fixed
  `boolAsInt` equations.
- Dependents: every positive claim containing at least one symbolic `Bool`.
- Control validation: not applicable; no control or execution is replaced.
- Value validation: both concrete Boolean values are exercised by
  `concrete_tests.py` and `differential_test.py`; all dependent symbolic claims
  close.
- Equation audit: the lemma agrees with both overlapping concrete reference
  equations and terminates in one step.

There are no operational bridges, proof-local trusted primitives, opaque
result oracles, auxiliary circularities, priority rules, or program-execution
summaries.

## Exact commands and actual outputs

The complete reproducible run is:

```bash
./prove.sh > prove.log 2>&1
```

Actual exit code: `0`. `prove.log` contains the complete output.

The script executes these target commands:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual decisive outputs and exits:

```text
program-identity=match
krun: <k> .K </k>, <exc> NoExc </exc>, <exit-code> 0 </exit-code>
kprove spec.k: #Top
target kprove exit: 0
```

The compilers exited 0. Their warnings concern unused variables and
non-exhaustive total functions in unrelated supplied-semantics modules, plus
intentionally unreachable later variables in the short-circuit claims.

The validation commands and actual results are:

```bash
python3 differential_test.py
# cases=1789 mismatches=0
# Exit: 0

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# WarnStuckClaimState; residual <k> true ~> .K </k>
# Exit: 1 (expected)

kompile --backend haskell verification-mutant.k \
  --main-module VERIFICATION-MUTANT \
  --syntax-module MPY-SYNTAX \
  --output-definition mutant-kompiled
# Exit: 0

kprove spec-mutant.k \
  --definition mutant-kompiled \
  --spec-module SPEC-MUTANT
# WarnStuckClaimState; residual <k> false ~> .K </k>
# Exit: 1 (expected)
```

## Gate results

### Gate A — PASS

- A1: the module scope contains the exact translated body, and
  `Call(Name("any_int"), ...)` performs normal binding lookup. Every
  program-defined operation executes in fixed semantics. The body mutant
  replaces the third disjunct with `false`; witness `(3, 1, 2)` then leaves a
  residual `false` against expected `true`, so the proof is body-sensitive.
- A2: there is no operational bridge. The claims pin all state cells. Function
  call allocation and frame state are transient; the final environment,
  scopes, allocators, heap, stack, return state, exception state, and exit code
  must equal the initial values.
- A3: fixed semantics performs name lookup, left-to-right call argument
  evaluation, builtin lookup, parameter binding, short-circuit evaluation,
  return, and frame pop. The proof adds no rule over those configurations.
- A4: `anySum` has one total terminating equation. The `boolAsInt` lemma is
  exhaustive over the two Boolean constructors and agrees with the supplied
  equations on both overlaps.
- A5: `(5, 2, 7)` is a realizable witness. `spec-vacuity.k` changes its expected
  result from `true` to `false`; `kprove` exits 1 with residual `true`.

### Gate B — PASS

- B1: the prompt's material domain is three numbers. The reference semantics
  represents numeric inputs as `Int`, `Bool`, and `Float`; the 15 claims cover
  every combination of those sorts symbolically. There are no fixed-size,
  bounded-value, or example-only restrictions.
- B2: K `Int` matches Python's unbounded integer model. The supplied model makes
  `Bool` an `int` subtype, matching CPython `isinstance`. Symbolic floats are
  rejected before float arithmetic, so no opaque float operation affects the
  theorem. Python numeric classes absent from the fixed semantics (for example
  `complex`, `Decimal`, `Fraction`, or third-party scalar classes) are a
  recorded model boundary, not candidate-created narrowing.
- B3: `anySum` transparently expands to the exact three equalities in the
  natural-language contract.
- B4: `solution.py`, `solution.mpy`, the loaded proof binding, prompt examples,
  and the contract agree.

### Gate C — PASS

The trust boundary and every validation artifact are recorded below.
`prove.sh` reproduces the target proof, concrete execution, differential
evidence, false-postcondition probe, and body mutation. `prove.log` preserves
their actual outputs.

## Trust boundary

- The supplied read-only `reference-semantics/` definition is the fixed
  execution model. All 15 claims depend on its lookup, call, `isinstance`,
  integer/Boolean operator, short-circuit, and return rules.
- The K toolchain, Haskell prover backend, LLVM execution backend, and K
  integer/Boolean theories are trusted infrastructure.
- `py2mpy.py` is the supplied syntactic translator. `prove.sh` regenerates
  `solution.mpy`; its AST identity check confirms that the function exercised
  by `concrete_tests.py` is identical to `solution.py`.
- No proof-local trusted primitive or operational bridge is present.
- The Python-to-MPY model cannot represent every Python numeric class. The
  theorem is therefore conditional on the supplied model for all numeric
  values that model represents.

## Empirically supported facts

- `concrete_tests.py` executes the four prompt examples plus two Boolean
  subtype boundary cases under LLVM. All assertions finish with `.K`, `NoExc`,
  and exit code 0.
- `differential_test.py` imports the submitted `solution.py` and compares it
  with an independently structured oracle that iterates over each possible
  target position and sums the other two values.
- Its complete finite scope is 1,331 integer triples from `[-5, 5]^3`, all
  eight Boolean triples, and 450 cases placing each of six float values in each
  argument position with the other arguments in `[-2, 2]`. Actual result:
  `cases=1789 mismatches=0`.
- These finite checks support implementation/model alignment; the universal
  result comes from the symbolic K claims.

## Excluded behavior

- Numeric classes not representable by the supplied semantics are outside the
  fixed-model theorem and are listed in the trust boundary.
- Non-numeric Python objects are outside the prompt's stated “three numbers”
  input domain.
- The reachability claims establish partial correctness, not a standalone
  total-correctness theorem.
