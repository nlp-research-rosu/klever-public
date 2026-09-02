VALIDATED

## What is proven

Under the supplied MPY semantics, `get_positive` is partially correct for every
arbitrary finite list whose elements are MPY `Int` or `Float` values. It returns
a fresh list containing exactly the input elements whose MPY comparison with
`0.0` is true, in their original order and with duplicates preserved.

This is an unbounded symbolic theorem over `VS:ValSeq`; it is not a collection
of fixed-length claims. The exact translated function definition, lookup,
argument binding, allocation, loop, `append`, return, frame pop, heap result,
exception cell, and exit code all execute in the target claim.

This is a partial-correctness result. Termination is not a conclusion of the K
reachability claims.

## Formal claim and scope

The required entry claim is `SPEC.get-positive` in `spec.k`:

```k
<k>
  FuncDef("get_positive", Params("l"), EXACT-BODY)
  ~> Call(Name("get_positive"), list(VS:ValSeq))
  => ref(0)
</k>
<heap> .Map => 0 |-> list(filterPositive(.ValSeq, VS)) </heap>
requires numericVals(VS)
```

The other cells state that the call starts in the module environment with the
supplied builtins, restores the caller environment and empty stack, leaves
`NoExc`, and leaves exit code `0`.

Validation scope:

- Program boundary: the exact `FuncDef` and real call through MPY, including
  every operation defined in `solution.mpy`.
- Input domain: all finite `ValSeq` values satisfying `numericVals`, i.e. every
  element is an MPY `Int` or `Float`. Length is symbolic and unbounded.
- Observable final state: returned reference, referenced list contents, heap
  allocation counter, caller environment, stack, return state, exception, and
  exit code.
- Intended property: stable filtering by strict positivity, preserving values,
  order, and multiplicity.

`SPEC.filter-loop` is the circular loop invariant. Starting with accumulator
contents `ACC` and remaining input `VS`, it ends with accumulator contents
`filterPositive(ACC, VS)`. Its frame pins the exact three local bindings
`l`, `positive`, and `x`, and the exact loop body.

## Proof-extension inventory

### `numericVal` and `numericVals`

- Class: definitional summaries.
- Semantic role: describe the input domain; they replace no execution.
- Domain: all `Val` and `ValSeq` terms.
- Matched context and justification scope: pure function terms only; no
  continuation, stack, binding, or cell context.
- Equations: `numericVal(V)` is `isInt(V) orBool isFloat(V)`;
  `numericVals` is the usual empty/cons recursion.
- State footprint: none.
- Value influence: the entry precondition, loop invariant precondition,
  `positiveNumeric` default guard, and dynamic dispatch guard.
- Value justification: built-in sort predicates and exhaustive, disjoint
  empty/cons equations.
- Dependents: every target and connection claim.
- Validation: recursive descent is strict; constructor cases cover all
  `ValSeq`; concrete Int/Float cases occur in `smoke.py` and the differential
  corpus.

### `positiveNumeric`

- Class: definitional summary.
- Semantic role: names the Boolean positivity atom; it replaces no program
  operation by itself.
- Domain: all `Val` values.
- Matched context and justification scope: pure function terms only.
- Equations: Int maps to `gtF(intToF(I), 0.0)`, Float maps to
  `gtF(F, 0.0)`, and nonnumeric values map to `false`.
- Coverage and overlap: Int and Float are disjoint; the third guard is their
  exact negation, so the total equations are exhaustive and nonoverlapping.
- State footprint: none.
- Value influence: selects `append` versus skip and therefore affects the
  returned list.
- Value justification: on the formal numeric domain, the bridge-free
  `compare-*` and `applycmp-*` connection claims establish equality to fixed
  MPY execution. The underlying `intToF` and `gtF` meanings remain the supplied
  external float trust boundary.
- Dependents: `filterPositive`, the dispatch twin, both target claims, and the
  negative probes.
- Validation: all connection claims print `#Top`; LLVM/CPython differential
  evidence has zero mismatches.

### `filterPositive`

- Class: definitional summary.
- Semantic role: describes the final accumulator; it does not replace the
  loop or `append`.
- Domain: all accumulator and remaining `ValSeq` pairs.
- Matched context and justification scope: pure function terms only.
- Equations: empty input returns the accumulator; a positive head is appended
  with the fixed `valSeqConcat`; a nonpositive head is skipped.
- Coverage and overlap: empty and cons are disjoint; `positiveNumeric(V)` and
  its negation are exhaustive and disjoint. Every recursive equation consumes
  one cons cell.
- State footprint: none.
- Value influence: fixes the target heap contents.
- Value justification: its equations are the mathematical stable-filter
  definition and use the same connected positivity predicate as execution.
- Dependents: the loop invariant and entry claim.
- Validation: the loop circularity prints `#Top`; false-result and body
  mutations are rejected.

### Guarded `applyCmp` dispatch twin

Exact rule:

```k
rule applyCmp(">", V:Val, 0.0) => positiveNumeric(V)
  requires numericVal(V)
  [simplification]
```

- Class: operational bridge, classified conservatively because it accelerates
  a fixed semantic function during symbolic execution.
- Domain: exactly `applyCmp(">", V, 0.0)` with `V` an Int or Float.
- Matched context: a pure function occurrence in any congruent term. It reads
  no cells, changes no continuation, introduces no control effect, and has no
  binding assumptions.
- Justification scope: the union of universal Int and Float connection claims
  in `spec-connection.k`, compiled with main module `VERIFICATION-BASE`.
  That module does not import this twin.
- Context containment: the connection claims establish the pure `applyCmp`
  equation for both static sorts; pure equality is congruent in every matched
  context. End-to-end `Compare` claims also cover evaluation and an arbitrary
  continuation.
- State footprint: none read, written, preserved, or abstracted.
- Value influence: controls the branch and final list.
- Value justification: bridge-free Int and Float `applyCmp` and `Compare`
  claims collectively cover the complete `numericVal` guard.
- Dependents: loop invariant and entry claim.
- Control validation: end-to-end connection claims preserve arbitrary trailing
  computation and every framed configuration cell.
- Value validation: the false-result probe rejects the opposite result for a
  satisfiable `positiveNumeric(I)` witness; LLVM evidence includes positive,
  zero, and negative Int/Float values.

### `SPEC.filter-loop`

- Class: derived reachability lemma used coinductively as the loop circularity.
- Domain: arbitrary numeric `VS`, arbitrary accumulator `ACC`, and the exact
  reachable plain function frame and heap binding.
- Matched context: exact `#loop`, target, body, local scope shape, and
  accumulator heap object; arbitrary trailing continuation and framed
  unrelated cells are preserved.
- Justification scope and context containment: the claim itself quantifies over
  the arbitrary continuation and framed cells. `kprove` checks its empty and
  cons cases under fixed loop, binding, comparison, method-call, and heap
  rules.
- State footprint: reads `x` and `positive`; updates `x` and the list at `H`;
  preserves `l`, the positive reference, environment, unrelated heap entries,
  allocation counter, stack, return state, exception, exit code, and
  continuation.
- Value influence: fixes the accumulator and final returned list.
- Dependents: `SPEC.get-positive`.
- Validation: focused proof prints `#Top`; removing `append` makes the
  corresponding result claim fail.

No rule intercepts `FuncDef`, `Call`, `For`, `#loop`, `append`, `Return`, or
frame popping.

## Exact commands and actual outputs

`prove.sh` is the complete reproducible command record. The final audit run was:

```sh
./prove.sh > proof-run.log 2>&1
```

Actual exit: `0`.

The script ran these material commands:

```sh
python3 py2mpy.py solution.py > solution.mpy
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled
python3 differential_test.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove spec-connection.k --definition connection-kompiled \
  --spec-module SPEC-CONNECTION

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.filter-loop
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Actual positive outputs in `proof-run.log`:

- LLVM `krun`: final `<k> .K </k>`, `<exc> NoExc </exc>`, and
  `<exit-code> 0 </exit-code>`.
- Differential harness:
  `cases=60 cpython_mismatches=0 mpy_llvm_mismatches=0`.
- Bridge-free connection proof: `#Top`, exit `0`.
- Focused unbounded loop proof: `#Top`, exit `0`.
- Complete target proof: `#Top`, exit `0`.

The expected-failure commands in `prove.sh` actually exited `1`:

- `SPEC-VACUITY.false-result`: `WarnStuckClaimState`; residual heap contains
  `list(vCons(I, .ValSeq))` while the mutation demands `list(.ValSeq)`.
- `SPEC-BODY-MUTATION.removed-append`: `WarnStuckClaimState`; residual heap
  contains `list(.ValSeq)` while the claim demands the singleton.

The supplied semantics emits compiler warnings unrelated to this proof
(unused variables and some LLVM non-exhaustive-function warnings). No positive
proof command failed.

## Gate results

### Gate A — PASS

- A1: the real definition and every program-defined operation execute. The
  removed-append mutation is rejected.
- A2: the only execution-accelerating rule is a pure comparison equation with
  no state footprint and bridge-free universal Int/Float connection proofs.
  The loop invariant explicitly tracks all changed state.
- A3: the entry claim executes definition lookup, call evaluation, argument
  binding, the exact plain local frame, method binding, return, and frame pop.
  Connection claims use arbitrary continuations.
- A4: all proof-local equations have disjoint/exhaustive guards and terminating
  recursion. The dispatch twin is restricted to its proved domain.
- A5: empty and positive-singleton preconditions are realizable. The false
  result and body mutations both fail with discriminating residual heaps.

### Gate B — PASS

The source contract's material domain is arbitrary finite lists of numbers.
The formal domain covers arbitrary, mixed, unbounded finite sequences of both
numeric value sorts supplied by MPY, Int and Float. The theorem is not bounded
by length or examples. Comparing to `0.0` is equivalent to strict positivity
for these Python numeric values.

The summary-to-human-property bridge is conditional on the supplied
`intToF`/`gtF` contracts and is empirically supported by LLVM/CPython
differential evidence. That condition is explicit rather than hidden.

### Gate C — PASS

Every proof-local extension, named trust boundary, positive command, negative
probe, and finite differential is recorded with an existing artifact, exact
command, scope, oracle, and actual result.

## Trust boundary

- The read-only supplied MPY semantics is fixed and trusted as the Python
  execution model for this task.
- `intToF` and `gtF` are supplied opaque Haskell proof primitives with concrete
  LLVM rules. They influence the positivity branch and therefore the final
  result. Both target claims depend on them through `positiveNumeric`.
- K's built-in Int, Float, Bool, Map, and solver theories and the K toolchain
  are trusted.
- No program-defined function is trusted or summarized without execution.

The formal fact is closure under this supplied theory. The interpretation that
opaque float atoms implement Python numeric comparison is conditional on the
named supplied primitive contracts.

## Empirically supported facts

- `smoke.py` executes both prompt examples plus a mixed Int/Float boundary case
  through MPY/LLVM with exit code `0`.
- `differential_test.py` uses an independent CPython list-comprehension oracle.
  Its 60 cases include empty/singleton lists, zero and negative zero, positive
  and negative Int/Float values, both prompt examples, large magnitudes, and
  50 deterministic seeded mixed lists. Actual result: zero CPython or MPY/LLVM
  mismatches.
- These finite tests support the float primitive interpretation and language
  adequacy; they do not replace the universal K claims.

## Excluded behavior

- Lists containing nonnumeric MPY values are outside the natural-language
  contract and the formal precondition; their possible comparison exceptions
  are not claimed.
- Python behaviors not represented by the supplied MPY subset are not claimed.
- Total termination and resource bounds are not proved; the K result is
  partial correctness.
