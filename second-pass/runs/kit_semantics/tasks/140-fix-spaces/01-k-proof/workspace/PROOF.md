VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every symbolic string value
`str(CS:IntSeq)`, calling the module binding named `fix_spaces` whose parameter
list and body are exactly those in `solution.mpy` terminates with
`str(fixedSpaces(CS))`.

The proof executes the real function body through the supplied rules for name
lookup, calls, parameter binding, assignments, string iteration, comparisons,
conditionals, string concatenation, loop control, return, and frame cleanup.
The proof adds no rule that intercepts or replaces any of those operations.

`fixedSpaces` characterizes the requested transformation:

- a run of one space contributes `_`;
- a run of two spaces contributes `__`;
- a run of three or more spaces contributes `-`;
- every non-space character is preserved in order.

This is a partial-correctness reachability proof in K. The terminating loop is
also evident from the fixed string iterator consuming one constructor per
iteration, but termination is not the reachability theorem reported by
`kprove`.

## Formal claims

`spec.k` contains:

1. `SPEC.loop-invariant`: from a loop head over the remaining code sequence
   `CS`, it gives the exact final values of the local variables `result`,
   `spaces`, and `char`. It pins the active environment to the local scope,
   preserves `text`, and frames the arbitrary continuation and all untouched
   configuration cells.
2. `SPEC.target`: from the exact `fix_spaces` binding, closure body, argument,
   module environment, heap, stack, return state, exception state, and exit
   code, the call returns `str(fixedSpaces(CS))` and restores all framed state.

The loop invariant has three obligation shapes:

- Base: `.IntSeq` exits the loop, so the local state is unchanged.
- Step: one `#iterYield` binds `char`, executes the real branch, and returns to
  the invariant with a strictly shorter remaining `IntSeq`.
- Entry discharge: after exact initialization, the invariant yields the two
  final string components whose concatenation is `fixedSpaces(CS)`.

## Proof-extension inventory

### `#fixSpacesLoopBody` and `#fixSpacesBody`

- Class: definitional summaries (exact AST aliases).
- Semantic role: name syntax trees; they do not replace execution.
- Domain: the two nullary terms.
- Matched context and justification scope: only those exact terms; each has
  one unconditional equation.
- Context containment: exact equality of match and definition domains.
- State footprint: none while simplifying the alias. The resulting AST is
  then executed by fixed semantics.
- Value/control influence: determines the actual function and loop bodies.
- Value justification: the equations reproduce the generated constructors in
  `solution.mpy`, statement for statement.
- Justification: direct comparison with the generated translation plus the
  exact-body call in `SPEC.target`.
- Dependents: both formal claims.
- Validation: `spec-body-mutation.k` changes the initialization
  `spaces = ""` to `spaces = "-"`; `kprove` exits 1 and exposes the changed
  result `str(iCons(45, .IntSeq))`.

### `pendingSpace`

- Class: definitional summary.
- Semantic role: the exact state transition for `spaces` when the current
  character is a space; it does not rewrite a program term.
- Domain: every `IntSeq`.
- Equations: `"__"` maps to `"-"`; `"-"` remains `"-"`; every other sequence
  appends `"_"`.
- Coverage/overlap: the three guards are exhaustive and pairwise disjoint.
- Matched context and justification scope: the pure term
  `pendingSpace(P)` under exactly the displayed guards.
- Context containment: no continuation, binding, or cell is matched.
- State footprint: none.
- Value influence: contributes to `spaces`, the final returned value, and the
  postcondition.
- Value justification: exactly the nested `if`/`elif` branch in the source
  loop.
- Dependents: `resultAfter`, `pendingAfter`, `loop-invariant`, and `target`.
- Validation: the formal loop step covers each guard; concrete and Python
  tests cover run lengths 0, 1, 2, 3, and greater than 3.

### `resultAfter`

- Class: definitional summary.
- Semantic role: exact final `result` local after processing a remaining
  sequence; no execution is replaced.
- Domain: every triple `(CS, R, P)` of `IntSeq`.
- Equations: empty, space-head, and non-space-head cases.
- Coverage/overlap: `.IntSeq` is disjoint from `iCons`; the `32` and
  `C =/=Int 32` head cases are exhaustive and disjoint.
- Descent: every recursive equation removes one constructor from `CS`.
- Matched context and justification scope: only the pure function term and
  its exact constructor/guard case.
- Context containment: no operational context is matched.
- State footprint: none.
- Value influence: fixes the final `result` local and returned string.
- Value justification: the non-space equation uses the exact Python
  evaluation grouping `R + (P + char)`; the space equation leaves `R`
  unchanged.
- Dependents: `fixedSpaces`, `loop-invariant`, and `target`.
- Validation: the machine-checked loop invariant connects fixed execution to
  this value for its complete domain.

### `pendingAfter`

- Class: definitional summary.
- Semantic role: exact final `spaces` local after processing a remaining
  sequence; no execution is replaced.
- Domain, coverage, overlap, and descent: the same exhaustive empty,
  space-head, and non-space-head partition as `resultAfter`; recursion removes
  one `CS` constructor.
- Matched context and justification scope: the exact pure function term and
  guard.
- Context containment and state footprint: no operational context or state.
- Value influence: fixes the final `spaces` local and returned string.
- Value justification: a space applies `pendingSpace`; a non-space resets the
  pending sequence to empty.
- Dependents: `fixedSpaces`, `loop-invariant`, and `target`.
- Validation: exact connection through `SPEC.loop-invariant`.

### `charAfter`

- Class: definitional summary.
- Semantic role: exact final loop-target local; no execution is replaced.
- Domain: every `(CS:IntSeq, CH:Val)`.
- Coverage/overlap: disjoint empty/constructor equations cover all `IntSeq`.
- Descent: the recursive equation removes one constructor from `CS`.
- Matched context and justification scope: the pure function term.
- Context containment and state footprint: no operational context or state.
- Value influence: only the final local scope; it does not affect the
  postcondition after the loop.
- Value justification: each fixed `#bindTgt` writes the one-character string.
- Dependents: `SPEC.loop-invariant`.
- Validation: exact connection through the invariant's fixed-semantics step.

### `fixedSpaces`

- Class: definitional summary.
- Semantic role: names the returned code sequence; no execution is replaced.
- Domain: every `IntSeq`, covered by one unconditional equation.
- Matched context and justification scope: the pure term `fixedSpaces(CS)`.
- Context containment and state footprint: no operational context or state.
- Value influence: it is the target postcondition.
- Value justification: it concatenates the exact final `result` and `spaces`
  values, matching the source return expression.
- Dependents: `SPEC.target`.
- Validation: `SPEC.target` is a universal fixed-execution connection theorem;
  the false-result probe rejects the opposite value for a ground witness.

### `SPEC.loop-invariant`

- Class: derived reachability lemma/circularity.
- Semantic role: reasons about fixed loop execution; it is not an ordinary
  rewrite in `verification.k`.
- Domain: every remaining `CS`, prior `R`, pending `P`, prior `CH`, text `T`,
  active location `L`, parent `PAR`, arbitrary outer scopes not containing
  `L`, arbitrary continuation, and automatically framed untouched cells.
- Matched context: exactly
  `#loop(str(CS), Name("char"), #fixSpacesLoopBody)` in environment `L`, with
  an exact four-binding local scope.
- Justification scope: the same complete configuration accepted by the claim.
- Context containment: the arbitrary continuation is present in both the claim
  and its proof; the loop consumes only its own term and preserves the suffix.
- State footprint: reads `<k>`, `<env>`, `text`, `result`, `spaces`, and
  `char`; writes `result`, `spaces`, and `char`; preserves `text`, environment,
  outer scopes, heap, allocation counters, stack, return state, exception
  state, exit code, and continuation.
- Value influence: establishes every local value used by the return.
- Value justification: the exhaustive, terminating equations above, connected
  by one real loop iteration and the circularity.
- Dependents: `SPEC.target`.
- Control validation: fixed semantics performs `#iterNext`, `#bindTgt`, body
  execution, `#loopLbl`, and recurrence. There is no abrupt control bridge.
- Value validation: focused `kprove` returns `#Top`; ground tests have distinct
  outputs; false and body-mutated interpretations are rejected.

There are no operational bridges, opaque result-bearing symbols, ordinary
proof-local execution rewrites, priority shortcuts, or trusted proof-local
primitives.

## Exact commands and actual outputs

The complete reproducible workflow is in `prove.sh`; its combined actual output
is in `prove.out`.

### Translation and independent Python differential test

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 test_solution.py
```

Actual output and exit:

```text
Python examples: 4/4; exhaustive strings over {space,a,B} of length 0..7: 3280 checked, 0 mismatches
Exit: 0
```

The oracle in `test_solution.py` independently scans maximal space runs; it
does not reuse the proof equations or the implementation's pending-string
state machine.

### Concrete LLVM execution

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Actual result: both commands exited 0. `krun` ended with:

```text
<k> .K </k>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

The full final configuration is recorded in `prove.out`. LLVM compilation
printed only supplied-semantics warnings about several total functions and
unused variables; it did not fail.

### Symbolic compilation and positive proofs

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual output and exit:

```text
#Top
Exit: 0

#Top
Exit: 0
```

The second invocation proves the complete module, including both
`loop-invariant` and `target`. Haskell compilation exited 0 and printed only
unused-variable warnings from the supplied `str.k`.

### Gate A5 false-postcondition mutation

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual output and exit:

```text
WarnStuckClaimState
reached: str(.IntSeq)
claimed: str(iCons(95, .IntSeq))
Exit: 1
```

The witness is the realizable empty string. The mutation claims `_` instead of
the actual empty result.

### Gate A1 body-sensitivity mutation

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual output and exit:

```text
WarnStuckClaimState
reached: str(iCons(45, .IntSeq))
claimed: str(.IntSeq)
Exit: 1
```

The witness is again the empty string. Changing the real initialization from
`spaces = ""` to `spaces = "-"` changes the returned result to `-` and
invalidates the original theorem.

The wrapper logic in `prove.sh` treats both nonzero mutation results as expected
and itself exited 0:

```text
EXPECTED FAILURE: false-result mutation was rejected
EXPECTED FAILURE: material body mutation was rejected
PROVE_SH_EXIT=0
```

## Gate results

### Gate A — PASS

- A1: the target pins the exact name binding, one-parameter closure, body,
  argument, and module environment. Fixed semantics executes the body. The
  material body mutation is rejected.
- A2: there is no operational bridge. The target pins heap, counters, stack,
  return, exception, exit code, and scope restoration; the loop invariant
  records every local write and preserves all framed cells.
- A3: supplied rules perform lookup, left-to-right call/argument handling,
  parameter binding, branch evaluation, loop control, return, and frame pop.
  The loop claim accepts and preserves the same arbitrary continuation it
  proves over.
- A4: all proof-local function equations are truthful, exhaustive, disjoint,
  and structurally descending where recursive. The two non-space equations
  marked `[simplification]` are the same guarded defining equations, not
  additional facts.
- A5: the empty-string pre-state is realizable. The target constrains the
  returned string, and the false-result mutation exits 1 with the actual empty
  result visible in the residual.

### Gate B — PASS

- Input domain: the source contract is for a string. The theorem covers every
  supplied-semantics string `str(CS:IntSeq)` and intentionally excludes
  non-string arguments.
- Language model: strings are modeled as code sequences. The implementation
  only iterates codes, compares with U+0020 (`32`), and concatenates codes, so
  the model preserves every behavior material to this task. Symbolic inputs
  are not limited by the ASCII-only concrete literal parser. CPython behavior
  for non-string arguments and malformed code sequences is excluded.
- Summary-to-property adequacy: `spaces` encodes the current maximal run as
  empty, `_`, `__`, or `-`; another space advances/saturates that encoding and
  a non-space flushes it before that character. Thus `fixedSpaces` implements
  the prompt's maximal-run transformation. This derivation is independently
  supported by the 3,280-case differential test.
- Implementation alignment: all four prompt examples match, and no
  implementation/specification discrepancy was found.

### Gate C — PASS

Every evidence artifact named here exists and is replayed by `prove.sh`.
Positive proof output, negative-probe residuals, and concrete output are
preserved in `prove.out`, `vacuity-probe.out`,
`body-mutation-probe.out`, and `krun-smoke.out`.

## Trust boundary

| Component | Why outside this theorem | Influence | Dependents | Evidence |
|---|---|---|---|---|
| Supplied read-only `reference-semantics/` | It is the fixed execution model, not proved by this task | Value, control, state, exceptions, and the partial-correctness interpretation | All claims | LLVM smoke execution and Haskell proof; manual adequacy audit above |
| K v7.1.293 toolchain and backend | Verifier/runtime implementation is trusted infrastructure | Compilation and proof result | All machine-checked evidence | Clean `prove.sh` replay, two `#Top` results, discriminating negative probes |
| `py2mpy.py` and CPython AST parsing | The fixed translator is an input, not verified in K | Program-to-constructor identity | `solution.mpy` and exact AST aliases | Regeneration in `prove.sh`, direct artifact comparison, and body-sensitivity mutation |
| Human-language interpretation of “space” | Prompt interpretation is an adequacy judgment | Meaning of code `32` and maximal runs | Gate B conclusion | Prompt examples, invariant derivation, independent differential tests |

No unproved proof-local component affects the result. In particular, every
new result-bearing symbol has complete defining equations and a
machine-checked connection to fixed execution.

## Empirically supported facts

- `smoke.py` contains six K-executed cases: empty input, all four prompt
  examples, and a mixed case exercising run lengths 1, 2, and 4.
- `test_solution.py` checks the four examples and every string of length 0
  through 7 over `{space, a, B}` against an independently structured
  maximal-run oracle: 3,280 inputs and zero mismatches.
- These finite results support model and intent adequacy. They are not used as
  a substitute for the universal K reachability proof.

## Excluded behavior

- Non-string arguments.
- Python exceptions or behaviors outside the supplied semantics subset.
- A claim that the supplied K semantics or the K implementation is itself a
  formally verified model of CPython.
- Total-correctness/liveness as a `kprove` conclusion.
