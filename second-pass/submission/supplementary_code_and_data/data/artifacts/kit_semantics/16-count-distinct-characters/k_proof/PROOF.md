VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, for every finite symbolic
`CS:IntSeq`, calling the exact translated body of
`count_distinct_characters(str(CS))` returns

```k
isLen(dedupCodes(mapLower(CS)))
```

This is the reference semantics' cardinality of the set of character codes
after case lowering. The claim has no length bound and no precondition, so it
covers empty and nonempty `IntSeq` values of arbitrary finite length. This is a
partial-correctness result in the Kit sense; no separate liveness theorem is
claimed.

## Formal claim

`SPEC.count-distinct-characters` in `spec.k` starts from:

- the exact public function call;
- an exact module binding from the public name to the closure translated from
  `solution.py`;
- the concrete builtins scope and otherwise pristine runtime cells.

It reaches the result above while restoring/preserving `env`, `scopes`,
`scopeLoc`, `heap`, `heapLoc`, `stack`, `ret`, `exc`, and `exit-code`. The
function lookup, argument evaluation, method call, built-in calls, return, and
frame pop all execute through the fixed semantics.

The body in the closure is the body emitted in `solution.mpy`:

```k
Return(
  Call(
    Name("len"),
    Call(
      Name("set"),
      Call(Attribute(Name("string"), "lower"), .Exprs)
    )
  )
)
```

## Proof-extension inventory

The independently rebuilt inventory is empty:

- `verification.k` only imports the supplied `MPY` module.
- `spec.k` contains one reachability claim and no function declarations,
  equations, simplification rules, ordinary rewrites, priority rules, opaque
  terms, operational bridges, or auxiliary claims.
- Therefore there is no proof-local extension to classify and no match domain,
  state footprint, value abstraction, context-containment argument, or
  dependent claim to record.

The functions `mapLower`, `dedupCodes`, and `isLen` and the call/lookup rules
are part of the supplied fixed semantics, not proof extensions.

## Exact commands and actual outputs

The complete reproducible command sequence is executable as:

```bash
./prove.sh
```

It performs these positive build and proof commands:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 test_solution.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

The final end-to-end run exited 0. Its material output was:

```text
cases=1563 mismatches=0
unicode_witness='İ' lowered_code_points=[105, 775] result=2
"empty_result" |-> 0
"example_one_result" |-> 3
"example_two_result" |-> 4
#Top
```

The LLVM compile exited 0 with supplied-semantics non-exhaustiveness warnings
for unrelated functions (`mapStrVS`, float helpers, `joinCodes`, and
`valSeqAt`). The Haskell compile exited 0 with unused-variable warnings in
`strLt`. None of those symbols lies on this claim's execution path.

The exact negative validation commands were:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Both exited 1 as expected:

```text
VACUITY_EXIT=1
BODY_MUTATION_EXIT=1
```

`vacuity.out` records the rejected equality between
`isLen(dedupFrom(mapLower(CS), .IntSeq)) +Int 1` and the genuine result.
`body-mutation.out` records the rejected equality between `0` and the genuine
result. The positive proof output is preserved in `positive-proof.out`; the
full reproducibility log is `prove-run.out`.

## Gate results

### Gate A — PASS

- **A1:** The exact program-defined closure body executes under fixed
  semantics. Replacing it with `return 0` makes the proof fail with exit 1.
- **A2:** No execution is skipped. Every runtime cell exposed by the active
  configuration is pinned on both sides of the claim.
- **A3:** The initial scopes map pins
  `count_distinct_characters` to the exact closure, and lookup, left-to-right
  argument evaluation, return control, and frame restoration use only supplied
  rules. There is no framed operational bridge.
- **A4:** No proof-local equation or total function was added, so there are no
  extension coverage or overlap obligations.
- **A5:** `CS = .IntSeq` is a realizable witness (result 0), as are the two
  prompt examples. The off-by-one postcondition mutation fails with exit 1 and
  an implication residual.

### Gate B — PASS

- **B1:** The prompt's input is a string. The theorem quantifies over an
  unrestricted symbolic `IntSeq`, the supplied representation of arbitrary
  finite strings; it does not bound or enumerate lengths.
- **B2:** The program is faithful to CPython, but the fixed model has an
  explicit text/case-mapping boundary: its literal loader is ASCII-only and
  `lowerC` maps only ASCII `A`–`Z`. The theorem nevertheless covers every
  `IntSeq` represented by the fixed model, without a candidate-added
  restriction. This is the shared contract's model-boundary case, not domain
  narrowing. A concrete divergence witness is U+0130: CPython lowers `"İ"` to
  code points `[105, 775]`, so the implementation returns 2, whereas the fixed
  model leaves code 304 unchanged and returns 1.
- **B3:** The postcondition is the fixed semantics' actual lower/set/length
  composition, not an opaque summary or asserted human-facing lemma.
- **B4:** The implementation `len(set(string.lower()))` directly implements
  the prompt's requested count.

### Gate C — PASS

The trust ledger below names every boundary and its evidence. All reported
commands, outputs, mutations, and tests exist in the workspace. Formal results,
conditional model adequacy, and finite empirical evidence are kept separate.

## Trust boundary

| Component | Role and influence | Dependents | Evidence |
|---|---|---|---|
| Supplied `MPY` semantics | Trusted operational definition; lookup/call rules affect control and state, while `applyMethod(..., "lower", ...)`, `mapLower/lowerC`, `applyBuiltin("set", ...)`, `dedupCodes`, `applyBuiltin("len", ...)`, and `isLen` determine the result | Target claim | Read-only supplied source, LLVM examples, unbounded Haskell proof, and both mutation probes |
| `py2mpy.py` | Supplied translation boundary from CPython AST to the K constructor program | Program identity | Exact regeneration command; emitted body in `solution.mpy` matches the closure body in `spec.k` |
| K v7.1.293 and its LLVM/Haskell backends | Compiler, concrete executor, symbolic prover, and SMT implementation | All machine-checked evidence | Version commands succeeded; clean end-to-end `prove.sh` exit 0 |
| Unicode case behavior beyond the fixed ASCII mapping | Conditional adequacy boundary; affects connection to CPython Unicode behavior, not the theorem under `MPY` | HumanEval interpretation for non-ASCII inputs | Explicit U+0130 fixed-model/CPython witness and independent Python tests |

No program-derived value is opaque, and there is no proof-local trusted
primitive or operational bridge.

## Empirically supported facts

- LLVM execution produced 0, 3, and 4 for the empty string and the two prompt
  examples.
- `test_solution.py` compares the implementation against an independently
  written list-based oracle (no `set`) on the examples, boundary/Unicode cases,
  and every string of lengths 0 through 4 over `aA0!zZ`: 1,563 cases and zero
  mismatches.
- The U+0130 test demonstrates the recorded model boundary. These finite tests
  validate examples and boundaries; they are not used as a universal proof.
- The postcondition and body mutations provide discrimination evidence, not
  proof axioms.

## Excluded behavior

- Non-string arguments are outside the prompt's `string: str` contract.
- The formal K result is conditional on the supplied reference semantics.
  Full CPython Unicode lowercase behavior is not established by that
  ASCII-oriented model; this is recorded as a model boundary rather than
  silently excluded from the symbolic input domain.
- No claim about time, memory use, or a separate termination/liveness theorem
  is made.

The positive target execution marker is `KPROVE_PASSED`: the sole required
positive target claim printed `#Top`, exited 0, and Gate B covers the full
unbounded contract relative to the supplied model. This execution marker is
separate from the `VALIDATED` proof-quality headline above.
