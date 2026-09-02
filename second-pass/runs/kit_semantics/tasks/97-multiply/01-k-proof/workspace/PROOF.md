VALIDATED

# What is proven

Under the supplied MPY reference semantics, the exact translated body of
`multiply(a, b)` returns

```k
pyMod(A, 10) *Int pyMod(B, 10)
```

for every pair `A:Int`, `B:Int`. There is no precondition and no finite bound.
The claim also requires the call to restore the original environment, scope
map, heap, allocation counters, stack, return cell, exception cell, and exit
code after returning.

This is a K partial-correctness result. The prompt's valid domain is two Python
integers; non-integer arguments are outside that stated domain.

# Formal claim

`SPEC.multiply-correct` in `spec.k` starts with `Name("multiply")` bound to the
closure whose body is exactly:

```k
Return(
  BinOp(
    "*",
    BinOp("%", Name("a"), Int(10)),
    BinOp("%", Name("b"), Int(10))
  )
)
```

It invokes that closure through the fixed call, name-lookup, argument-binding,
operator, return, and frame-pop rules. Its destination is the symbolic product
of the two fixed-semantics Python remainders. With divisor 10, `pyMod` produces
the direct Python `% 10` digit extraction required by the naive reference-
implementation reading of the prompt, including negative inputs.

`check-program-identity.py` checks the source signature and AST, and checks that
the same canonical K body occurs in both `solution.mpy` and `spec.k`.

# Proof-extension inventory

There are no proof-local extensions.

- `verification.k` only imports the supplied `MPY` module.
- It defines no functions, equations, simplification rules, ordinary rewrites,
  operational bridges, opaque summaries, trusted primitives, or auxiliary
  claims.
- `spec.k` contains only the target reachability claim. The program is
  loop-free and does not recur to the claim's initial configuration, so the
  target claim is not used as a circularity.
- `pyMod` and integer multiplication are fixed rules from the supplied
  `MPY-INT` semantics, not proof extensions.

Consequently, no proof-extension record under the four extension classes is
applicable.

# Exact commands and actual results

The complete reproducible command is:

```sh
./prove.sh
```

`prove.sh` records and runs these positive commands:

```sh
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 check-program-identity.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual results from the final run:

- Program identity check: `PROGRAM IDENTITY: PASS`, exit 0.
- LLVM compilation: exit 0.
- Concrete execution: exit 0, final `<k> .K </k>`,
  `<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`.
- Haskell compilation: exit 0.
- Required target proof: output `#Top`, exit 0.
- `prove.sh`: exit 0 after also checking both expected failures below.

The compilers emitted warnings in supplied, unmodified semantics modules about
unused variables and non-exhaustive unrelated helpers. No warned helper is used
by this integer-only program.

# Negative validation probes

The false-postcondition probe keeps the real body but requires 17 for the
realizable input `(148, 412)`:

```sh
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`; the residual `<k>` value is
16, which does not unify with 17.

The operational body-sensitivity probe changes the body operator from `*` to
`+` but still requires 16 for `(148, 412)`:

```sh
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`; the changed body produces the
residual `<k>` value 10, which does not unify with 16.

The exact expected-failure control flow is preserved in `prove.sh`.

# Gate results

## Gate A — PASS

- A1: The target executes the exact program-defined closure body. The identity
  checker passes, and the changed-body probe is rejected with the changed
  result visible.
- A2: There are no operational bridges. The claim pins all MPY state cells and
  proves the call frame's state changes are restored at return.
- A3: The initial scope pins `"multiply"` to the exact closure. Fixed semantics
  performs lookup, left-to-right argument evaluation, parameter binding,
  return, and frame popping.
- A4: There are no proof-local equations or rules to audit for consistency,
  overlap, totality, or descent.
- A5: `(148, 412)` realizes the guard-free precondition. The false
  postcondition is rejected and exposes the real result 16.

## Gate B — PASS

- B1: `A:Int` and `B:Int` range symbolically over all unbounded K integers.
  There are no sign, magnitude, or enumeration restrictions.
- B2: The supplied model represents the material contract's integer values and
  defines Python-floored remainder for the fixed positive divisor 10.
- B3: The postcondition is the product of the two `% 10` results; it is the
  requested result itself, not an opaque summary awaiting a meaning theorem.
- B4: The implementation, generated constructor term, executed closure, and
  formal postcondition all use the same direct expression.

## Gate C — PASS

- All asserted build, execution, proof, and mutation evidence has an existing
  artifact and exact command.
- Formal proof evidence, finite concrete evidence, and conditional trust
  boundaries are separated below.
- Both mutation probes retain their non-zero result and diagnostic residual.

# Trust ledger

| Trusted component | Effect and dependents | Evidence |
|---|---|---|
| Supplied, unmodified `reference-semantics/` | Defines value, binding, control, state, return, `%`, and `*` behavior for the target and both probes | LLVM concrete run, Haskell symbolic proof, and two rejected mutations |
| K v7.1.293 backends and builtin integer theory | Executes and proves every K claim | Version checks, successful compilation, `#Top`, and discriminating negative probes |
| Supplied `py2mpy.py` | Translates `solution.py` to `solution.mpy` | Regeneration exits 0; `check-program-identity.py` confirms the source AST and the body shared with the claim |
| MPY-to-intended-Python correspondence for the exercised subset | Connects the theorem under the supplied semantics to the HumanEval contract | The fixed `pyMod` definition uses floored remainder; all four prompt examples and two extra negative cases execute successfully |

No program-derived value is opaque, no execution is bypassed, and no result-
bearing external primitive is used.

# Empirical evidence

`concrete-tests.py` contains the four prompt examples:

```text
(148, 412) -> 16
(19, 28) -> 72
(2020, 1851) -> 0
(14, -15) -> 20
```

It also checks `(-14, 15) -> 30` and `(-14, -15) -> 30`, documenting Python's
nonnegative remainder for a positive divisor. The LLVM run completed with no
assertion exception. These six ground cases support intent validation; the
universal result comes from `SPEC.multiply-correct`, not from testing.

# Excluded behavior

- Non-integer arguments are excluded by the prompt's valid-input contract.
- Behavior under a Python implementation other than the supplied MPY model is
  conditional on the model-correspondence trust boundary above.
- No separate total-correctness or resource-bound theorem is claimed.
