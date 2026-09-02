VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, `solution.py` is partially
correct for every arbitrary finite list whose elements are K `Int` values.
The primary `SPEC.sum-squares` claim starts with a heap-referenced Python list
at an arbitrary heap location in an arbitrary disjoint heap context. It loads
the exact translated function definition, resolves the resulting binding,
calls the function, executes every loop iteration, returns, and produces
`sumSquaresAcc(VS, 0, 0)`. The input heap and allocation counter are unchanged,
so the list is not mutated. The supporting `SPEC.sum-squares-bare` claim proves
the same result for MPY-CORE's read-only bare-list claim representation.

This is a reachability proof of partial correctness. It does not separately
claim a liveness theorem, although all concrete tests terminate.

## Formal claim

For `allInts(VS)`, define the accumulator fold:

```text
S([], i, a) = a
S(v :: rest, i, a) =
  S(rest, i + 1, a + v*v)       when i mod 3 = 0
  S(rest, i + 1, a + v*v*v)     when i mod 3 != 0 and i mod 4 = 0
  S(rest, i + 1, a + v)         otherwise
```

`SPEC.sum-squares` proves that the returned value is `S(VS, 0, 0)`. The
`SPEC.loop-invariant` circularity proves the more general statement
`S(VS, INDEX, ACC)` from every reachable loop head with `INDEX >= 0`, including
the exact remaining `Return(...) .Stmts ~> #endcall` continuation and the real
function-frame pop.

The empty-sequence case discharges the base case. Each nonempty case performs
one fixed-semantics iteration and reuses the circularity on the tail. The entry
claim loads and calls the exact function and instantiates the invariant with
index and accumulator both zero.

## Proof-extension inventory

### Exact program macros

- Extension: `sumSquaresLoopBody`, `sumSquaresFunctionBody`, and
  `sumSquaresDef`.
- Class: definitional summaries (compile-time syntactic abbreviations).
- Semantic role and context: they abbreviate the exact MPY constructor term;
  they do not rewrite a runtime computation or accept a continuation frame.
- Domain and justification scope: their only uses are the displayed function,
  loop, and definition terms. Macro-expanded `Module(sumSquaresDef)` is
  byte-identical KORE to the regenerated `solution.mpy`.
- Context containment and state footprint: compile-time only; no cells are
  read, written, preserved, or abstracted.
- Value influence and justification: they select the program body executed by
  all claims; exact KORE identity fixes that body.
- Dependents: the loop, primary entry, bare entry, and mutation claims.
- Control/value validation: the identity `cmp` succeeds, both backends execute
  the same ground programs, and changing `result = 0` to `result = 1` makes the
  empty-list theorem fail.

### `allInts`

- Class: definitional summary.
- Domain and matched context: every `ValSeq`, as a pure Boolean term.
- Equations: empty and cons constructors are disjoint and exhaustive; recursion
  strictly descends to the tail. `notBool isRefV(V)` is redundant for an `Int`
  but gives the backend the corresponding disjoint-constructor fact.
- State footprint: none.
- Value influence: preconditions only.
- Value justification: it is true exactly for finite sequences of MPY `Int`
  elements; this is the prompt's integer-list domain.
- Dependents and validation: all three positive claims. Constructor coverage,
  concrete examples, and the exhaustive differential sample validate its use.

### Guarded integer projection

- Extension: `definedProjectInt`, `projectIntTotal`, the `#Ceil`
  characterization, the guarded orientation pair, the Int collapse, and
  idempotence.
- Class: `definedProjectInt` is a definitional summary; the remaining equations
  are derived sort-refinement lemmas using the kit's guarded-total-projection
  pattern.
- Domain: the `#Ceil` characterization covers every `Val`; every value-bearing
  orientation or use is guarded by `isInt`, except the statically sorted Int
  collapse.
- Matched context and containment: pure projection/cast terms only, with no K
  continuation, binding, or cell frame. The guard is exactly the definedness
  domain of the built-in partial projection `{V}:>Int`.
- State footprint: none.
- Value influence: projected values feed arithmetic and the result summary.
- Value justification: on the guard, the partial subsort cast fixes the unique
  Int value; `projectIntTotal(I:Int) => I`. There is no evaluator that invents
  an Int off-domain, and the off-domain summary branch does not use it.
- Dependents: both dispatch twins, `sumSquaresAcc`, and all positive claims.
- Control validation: not applicable; no operational control is replaced.
- Value validation: fixed and proof-extended concrete configurations are
  identical for all six smoke cases, while the opposite ground interpretation
  `projectIntTotal(2) => 3` exits 1 with `WarnStuckClaimState`.

### Guarded `applyBin` dispatch twins

- Extension: the guarded `applyBin("*", V, W)` and
  `applyBin("+", I, V)` simplification rules.
- Class: derived lemmas, not K-cell operational bridges.
- Domain: respectively `isInt(V) andBool isInt(W)` and `isInt(V)`.
- Matched context and justification scope: exactly the pure `applyBin` terms.
  Under the guards, the projections yield Int operands and the right sides are
  precisely MPY-INT's existing `I1 *Int I2` and `I1 +Int I2` equations.
  For statically Int operands the overlaps agree after projection collapse.
- State footprint and control: none.
- Value influence: loop arithmetic and final results.
- Dependents: the loop theorem and both entry theorems.
- Value/control validation: fixed-versus-extended ground execution is
  byte-identical. Square, cube, unchanged, negative cube, and the index-12
  square-over-cube precedence case are exercised.

### `squareContribution`

- Class: definitional summary.
- Domain and context: all pairs of K Int values, as a pure function.
- Equations: the three guards are pairwise disjoint and exhaustive:
  modulo-3 zero; modulo-3 nonzero and modulo-4 zero; both nonzero.
- State footprint: none.
- Value influence: it defines the per-position contribution in the formal
  postcondition.
- Value justification: its equations are the prompt's square/cube/unchanged
  cases in the same precedence order as the program.
- Dependents and validation: `sumSquaresAcc` and every positive claim; all
  branches and the common-multiple precedence are covered concretely and in the
  19,608-case differential sample.

### `sumSquaresAcc`

- Class: definitional summary.
- Domain and context: every `ValSeq`, index, and accumulator, as a pure
  function.
- Equations: empty versus cons are disjoint; the cons guards `isInt(V)` and
  `notBool isInt(V)` are complementary. The recursive Int case strictly
  descends to the tail. The off-domain result `0` totalizes the helper and is
  unreachable under `allInts`.
- State footprint: none.
- Value influence: this is the formal postcondition.
- Value justification: its Int-domain recurrence is exactly the running loop
  accumulator transformation.
- Dependents and validation: all positive claims and both result-mutation
  probes; the loop theorem machine-checks the universal connection between
  fixed execution and this summary.

### `SPEC.loop-invariant`

- Class: derived auxiliary reachability theorem.
- Domain: arbitrary all-Int remaining `ValSeq`, arbitrary nonnegative index,
  arbitrary Int accumulator, and the exact reachable unannotated function
  frame.
- Matched context: exact `#loop`, loop target/body, remaining
  `Return(...) .Stmts ~> #endcall`, environment 1, scope location 2, top-level
  call frame, return/exception/exit cells, and arbitrary preserved heap and
  heap-location cells. The final lexical-scope map is intentionally
  existential because lexical scopes are not an observable HumanEval result.
- Justification scope and containment: identical to the matched claim; there
  are no wild continuation or stack frames.
- State footprint: fixed execution reads/writes the four local bindings,
  iterates the list snapshot, returns, removes the callee frame, restores the
  caller environment/scope location/stack, and preserves heap, heap location,
  exception, and exit status.
- Value influence: it produces `sumSquaresAcc(VS, INDEX, ACC)`.
- Value justification: independently proved with `#Top` before being supplied
  as an auxiliary theorem to the entry claims.
- Dependents: `SPEC.sum-squares` and `SPEC.sum-squares-bare`.
- Control/value validation: exact concrete fixed execution, exact body identity,
  rejected body mutation, rejected false result, and the independently checked
  invariant proof.

There are no call, loop, return, frame-pop, exception, heap, or continuation
operational bridges.

## Exact commands and actual results

The complete reproducible sequence is executable as:

```bash
./prove.sh > prove-full.out 2>&1
```

It exited 0. `prove.sh` contains the exact commands and preserves outputs in
`kprove-loop.out`, `kprove-target.out`, `vacuity.out`,
`body-mutation.out`, `projection-mutation.out`, and both concrete `krun`
outputs; the outer redirection preserves the complete transcript in
`prove-full.out`.

The positive proof commands and observed results were:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
# Output: #Top
# Exit: 0

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --trusted SPEC.loop-invariant
# Output: #Top
# Exit: 0
```

The second command uses the exact claim proved by the first command. With this
K version, a regular claim is not available as a cross-claim lemma during the
same proof invocation, so the explicit `--trusted` handoff is required.

Other observed results:

```text
python3 differential_test.py
cases=19608 mismatches=0 smoke_body_matches_solution=yes
Exit: 0

cmp solution-term.kore verification-term.kore
Exit: 0
translated program and verification term are identical

krun concrete-smoke.mpy --definition runtime-kompiled
Exit: 0; final <k> .K, <exc> NoExc, <exit-code> 0

krun concrete-smoke.mpy --definition verification-kompiled
Exit: 0; final configuration byte-identical to the fixed-semantics run

kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
Exit: 1 (expected); WarnStuckClaimState; actual empty-list result 0, claimed 1

kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
Exit: 1 (expected); WarnStuckClaimState; mutated empty-list result 1, claimed 0

kprove spec-projection-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-PROJECTION-VACUITY
Exit: 1 (expected); WarnStuckClaimState; actual projection 2, claimed 3
```

The LLVM definition was compiled from the required
`reference-semantics/semantics.k` with `--main-module MPY-KRUN` and
`--syntax-module MPY-SYNTAX`. The Haskell proof definition imports `MPY`
through `verification.k` and does not import `MPY-CONCRETE`.

## Gate results

- Gate A — PASS. The exact translated body executes under fixed semantics;
  expanded program identity is machine-compared; there are no control or state
  bridges; all proof equations have exhaustive/disjoint guards or consistent
  overlaps; the empty input is a satisfiable witness; the wrong-result,
  wrong-projection, and changed-body probes are all rejected.
- Gate B — PASS. `VS:ValSeq` is symbolic and unbounded in length, and
  `allInts(VS)` is exactly the prompt's integer-element restriction. The
  heap-referenced theorem admits an arbitrary disjoint heap context and
  preserves it, covers unbounded mathematical integers, and formalizes the
  requested branch precedence and sum. No finite-size bound is part of the
  theorem.
- Gate C — PASS. Every proof-local extension and the auxiliary-theorem handoff
  are inventoried; commands, artifacts, outputs, scopes, and trust assumptions
  are recorded; concrete, differential, identity, and negative evidence is
  reproducible and is not presented as a replacement for the symbolic proof.

## Trust boundary

- The supplied read-only MPY reference semantics, the fixed `py2mpy.py`
  translator, K v7.1.293, its Haskell/LLVM backends, and the backend's
  integer/Boolean reasoning are foundational benchmark assumptions.
- The target command's `--trusted SPEC.loop-invariant` is not an unproved
  semantic assumption: the exact claim, against the same unchanged compiled
  definition, is independently proved by the immediately preceding command.
- The guarded projection relies on K's subsort predicate and partial-cast
  definedness. It has no off-domain evaluator and is only result-bearing under
  `isInt`; its ground opposite interpretation is rejected.
- Finite tests support implementation/semantics alignment only. Universal
  correctness comes from the two symbolic `#Top` results.

## Empirically supported facts

- All three prompt examples pass in CPython and under the fixed LLVM semantics.
- Three additional K smoke cases cover every branch, a negative cube, and index
  12 where both divisibility tests hold and squaring must take precedence.
- `differential_test.py` compares the implementation with an independently
  written oracle over every list of length 0 through 5 with values from -3
  through 3: 19,608 cases, zero mismatches.
- The fixed MPY-KRUN and proof-extended concrete final configurations are
  byte-identical for the six K smoke cases.

## Excluded behavior

- Non-integer list elements are outside the prompt's stated input contract and
  outside the positive claims.
- The claims do not specify behavior for malformed calls or exceptional
  off-contract inputs.
- Final lexical/module scope maps are existential because they are not part of
  the HumanEval observable result. Return value, input heap preservation,
  allocation state, control stack, return state, exception state, and exit code
  are constrained.
- Termination is not a separate theorem; the result is explicitly a partial
  correctness proof.
