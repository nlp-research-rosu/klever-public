VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every K integer `N > 0`, if the exact
translated call `get_odd_collatz(N)` terminates, it returns a reference to a
list of the odd values in its Collatz trace, including the terminal `1`, sorted
by the supplied `sortVS` primitive.

This is a partial-correctness result. It does not prove the Collatz conjecture
or termination for every positive integer. The implementation records its
finite execution trace in an internal local list so that the theorem can
validate a terminating trace structurally without assuming that every possible
trace is finite.

## Formal claim

`SPEC.get-odd-collatz` starts with the exact translated `FuncDef`, an empty
module scope, the supplied builtins scope, an empty heap, and symbolic
`N >Int 0`. It executes definition, name lookup, argument binding, the actual
body, list allocation and mutation, in-place sort, return, and frame cleanup.

At the destination there is an existential finite sequence `?TF` such that:

- `validCollatzTrace(?TF)` is true;
- `traceFirstInt(?TF) ==Int N`;
- `traceLastInt(?TF) ==Int 1`; and
- the returned heap object is
  `list(sortVS(valSeqConcat(oddWithoutLast(?TF), vCons(1, .ValSeq))))`.

`SPEC.collatz-loop` is the circularity. At a loop head, the actual `trace` heap
object is a nonempty valid trace from local `start` through current `n`, and
the actual `odds` heap object equals `oddWithoutLast(trace)`. One real loop
iteration preserves those facts. At exit, positivity and the false `n > 1`
guard imply `n == 1`.

The observable final state in the entry theorem includes the return reference,
both allocated heap lists (returned odds and internal trace), `heapLoc`,
module binding, environment, call stack, return state, exception state, and
exit code. Resource usage and termination are not asserted.

## Proof-extension inventory

There are no proof-local operational bridges. No rule intercepts a program
call, loop, method, return, frame operation, or heap update. All
program-defined code executes under the fixed semantics.

### `collatzNext`

- **Extension/class:** two guarded equations for
  `collatzNext(Int)`; definitional summary.
- **Semantic role:** names one mathematical Collatz transition; it does not
  replace the source execution.
- **Domain:** all `Int`; guards are `pyMod(N, 2) ==Int 0` and
  `pyMod(N, 2) ==Int 1`.
- **Matched context / justification scope:** only an exact
  `collatzNext(N)` function term. Python remainder modulo positive `2` is
  exactly `0` or `1`; the cases are disjoint and exhaustive.
- **Context containment:** no continuation, binding, control stack, or cell is
  matched.
- **State footprint:** none.
- **Value influence / justification:** fixes adjacency in
  `validCollatzTrace`; equations are exactly the two arithmetic assignments in
  `solution.mpy`.
- **Dependents / validation:** both claims. The body-mutation probe and the
  concrete traces exercise distinct even and odd transitions.

### Finite-trace observers

- **Extensions/class:** equations for `validCollatzTrace`,
  `traceFirstInt`, `traceLastInt`, `oddWithoutLast`, and `maybeOdd`;
  definitional summaries.
- **Semantic role:** structurally inspect finite `ValSeq` values; they do not
  replace execution.
- **Domain:** every `ValSeq` (and every `Int` for `maybeOdd`). Constructor
  cases plus guarded parity cases and `[owise]` cases are exhaustive.
- **Matched context / justification scope:** exact top-level function terms
  only. Each recursive call consumes the tail of a finite sequence.
- **Context containment:** no framed K context or operational cell is matched.
- **State footprint:** none.
- **Value influence / justification:** determines trace validity and the
  unsorted odd-value sequence in both postconditions. The definitions directly
  encode adjacency, endpoints, and filtering of every position except the
  final one.
- **Dependents / validation:** both claims. LLVM traces for inputs
  `1, 2, 3, 5, 6, 7` exhibit endpoints and both parity branches; the
  207-input differential test independently checks returned values.

### `valSeqConcat` derived laws

- **Extensions/class:** right identity, associativity, and the two
  nonempty-result K-equality simplifications; derived lemmas.
- **Semantic role:** normalize sequence expressions only.
- **Domain:** all `ValSeq`; the nonempty laws require a constructor
  `vCons(_, _)` as the right operand.
- **Matched context / justification scope:** the displayed `valSeqConcat` or
  equality term, with no operational configuration.
- **Context containment / state footprint:** exact term only; no state.
- **Value influence / justification:** sequence shape in the heap
  postcondition. Right identity and associativity follow by structural
  induction on the first sequence from the two fixed `valSeqConcat` equations.
  Concatenating a sequence with a nonempty sequence is nonempty by the same
  induction.
- **Dependents / validation:** the loop and entry claims; the false-result
  probe confirms these laws do not erase a differing element.

### Append-observer derived laws

- **Extensions/class:** four `[simplification]` rules for
  `traceFirstInt`, `traceLastInt`, `validCollatzTrace`, and
  `oddWithoutLast` over
  `valSeqConcat(T, vCons(J, .ValSeq))`; derived lemmas.
- **Semantic role:** summarize the result of the fixed semantics' already
  executed list append; they do not perform or replace the append.
- **Domain:** `traceFirstInt` requires nonempty `T`;
  `traceLastInt` accepts every `T` and integer `J`;
  `validCollatzTrace` requires nonempty `T`; `oddWithoutLast` requires
  `validCollatzTrace(T)`.
- **Matched context / justification scope:** exact observer terms over the
  one-element append shape. No arbitrary continuation or heap is matched.
- **Context containment / state footprint:** pure terms only; no cells are
  read or written.
- **Value influence / justification:** re-establishes the invariant after the
  concrete heap mutation. Each law follows by structural induction on `T`.
  For the odd-filter law, a valid trace is nonempty and contains only integers,
  so excluding newly appended `J` means adding the former last element iff it
  is odd.
- **Dependents / validation:** `SPEC.collatz-loop`, then the entry claim. Both
  the even and odd branches close in the focused loop proof.

### `SPEC.collatz-loop`

- **Extension/class:** auxiliary reachability claim used as a circularity;
  derived lemma.
- **Semantic role:** proves the exact `#while` computation from a valid
  loop-head state to a valid terminal finite trace.
- **Domain:** `N > 0`, exact plain local frame with `n`, `odds`, `start`, and
  `trace`, two distinct heap entries, a valid nonempty trace ending at `N`,
  and an odds accumulator equal to `oddWithoutLast(T)`.
- **Matched context:** exact loop condition and body, exact active local scope
  and heap; the continuation and unrelated outer scopes/configuration cells
  are framed by the claim itself.
- **Justification scope / containment:** `kprove` checks that same framed claim
  under fixed semantics. The arbitrary continuation is preserved; the claim
  introduces no abrupt return, exception, or frame operation.
- **State footprint:** reads and writes local `n`; reads `start`; mutates the
  odds and trace heap entries; preserves their references and all framed cells.
- **Value influence / justification:** supplies the existential terminal trace
  and odd sequence used by the target result. Base and step/circularity
  obligations printed `#Top`.
- **Dependents / validation:** `SPEC.get-odd-collatz`. Replacing the odd append
  with `append(2)` is rejected by `spec-body-mutation.k`.

## Exact commands and actual outputs

The complete reproducible command is:

```bash
./prove.sh
```

It exited `0`. Its component commands are recorded verbatim in `prove.sh` and
had these results:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-smoke.py > concrete-smoke.mpy
```

Both exited `0`. The current `solution.mpy` contains the same function body
embedded in the entry claim.

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-smoke.mpy --definition runtime-kompiled
```

Both exited `0`. `krun` ended with `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>` after all six assertions.

```bash
python3 test_differential.py
```

Actual output and exit:

```text
checked=207 mismatches=0
Exit: 0
```

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.collatz-loop
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

The compile exited `0`. Each `kprove` command printed:

```text
#Top
Exit: 0
```

The compilers also emitted non-fatal warnings from the supplied semantics about
unused variables and concrete-only non-exhaustive helper cases.

The A5 postcondition mutation:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

exited `1` with `WarnStuckClaimState`. For satisfiable input `n = 1`, its
residual contained the real heap
`0 |-> list(vCons(1, .ValSeq))`, contradicting the deliberately mutated
`[2]` result.

The A1 body-sensitivity mutation:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

exited `1` with `WarnStuckClaimState`. For input `n = 3`, its residual contained
the mutated result `vCons(1, vCons(2, vCons(2, .ValSeq)))`, which does not
match the original `[1, 3, 5]` postcondition.

## Gate results

### Gate A — PASS

- **A1:** The exact `FuncDef`, binding, call, body, loop, appends, sort method,
  and return execute under fixed semantics. The body mutation is rejected.
- **A2:** There are no operational bridges. The entry claim observes return,
  scopes, allocation, both heap values, stack, return state, exception state,
  and exit code.
- **A3:** Definition and ordinary lookup select the target closure; ordinary
  call machinery evaluates the argument and creates the frame. The loop claim
  preserves its arbitrary continuation and introduces no abrupt control.
- **A4:** All proof-local equations are exhaustive on their declared sorts or
  explicitly guarded, parity guards are disjoint, recursive definitions
  descend structurally, and derived sequence laws are valid over their complete
  guards. The earlier unsafe future-recursive Collatz summary was removed
  during the Gate A repair; the final proof uses only a finite actual trace.
- **A5:** `n = 1` realizes the precondition. The false `[2]` postcondition is
  rejected, and the body mutation changes the residual result.

### Gate B — PASS

- The formal domain `N > 0` is exactly the prompt's positive-integer domain.
- The finite trace begins at `N`, ends at `1`, and every adjacent pair is an
  exact Collatz step.
- The result contains exactly the odd trace elements, including terminal `1`,
  and is ordered by the supplied ascending-sort contract.
- K integers are unbounded like Python integers. The theorem is intentionally
  partial correctness; termination would require resolving the Collatz
  conjecture and is not silently assumed.
- The internal `start` and `trace` locals change only unobservable local memory,
  not the function signature or returned list.

### Gate C — PASS

- Every proof-local function, lemma, and auxiliary claim is inventoried above.
- Every named command, test input scope, oracle, output, and exit status is
  reproducible from existing artifacts.
- Formal facts, trusted semantics, finite empirical evidence, and excluded
  behavior are separated below.

## Trust boundary

1. **Supplied `sortVS` primitive and in-place sort rule.** In the Haskell proof,
   `sortVS` is an opaque total symbol fixed by
   `reference-semantics/semantics/sort.k`. The fixed method rule formally
   updates only the referenced heap sequence and returns `noneV`; the
   human-facing fact that `sortVS` is an ascending permutation of an integer
   sequence is trusted. It affects the order and contents of the returned list,
   and `SPEC.get-odd-collatz` depends on it. The LLVM definition uses the
   supplied concrete insertion sort, and the smoke/differential evidence below
   supports the contract on tested inputs.
2. **Supplied Python semantics and translator.** The theorem is about the
   constructor program generated by the supplied `py2mpy.py` and the supplied
   `MPY` rules. Adequacy of those fixed artifacts to CPython is part of the
   task's trust base. `solution.mpy`, concrete execution, exact body embedding,
   and the body-sensitivity probe make this boundary auditable.
3. **K toolchain/backend correctness.** `kompile`, LLVM `krun`, Haskell
   `kprove`, and their SMT reasoning are in the ordinary verification TCB.

There are no trusted proof-local program summaries, result-bearing oracles, or
execution-bypassing rewrites.

## Empirically supported facts

- `concrete-smoke.py` independently states exact expected lists for
  `1, 2, 3, 5, 6, 7`. Its translated LLVM execution completed all assertions
  with `NoExc`.
- `test_differential.py` uses a separate direct Collatz iterator and Python's
  `sorted`, not the K proof equations. It compared inputs `1..200` plus
  `255, 256, 257, 511, 512, 513, 1024`: 207 checks and zero mismatches.
- `spec-vacuity.k` and `spec-body-mutation.k` are negative validation probes;
  both produced the expected nonzero result and concrete distinguishing
  residual.

These finite tests support the translator/semantics/sort adequacy boundary.
They are not used as universal proofs.

## Excluded behavior

- Termination for all positive integers is not proved.
- Inputs that are not positive K integers are outside the claim.
- Resource exhaustion, finite-memory effects of retaining the internal trace,
  recursion/iteration limits outside the supplied model, and implementation
  timing are excluded.
- The K proof does not internally prove the ascending-permutation theorem for
  opaque `sortVS`; the result's human-facing ordering is conditional on the
  supplied primitive's stated contract.
