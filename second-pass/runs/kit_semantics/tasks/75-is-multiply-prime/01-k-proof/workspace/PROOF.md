VALIDATED

## What is proven

Under the supplied MPY semantics, the claim `SPEC.is-multiply-prime` proves
partial correctness of the translated `is_multiply_prime` function for every K
integer `A` satisfying `A <Int 100`.

The claim starts in the normal empty-module configuration, loads the exact
translated function definition, looks up and calls that function with `A`,
executes its real body, returns through the ordinary call frame, and leaves this
Boolean in `<k>`:

```text
A == 8  or A == 12 or A == 18 or A == 20 or A == 27 or A == 28
or A == 30 or A == 42 or A == 44 or A == 45 or A == 50
or A == 52 or A == 63 or A == 66 or A == 68 or A == 70
or A == 75 or A == 76 or A == 78 or A == 92 or A == 98
or A == 99
```

Prime factors are counted with multiplicity. Thus `8 = 2 * 2 * 2` is in the
set. Inputs below 2 are covered by the formal domain and return false.

## Formal claim

The program boundary is the `#loadAll(Module(FuncDef(...)))` computation
followed by `Call(Name("is_multiply_prime"), (A, .Exprs))`. This includes
definition binding, name lookup, argument binding, all comparisons and
short-circuit operations, `Return`, and frame cleanup.

The precondition is:

```k
requires A <Int 100
```

The observable result is the final Boolean in `<k>`. The claim also fixes the
normal initial state and checks the final environment, function binding,
scope allocator, empty heap, heap allocator, empty stack, return state,
exception state, and exit code.

The finite result set is exactly the three-prime-product set below 100. To see
exhaustiveness, order the prime factors as `p <= q <= r`.

- `p` can only be `2` or `3`, since `5^3 > 100`.
- For `p = 2`, `q` can only be `2, 3, 5, 7`. Enumerating the possible prime
  `r` gives respectively:
  `{8,12,20,28,44,52,68,76,92}`,
  `{18,30,42,66,78}`, `{50,70}`, and `{98}`.
- For `p = 3`, `q` can only be `3` or `5`. These give
  `{27,45,63,99}` and `{75}`.
- A product of positive primes cannot be negative, so all negative integers in
  the formal domain correctly map to false.

Their union is precisely the 22 values in the postcondition.

## Proof-extension inventory

There are no proof-local semantic extensions.

- `verification.k` only imports the supplied `MPY` module.
- It declares no functions, total functions, equations, simplification rules,
  concrete rules, priority rules, ordinary rewrites, opaque symbols,
  operational bridges, trusted primitives, or auxiliary claims.
- `spec.k` contains only the single target reachability claim.

Consequently there is no proof-local matched context, state footprint,
result-bearing abstraction, totality coverage, overlap, descent, or connection
theorem obligation. All source operations execute through the fixed supplied
semantics.

## Commands and actual results

The complete reproducible run is:

```bash
./prove.sh
```

It exited `0`. `prove.sh` records and executes these commands:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py krun_tests.py > krun_tests.mpy
python3 test_solution.py
```

Actual Python output and exit:

```text
checked: 200 mismatches: 0
Exit: 0
```

The concrete definition and executions were:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled > krun-solution.out
krun krun_tests.mpy --definition runtime-kompiled > krun-tests.out
```

All three commands exited `0`. Both `krun` outputs end with `.K`, `NoExc`, and
an `<exit-code>` of `0`. `krun_tests.mpy` calls the function on true cases
`8`, `30`, and `99`, and false cases `1`, `16`, and `97`.

The symbolic definition and positive target proof were:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.is-multiply-prime
```

Actual positive proof output and exit:

```text
#Top
Exit: 0
```

The compilers also emitted warnings from supplied, imported semantic modules:
unused variables in `semantics/str.k`, plus LLVM non-exhaustiveness warnings
for functions in float, method, builtin, and subscript modules. None of those
functions occurs on this claim's execution path. The warnings are retained in
the end-to-end console output; the positive proof output is in
`positive-proof.out`.

The false-postcondition mutation changes only the expected `A == 99` disjunct
to `A == 100`:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.false-postcondition
```

Actual result:

```text
WarnStuckClaimState: implication check between the conditions has failed
Residual includes: (postcondition with A ==Int 100) #Equals (A ==Int 99)
Exit: 1 (EXPECTED FAILURE)
```

The body-sensitivity mutation changes the final source comparison from `99` to
`97` in both the loaded body and the expected retained closure, while leaving
the result property unchanged:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --claims SPEC-BODY-MUTATION.changed-body
```

Actual result:

```text
WarnStuckClaimState: implication check between the conditions has failed
Residual includes: (original postcondition) #Equals (A ==Int 97)
Exit: 1 (EXPECTED FAILURE)
```

## Gate results

### Gate A — PASS

- **A1 program identity and body sensitivity:** The real translated body
  executes; no rule replaces the call or body. The changed-body mutation is
  rejected.
- **A2 operational state preservation:** There is no operational bridge. The
  claim observes the return value and fixes all MPY state cells, including the
  final function binding and empty control state.
- **A3 binding, evaluation, and control fidelity:** Module binding, name
  lookup, argument evaluation and binding, left-to-right short-circuit
  evaluation, return, and frame popping all use supplied MPY rules.
- **A4 logical consistency:** No proof-local equations or total functions
  exist. Coverage, overlap, and opaque-value obligations are therefore
  inapplicable.
- **A5 non-vacuity:** `A = 30` is a satisfiable true witness and `A = 16` is a
  satisfiable false witness. The false-postcondition mutation is rejected at
  the boundary witness `A = 99`.

### Gate B — PASS

- **B1 input domain:** The theorem takes MPY integers and uses the prompt's
  stated upper bound `A < 100`. Negative integers are additionally covered and
  return false.
- **B2 language model:** The implementation uses only integer equality,
  Boolean short-circuit `or`, function calls, and return, all directly modeled
  on the proof path.
- **B3 summary to property:** There is no opaque summary. The factor-ordering
  argument above exhaustively derives the 22 values from the
  three-prime-factor property.
- **B4 implementation to intent:** The proved finite set agrees with the
  prompt and its `30 = 2 * 3 * 5` example.

### Gate C — PASS

- The trust boundary and every evidence artifact are named below.
- `test_solution.py` uses an independently written repeated-division oracle,
  not the finite disjunction or any K proof equation. It has zero mismatches on
  every integer from `-100` through `99`; this includes the complete
  nonnegative prompt domain and 100 representative negative inputs.
- The concrete K tests exercise both outcomes and boundary products.
- The positive proof and both negative probes are reproducible from
  `prove.sh`, with their full outputs retained in the workspace.
- Formal proof, mathematical adequacy reasoning, finite evidence, and
  exclusions are separated in this report.

## Trust boundary

- The supplied read-only MPY semantics is the operational model. The target
  depends specifically on its module loading, scopes, calls, returns, integer
  comparison, and Boolean short-circuit rules.
- The supplied `py2mpy.py` translator is trusted to transliterate the CPython
  AST faithfully. `prove.sh` regenerates `solution.mpy` from `solution.py`
  before every run.
- K version `v7.1.293`, its LLVM and Haskell backends, the SMT solver used by
  `kprove`, and the host runtime are trusted.
- The elementary factor-ordering argument connects the explicit formal result
  set to the natural-language phrase “multiplication of 3 prime numbers.”
  It is independently supported over the bounded intended domain by the
  repeated-division oracle, but that Python test is finite evidence rather than
  a universal K theorem.

No opaque or externally trusted value affects this program's branch or result.

## Empirically supported facts

- `test_solution.py`: exact command `python3 test_solution.py`; scope
  `range(-100, 100)`; oracle is repeated prime-factor division; result
  `checked: 200 mismatches: 0`.
- `krun_tests.mpy`: exact command
  `krun krun_tests.mpy --definition runtime-kompiled`; cases
  `8, 30, 99, 1, 16, 97`; oracle is explicit assertions; result `.K`,
  `NoExc`, exit code `0`.
- `spec-vacuity.k`: expected-failure mutation, exit `1`, with an implication
  residual exposing the `99` result.
- `spec-body-mutation.k`: expected-failure source mutation, exit `1`, with an
  implication residual exposing the altered `97` comparison.

## Excluded behavior

- The K theorem does not cover non-integer Python values or integers
  `A >= 100`.
- “Three primes” is interpreted with multiplicity, as is conventional for
  prime-factor counting; a distinct-primes-only interpretation is not claimed.
- The K theorem is a partial-correctness result. The implementation is visibly
  loop-free and all recorded concrete executions terminate, but no separate
  liveness theorem is claimed.
- Equivalence of the whole supplied MPY semantics to every behavior of CPython
  is outside this proof; only the supplied reference model is the formal
  execution authority.
