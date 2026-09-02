VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, calling the exact translated
`starts_one_ends` closure on a positive K `Int`, if it terminates, has the
claimed integer result while restoring the caller environment, scope
allocation counter, heap, stack, return state, exception state, and exit code:

- If `n == 1`, the result is `1`.
- If `n > 1`, the result is `18 *Int (10 ^Int (n -Int 2))`.

This is a partial-correctness result in the Kit sense. The `#Top` executions
reported below establish the K reachability claims; the separate Gate A/B/C
audit establishes this document's `VALIDATED` headline.

## Formal claim and scope

`spec.k` contains two target claims whose preconditions partition the prompt's
entire positive-integer domain:

- `SPEC.starts-one-ends-one-digit` has `requires N ==Int 1`.
- `SPEC.starts-one-ends-multi-digit` has `requires N >Int 1`.

Each claim starts at `Call(Name("starts_one_ends"), N)` with the module binding
fixed to a closure containing the complete `solution.mpy` body. The complete
active configuration is stated: environment `0`, the module and builtin
scopes, `scopeLoc` `1`, empty heap, `heapLoc` `0`, empty stack, `noRet`,
`NoExc`, and exit code `0`. The result in `<k>` and all these cells are
observable in the theorem; no cell is omitted or framed.

For `n >= 2`, let `A` be the n-digit numbers starting with `1` and `B` those
ending with `1`. Then:

- `|A| = 10^(n-1)`;
- `|B| = 9 * 10^(n-2)`;
- `|A intersection B| = 10^(n-2)`.

Inclusion-exclusion therefore gives
`10^(n-1) + 8 * 10^(n-2) = 18 * 10^(n-2)`. For one digit, only the number `1`
qualifies.

## Proof-extension inventory

The rebuilt inventory is empty. `verification.k` only imports the supplied
`MPY` module. It declares no syntax, function, totality attribute, equation,
lemma, rewrite, priority rule, operational bridge, trusted primitive, opaque
term, or auxiliary claim. `spec.k` contains only the two target reachability
claims.

Consequently, the proof-extension record's domain, matched context,
justification scope, containment, state footprint, value influence, value
justification, dependents, and control/value validation fields are all not
applicable. In particular, no program operation is replaced or accelerated:
name lookup, argument binding, conditional selection, arithmetic, return, and
frame popping all execute under the fixed semantics.

## Reproduction and actual results

The complete executable record is `./prove.sh`. It was run from `/workspace`
and exited `0` with K `v7.1.293` and Python `3.10.12`.

Translation and concrete execution:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled --output none
```

Actual result: all commands exited `0`; the runner printed
`LLVM concrete assertions: PASS`. The assertions cover `n = 1, 2, 3, 6`.

Independent executable oracle:

```bash
python3 validate.py
```

Actual output and exit:

```text
validated n=1..6: [(1, 1), (2, 18), (3, 180), (4, 1800), (5, 18000), (6, 180000)]
mismatches: 0
Exit: 0
```

Symbolic definition and all positive target proofs:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.starts-one-ends-one-digit
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.starts-one-ends-multi-digit
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Actual results:

```text
one-digit claim:   #Top, exit 0
multi-digit claim: #Top, exit 0
complete spec:     #Top, exit 0
```

The compilers also emitted warnings from untouched, imported reference modules:
unused variables in `semantics/str.k`, and LLVM exhaustiveness warnings in
operations outside this program's integer/call fragment. No warning identified
a stuck or incomplete target computation.

Body-sensitivity probe:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: expected exit `1` with `WarnStuckClaimState`; after changing the
body coefficient from `18` to `17`, the residual `<k>` value was `17` while
the destination required `18`.

False-result/non-vacuity probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: expected exit `1` with `WarnStuckClaimState`; the exact original
body reached residual `<k>` value `18` while the false destination required
`19`.

## Gate results

### Gate A — PASS

- A1: Both claims pin the exact function name, module binding, parameter,
  translated body, argument, and environment. The material body mutation is
  rejected and changes the residual result.
- A2: There is no operational bridge. The claims explicitly constrain every
  active state cell, and fixed semantics performs frame creation and removal.
- A3: Fixed semantics performs `Name` lookup, parameter binding, conditional
  evaluation, return, and control restoration. The argument is already an
  integer value, so it has no skipped side effects or evaluation order.
- A4: There are no proof-local equations, total functions, lemmas, or rewrite
  rules to check for coverage, overlap, descent, or consistency.
- A5: `n = 1` and `n = 2` are realizable witnesses. Both result branches are
  constrained, and the false result at `n = 2` is rejected with residual `18`.

### Gate B — PASS

- B1: `N ==Int 1` or `N >Int 1` is exactly the positive-integer input domain
  stated by the prompt; no valid prompt input is removed.
- B2: On this domain, the used `MPY` integer operations model unbounded
  integers and nonnegative exponentiation, matching CPython's relevant
  behavior. Non-integer inputs and invalid exponents are outside the contract.
- B3: The formula-to-count bridge is justified by the inclusion-exclusion
  argument above and independently checked by decimal enumeration for
  `n = 1..6`.
- B4: The implementation's two branches are precisely the one-digit case and
  the derived multi-digit count.

### Gate C — PASS

- C1: The trust ledger below names every component outside the target claims
  and its influence.
- C2: `prove.sh`, `concrete-tests.mpy`, `spec-body-mutation.k`,
  `spec-vacuity.k`, and `validate.py` are present and record exact commands,
  scopes, oracles, and observed results.
- C3: K proof closure, mathematical intent reasoning, finite empirical
  evidence, trusted infrastructure, and excluded behavior are kept distinct.

## Trust boundary

- The supplied read-only `reference-semantics/` definition is trusted as the
  execution model. Its call, function, control, and integer rules affect the
  result and control/state restoration of both claims.
- K `v7.1.293`, its Haskell/LLVM backends, and the host runtime are trusted to
  implement compilation, rewriting, and constraint solving correctly.
- The supplied `py2mpy.py` and CPython AST parser are trusted for
  transliteration. `solution.mpy` was regenerated by the exact required
  command, and its body was manually matched against the closure in both
  target claims.
- The inclusion-exclusion bridge from the formal numeric formula to the
  natural-language counting property is mathematical reasoning outside K. It
  affects intent validation, not closure of the execution claims.
- `validate.py` uses direct decimal enumeration and imports `solution.py`; it
  does not reuse the closed-form proof equation as its oracle. Its result is
  finite evidence, not a universal proof.

## Empirically supported facts

- LLVM execution of the translated body satisfies the four ground assertions
  at `n = 1, 2, 3, 6`.
- Direct enumeration of all n-digit positive integers for every `n` from `1`
  through `6` found zero mismatches.
- The two negative K probes demonstrate body sensitivity and result
  non-vacuity at the satisfiable witness `n = 2`.

## Excluded behavior

- Inputs `n <= 0`, booleans, floats, strings, and other non-integer values are
  outside the prompt's positive-integer domain and the formal claims.
- The result is established under the supplied partial Python semantics, not a
  claim that this reference semantics is a complete model of CPython.
- Total correctness, resource consumption, and feasibility of constructing or
  printing the enormous result for arbitrarily large `n` are not claimed.
- The finite concrete and brute-force tests do not replace the universal
  symbolic reachability claims or the mathematical inclusion-exclusion
  argument.
