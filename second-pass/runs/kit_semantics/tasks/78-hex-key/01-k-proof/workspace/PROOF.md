VALIDATED

## What is proven

Under the supplied `MPY` semantics, invoking the exact translated
`hex_key` closure on any finite `str(CS)` value returns `hexCount(CS)` if the
invocation terminates. `hexCount` adds one for each one-character string that
occurs in `"2357BD"` and zero otherwise.

This is a partial-correctness theorem. It does not itself prove termination.
For the finite strings in the HumanEval contract, concrete execution terminates
and the implementation has the expected ordinary Python loop structure.

## Formal claims and validation scope

- Program boundary: `SPEC.hex-key` begins with lookup and invocation of
  `Name("hex_key")`. The module binding is pinned to a closure containing the
  exact body in `solution.mpy`, including parameter binding, both
  initializations, the `for` loop, membership comparison, augmented assignment,
  return, and call-frame pop.
- Input domain: all finite K `IntSeq` terms wrapped by `str`. This is broader
  than the prompt's domain of empty or valid uppercase hexadecimal strings, so
  no prompt-valid input is excluded.
- Observable final state: the returned integer. The entry claim also pins and
  preserves the module environment, empty heap, heap counter, scope counter,
  empty stack, return state, exception state, and exit code.
- Intended property: count exactly the occurrences of `2`, `3`, `5`, `7`,
  `B`, and `D`.

The two claims in `spec.k` are:

1. `SPEC.hex-loop`: from the exact loop head and exact
   `Return(Name("count")) .Stmts ~> #endcall` continuation, update `count`
   from `ACC` to `ACC +Int hexCount(CS)` while allowing `digit` to hold the
   loop's final character.
2. `SPEC.hex-key`: the exact function invocation returns `hexCount(CS)`.

## Proof-extension inventory

### `hexCount`

- Extension: the symbol `hexCount(IntSeq)` and its two equations in
  `verification.k`.
- Class: definitional summary.
- Semantic role: names a mathematical value; it does not rewrite or replace a
  Python program term.
- Domain: every `IntSeq`. `.IntSeq` and `iCons(C, CS)` are disjoint and
  exhaustive.
- Matched context and justification scope: equations apply only to
  `hexCount`; no operational configuration or continuation is matched.
- Context containment: not applicable to program execution.
- State footprint: none.
- Value influence: final `count`, the loop post-state, and the entry
  postcondition.
- Value justification: the base equation yields zero. The constructor equation
  adds the fixed-semantics membership result
  `strContains(iCons(C, .IntSeq), strToCodes("2357BD"))` and recurses on the
  strict structural tail `CS`.
- Justification: exhaustive, non-overlapping, structurally descending
  equations that directly define the requested count.
- Dependents: `SPEC.hex-loop` and `SPEC.hex-key`.
- Control validation: none required; the equations replace no execution.
- Value validation: `spec-value-mutation.k` rejects the opposite ground result
  `"2" -> 0`; its residual contains the actual result `1`.

### `SPEC.hex-loop` and its trusted reuse

- Extension: the auxiliary reachability claim `SPEC.hex-loop`; the second
  positive command reuses it with `--trusted SPEC.hex-loop`.
- Class: the independently checked claim is a derived lemma. Its trusted reuse
  is an operational acceleration whose bridge-free connection theorem is the
  first positive `kprove` command.
- Semantic role: fixed semantics executes the loop while proving the lemma.
  The already-proved reachability result then accelerates the same loop in the
  entry proof.
- Domain: arbitrary finite remaining codes `CS`, original codes `NUMCS`,
  accumulator `ACC`, initial `digit`, and module map `GLOBALS`, with exact
  environment 1, exact three-entry local frame, empty heap, scope location 2,
  call frame `frame(.K, 0, 1)`, `noRet`, `NoExc`, exit code 0, exact loop body,
  and exact return/end-call continuation.
- Matched context: there is no continuation wildcard. The loop body and the
  one-element return `Stmts` continuation are syntactically exact. `GLOBALS`
  is abstract but preserved, and the independent theorem is universally
  quantified over the same map.
- Justification scope: exactly the complete claim configuration above.
- Context containment: equality of the trusted claim's match domain and its
  independently proved domain.
- State footprint: reads and writes local `count`; writes local `digit`;
  preserves local `num`, module globals, environment, heap, allocation
  counters, call stack, return state, exception state, and exit code; consumes
  only the loop and leaves the exact return/end-call continuation.
- Value influence: fixes the final accumulator used by the returned result.
- Value justification: the program's fixed membership and integer-addition
  rules produce the same head contribution used by the `hexCount` constructor
  equation.
- Justification: the bridge-free command proving only `SPEC.hex-loop` printed
  `#Top` and exited 0 before any trusted reuse.
- Dependents: `SPEC.hex-key`.
- Control validation: `spec-loop-body-mutation.k` removes `D` from the
  displaced loop literal. The original lemma no longer matches, fixed
  execution returns 0 for `"D"`, and the expected-result claim is rejected.
  This also demonstrates body sensitivity.
- Value validation: `spec-body-mutation.k` starts the accumulator at 1 and is
  rejected with residual `hexCount(CS) +Int 1`; the universal off-by-one
  postcondition is independently rejected by `spec-vacuity.k`.

There are no proof-local simplification rules, opaque result symbols, priority
rules, external primitives, or unconstrained program-derived oracles.

## Exact commands and actual results

The complete reproducible command sequence is executable as:

```bash
./prove.sh
```

Its final run exited 0. The important individual commands and outputs were:

```bash
kompile --version
kprove --version
```

Output for both: K `v7.1.293`.

```bash
python3 py2mpy.py solution.py > solution.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
krun concrete_tests.mpy --definition runtime-kompiled
```

Actual result: both translation commands and LLVM compilation exited 0.
`krun` exited 0 with `.K`, `NoExc`, and `<exit-code> 0 </exit-code>` after all
six assertions. LLVM compilation emitted supplied-semantics warnings about
unrelated non-exhaustive helper matches; none of the warned helpers is used by
this program.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.hex-loop
```

Actual result: compilation exited 0; the claim command printed `#Top` and
exited 0.

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.hex-key,SPEC.hex-loop \
  --trusted SPEC.hex-loop
```

Actual result: `#Top`, exit 0. Including both labels keeps the independently
proved loop claim available while marking it trusted for the entry proof.

```bash
python3 test_solution.py
```

Actual output and exit: `checked=69905 mismatches=0`, exit 0. The independent
oracle uses a set-membership loop and exhaustively checks every uppercase
hexadecimal string of lengths 0 through 4.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.hex-key-off-by-one,SPEC.hex-loop \
  --trusted SPEC.hex-loop
```

Actual result: exit 1 with `WarnStuckClaimState`; the residual rejects
`hexCount(CS) +Int 1 ==Int hexCount(CS)`.

```bash
kprove spec-value-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-VALUE-MUTATION \
  --claims SPEC-VALUE-MUTATION.two-is-zero,SPEC.hex-loop \
  --trusted SPEC.hex-loop
```

Actual result: exit 1 with `WarnStuckClaimState`; the residual result is `1`,
not the mutated ground expectation `0`.

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --claims SPEC-BODY-MUTATION.starts-at-one,SPEC.hex-loop \
  --trusted SPEC.hex-loop
```

Actual result: exit 1 with `WarnStuckClaimState`; the residual is
`hexCount(CS) +Int 1`.

```bash
kprove spec-loop-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-LOOP-BODY-MUTATION \
  --claims SPEC-LOOP-BODY-MUTATION.d-is-still-counted,SPEC.hex-loop \
  --trusted SPEC.hex-loop
```

Actual result: exit 1 with `WarnStuckClaimState`; after removing `D` from the
loop literal, fixed execution on `"D"` returns `0`.

During construction, bounded proof inspection exposed that the real
continuation contained `Return(...) .Stmts`, not a bare `Return(...)` `Stmt`.
The invariant was narrowed to the real continuation and both positive proofs
were rerun successfully. Those diagnostic runs are not positive target-proof
commands.

## Gate results

### Gate A — PASS

- A1: the entry claim pins the exact closure binding and body. Both the initial
  accumulator mutation and displaced loop-literal mutation are rejected.
- A2: the loop claim describes every cell it changes and preserves all other
  modeled state. Its bridge-free proof uses fixed semantics.
- A3: lookup, argument passing, loop-target binding, evaluation order, exact
  continuation, return, and call-frame pop all execute under the fixed
  semantics. Trusted reuse has exactly the independently proved context.
- A4: `hexCount` has disjoint exhaustive cases and structurally descends.
- A5: the empty string is a realizable witness and concretely returns 0. The
  false off-by-one postcondition and wrong ground interpretation are rejected.

### Gate B — PASS

- The formal domain contains the prompt's entire valid-input domain.
- On uppercase ASCII hexadecimal strings, the supplied string-code,
  membership, iteration, Boolean-to-integer addition, and arbitrary-precision
  integer model agree with the relevant Python behavior.
- The summary-to-English bridge is direct: the singleton character is tested
  against exactly `"2357BD"`, the six prime-valued hexadecimal digits named in
  the prompt, and the recurrence sums those tests.
- All prompt examples pass under both CPython and the concrete K execution
  artifact. No implementation/specification discrepancy was found.
- Termination and behavior outside finite string values remain outside this
  partial-correctness theorem, as required by the Kit proof model.

### Gate C — PASS

All evidence artifacts exist, their exact commands are in `prove.sh`, and the
final script run exited 0. Negative probes are explicitly treated as expected
nonzero results, not positive proof commands.

## Trust boundary

- The supplied, unmodified `reference-semantics/` is the execution-model trust
  boundary. It affects value, control, state, and exception behavior of both
  claims. Evidence consists of successful compilation, concrete execution of
  all prompt examples, and the fact that the proof uses only its ordinary
  string, integer, call, function, and control rules.
- The supplied, unmodified `py2mpy.py` is trusted for the Python-AST to
  constructor translation. `solution.mpy` is regenerated in `prove.sh`; its
  displayed constructors correspond directly to every statement in
  `solution.py`.
- K `v7.1.293`, its Haskell prover backend, and its SMT/proof implementation
  are foundational checker trust.
- The `--trusted SPEC.hex-loop` use is not an unproved local assumption: its
  exact claim is proved bridge-free by the immediately preceding positive
  command.

No finite test is used as a substitute for the universal loop connection
theorem or the universal entry proof.

## Empirical support and excluded behavior

- Concrete K: empty input and all five prompt examples, zero assertion
  failures.
- CPython differential: all 69,905 valid uppercase hexadecimal strings of
  lengths 0 through 4, zero mismatches against an independent oracle.
- Excluded from the formal result: termination, CPython implementation details
  not represented by the supplied subset semantics, non-string arguments, and
  mutable/concurrent/external state not present in this task.
