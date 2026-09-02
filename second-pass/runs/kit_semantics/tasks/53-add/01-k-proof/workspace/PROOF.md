VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, for every pair of K integers
`X` and `Y`, loading the exact translation of `solution.py` into the initial
module scope and invoking `add(Int(X), Int(Y))` reaches the integer value
`X +Int Y`.

This is a partial-correctness reachability result in the sense of the Kit
workflow. It is conditional on the supplied semantics, `py2mpy.py`, and the K
toolchain implementing their stated meanings.

## Formal claim

`SPEC.add-correct` in `spec.k` starts with:

```k
#loadAll(
  Module(
    FuncDef("add", Params("x", "y"),
      Return(BinOp("+", Name("x"), Name("y"))))
  )
)
~> Call(Name("add"), Int(X:Int), Int(Y:Int))
```

and reaches `X +Int Y`. There is no `requires` clause, so the claim covers all
mathematical K integers. The claim also specifies the complete final
configuration: module loading leaves the exact `add` closure in scope 0;
`env`, `scopeLoc`, `heap`, `heapLoc`, `stack`, `ret`, `exc`, and `exit-code`
have their expected restored or unchanged values.

`check_artifact_identity.py` mechanically removes layout whitespace and checks
that the complete regenerated `solution.mpy` term occurs in `spec.k`. It also
checks that the `FuncDef` constructor used by `concrete-tests.mpy` is identical
to the translated function.

## Proof-extension inventory

There are no proof extensions.

- `verification.k` requires the supplied `reference-semantics/semantics.k` and
  imports `MPY`; it declares no syntax, function, equation, rewrite,
  simplification lemma, priority rule, opaque symbol, operational bridge, or
  auxiliary claim.
- `spec.k` contains only the positive target claim.
- The target claim is the theorem being proved, not an auxiliary fact used to
  close itself.
- Consequently, all proof-extension-record fields concerning match domains,
  justification domains, state footprints, value abstractions, and bridge
  validation are not applicable. The program-defined `add` body runs through
  fixed semantics.

The relevant fixed rules are the module loader and statement sequencing in
`semantics/core.k`, function binding and frame lifecycle in
`semantics/functions.k`, callee and left-to-right argument evaluation in
`semantics/call.k`, `BinOp` dispatch in `semantics/operators.k`, and the
integer-addition equation in `semantics/int.k`.

## Reproducible commands and actual results

The complete executable record is `prove.sh`; the combined output of the last
end-to-end run is `proof-run.log`. Raw negative-probe outputs are also
preserved in `vacuity-probe.log` and `body-mutation-probe.log`.

Program generation and identity:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 check_artifact_identity.py
```

Actual result: exit 0, with:

```text
Artifact identity: solution.mpy == spec program; concrete body matches
```

Independent CPython evidence:

```bash
python3 test_solution.py
```

Actual result: exit 0, with:

```text
CPython differential checks: 49; mismatches: 0
```

Concrete K build and execution:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled
```

Actual results: all exit 0. The LLVM compilation emitted the supplied
definition's non-exhaustive-match and unused-variable warnings. `solution.mpy`
ended with `.K` and the exact `add` closure in module scope. The concrete call
artifact ended with:

```text
"example_2_3" |-> 5
"example_5_7" |-> 12
"mixed_sign" |-> 5
"zero" |-> 0
```

Symbolic build and the sole positive target-proof command:

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

Actual results: both exit 0; `kprove` printed:

```text
#Top
```

The build/proof also reported pre-existing unused-variable warnings in
`reference-semantics/semantics/str.k`; those rules are not on this proof path.

False-postcondition probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`. The failed implication was:

```text
X +Int Y +Int 1
#Equals
X +Int Y
```

Changed-body probe:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`. The residual computation was
`X -Int Y`, and the failed implication compared it with `X +Int Y`.

Finally:

```bash
./prove.sh > proof-run.log 2>&1
```

Actual result: exit 0. The script treats both mutation commands as successful
validation only when their `kprove` invocations exit nonzero.

## Gate results

### Gate A — PASS

- A1: `solution.py`, regenerated `solution.mpy`, and the program term in
  `spec.k` are mechanically connected by `check_artifact_identity.py`.
  `add` is loaded, looked up by its module binding, and executed. No rule
  replaces the function call or body. Changing `+` to `-` makes the proof fail
  with result `X -Int Y`.
- A2: there is no operational bridge. The claim specifies the returned value,
  exact final module binding, restored call stack/environment, empty heap,
  `noRet`, `NoExc`, and exit code 0.
- A3: the fixed call rules perform binding lookup, evaluate arguments
  left-to-right, bind `x` and `y`, evaluate both names in the callee frame,
  return, pop the frame, and restore the caller. No fresh or opaque
  result-bearing value appears.
- A4: the independently rebuilt proof-local extension inventory is empty, so
  there are no local equations to audit for truth, overlap, totality, or
  descent.
- A5: the precondition is satisfiable; `X = 2`, `Y = 3` is a concrete witness.
  The result is materially constrained: the off-by-one postcondition mutation
  exits 1 with the expected failed implication.

### Gate B — PASS

- The formal domain is all integers, matching the prompt's `int` annotations
  and integer examples.
- K `Int` and CPython integers are both unbounded mathematical integers for
  this addition behavior; no overflow distinction arises.
- There is no summary-to-property bridge: fixed execution directly produces
  `X +Int Y`, which is exactly the requested addition result.
- The implementation `return x + y` aligns with the prompt and both examples.

The theorem intentionally does not generalize the word “numbers” beyond the
annotated integer domain. Python type annotations are not runtime guards, but
non-integer runtime values are outside this theorem.

### Gate C — PASS

Every evidence artifact named above exists, every command is in `prove.sh`, and
the actual combined output is preserved in `proof-run.log`. The report
separates the universal formal result, negative proof validation, finite
execution evidence, and assumptions.

## Trust boundary

- **Supplied `MPY` semantics.** The relevant module loading, binding, call,
  return, and integer-addition rules are fixed inputs rather than proof-local
  extensions. They affect control, scopes, and the result; `SPEC.add-correct`
  depends on them. Evidence consists of LLVM executions, the two mutation
  probes, and agreement with CPython on the recorded cases. These tests do not
  prove the semantics universally.
- **Supplied `py2mpy.py`.** Its CPython-AST-to-constructor mapping is outside
  the theorem. `solution.mpy` is regenerated on every run, and the identity
  check connects that output to the formal and concrete K artifacts.
- **K v7.1.293 and its LLVM/Haskell backends.** Compiler, runtime, prover, SMT
  reasoning, and host platform behavior are trusted.
- **CPython and `operator.add`.** They are used only as an independent finite
  test oracle, not as an axiom or proof rule.

## Empirically supported facts

- LLVM execution of the exact function constructor gives 5 for `(2, 3)`, 12
  for `(5, 7)`, 5 for `(-4, 9)`, and 0 for `(0, 0)`.
- CPython execution agrees with `operator.add` on the Cartesian product of
  `(-100, -7, -1, 0, 1, 8, 100)`, for 49 checks and zero mismatches.
- These finite runs support implementation and semantics adequacy; the
  universal integer conclusion comes from `kprove`, not from testing.

## Excluded behavior

- Non-integer inputs, including floats, strings, lists, booleans, and custom
  Python objects, are outside the formal domain.
- Calls made in an arbitrary pre-existing or adversarial Python module state
  are outside the claim; it models normal loading into the supplied initial
  module configuration.
- Behaviors not modeled by the supplied Python subset are outside the theorem.
- Correctness of the translator, supplied semantics, K implementation, and SMT
  solver is trusted rather than proved here.
- As specified by the Kit workflow, the report claims partial correctness and
  does not separately claim a liveness theorem.
