VALIDATED

## What is proven

Under the supplied `MPY` semantics, `digitSum` is partially correct for every
finite modeled string `str(CODES)`, with no length bound. The named function
call reaches:

```k
digitSumIS(CODES)
```

where `digitSumIS` recursively adds a character code exactly when the supplied
one-character `str.isupper()` semantics is true. In this semantics that is the
ASCII uppercase range `65..90`. Lookup, argument evaluation, string iteration,
method dispatch, `ord`, assignment, return, and frame removal all execute using
the unmodified reference semantics.

This is a partial-correctness reachability result. It does not separately claim
a liveness theorem.

## Formal claims

- `SPEC.digitSum-loop` is the circularity for arbitrary remaining
  `CODES:IntSeq`, arbitrary accumulator `TOTAL:Int`, original string contents,
  and current loop-variable value. Its exact continuation is the translated
  singleton `Return(Name("total")) .Stmts` followed by `#endcall`. It reaches
  `TOTAL +Int digitSumIS(CODES)` after the real function frame is popped.
- `SPEC.digitSum-entry` invokes the exact translated closure through the
  `"digitSum"` module binding on arbitrary `str(CODES:IntSeq)` and reaches
  `digitSumIS(CODES)`.

The two equations defining the result are:

```k
digitSumIS(.IntSeq) = 0
digitSumIS(iCons(C, REST))
  = (if isUpperC(C) and not isLowerC(C) then C else 0)
    + digitSumIS(REST)
```

## Proof-extension inventory

### `digitSumIS`

- Extension: the `[function, total]` symbol `digitSumIS(IntSeq)` and its two
  equations in `verification.k`.
- Class: definitional summary.
- Semantic role: names the mathematical result; it never rewrites a program
  term or replaces execution.
- Domain: every `IntSeq`; `.IntSeq` and `iCons(C, REST)` are disjoint and
  exhaustive.
- Matched context: summary-function applications only; no continuation,
  binding, control stack, configuration cell, frame, wildcard, or priority is
  matched.
- Justification scope and containment: the base equation covers the empty
  constructor; the recursive equation covers every nonempty constructor and
  descends structurally to `REST`.
- State footprint: none.
- Value influence: the loop and entry postconditions.
- Value justification: its condition is the exact fixed-semantics reduction of
  one-character `str.isupper()`; the loop claim connects every recursive
  equation to fixed execution.
- Dependents: both claims in `SPEC`.
- Control validation: not applicable because this is not an operational
  bridge.
- Value validation: the full symbolic connection claim, prompt examples,
  208-case differential run, false-postcondition probe, and body-sensitivity
  probe described below.

### `SPEC.digitSum-loop`

- Extension: the loop-invariant reachability claim.
- Class: derived lemma, proved as a K circularity.
- Semantic role: summarizes execution only through a machine-checked
  reachability claim; it is not an ordinary rewrite rule.
- Domain: arbitrary finite remaining `IntSeq`, `TOTAL:Int`, original modeled
  string, and `CHAR:Val`, in the exact ordinary three-local function frame.
- Matched context: exact `#loop` body, exact singleton-return continuation,
  exact `#endcall`, module binding to the exact translated closure, caller and
  callee environments, frame stack, scope locations, empty heap, return state,
  exception state, and exit code.
- Justification scope and containment: identical to the claim's complete
  match; there are no continuation or cell ellipses.
- State footprint: reads and removes the callee scope, restores the caller
  environment and scope location, pops the frame, and preserves the explicitly
  stated heap, return, exception, and exit-code cells.
- Value influence: supplies the result used by the entry claim.
- Value justification: base and inductive paths execute the supplied iterator,
  method, builtin, arithmetic, assignment, and frame rules and close against
  `digitSumIS`.
- Dependents: `SPEC.digitSum-entry`.
- Control validation: exact-continuation matching plus successful concrete
  calls; no abrupt-control bridge exists.
- Value validation: `#Top` for the full spec; the two negative probes are
  rejected.

There are no operational bridges, trusted proof-local primitives,
simplification lemmas, priority rules, opaque result symbols, or program-call
interceptions in `verification.k` or `spec.k`.

## Reproducible commands and actual results

The complete executable record is `./prove.sh`, which exited `0`.

Translation:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 py2mpy.py body_mutation.py > body_mutation.mpy
```

All exited `0`.

Concrete LLVM build and executions:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
krun body_mutation.mpy --definition runtime-kompiled
python3 differential_test.py
```

All exited `0`. Both `krun` runs ended with `.K`, `NoExc`, and exit code `0`.
The differential output was:

```text
cases=208 python_mismatches=0 krun_assertion_failures=0 krun_exit=0
```

Symbolic Haskell build and required positive target proof:

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Both exited `0`. The complete positive proof output recorded in
`proof-positive.log` is:

```text
#Top
```

The compilers also printed warnings originating in supplied, unrelated
reference-semantics functions and unused variables; none was an error or a
stuck target path.

False-postcondition probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

This exited `1` as required. For the satisfiable empty-string witness, the
mutated claim expected `digitSumIS(.IntSeq) + 1`; the residual contained
`<k> 0 ~> .K </k>` and `WarnStuckClaimState`.

Body-sensitivity probe:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

This exited `1` as required. The exact loop-body contribution was changed from
`ord(char)` to `0`; on the ground input `"A"` the unchanged theorem expects
`65`, while the residual contained `<k> 0 ~> .K </k>`.

## Gate results

### Gate A — PASS

- A1: the exact translated closure body executes. No program-defined operation
  is summarized by an ordinary rule. The material body mutation invalidates the
  unchanged result claim.
- A2: no operational bridge exists. Every active configuration cell is stated,
  and the loop claim includes the real frame-pop transition.
- A3: the module binding, builtin `ord` lookup, argument order, receiver method
  call, loop continuation, return, and caller restoration are exact.
- A4: `digitSumIS` has disjoint, exhaustive constructor equations and strict
  structural descent.
- A5: empty string and `"A"` are realizable witnesses. The off-by-one
  postcondition mutation is rejected.

### Gate B — PASS

- B1: the formal entry domain is every finite `IntSeq` carried by the supplied
  string value, not fixed examples or bounded lengths. This covers the full
  material string domain represented by the reference semantics.
- B2: the reference semantics uses an ASCII character model for literals and
  case classification. CPython Unicode case behavior is a fixed-model boundary,
  not a candidate-added restriction. The theorem covers every code sequence the
  symbolic model represents.
- B3: the recursive summary directly states the sum of exactly those codes for
  which the fixed one-character `isupper()` is true, and the loop claim formally
  connects it to execution.
- B4: the implementation matches the prompt examples and the independent ASCII
  contract oracle.

### Gate C — PASS

All assumptions, commands, artifacts, input scopes, outputs, and negative
results are recorded here and in the logs produced by `prove.sh`. Formal,
conditional, empirical, and excluded conclusions are separated below.

## Trust boundary

| Component | Effect and dependents | Evidence |
|---|---|---|
| Supplied, unmodified `reference-semantics/` | Defines all value, binding, control, state, and partial-correctness behavior used by both claims | Required LLVM/Haskell builds, six prompt examples, symbolic `#Top`, and concrete differentials |
| Fixed `py2mpy.py` | Establishes the Python-AST-to-constructor representation used by `solution.mpy` | Successful translation, direct body identity in the formal closure, and concrete execution |
| K v7.1.293, Haskell backend, LLVM backend, and their solver/runtime | Trusted proof and execution infrastructure for every reported command | Clean command exits and recorded outputs |
| ASCII string/case model in the supplied semantics | Determines that uppercase means codes `65..90`; affects the result theorem | Exact imported rules, all-printable-ASCII coverage, and explicit model-boundary disclosure |

No unproved program-local value oracle or control rule is trusted.

## Empirically supported facts

- `smoke.py` checks all six prompt examples through the LLVM semantics.
- `differential_test.py` uses an independent oracle
  `sum(code for code if 65 <= code <= 90)`. It checks the examples, all 95
  printable ASCII characters in one boundary string, a boundary-focused
  string, and 200 deterministic random printable-ASCII strings of lengths
  `0..64`. CPython and LLVM-semantic execution had zero mismatches.
- `body_mutation.py` concretely confirms that the mutated program returns `0`
  for `"A"` before the symbolic body-sensitivity proof rejects the unchanged
  result property.

These finite tests support validation; the universal result comes from the
symbolic claims, not from testing.

## Excluded behavior

- Non-string arguments are outside the prompt's stated input type and the entry
  claim.
- CPython Unicode-specific `str.isupper()` classification is outside the
  supplied semantics' ASCII model. `solution.py` will use CPython's Unicode
  behavior when run directly, but that behavior is not the K theorem.
- Total termination and resource bounds are not claimed separately from the
  partial-correctness reachability proof.
