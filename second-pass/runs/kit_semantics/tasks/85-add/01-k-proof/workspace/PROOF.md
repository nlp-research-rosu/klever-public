VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, the exact `add` body in
`solution.mpy` is partially correct for every non-empty finite list whose
elements are semantic integers.  If the call terminates, it returns the sum of
exactly those even-valued elements whose zero-based indices are odd.

The theorem is symbolic in the complete `ValSeq`; it is not a finite-size
unrolling.  The entry claim also executes definition loading, name lookup,
argument binding, the complete function body, return, and frame cleanup.

## Formal claims

- `SPEC.add-loop` is a circularity over an arbitrary finite suffix `VS`.
  Starting with accumulator `ACC` and next-index parity `ODD`, it executes the
  exact source loop and leaves `ACC +Int addSummary(VS, ODD)`.
- `SPEC.add-entry` starts from the complete initial MPY configuration, loads
  the exact translated `add` definition, calls it on symbolic `list(VS)`, and
  finishes with `$result |-> addSummary(VS, false)`.
- The entry precondition is
  `allInts(VS) andBool VS =/=K .ValSeq`.  This is exactly an arbitrary
  non-empty finite list of K integers.
- `addSummary` starts with parity `false` at index zero, flips parity at every
  constructor, and adds a value only when parity is `true` and Python-style
  remainder modulo two is zero.  Thus its recursive equations directly state
  the HumanEval property.

The observable final configuration constrains `.K`, the returned module result,
the restored environment and allocation counters, the empty heap and call
stack, `noRet`, `NoExc`, and exit code zero.  The retained function closure is
not an observable required by the prompt and is existentially framed.

## Proof-extension inventory

This inventory was rebuilt from the final `verification.k` and `spec.k`.

### `allInts`

- **Class / role:** Definitional summary used only as an input-domain
  predicate; it does not replace execution.
- **Domain:** All finite `ValSeq` terms.  The empty/constructor equations are
  exhaustive and disjoint.
- **Matched context:** Only the pure term `allInts(VS)`; no continuation,
  bindings, control stack, or configuration cells are matched.
- **Justification scope / containment:** Structural recursion on `ValSeq`.
  Every accepted non-empty sequence has `isInt` true at every element.
- **State footprint:** None.
- **Value influence / justification:** It guards both formal claims and enables
  the guarded integer equations.  Its value is fixed by exhaustive recursive
  equations.
- **Dependents:** `SPEC.add-loop` and `SPEC.add-entry`.
- **Control/value validation:** No control effect.  The concrete witness
  `[4,2,6,7]` satisfies it; non-integer constructors are excluded by the same
  recursive equation.

### `definedProjectInt`, `projectIntTotal`, and cast-orientation rules

- **Class / role:** Definitional summary plus derived sort-projection lemmas;
  no source or MPY operational K item is skipped.
- **Domain:** `definedProjectInt` covers all `Val`.  Projection orientation is
  guarded by exactly `isInt(V)`; collapse covers statically sorted `Int`.
- **Matched context:** A partial Val-to-Int cast or `projectIntTotal(V)` in any
  pure term context.  There is no K continuation, control frame, binding, or
  cell match.
- **Justification scope / containment:** The `#Ceil` characterization,
  guarded orientations, collapse, and idempotence are the Kit's guarded-total
  projection idiom.  No rule produces an Int unless the built-in sort predicate
  already establishes that the source value is an Int.
- **State footprint:** None.
- **Value influence:** The projected integer feeds `%`, `+`, `addSummary`, and
  therefore the final result.
- **Value justification:** On the complete claim domain, `allInts` entails
  `isInt` for every current head, and the guarded cast is the same semantic
  value.  Outside that guard the total symbol has no evaluator and remains
  opaque; no claim uses such a value.
- **Dependents:** Both guarded dispatch lemmas, `addSummary`, and both claims.
- **Control/value validation:** No control effect.  Ground MPY execution,
  the rejected body mutation, and the rejected false result all remain
  value-sensitive; there is no independently selectable oracle value.

### Guarded `%` dispatch twin

- **Class / role:** Derived lemma for dynamic-to-static sort refinement.
- **Domain:** `applyBin("%", V:Val, I:Int)` under exactly `isInt(V)`.
- **Matched context:** The pure `applyBin` term in any simplification context;
  no cells, continuation, stack, binding, or exception state are omitted.
- **Justification scope / containment:** MPY-INT already defines
  `applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)`.  The twin has precisely
  that static domain through the guarded projection.  On overlap with the
  fixed rule, `projectIntTotal(I1)` collapses to `I1`, so both right-hand sides
  agree.
- **State footprint:** None.
- **Value influence:** It decides the even-value branch.
- **Value justification:** The fixed MPY-INT equation plus guarded projection.
- **Dependents:** `SPEC.add-loop` and therefore `SPEC.add-entry`.
- **Control/value validation:** The reference-only LLVM run takes the same
  branches for positive, zero, and negative even/odd witnesses.  The mutation
  probes reject wrong observable results.

### Guarded `+` dispatch twin

- **Class / role:** Derived lemma for dynamic-to-static sort refinement.
- **Domain:** `applyBin("+", I:Int, V:Val)` under exactly `isInt(V)`.
- **Matched context:** The pure `applyBin` term in any simplification context;
  no operational cell or continuation is matched.
- **Justification scope / containment:** MPY-INT already defines
  `applyBin("+", I1:Int, I2:Int) => I1 +Int I2`.  The guard and projection
  recover exactly that domain.  The overlap with the fixed rule has the same
  right-hand side.
- **State footprint:** None.
- **Value influence:** It updates the accumulator and final result.
- **Value justification:** The fixed MPY-INT equation plus guarded projection.
- **Dependents:** `SPEC.add-loop` and `SPEC.add-entry`.
- **Control/value validation:** No control effect.  The body mutant that adds
  `1` instead of the selected value reaches `1`, not `2`, and is rejected.

### `addSummary`

- **Class / role:** Definitional mathematical summary; it appears only in
  claims and does not rewrite source syntax or MPY operational K items.
- **Domain:** All finite `ValSeq` and both Boolean parity constructors.  The
  base, false-parity, and true-parity equations are exhaustive, disjoint, and
  structurally descending.
- **Matched context:** Only `addSummary(VS, ODD)`; no operational context or
  state is matched.
- **Justification scope / containment:** Structural definition over the exact
  sequence used by the claims.  Human-facing meaning is asserted only under
  `allInts(VS)`.
- **State footprint:** None.
- **Value influence / justification:** It is the postcondition.  Its value is
  fixed recursively: skip even indices, and at odd indices add the head iff
  `pyMod(head,2) == 0`.
- **Dependents:** Both claims.
- **Control/value validation:** The false postcondition `3` for `[4,2,6,7]`
  is rejected while the executed result is `2`; 20,612 independent
  differential cases have zero mismatches.

### `SPEC.add-loop`

- **Class / role:** Derived auxiliary reachability claim used coinductively as
  the loop invariant; it summarizes fixed execution without adding an
  operational rewrite.
- **Domain:** Every finite `VS` satisfying `allInts(VS)`, arbitrary accumulator
  and Boolean next-index parity, and the exact local function frame.
- **Matched context:** The exact `#loop`, target, body, current environment and
  local bindings.  The active continuation and unrelated configuration cells
  are framed because this loop contains no `return`, `break`, exception,
  allocation, or other abrupt/control-state effect.
- **Justification scope / containment:** `kprove` checks the empty base branch
  and every constructor step.  A step binds the real head, executes both source
  conditionals and the parity assignment, and reapplies the circularity to the
  structural tail.  The framed context is preserved by every fixed MPY rule
  used in that execution.
- **State footprint:** Reads `lst`, `odd`, and `value`; writes `result`, `odd`,
  and `value`; preserves the environment, list binding, parent, continuation,
  heap, stack, return/exception state, and all other framed cells.
- **Value influence / justification:** It determines the accumulator result
  via the structurally defined `addSummary`.
- **Dependents:** `SPEC.add-entry`.
- **Control/value validation:** Focused proof is `#Top`; whole proof is `#Top`;
  both negative probes are rejected with concrete wrong final values.

There are no operational bridges and no trusted result-bearing primitives in
the proof-local theory.

## Exact commands and actual outputs

All reproducible commands are in `prove.sh`.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 test_solution.py
```

Actual differential output, exit 0:

```text
checked=20612 mismatches=0
```

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Both commands exited 0.  `krun` ended at `.K`, with `NoExc`, exit code `0`,
and these module bindings:

```text
"example" |-> 2
"singleton" |-> 0
"mixed_sign" |-> 2
```

LLVM compilation emitted only supplied-semantics exhaustiveness/unused-variable
warnings; it emitted no error.

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.add-loop
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual result for each `kprove` command:

```text
#Top
```

Each exited 0.  The only compiler messages were pre-existing unused-variable
warnings in `reference-semantics/semantics/str.k`.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`; the residual contains
`"$result" |-> 2` while the mutated destination requires `3`.

```bash
kprove spec-body-mutant.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTANT
```

Actual result: exit 1 with `WarnStuckClaimState`; the mutated body reaches
`"$result" |-> 1` while the real expected result is `2`.

## Gate results

- **Gate A — PASS.** The exact program-defined body executes under fixed MPY.
  There is no operational bridge.  State/control effects are preserved, the
  equations are exhaustive or exactly guarded, overlaps agree, the precondition
  has concrete witnesses, and both body-sensitivity and false-postcondition
  mutations are rejected.
- **Gate B — PASS.** `allInts(VS) and VS != .ValSeq` covers every non-empty
  finite integer list represented by MPY, with no length or value bound.
  `addSummary(VS,false)` is exactly the prompt's odd-index/even-value sum, and
  the implementation matches it.
- **Gate C — PASS.** Commands, artifacts, actual results, proof-local
  extensions, assumptions, negative probes, and finite differential evidence
  are all recorded and reproducible.

## Trust boundary

- The supplied, unmodified `reference-semantics/` definition and the installed
  K parser/compiler/Haskell prover/LLVM runtime are trusted.
- The AST translator `py2mpy.py` is supplied and unmodified; its generated
  `solution.mpy` was reproduced from `solution.py`.
- K reachability establishes partial correctness.  Termination is not a
  theorem claimed here, although concrete runs terminate and the source loop
  traverses a finite list.
- No external primitive, opaque program result, or unproved operational bridge
  affects the theorem.

## Empirically supported facts

- `test_solution.py` uses an independently written `enumerate`-based oracle.
  It checks five named boundary/example lists, every list of lengths 1 through
  5 over `[-3,3]`, and 1,000 deterministic random lists of lengths 1 through
  40 over `[-1000,1000]`: 20,612 cases, zero mismatches.
- `smoke.mpy` executes three representative calls on the untouched LLVM
  semantics, including singleton and negative-value cases.
- These finite tests support translation and implementation adequacy; the
  universal result comes from the symbolic K claims, not from testing.

## Excluded behavior

- Empty lists and lists containing non-integer values are outside the prompt's
  stated contract and outside `SPEC.add-entry`.
- Behavior beyond the supplied MPY model is not claimed.
