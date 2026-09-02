VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, the exact translated
`is_equal_to_sum_even` module is loaded and the resulting function is called
with an arbitrary K `Int` value `N`. The reachability claim proves that the
returned Boolean is

```text
N >=Int 8 andBool pyMod(N, 2) ==Int 0
```

and that execution ends with the expected module binding, empty call stack,
`NoExc`, exit code `0`, unchanged heap, and restored environment and allocation
counters. This is a partial-correctness reachability result under the supplied
semantics.

For mathematical integers, that Boolean is equivalent to the HumanEval
property:

- Any sum of four positive even integers is even and is at least
  `2 + 2 + 2 + 2 = 8`.
- If `N` is even and `N >= 8`, then
  `N = 2 + 2 + 2 + (N - 6)`, and `N - 6` is a positive even integer.

## Formal claim

`SPEC.is-equal-to-sum-even` in `spec.k` has no precondition beyond the sort
constraint `N:Int`, so its domain is every mathematical integer represented by
the supplied semantics. Its source term contains the exact AST from
`solution.mpy`: module load, function definition, body, lookup, argument, and
call. Its destination constrains the returned value directly; it does not use
an existential oracle or a program summary.

The observed final state is complete for the supplied configuration:
`<k>`, `<env>`, `<scopes>`, `<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`,
`<ret>`, `<exc>`, and `<exit-code>` are all constrained. There are no loops, so
no loop-invariant claim is needed.

## Proof-extension inventory

The rebuilt inventory is empty:

- `verification.k` only imports the supplied `MPY` module.
- It declares no syntax, function, equation, ordinary rewrite,
  simplification rule, priority rule, operational bridge, trusted primitive,
  opaque value, or auxiliary claim.
- `spec.k` contains only the target reachability claim. The claim is the proof
  goal, not an axiom or execution-replacing extension.

Consequently, there is no proof-local matched context, state footprint,
result-bearing abstraction, overlap/coverage obligation, dependent claim, or
bridge connection theorem to audit. All program-defined code executes through
the fixed reference semantics.

## Exact commands and actual outputs

The complete recorded run is:

```bash
./prove.sh > prove-output.log 2>&1
```

It exited `0`. `prove.sh` contains and ran these commands:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled
python3 differential_test.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual positive outputs and exits:

- LLVM `kompile`: exit `0`. It reported existing non-exhaustiveness warnings
  in unrelated imported helpers (`mapStrVS`, `floorFI`, `toF`, `ceilF`,
  `joinCodes`, and `valSeqAt`) and unused-variable warnings in `strLt`.
- `krun solution.mpy`: exit `0`; final `<k>` was `.K`, `<exc>` was `NoExc`,
  and `<exit-code>` was `0`.
- `krun concrete_tests.mpy`: exit `0`; all six assertions were consumed, final
  `<k>` was `.K`, `<exc>` was `NoExc`, and `<exit-code>` was `0`.
- `python3 differential_test.py`: exit `0`, with exact output
  `checked=121 mismatches=0`.
- Haskell `kompile`: exit `0`; it reported only the existing unused-variable
  warnings in `strLt`.
- The required positive `kprove`: exit `0`, with exact proof result `#Top`.
  The log then records `POSITIVE PROOF EXIT: 0`.

The A5 false-postcondition probe was run by `prove.sh` as:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

It exited `1` as expected. At the satisfiable witness `N = 8`, its residual
contained `<k> true ~> .K </k>` while the deliberately false destination
required `false`. The log records:

```text
EXPECTED FAILURE: false-postcondition mutation exited 1
```

The A1 body-sensitivity probe was run as:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

It exited `1` as expected. Changing the body to `return False` produced the
residual `<k> false ~> .K </k>` while the `N = 8` destination required `true`.
The log records:

```text
EXPECTED FAILURE: mutated-body claim exited 1
```

All raw output, including compiler warnings and stuck-claim residuals, is in
`prove-output.log`.

## Gate results

### Gate A — PASS

- **A1:** The exact translated module, definition, lookup, call, argument
  binding, body, and return execute under fixed semantics. The body mutation
  is rejected with the changed value visible in the residual.
- **A2:** There are no operational bridges. Every supplied configuration cell
  is constrained, including the module-scope update and restored call state.
- **A3:** Fixed semantics performs callee lookup, left-to-right argument
  evaluation, frame creation, parameter binding, return, and frame pop. The
  claim fixes the selected binding and complete continuation.
- **A4:** No proof-local functions, equations, lemmas, totality declarations,
  or rules exist.
- **A5:** `N = 8` realizes the domain and returns `true`; the deliberately
  false result mutation exits `1` with a discriminating residual.

### Gate B — PASS

- **B1:** The formal domain is all K integers, matching the task's intended
  integer input domain and covering the examples as well as negative values.
- **B2:** For the used fragment, K `Int` and CPython integers are both
  unbounded; integer comparison, modulo by the nonzero constant `2`, Boolean
  short-circuiting, function calls, and returns have the material behavior
  needed here. Non-integer Python values are outside the formal domain.
- **B3:** The elementary necessity/construction argument above establishes
  that the proved parity-and-lower-bound result is exactly the requested
  four-positive-even-summands property.
- **B4:** The implementation and the intended property agree.

### Gate C — PASS

- The trust boundary and every proof dependency are listed below.
- `prove.sh`, both mutation specs, `concrete_tests.py`,
  `concrete_tests.mpy`, `differential_test.py`, and the complete
  `prove-output.log` exist and reproduce the stated evidence.
- Formal proof, trusted inputs, finite evidence, and excluded behavior are
  distinguished explicitly.

## Trust boundary

No proof-local assumption is introduced. The external trust ledger is:

| Trusted component | Effect and dependent claim | Evidence |
|---|---|---|
| Supplied `reference-semantics/semantics.k` and its imported `MPY` rules, including `#loadAll`, statement sequencing, `FuncDef`, `Call`/`#applyK`, `#bindP`, name lookup, `Return`/`#pop`, `BoolOp`, `Compare`, `BinOp`, `applyCmp`, `applyBin`, and `pyMod` | Defines source execution, binding, control, state, and values for `SPEC.is-equal-to-sum-even` | Required reference input; SHA-256 `57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97`; LLVM concrete runs and both sensitivity probes |
| Supplied `py2mpy.py` | Maps `solution.py` to the AST executed and proved | Regeneration in `prove.sh`; generated term inspected; SHA-256 `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` |
| K v7.1.293, its LLVM/Haskell backends, builtin Int/Bool/Map theories, and solver | Executes and closes the reachability claim | Tool version checks; positive `#Top`; two deliberately false claims rejected |
| `prompt.py` as the statement of intent | Supplies the human-facing contract and examples | Read directly and left unchanged; SHA-256 `e49218abe89b2b138512731659d96115b045637b8cebe43d2407656209332e58` |

The compile-time non-exhaustiveness warnings concern imported semantic
operations that this program never constructs. They remain visible in
`prove-output.log`; this report does not claim that the supplied semantics is a
complete Python semantics.

## Empirically supported facts

`concrete_tests.py` is translated by the supplied translator and run with the
required LLVM `MPY-KRUN` definition. It checks the three prompt examples plus
`-2`, `9`, and `10`; all six assertions pass.

`differential_test.py` independently constructs the set of sums obtained by
exhaustively enumerating four values from the positive even integers
`2, 4, ..., 100`. It compares CPython execution of `solution.py` with membership
in that set for every integer from `-20` through `100`, inclusive. Its output
was `checked=121 mismatches=0`. This is finite evidence, not a universal proof;
the universal result comes from `kprove` plus the elementary mathematical
equivalence argument.

## Excluded behavior

- Inputs that are not K `Int` values, including floats, strings, collections,
  and Python's `bool` subtype behavior, are outside the formal theorem.
- The theorem uses the supplied partial Python semantics and does not claim
  adequacy for Python constructs not exercised by this function.
- The result is a partial-correctness reachability proof; no separate liveness
  theorem or resource bound is claimed.
- `#Top` reports closure under the supplied theory. The `VALIDATED` headline is
  the separate Gate A/B/C audit outcome, not a reinterpretation of that runner
  marker.
