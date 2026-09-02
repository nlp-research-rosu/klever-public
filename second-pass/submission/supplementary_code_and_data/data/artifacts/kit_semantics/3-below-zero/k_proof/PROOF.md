VALIDATED

## What is proven

Under the supplied MPY semantics, the exact translated `below_zero` module is
partially correct for every finite `List[int]`: after loading the module and
calling `below_zero`, the result is `true` exactly when some nonempty prefix has
negative sum, and is `false` otherwise. The theorem is symbolic in the list
length and every integer value; it is not a bounded unrolling.

The target also observes the complete MPY state. The call returns to environment
0 with an empty stack, `noRet`, `NoExc`, unchanged heap and allocation counters,
and only the installed module-level closure remaining in the scopes map.

## Formal claim

`SPEC.below-zero` starts with the initial MPY configuration, executes the exact
`Module` term in `solution.mpy`, and invokes the exact installed closure on
`list(INPUT:ValSeq)`. Its precondition is `allInts(INPUT)`. Its result is:

```k
belowFrom(0, INPUT)
```

`belowFrom(B, VS)` is structurally defined as follows:

- the empty sequence returns `false`;
- for integer head `V`, it returns `true` if `B + V < 0`;
- otherwise it recurses on the tail with balance `B + V`.

Thus its definition is the prompt's prefix-balance property. The loop proof is
`CONNECTION-SPEC.loop-connection`, a circularity over an arbitrary symbolic
`ValSeq`. The exact call connection is split into three bridge-free reachability
claims and composed by reachability transitivity:

1. `call-prefix-connection` executes lookup, argument evaluation, frame setup,
   parameter binding, and local initialization to the evaluated `For` node.
2. `for-to-loop-connection` executes MPY's fixed `For`-to-`#loop` step.
3. `loop-connection` executes the loop, early return, and frame pop to
   `belowFrom`.

All three claims import `VERIFICATION-BASE`, which contains no call bridge.

## Proof-extension inventory

| Extension | Class | Domain and truth obligation | Semantic role and dependents | Validation |
|---|---|---|---|---|
| `allInts` | Definitional summary | Total on raw `.ValSeq`/`vCons`; recursive descent is structural | Names the declared `List[int]` domain; affects all connection and target preconditions | Equations are exhaustive and non-overlapping |
| `definedProjectInt`, `projectIntTotal`, cast orientation/collapse/idempotence rules | Definitional summary and derived sort lemmas | Projection is used only under `isInt`; orientation connects it to K's built-in `Val :> Int` cast | Refines a dynamic `Val` head to the static `Int` required by MPY integer arithmetic; affects balance, branch, and result | Kit guarded-projection pattern; collapse agrees on concrete integers; connection proof covers all typed heads |
| `belowFrom` | Definitional summary | Total on `Int × ValSeq`; empty, integer-head, and non-integer-head cases are exhaustive and disjoint | Does not replace execution; names the recursively defined result. Used by the loop connection, call bridge, and target postcondition | Valid typed case is connected universally to fixed execution; invalid-head totalization is outside target preconditions |
| guarded `applyBin("+", I, V)` rule | Derived lemma | `requires isInt(V)`; overlaps MPY's existing `Int + Int` equation only where `projectIntTotal(V)` is that same integer | Restates fixed integer addition over the dynamic supersort; no state or control effect | Universal loop connection proves its use through every symbolic iteration |
| fresh-map deletion rule | Derived lemma | `((L |-> S) STORE)[L <- undef] = STORE` when `L` is absent from `STORE` | Normalizes MPY's real frame-pop map update; reads no program value and skips no pop | Standard finite-map identity; required after fixed `#pop` in the bridge-free loop proof |
| `call-prefix-connection`, `for-to-loop-connection`, `loop-connection` | Derived reachability theorems | Exact source call/frame context; arbitrary finite integer input; module and builtin scopes are framed where the loop does not inspect them | Execute the program under fixed MPY and establish the complete connection used below | `kprove connection-spec.k ...` prints `#Top`, exit 0, using the bridge-free definition |
| exact `Call(Name("below_zero"), list(INPUT))` rule in `verification.k` | Operational bridge | Exact closure body and binding, env 0, scopeLoc 1, empty heap/stack, `noRet`, `NoExc`, exit 0, no continuation, and `allInts(INPUT)` | Replaces the already-proved whole call transition with `belowFrom(0, INPUT)`; used only by `SPEC.below-zero` | Complete connection is the composition of the three bridge-free claims; continuation and body mutations behave sensitively as recorded below |

For the operational bridge, the matched context is a complete configuration,
not a framed `<k>` suffix. It accepts no continuation and no alternative
binding. Its skipped state footprint is frame allocation, local bindings,
balance updates, loop control, return state, frame deletion, and restoration of
the caller; the connection claims establish every one of those transitions.
The heap, heap counter, exception, exit-code, and caller scopes are preserved.
The bridge's value affects the returned Boolean, and that value is fixed by the
bridge-free loop theorem, not by an opaque symbol.

## Exact commands and actual outputs

The complete recorded runner is `./prove.sh`. Its final run exited 0; the full
output is in `prove-run.out`.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Actual result: all six K assertions completed; `krun` exited 0 with `.K`,
`NoExc`, and exit code 0 (`krun-smoke.out`).

```bash
kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove connection-spec.k \
  --definition verification-base-kompiled \
  --spec-module CONNECTION-SPEC
```

Actual result: `#Top`, exit 0. This proves all three bridge-free connection
claims (`kprove-connection.out`).

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Actual result: `#Top`, exit 0 (`kprove-target.out`).

```bash
kprove context-spec.k \
  --definition verification-kompiled --spec-module CONTEXT-SPEC
python3 differential_test.py
```

Actual results: context claim `#Top`, exit 0; differential test
`DIFFERENTIAL_CASES=139257 MISMATCHES=0`, exit 0.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled --spec-module SPEC-VACUITY
kprove spec-body-mutation.k \
  --definition verification-kompiled --spec-module SPEC-BODY-MUTATION
```

Actual expected failures:

- `spec-vacuity.k` exited 1 with a stuck final `false` against deliberately
  expected `true` for `[]` (`kprove-vacuity.out`).
- `spec-body-mutation.k` exited 1 with a stuck final `true` against expected
  `false` after changing `balance += operation` to subtraction on `[1]`
  (`kprove-body-mutation.out`). The exact-body bridge did not match.

## Gate results

### Gate A — PASS

- Program identity: `spec.k` loads the exact module/closure body generated in
  `solution.mpy`. The changed-body probe bypasses the exact bridge and is
  rejected with the fixed semantics' changed result.
- State/control fidelity: the bridge-free connection claims cover lookup,
  evaluation, binding, loop execution, early return, pop, and all MPY cells.
- Context containment: the bridge accepts only an empty continuation. With
  `#notB` appended, `context-spec.k` proves through fixed execution and reaches
  `true`, showing the bridge does not discard the continuation.
- Equation validity: total definitions have exhaustive, disjoint cases;
  recursive definitions descend structurally; overlapping projection/addition
  rules agree with the fixed Int equations.
- Non-vacuity: the empty list satisfies `allInts`; the false-result mutation is
  rejected with an explicit final `false` residual.

### Gate B — PASS

- The domain is every finite MPY sequence whose elements are K `Int` values,
  matching the prompt's `List[int]`; no length or magnitude bound is imposed.
- K `Int` and Python integers are unbounded. The input is read-only, so MPY's
  documented bare-list claim representation is observationally equivalent to
  the heap-backed concrete list exercised by `krun`.
- The recursive summary is exactly the stated “some running balance is below
  zero” property, and the implementation returns early on precisely that case.
- Both prompt examples, empty input, zero, immediate deficit, and a later
  deficit execute correctly.

### Gate C — PASS

- Every proof-local rule and its dependents are inventoried above.
- Every claimed test has an artifact, exact command, scope, oracle, and actual
  result. Negative probes retain their nonzero outputs.
- Formal results, trusted foundations, finite evidence, and exclusions are
  separated below.

## Trust boundary

The proof trusts the supplied read-only MPY semantics as the model of the
supported Python subset, K's reachability logic (including transitivity), K's
generated sort predicates/casts and collection hooks, the Haskell backend/SMT
solver, and the LLVM backend for concrete evidence. There are no opaque or
unproved proof-local primitives. The exact operational bridge is not trusted:
its full value, control, binding, and state transition is established by the
bridge-free connection claims.

## Empirically supported facts

- `smoke.py` runs six fixed-semantics K assertions: empty, both prompt examples,
  zero, immediate negative, and a later negative prefix.
- `differential_test.py` compares `solution.py` with an independently written
  prefix-sum oracle on all lists of lengths 0–6 over `[-3, 3]` plus 2,000
  deterministic random lists of lengths 0–40 over `[-100, 100]`: 139,257 cases,
  zero mismatches.

These tests are validation evidence, not substitutes for the universal K
claims.

## Excluded behavior

- Values outside the declared `List[int]` element type are outside the target
  precondition. The non-integer `belowFrom` equation only totalizes a helper and
  is not used to claim behavior for such inputs.
- Infinite lists are not representable by the finite `ValSeq` input datatype.
- The K theorem is partial correctness. Termination is not a reachability-claim
  conclusion, although the concrete implementation consumes one element of a
  finite list per iteration.
- Python behavior outside the supplied MPY subset is outside this benchmark's
  fixed semantic model.
