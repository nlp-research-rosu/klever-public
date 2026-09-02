VALIDATED

## What is proven

Under the supplied MPY semantics, calling the exact generated `unique` closure
on any finite symbolic `ValSeq` terminates with:

```k
list(sortVS(dedupFromVS(INPUT, .ValSeq)))
```

at the returned heap reference. The input list is preserved.
`dedupFromVS` is the first-seen fold that appends an element exactly when the
fixed MPY list-membership computation says it is absent. There is no length
bound, fixed unrolling, or element-type precondition.

This is a partial-correctness statement in the Kit sense. The human-facing
statement “sorted unique elements” is conditional on the supplied external
contract for the opaque symbolic primitive `sortVS`.

## Formal claims

- `MEMBER-SPEC.member-summary` proves, without the membership bridge, that
  fixed `#memberAcc(V, list(VS))` produces `memberVS(V, VS)` for every finite
  `VS` and every continuation.
- `LOOP-SPEC.unique-loop` proves, without the loop bridge, that the exact
  source `for` loop transforms any accumulator `ACC` to
  `dedupFromVS(VS, ACC)`. It also proves the final loop-target value
  `lastFromVS(VS, X)` and preserves an arbitrary continuation.
- `SPEC.unique-full-domain` proves the exact closure call over arbitrary
  finite `INPUT:ValSeq`. Lookup, argument binding, list allocation, `sorted`,
  return, frame pop, and final heap allocation execute in the fixed semantics.

The entry representation uses heap location 0 for the supplied list and fresh
locations 1 and 2 for the working and returned lists. This is an allocation
normal form, not a restriction on list length or values.

## Proof-extension inventory

### Definitional summaries

- `memberVS(Val, ValSeq)`: exact Boolean result of fixed `#memberAcc`.
  Its empty, equal-head, and unequal-head equations cover the domain; the two
  guarded cons equations are disjoint. The cons equations have
  `[simplification]` only to expose path-conditioned evaluation. It reads no K
  cells. It affects `appendUnique`, the loop branch summary, and all later
  claims. Its value is fixed by `MEMBER-SPEC.member-summary`.
- `appendUnique(ValSeq, Val)`: returns the accumulator if `memberVS` is true,
  otherwise uses the fixed `valSeqConcat` append operation. The guards are
  complementary and exhaustive. It is used by `dedupFromVS`.
- `dedupFromVS(ValSeq, ValSeq)`: structurally recursive first-seen
  deduplication. The empty and cons equations are disjoint, exhaustive, and
  descend on the first sequence. It characterizes the observable working and
  returned lists.
- `lastFromVS(ValSeq, Val)`: structurally recursive summary of Python’s final
  loop-target binding. It is exhaustive, descending, and affects only the
  local `x` binding that the loop bridge preserves for its continuation.

### Operational bridges

- Membership bridge:

  ```k
  <k> #memberAcc(V, list(VS)) => memberVS(V, VS) ... </k>
  ```

  It has priority 40. Its match domain and arbitrary continuation are identical
  to `MEMBER-SPEC.member-summary`, proved using `VERIFICATION-BASE`, which does
  not import the bridge. It reads or writes no state cell and introduces no
  control effect. Present and absent ground cases were checked both without
  and with the bridge.

- Loop bridge: matches the exact `#loop` body generated from `solution.py`,
  environment 1, the closed capture-free local scope containing `l`, `result`,
  and `x`, and heap location 1 containing the accumulator. It transforms only
  `x` and heap entry 1, frames all other scopes and heap entries, and preserves
  an arbitrary continuation and every omitted cell. It has priority 40.
  `LOOP-SPEC.unique-loop` proves the identical domain and state transition
  using `VERIFICATION-MEMBER`, which contains only the independently proved
  membership bridge. The bridge does not perform return, frame pop, allocation,
  exception handling, or `sorted`.

  `bridge-probes.k` places an observable `x = 99` continuation after the loop.
  Fixed and bridged definitions both prove the same final accumulator and
  continuation effect. Removing the source `append` statement prevents the
  bridge from matching and makes the original-result claim fail.

## Exact verification commands and results

The complete reproducible sequence is in `prove.sh`.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module MEMBER-SPEC
# actual output: #Top
# exit: 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION-MEMBER \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-member-kompiled
kprove spec.k \
  --definition verification-member-kompiled \
  --spec-module LOOP-SPEC
# actual output: #Top
# exit: 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
# actual output: #Top
# exit: 0
```

All four fixed-versus-bridged commands in `prove.sh` printed `#Top` and exited
0. `model-boundary.k` also printed `#Top` and exited 0.

Concrete execution used the required definition:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

The prompt example terminated with exit code 0 and returned
`[0, 2, 3, 5, 9, 123]`.

## Negative validation

The satisfiable witness `[2, 1, 2]` was used for both probes.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# actual exit: 1
```

The residual contains the actual returned heap
`2 |-> list(vCons(1, vCons(2, .ValSeq)))`, rejecting the deliberately false
`[2, 1]` postcondition.

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
# actual exit: 1
```

The mutated closure removes `result.append(x)`. The residual contains empty
working and returned lists, showing that the original loop bridge did not
match and that the expected original result was rejected. Full logs are
`vacuity.log` and `body-mutation.log`.

## Gate results

- Gate A — PASS. The exact closure body is bound at the entry point.
  Program-defined execution either runs in the fixed semantics or is covered
  by the staged, bridge-free loop connection theorem. Bridge contexts,
  bindings, continuations, state footprints, result values, equation coverage,
  body sensitivity, and non-vacuity were checked.
- Gate B — PASS, conditional on the recorded fixed-model boundaries. The
  theorem covers every finite `ValSeq` represented by MPY, with no element or
  size restriction. The summary equations definitionally express first-seen
  uniqueness, and the machine-checked membership and loop claims connect them
  to execution. Ascending ordering is conditional on the supplied `sortVS`
  contract.
- Gate C — PASS. Every proof-local extension, external trust assumption,
  positive command, finite test, bridge comparison, model witness, and negative
  mutation has an existing artifact and exact command.

## Trust ledger and model boundaries

- `sortVS(ValSeq)` in `reference-semantics/semantics/sort.k` is a supplied
  trusted primitive: opaque under symbolic proof and implemented by concrete
  insertion-sort rules for supported numeric and string lists. It affects the
  order and value sequence at the returned reference and is depended on by
  `SPEC.unique-full-domain`, but not by the membership or loop connection
  claims. The conclusion about ascending Python order is conditional on the
  contract that `sortVS` is Python’s ascending stable sort on its supported
  domain.
- The fixed symbolic MPY list-membership rules compare elements with structural
  `==K`; MPY-KRUN adds concrete-only `numOrKEq` rules so mixed
  `int`/`bool`/`float` membership matches CPython. `model-boundary.k` records the
  symbolic witness `[True, 1]` as two structural elements, while CPython and
  LLVM both return `[True]`. The unbounded theorem covers both represented
  values; its interpretation as CPython equality is conditional on this
  documented language-model boundary.
- MPY literals are ASCII-only and the concrete sort does not model all Python
  orderable object classes or every exceptional comparison. These are fixed
  reference-model boundaries, not theorem preconditions. The implementation
  itself uses ordinary Python membership and `sorted` and remains faithful to
  Python on inputs for which sorting returns normally.
- The K toolchain and the supplied read-only MPY semantics are the foundational
  trusted computing base.

## Empirical evidence

`concrete_tests.py` uses CPython’s independently implemented
`sorted(set(case))` as the oracle. Seven cases cover empty input, the prompt
example, repeated strings, the isolated `True`/`1` boundary, mixed numerics,
mixed int/float equality, negatives, and duplicates:

```text
CPYTHON_MISMATCHES=0 CASES=7
```

The matching translated cases in `concrete-tests.mpy` ran under MPY-KRUN with
`<exit-code> 0 </exit-code>`. These finite tests support the supplied sort and
concrete numeric-equality boundaries; they are not used as universal proofs.

## Excluded or conditional behavior

The formal result does not independently prove the implementation of
`sortVS`, Python Unicode behavior beyond the supplied text model, arbitrary
user-defined comparison methods, or Python exception behavior for mutually
unorderable elements. Those behaviors remain conditional on the trust ledger
above. No finite-size or bounded-list behavior is substituted for the required
unbounded target theorem.
