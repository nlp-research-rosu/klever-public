VALIDATED

# What is proven

Under the supplied `MPY` semantics, for arbitrary input sequences
`A:ValSeq` and `B:ValSeq`, loading the exact translated `common` definition
and calling it with `list(A)` and `list(B)` reaches:

- return value `ref(1)`;
- heap location `0` containing
  `list(commonAcc(A, B, .ValSeq))`; and
- heap location `1` containing
  `list(sortVS(commonAcc(A, B, .ValSeq)))`.

`commonAcc` visits `A` in encounter order. It appends an element exactly when
the fixed list-membership result says that the element occurs in `B` and does
not yet occur in the accumulator. Thus it defines the duplicate-free
intersection. The final ordering statement is conditional on the supplied
`sortVS` contract: for supported mutually orderable values, `sortVS` is their
ascending sort.

This is a K reachability proof of partial correctness. It does not prove
termination.

# Formal claims

`spec.k` contains three positive claims, all proved together:

1. `member-fold` connects fixed execution of
   `#memberAcc(V, list(S))` to `commonMember(V, S)`.
2. `common-loop` is the loop circularity. From an unprocessed suffix `A` and
   accumulator `ACC`, it preserves the exact continuation, bindings, stack,
   exception state, and allocation state, changes only the loop target and the
   result-list heap object, and leaves that object as
   `commonAcc(A, B, ACC)`.
3. `common-program` loads the exact function body, invokes it through normal
   lookup/call/frame rules, executes the loop, calls the supplied `sorted`
   builtin, and constrains the returned reference and both allocated lists.

The entry claim has no `requires` clause: its execution characterization ranges
over all `ValSeq` inputs in the supplied model. The human-facing sortedness
interpretation is conditional on `sortVS`'s named contract.

# Proof-extension inventory

## `commonMember`

- Class: definitional summary.
- Semantic role: names the mathematical result of fixed list membership; it
  does not rewrite a program term.
- Domain: every `Val` and every finite `ValSeq`.
- Equations: the empty and cons constructors are disjoint and exhaustive; the
  recursive call is on the strict tail.
- Matched context and state footprint: none; equations operate only on values.
- Value influence: controls both intersection filtering and duplicate
  suppression through `commonAcc`.
- Value justification: the universal `member-fold` reachability claim executes
  the supplied `#memberAcc/#iterNext/#memberCont` rules and produces exactly
  `commonMember`.
- Dependents: `member-fold`, `common-loop`, and `common-program`.
- Validation: the positive proof is `#Top`; the false-summary mutation and
  concrete/differential tests distinguish true from false membership outcomes.

## Guarded Boolean simplification rule

- Exact rule: when `notBool (E ==K V)` holds,
  `(E ==K V) orBool B` simplifies to `B`.
- Class: derived lemma.
- Semantic role: solver normalization only; it replaces no execution.
- Domain: arbitrary `E:Val`, `V:Val`, and `B:Bool` under the displayed guard.
- Context and state footprint: no configuration context and no state cells.
- Justification: under the guard, the left disjunct is false, so the equation
  is the Boolean identity `false or B = B`. Its overlap with the built-in
  concrete Boolean simplification has the same right-hand side.
- Dependents: `member-fold` and therefore the two larger claims.
- Validation: the bridge-free `member-fold` claim closes universally.

## `commonAcc`

- Class: definitional summary.
- Semantic role: names the mathematical result of the remaining loop; it does
  not intercept `For`, `#loop`, `Call`, or heap mutation.
- Domain: every triple of finite `ValSeq` values.
- Equations: empty and cons cases are disjoint and exhaustive. The cons case
  makes an explicit total Boolean choice and recurses on the strict tail.
- Context and state footprint: none in its equations.
- Value influence: fixes heap location `0`, the argument to `sortVS`, heap
  location `1`, and consequently the returned list's contents.
- Value justification: `common-loop` executes the exact loop body with fixed
  name lookup, short-circuiting membership checks, method binding, `append`
  heap mutation, and loop control, reaching exactly `commonAcc`.
- Dependents: `common-loop` and `common-program`.
- Validation: `spec-value-mutation.k` assigns the opposite empty result to the
  realizable input `[1], [1]`; `kprove` rejects it and exposes the actual
  `[1]` heaps.

## `member-fold`

- Class: derived auxiliary reachability theorem/circularity.
- Semantic role: summarizes fixed membership execution for reuse; it is a
  `claim`, not an operational `rule`.
- Complete match: `#memberAcc(V, list(S))` at the head of an arbitrary
  continuation, with all other configuration cells preserved and arbitrary.
- Justification scope and containment: the claim itself is universal over that
  exact continuation frame and all other cells. Membership reads no cells and
  has no abrupt control effect.
- State footprint: none.
- Value influence: produces the Boolean used by the source condition and
  `commonAcc`.
- Justification: induction on `S` by the supplied iterator and membership
  rules plus the truthful `commonMember` equations.
- Dependents: `common-loop` and `common-program`.
- Validation: machine-checked as part of the positive `#Top` run.

## `common-loop`

- Class: derived loop-invariant reachability theorem/circularity.
- Semantic role: executes and inductively summarizes the source loop; it is not
  an operational rule.
- Complete match: environment `1`; local bindings for `l1`, `l2`, `result`,
  and `item`; result object at heap location `0`; heap location counter `1`;
  exact caller frame; exact
  `Return(Call(Name("sorted"), Name("result"))) .Stmts ~> #endcall`
  continuation; and unchanged return, exception, and exit-code cells.
- Justification scope and containment: its match and theorem scope are the same.
  The module-scope map is universally framed and preserved because the loop
  accesses only the pinned local bindings.
- State footprint: reads `l2` and the result list; writes the local `item`
  binding and heap location `0`; preserves `l1`, `l2`, globals, allocation
  counters, stack, return state, exception state, and exit code.
- Value influence: fixes the unsorted accumulator consumed by `sorted`.
- Justification: base case uses the empty iterator; the step executes target
  binding, both fixed membership folds, short-circuit control, optional
  `append`, and `#loopLbl`, then reapplies the circularity to the strict suffix.
- Dependents: `common-program`.
- Control validation: `spec-body-mutation.k` removes duplicate suppression.
  On `[1, 1], [1]`, fixed execution reaches `[1, 1]` and rejects the original
  theorem's `[1]` result.

## Syntax macros

`commonLoopBody()` and `commonBody()` are compile-time abbreviations for the
exact constructors in `solution.mpy`. They add no equation about values and no
runtime rewrite. Regenerating `solution.mpy` from `solution.py` and the
body-sensitivity mutation check provide the identity evidence.

## Supplied `sortVS`

- Class: trusted primitive supplied by `reference-semantics/semantics/sort.k`;
  it is not a proof-local extension.
- Semantic role: the fixed `sorted` builtin allocates a new list containing
  `sortVS(VS)`. Symbolic proofs keep it opaque; the LLVM leg uses insertion
  sort for integer and string lists.
- Domain used for the human-facing conclusion: homogeneous, mutually
  orderable integer or modeled string lists.
- State/control footprint: reads the result list, allocates a fresh sorted list,
  increments `heapLoc`, and returns its reference. These surrounding effects
  execute in fixed semantics.
- Value influence: fixes the order of every final result element.
- Named contract: `sortVS(VS)` is the ascending permutation of `VS` on its
  supported domain.
- Dependents: `common-program` and the human-facing “sorted” conclusion.
- Evidence: eight LLVM assertions cover prompt examples, duplicates, empty
  lists, negative integers, and strings; the independent CPython differential
  suite covers 3,200 ordered input pairs with zero mismatches.
- Limitation: no universal K theorem of the sorting algorithm is claimed.

# Commands and actual results

The complete reproducible command sequence is in `prove.sh`.

```bash
python3 py2mpy.py solution.py > solution.mpy
```

Actual result: exit 0; `solution.mpy` contains the translated `common`
definition.

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete-smoke.py > concrete-smoke.mpy
krun concrete-smoke.mpy --definition runtime-kompiled
```

Actual result: all commands exit 0. The final LLVM configuration has
`<k> .K </k>`, `<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`.
Compiler warnings from the read-only supplied semantics were non-fatal.

```bash
python3 validate.py
```

Actual output and exit:

```text
CPython differential: 3200 pairs, 0 mismatches
Exit: 0
```

The oracle is independently implemented as
`sorted(set(left).intersection(set(right)))`. The complete finite scope is all
pairs of lists of lengths 0 through 3 over `(-1, 0, 1)`, plus the corresponding
scope over `("a", "b", "c")`.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual output and exit:

```text
#Top
Exit: 0
```

The one positive `kprove` command proves every claim in `spec.k`.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`. The residual contains
`<k> ref(1) </k>` while the deliberate mutation demands `ref(0)`.

```bash
kprove spec-value-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-VALUE-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`. For `[1], [1]`, the residual
contains `[1]` in both accumulator and returned heaps while the mutation
demands empty lists.

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`. The mutated body reaches
`[1, 1]` in both heaps, invalidating the original duplicate-free result.

# Gate results

## Gate A — PASS

- A1: the target claim loads and calls the exact body; no rule intercepts the
  function, loop, membership, append, return, or call. The body mutation is
  rejected with the changed `[1, 1]` result.
- A2: there are no operational bridges. The loop claim explicitly accounts for
  its local-binding and heap writes and preserves all other modeled cells.
- A3: the entry and loop claims pin function binding, local bindings,
  evaluation/control continuation, call frame, heap locations, return state,
  exception state, and exit code. The membership theorem is universal over the
  same arbitrary continuation it matches and has no cell effects.
- A4: proof-local function equations are disjoint, exhaustive, and descending.
  The sole simplifier is a guarded Boolean identity.
- A5: `[1], [1]` is a realizable witness. Both the false returned-reference and
  false summary-value mutations are rejected with explicit residual values.

## Gate B — PASS

- B1: the formal execution claim takes two arbitrary model lists. The
  human-facing sorting conclusion is stated for inputs on which the supplied
  sort contract applies, matching Python's requirement that common values be
  mutually orderable.
- B2: the theorem is explicitly about the user-supplied, partial Python
  semantics. Its opaque `sortVS`, flat modeled equality, and omitted full
  CPython exception/type behavior are recorded rather than silently treated as
  proved.
- B3: `commonMember` is universally connected to fixed membership execution,
  and `commonAcc` directly encodes encounter-order filtering plus duplicate
  suppression. Ascending order is conditional on the named `sortVS` contract
  and supported by independent finite evidence.
- B4: prompt examples and duplicate, empty, negative-integer, and string cases
  agree with the implementation and oracle.

## Gate C — PASS

- C1: every proof-local extension and the supplied `sortVS` trust boundary is
  inventoried with its domain, context, footprint, value influence,
  justification, and dependents.
- C2: all cited artifacts exist; commands, scopes, oracles, outputs, and exit
  codes are recorded above and in executable `prove.sh`.
- C3: formal execution facts, the conditional sorting conclusion, finite
  empirical evidence, and excluded behavior are separated.

# Trust boundary

The proof trusts the supplied `MPY` semantics, the K toolchain, and
`py2mpy.py` as the source-to-constructor translator. At the value level it also
trusts the supplied `sortVS` contract for ascending sorting. The proof does not
derive ordering facts about `sortVS`; it proves that the exact program passes
the exact duplicate-free intersection sequence to that primitive and returns
the newly allocated result.

# Empirically supported facts

- Eight concrete assertions execute through the LLVM semantics with no
  exception and exit code 0.
- The independent CPython oracle agrees on all 3,200 tested integer/string list
  pairs.
- Three independent negative K probes expose the actual fixed-semantics result
  and reject wrong result, wrong summary value, and mutated-body behavior.

These finite observations support the implementation-to-intent and sorting
trust bridges; they are not presented as universal proofs.

# Excluded behavior

- Termination is outside this partial-correctness proof.
- Full CPython behavior absent from the supplied reference semantics—including
  arbitrary user objects, custom equality/order methods, heterogeneous
  incomparable values, alias-sensitive nested mutable structures, and all
  unmodeled exceptions—is outside the human-facing conclusion.
- The universal theorem proved by K is the exact `sortVS(commonAcc(...))`
  execution characterization. “Ascending sorted” remains conditional on the
  supplied `sortVS` contract.
