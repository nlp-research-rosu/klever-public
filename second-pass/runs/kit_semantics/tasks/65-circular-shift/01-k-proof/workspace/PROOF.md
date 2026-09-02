VALIDATED

## What is proven

For every pair `X:Int` and `SHIFT:Int` represented by the supplied K model,
calling the exact translated `circular_shift` function returns:

- the reverse of `str(X)` when `SHIFT > len(str(X))`;
- `str(X)` when that first guard is false and `SHIFT < 0`; or
- the length-sized window beginning at `len(str(X)) - SHIFT` in
  `str(X) + str(X)` otherwise.

For `0 <= SHIFT <= len(str(X))`, the last case is the suffix beginning at
`len(str(X)) - SHIFT` followed by the preceding prefix, which is precisely a
right circular shift. The negative-shift case preserves the behavior of the
direct two-slice HumanEval implementation.

The claims also establish that the call restores the caller environment, scope
allocator, empty heap, heap allocator, empty call stack, return cell, exception
cell, and exit code shown in `spec.k`. This is a partial-correctness result under
the supplied semantics and proof theory.

## Formal claim

`spec.k` contains three complementary, symbolic, unbounded claims:

1. `SPEC.circular-shift-reverse` requires
   `SHIFT >Int isLen(strToCodes(Int2String(X)))`.
2. `SPEC.circular-shift-negative` requires the negation of the first guard and
   `SHIFT <Int 0`.
3. `SPEC.circular-shift-rotate` requires the negation of both guards.

The guards partition all K integer pairs; there is no length bound, finite
unrolling, or example-only restriction. Each claim starts from a normal call
whose global binding is `circularShiftClosure` and reaches
`circularShiftResult(X, SHIFT)`.

## Proof-extension inventory

### `circularShiftClosure`

- Class: definitional summary.
- Domain: one unguarded, total equation.
- Role: compactly names the exact `closureVal` transliterated in
  `solution.mpy`.
- Execution: it does not replace a call or body step. The supplied semantics
  still performs name lookup, left-to-right argument evaluation, parameter
  binding, frame creation, every statement/expression in the body, return, and
  frame restoration.
- State footprint: the definition itself reads and writes no cells.
- Value/control influence: it selects the exact program binding and body.
- Justification: direct constructor-for-constructor comparison with
  `solution.mpy`. The body-sensitivity mutation replaces it with
  `return str(x)` and is rejected.
- Dependents: all three target claims.

### `circularShiftResult`

- Class: definitional summary.
- Domain: three disjoint and exhaustive guards: `B`, `not B and C`, and
  `not B and not C`, where `B` is the oversized-shift comparison and `C` is
  `SHIFT <Int 0`.
- Role: names the requested mathematical return value using only fixed
  semantic functions: `Int2String`, `strToCodes`, `isLen`, `seqConcat`,
  `slAdjust`, and `buildIS`.
- Execution: it occurs only in claim destinations; no rule intercepts program
  execution.
- State footprint: none.
- Value influence: it fully constrains the returned `Str`.
- Value justification: exhaustive equations mirror the three source branches.
  In the rotation branch, a length-`n` window `[n-s, 2n-s)` in a doubled
  sequence is the original suffix `[n-s, n)` concatenated with prefix
  `[0, n-s)`.
- Dependents: the corresponding target claims and the two negative probes.

### `#Ceil(strToCodes(Int2String(X))) => #Top`

- Class: trusted-primitive definedness fact for a fixed K hook.
- Domain: every K `Int`.
- Role: establishes that the supplied partial ASCII `strToCodes` function is
  defined on the output of K's `Int2String` hook.
- Execution: it does not rewrite `Int2String`, choose any digit, replace any
  program operation, or constrain the resulting `IntSeq`.
- State footprint: none.
- Value influence: no value equation; it enables defined symbolic string
  conversion and therefore the branch guards.
- Justification/trust: K's fixed `Int2String` contract emits the optional minus
  sign and decimal digits, all ASCII. `strToCodes` then terminates because each
  character satisfies its `< 128` guard.
- Dependents: all target claims.
- Evidence: reference-semantics execution includes positive, zero-length-shift,
  oversized-shift, leading-zero-result, negative-shift, and negative-`X`
  witnesses; the independent differential test covers 16,884 cases.

There are no operational bridges, opaque result symbols, priority rules,
program-call interceptions, auxiliary circularities, or proof-local rules that
rewrite a program result to its postcondition.

## Commands and actual outputs

The complete reproducible workflow is `./prove.sh`.

```bash
python3 py2mpy.py solution.py > solution.mpy
```

Output: none. Exit: 0.

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Output: compiler warnings from the supplied semantics about several
non-exhaustive total functions and unused `strLt` pattern tails. Exit: 0.

```bash
krun solution.mpy --definition runtime-kompiled
```

Output: final configuration with `<k> .K </k>`, the exact
`circular_shift` closure in module scope, empty heap/stack, `NoExc`, and exit
code 0. Exit: 0.

```bash
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
krun concrete_tests.mpy --definition runtime-kompiled
```

Output: final configuration with `<k> .K </k>`, empty heap/stack, `NoExc`, and
exit code 0 after all eight assertions. Exit: 0.

```bash
python3 differential_test.py
```

Output:

```text
differential: 16884 cases, 0 mismatches
```

Exit: 0.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Output: the supplied `strLt` unused-variable warnings and an unused-pattern
warning for the proof-local definedness fact. Exit: 0.

```bash
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.circular-shift-reverse
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.circular-shift-negative
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.circular-shift-rotate
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Actual output from each command: `#Top` followed by the same compiler warnings.
Each command exited 0.

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual output: `WarnStuckClaimState`; the residual return is the code sequence
for `"21"` while the deliberately false destination is `"12"`. Exit: 1,
expected.

```bash
kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual output: `WarnStuckClaimState`; the mutated body returns the code sequence
for `"12"` instead of the required `"21"`. Exit: 1, expected.

The enclosing `./prove.sh` command exited 0.

## Gate results

- Gate A — PASS. The exact program-defined body executes under fixed semantics;
  no operational bridge exists; all summary cases are disjoint and exhaustive;
  the only trust fact is true over its complete `Int` domain; a satisfiable
  witness exists; both the false-result and body-sensitivity mutations fail.
- Gate B — PASS. The three symbolic claims collectively cover arbitrary,
  unbounded K integers for both parameters and formalize the full prompt
  behavior. The doubled-string window is mathematically the requested right
  rotation, and oversized shifts reverse the representation as required.
- Gate C — PASS. The sole trust item, every dependent claim, exact commands,
  concrete inputs, independent oracle, outputs, mutation residuals, and model
  boundaries are recorded in existing artifacts.

## Trust boundary

The proof is conditional only on the fixed K hook fact that `Int2String(I)`
produces the ASCII decimal representation of every K integer `I`. The proof
does not assume the returned digit sequence: fixed semantics threads that exact
sequence through length, concatenation, and slicing.

The reference model uses arbitrary-precision K integers, matching Python's
mathematical integer behavior for this task, and ASCII code sequences for
strings. Decimal integer representations fall entirely inside that ASCII
boundary.

## Empirically supported facts

- `concrete_tests.mpy` runs eight assertions through the supplied LLVM
  semantics. It covers both prompt examples, both threshold sides, shift zero,
  shift equal to length, a leading-zero result, a negative shift, and a
  negative integer.
- `differential_test.py` compares the doubled-window implementation with an
  independently written direct two-slice oracle for every `x` in `[-200, 200]`
  plus one 21-digit integer, and every shift in `[-12, 29]`: 16,884 cases and
  zero mismatches.
- These finite checks support implementation and adequacy; the universal result
  comes from the three symbolic K claims, not from testing.

## Excluded behavior

- Non-integer arguments are outside the prompt's integer contract and the
  formal domain.
- The theorem uses the supplied K model rather than all CPython implementation
  details outside this pure function.
- As specified by the Kit, the report is about partial correctness; no separate
  liveness theorem is claimed.
