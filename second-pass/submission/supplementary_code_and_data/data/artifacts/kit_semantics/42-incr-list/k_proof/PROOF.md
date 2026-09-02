VALIDATED

## What is proven

Under the supplied `MPY` semantics, `incr_list` is partially correct for every
finite, arbitrarily long list whose elements are any heterogeneous mixture of
`Int`, `Bool`, and `Float` values:

- the actual translated function body is defined and called through normal
  lookup, argument binding, frame setup, loop execution, method dispatch,
  mutation, return, and frame teardown;
- the input is a heap-backed list at `ref(0)` and is unchanged;
- the return value is a distinct freshly allocated list at `ref(1)`;
- its elements, in their original order, are the fixed semantics' result of
  applying `+ 1` to each input element.

There is no length bound. The theorem is a partial-correctness reachability
theorem; it does not separately establish total correctness.

## Formal claim

`SPEC.incr-list` begins in the canonical module configuration with:

- heap object `0 |-> list(INPUT)`;
- `heapLoc = 1`;
- the exact `FuncDef` emitted in `solution.mpy`;
- a call `Call(Name("incr_list"), (ref(0), .Exprs))`;
- precondition `allNumeric(INPUT)`.

It reaches:

- return value `ref(1)`;
- unchanged input `0 |-> list(INPUT)`;
- result `1 |-> list(incrAcc(.ValSeq, INPUT))`;
- `heapLoc = 2`;
- restored module environment, empty stack, `noRet`, `NoExc`, and exit code
  zero.

`incrAcc` is the structurally recursive, order-preserving fold:

```text
incrAcc(ACC, .ValSeq) = ACC
incrAcc(ACC, vCons(V, R))
  = incrAcc(valSeqConcat(ACC,
      vCons(applyBin("+", V, 1), .ValSeq)), R)
```

Here `applyBin` is the supplied semantics' own operator dispatch, not a
proof-local oracle.

`SPEC.loop-inv` is the unbounded circularity. At a real `#loop` head, if the
result heap object contains `ACC` and the remaining input is `REM`, the loop
finishes with that same object containing `incrAcc(ACC, REM)`. It frames the
continuation and all unrelated scopes and heap entries while preserving
`heapLoc`, stack, return state, exception state, and exit code.

## Proof-extension inventory

The inventory below was reconstructed from `verification.k` and `spec.k` after
the successful proof.

### `isNumericVal`

- **Class:** Definitional summary (domain predicate).
- **Semantic role:** Reasons about the source operation's defined domain; it
  replaces no execution.
- **Domain:** Every `Val`. `Int`, `Bool`, and `Float` map to `true`; the
  `[owise]` case maps every remaining `Val` to `false`.
- **Matched context:** The pure term `isNumericVal(V)` only; no continuation,
  binding, or configuration cell is matched.
- **Justification scope:** The complete `Val` constructor space supplied by
  `MPY`.
- **Context containment:** Match and justification domains are identical.
- **State footprint:** None.
- **Value influence:** Contributes only to the input precondition through
  `allNumeric`.
- **Value justification:** The supplied rules for `applyBin("+", _, 1)` exist
  exactly for `Int`, `Bool`, and `Float`.
- **Justification:** Disjoint constructor cases plus exhaustive `[owise]`.
- **Dependents:** `allNumeric`, `SPEC.loop-inv`, and `SPEC.incr-list`.
- **Control validation:** Not applicable; it is non-operational.
- **Value validation:** Ground witnesses include integer, Boolean, and float
  elements in `smoke.py`; nonnumeric values are excluded.
- **Validation:** Exhaustive coverage and non-overlap were inspected; Gate A4
  passes.

### `allNumeric`

- **Class:** Definitional summary (recursive domain predicate).
- **Semantic role:** Describes the admissible list domain; it replaces no
  execution.
- **Domain:** Every `ValSeq`.
- **Matched context:** `allNumeric(.ValSeq)` or
  `allNumeric(vCons(V, R))`; no configuration context.
- **Justification scope:** The complete two-constructor `ValSeq` domain.
- **Context containment:** Exact.
- **State footprint:** None.
- **Value influence:** Guards both positive claims.
- **Value justification:** Empty is admissible; a cons is admissible exactly
  when its head is numeric and its tail is admissible.
- **Justification:** Disjoint base/cons equations with strict recursive descent
  on `R`.
- **Dependents:** `SPEC.loop-inv` and `SPEC.incr-list`.
- **Control validation:** Not applicable.
- **Value validation:** The realizable ground witness `[0]` satisfies it; the
  mixed numeric concrete case also exercises all three admitted value classes.
- **Validation:** Totality, descent, and constructor coverage pass Gate A4.

### `incrAcc`

- **Class:** Definitional summary.
- **Semantic role:** Names the exact contents produced by repeated real loop
  iterations; it does not rewrite `#loop`, calls, lookups, operators, or heap
  mutation.
- **Domain:** Every pair of `ValSeq` values `(ACC, REM)`.
- **Matched context:** A pure `incrAcc` term only.
- **Justification scope:** The complete base/cons decomposition of `REM`.
- **Context containment:** Exact.
- **State footprint:** None itself. The connected loop theorem separately
  proves the write to result heap object `H`.
- **Value influence:** Characterizes the final result list in both positive
  claims.
- **Value justification:** Each step appends the exact fixed-semantics term
  `applyBin("+", V, 1)`. No fresh or unconstrained value is introduced.
- **Justification:** Disjoint equations, structural descent on `REM`, and the
  bridge-free universal connection theorem `SPEC.loop-inv`.
- **Dependents:** `SPEC.loop-inv` and `SPEC.incr-list`.
- **Control validation:** The loop executes under fixed semantics. The `+2`
  body mutation is rejected and produces `[2]` rather than the required `[1]`.
- **Value validation:** The false `[2]` postcondition for the original body is
  rejected; concrete and CPython differential checks have zero mismatches.
- **Validation:** Gate A1, A4, and A5 pass.

### `SPEC.loop-inv`

- **Class:** Derived lemma, machine-checked as a reachability circularity.
- **Semantic role:** Universally connects real fixed-semantics loop execution
  to `incrAcc`. It is an execution theorem, not an ordinary rewrite rule.
- **Domain:** Every `REM`, `ACC`, numeric remaining sequence, environment
  location, result reference, parent, heap location, stack, framed
  continuation, framed scope entries, and framed heap entries matching the
  claim.
- **Matched context:** Exact `#loop(list(REM), Name("x"), BODY)` at the head of
  `<k>` with arbitrary trailing continuation; a scope containing bindings for
  `l`, `result`, and `x`; result heap object `H |-> list(ACC)`; and the
  explicitly preserved operational cells.
- **Justification scope:** The same universally quantified configuration in
  `SPEC.loop-inv`.
- **Context containment:** The continuation and framed scope/heap portions are
  quantified in the theorem itself, so use by `SPEC.incr-list` is contained in
  the proved domain.
- **State footprint:** Reads the remaining list and bindings; updates `x`;
  appends to heap object `H`; consumes the loop. It preserves `l`, the result
  reference, other scopes and heap entries, `heapLoc`, stack, return state,
  exception state, and exit code.
- **Value influence:** Determines every element of the final result heap
  object.
- **Value justification:** One fixed-semantics iteration produces
  `applyBin("+", V, 1)` and mutates `H`; the recursive circularity handles the
  tail.
- **Justification:** `kprove` proves base, inductive, and framed-context cases
  and reports `#Top`.
- **Dependents:** `SPEC.incr-list`.
- **Control validation:** Concrete execution reaches `NoExc`/exit code zero;
  the material `+2` mutation fails its connection claim.
- **Value validation:** Original-body false-postcondition probe fails with a
  residual containing result `[1]`; the mutation probe fails with result `[2]`.
- **Validation:** Gate A1-A5 pass.

There are no proof-local operational bridges, simplification axioms, priority
rules, casts, or trusted primitives.

## Exact commands and actual outputs

The complete reproducible runner is `prove.sh`.

```bash
./prove.sh
```

Actual result:

```text
exit 0
#Top
cases=585 mismatches=0
```

The required positive proof command inside the runner is:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual output and status:

```text
#Top
exit 0
```

This unfiltered command proves both `SPEC.loop-inv` and `SPEC.incr-list`; the
entry claim uses the loop circularity. A separate focused construction check
also ran:

```bash
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-inv
```

Actual output and status:

```text
#Top
exit 0
```

Concrete build and execution:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled > concrete.out
```

Actual status is exit 0; `concrete.out` ends with `NoExc` and
`<exit-code> 0 </exit-code>`. Compiler warnings originate in the supplied
read-only semantics.

Symbolic build:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Actual status is exit 0. The only warnings are unused variables in the supplied
`str.k` plus intentionally framed variables in `spec.k`.

False-postcondition probe:

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual status is exit 1 with `WarnStuckClaimState`; the residual contains:

```text
0 |-> list(vCons(0, .ValSeq))
1 |-> list(vCons(1, .ValSeq))
```

Changed-body probe:

```bash
kprove spec-body-mutant.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTANT
```

Actual status is exit 1 with `WarnStuckClaimState`; the residual contains:

```text
0 |-> list(vCons(0, .ValSeq))
1 |-> list(vCons(2, .ValSeq))
```

Differential evidence:

```bash
python3 differential.py
```

Actual output and status:

```text
cases=585 mismatches=0
exit 0
```

## Gate results

### Gate A — PASS

- **A1:** `SPEC.incr-list` contains the exact `solution.mpy` function body and
  executes its definition and call. The `+2` body mutation is rejected.
- **A2:** No execution is skipped. Input heap object `0` is preserved; fresh
  result object `1`, heap location, scopes, stack, return state, exception
  state, and exit code are all constrained.
- **A3:** Fixed rules perform name lookup, left-to-right argument evaluation,
  binding, attribute lookup, bound-method dispatch, append, loop control,
  return, and frame restoration. No binding-pinning bridge exists.
- **A4:** All proof-local function equations have disjoint/exhaustive
  constructor cases. Recursive functions descend structurally. No inconsistent
  simplification rule exists.
- **A5:** `[0]` is a realizable input. The original function produces `[1]`;
  the deliberately false `[2]` postcondition is rejected.

### Gate B — PASS

- **B1:** `INPUT` has arbitrary finite symbolic length. `allNumeric` admits
  every heterogeneous mixture of the modeled classes for which the supplied
  `x + 1` operation is defined: `Int`, `Bool`, and `Float`. There is no size,
  sign, magnitude, or homogeneity restriction.
- **B2:** The theorem covers every such value represented by the fixed model.
  User-defined numeric classes, complex numbers, and other Python values not
  represented by `MPY` are a recorded model boundary, not candidate-created
  narrowing. The supplied semantics does not model Python `TypeError` for
  unsupported additions; those inputs are outside the defined computation.
- **B3:** `incrAcc` preserves order and records exactly one fixed-semantics
  `+ 1` result per element. `SPEC.loop-inv` formally connects this summary to
  execution.
- **B4:** The implementation returns a fresh list and leaves the input list
  unchanged, matching the prompt.

### Gate C — PASS

- All proof-local extensions, their dependents, domains, contexts, and state
  footprints are recorded above.
- The supplied semantics, translator, proof backend, and opaque float helpers
  are listed in the trust ledger below.
- Concrete, differential, mutation, and vacuity artifacts and exact commands
  are present and rerun by `prove.sh`.
- Formal conclusions, conditional trust, finite evidence, and exclusions are
  separated explicitly.

## Trust boundary

| Component | Influence | Dependents | Basis |
|---|---|---|---|
| Supplied read-only `MPY` semantics | Value, control, state, exceptions modeled by the task | All claims | Task-provided reference semantics; LLVM smoke execution and mutation probes provide independent evidence, not a proof of the semantics |
| `py2mpy.py` | Program syntax and body identity | `solution.mpy`, copied entry term | Task-provided fixed translator; successful translation and inspection of the emitted constructor tree |
| Supplied `intToF` and `addF` | Float result values | Float elements in `incrAcc` | Intentionally opaque under Haskell proof and concrete under LLVM; the theorem threads their exact terms and is conditional on their supplied contract |
| K/Haskell backend and its solver | Reachability closure | Both positive claims | Standard trusted proof toolchain; `#Top`/exit 0 is the machine-check result |
| K/LLVM backend | Concrete evidence only | `smoke.py` evidence | Finite testing; not used as a universal proof |

No unproved program-derived value oracle is trusted.

## Empirically supported facts

- `smoke.py` executes the empty list, both prompt examples, and a mixed
  `Bool`/`Float`/`Int` case under the mandated LLVM semantics. It reaches
  `NoExc` and exit code zero.
- `differential.py` compares `solution.incr_list` against an independent
  CPython list-comprehension oracle on all lists of lengths zero through three
  over eight representative integer, Boolean, and float values: 585 cases,
  zero mismatches.
- These finite checks support implementation/model alignment and the concrete
  float boundary. They do not replace the universal K proof.

## Excluded behavior

- Lists containing modeled values for which `x + 1` is undefined, such as
  strings, lists, tuples, sets, `None`, closures, or builtins.
- Python value classes absent from the supplied model, including user-defined
  objects with custom addition and complex numbers.
- Python exception details for unsupported addition; the supplied semantics
  gets stuck rather than modeling `TypeError`.
- A separate total-correctness or resource-bound theorem.
- Unconditional real/IEEE value theorems for the supplied opaque float
  primitives; float results are structurally proved relative to those named
  primitives and concretely tested.
