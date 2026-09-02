VALIDATED

## What is proven

Under the supplied `MPY` semantics, `solution.mpy` loads
`sorted_list_sum`, binds its exact translated body, and calls it on any finite
`ValSeq` satisfying `stringsOnly(INPUT)`. If the call terminates, it returns a
fresh list reference whose contents are

```k
sortKeyVS(
  sortVS(scanEven(.ValSeq, INPUT)),
  builtinV("len"))
```

`scanEven` is the stable filter that retains exactly the string values whose
fixed-semantics length is even. `sortVS` and `sortKeyVS` are the supplied
semantics' named trusted sorting primitives. Conditional on their documented
contracts, the first sort establishes alphabetical order and the stable second
sort establishes primary length order while retaining alphabetical tie order.

This is a partial-correctness result. `#Top` establishes the K reachability
claims under the supplied theory; the separate Gate A/B/C audit below supports
the `VALIDATED` proof-quality headline.

## Formal claim

The target claim `SPEC.sorted-list-sum` starts with:

```k
#loadAll(sortedListSumModule)
~> Call(Name("sorted_list_sum"), list(INPUT))
```

in the initial module environment, empty heap, empty stack, `NoExc`, and exit
code 0. Its precondition is `stringsOnly(INPUT)`.

The destination has result `ref(2)` and these exact heap objects:

```k
0 |-> list(scanEven(.ValSeq, INPUT))
1 |-> list(sortVS(scanEven(.ValSeq, INPUT)))
2 |-> list(sortKeyVS(
       sortVS(scanEven(.ValSeq, INPUT)),
       builtinV("len")))
```

The module binding contains the exact body represented by `solution.mpy`.
`python3 py2mpy.py solution.py | diff -u solution.mpy -` exited 0 with no
differences.

`SPEC.filter-loop` is the circularity used for the `for` loop. Starting with
accumulator `ACC` and remaining input `INPUT`, it ends with
`scanEven(ACC, INPUT)` in the same accumulator object.

## Proof-extension inventory

### `stringsOnly`

- Class: definitional summary.
- Semantic role: constrains the theorem's input; it does not replace execution.
- Domain: every `ValSeq`.
- Equations: empty is true; a cons is `isStrV(head) andBool
  stringsOnly(tail)`.
- Coverage/overlap/descent: the empty and cons constructors are exhaustive and
  disjoint; recursion is on the strict tail.
- Matched context and state footprint: a pure term only; no cells are read or
  changed.
- Value influence: the preconditions of both positive claims.
- Justification: direct recursive definition of “every element is a string.”
- Dependents: `SPEC.filter-loop` and `SPEC.sorted-list-sum`.
- Validation: empty, nonempty, duplicate, mixed-length, all-odd, and
  empty-string inputs occur in the concrete and differential evidence.

### `scanEven`

- Class: definitional summary.
- Semantic role: names the loop result; no rule rewrites a program operation.
- Domain: every pair of `ValSeq` values.
- Equations: empty input returns the accumulator; a string head is appended
  exactly when `pyMod(seqLen(head), 2) ==Int 0`; the other string-parity case
  skips it; a non-string head is totalized by skipping it.
- Coverage/overlap/descent: `isStrV` versus `notBool isStrV` is exhaustive and
  disjoint. In the string branch, modulo-zero versus modulo-nonzero is
  exhaustive and disjoint. Every recursive call consumes the strict input
  tail.
- Matched context and state footprint: a pure term only; no operational cell is
  read or changed.
- Value influence: the loop's accumulator post-state and the target result
  supplied to the two fixed sorting primitives.
- Value justification: the string-domain equations use the same fixed
  `seqLen`, `pyMod`, stable append, and branch condition executed by the
  program. `SPEC.filter-loop` machine-checks their connection to the actual
  loop.
- Dependents: both positive claims.
- Validation: `SPEC.filter-loop` and the full spec print `#Top`; the wrong
  result and changed-body probes are rejected; 156 differential cases have
  zero mismatches.

### `#Ceil(seqLen(V)) => #Top requires isStrV(V)`

- Class: derived lemma.
- Semantic role: states definedness only; it neither supplies a length value
  nor replaces a runtime step.
- Domain: exactly values satisfying the fixed `isStrV` predicate.
- Matched context: any logical definedness query for `seqLen(V)` under that
  guard; the equation is state-independent.
- State footprint: none.
- Value influence: permits symbolic parity reasoning but leaves the length
  value equal to the fixed-semantics `seqLen(V)`.
- Justification: fixed semantics has `isStrV(str(CS)) => true`,
  non-string values reduce to false, `seqLen(str(CS)) => isLen(CS)`, and
  `isLen` is total by exhaustive empty/cons recursion.
- Dependents: `SPEC.filter-loop`, then the entry claim.
- Validation: no fresh or opaque result is introduced; both parity branches
  remain constrained by the unchanged `seqLen(V)` term.

### `sortedListSumBody` and `sortedListSumModule`

- Class: definitional, compile-time syntax abbreviations.
- Semantic role: exact constructor-level names for `solution.mpy`; macro
  expansion leaves no runtime rewrite or oracle.
- Domain/context: only their literal syntax occurrences.
- State footprint/value influence: none independently; their expansions are
  the program executed by the claims.
- Justification: the translator/diff command above reports no difference.
- Dependents: both claims.
- Validation: changing the body comparison from `==` to `!=` makes
  `SPEC-BODY-MUTATION.odd-filter-mutant` fail with an empty accumulator for
  input `["aa"]`.

### `SPEC.filter-loop`

- Class: derived reachability lemma/circularity.
- Semantic role: symbolically executes the fixed `#loop`, name lookup, length
  call, comparison, branch, and `append`; it is not an operational semantics
  rule.
- Domain: the exact loop body and exact local/module scopes, a single
  accumulator heap object, and `stringsOnly(INPUT)`.
- Matched context: the loop computation may have an arbitrary preserved
  continuation. The local `lst` and `result` bindings are fixed; `word` may
  change to the last iterated value. The omitted configuration cells are
  framed.
- Justification scope/context containment: the claim itself is checked over
  that complete domain with fixed semantics. On valid inputs the loop body has
  no abrupt control, allocation, exception, output, or persistent stack/frame
  effect. The only persistent writes are the captured `word` binding and the
  captured heap object's list contents.
- State footprint: reads the exact scopes and accumulator heap entry; writes
  `word` and that heap entry; preserves the continuation and other cells.
- Value influence: establishes the filtered list used by the target claim.
- Dependents: `SPEC.sorted-list-sum`.
- Validation: focused proof prints `#Top`; the full proof uses this
  circularity and prints `#Top`.

No task-local operational bridge, trusted primitive, fresh result oracle, or
execution-bypassing rewrite exists.

## Exact commands and actual outputs

The reproducible runner is `./prove.sh` and exited 0. Its substantive commands
and observed results were:

```bash
python3 py2mpy.py solution.py > solution.mpy
# Exit: 0

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
# Exit: 0

krun smoke.mpy --definition runtime-kompiled
# Exit: 0; final <k> .K, <exc> NoExc, <exit-code> 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
# Exit: 0

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.filter-loop
# Output: #Top
# Exit: 0

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
# Output: #Top
# Exit: 0
```

The second command proves every claim in `spec.k`; the first proof command is
the focused invariant check. The compilers also emitted warnings originating
in the supplied reference semantics (non-exhaustive unrelated helpers for the
LLVM build and unused `strLt` variables). Neither build failed.

Negative validation:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# Exit: 1 (expected)
# Residual: .ValSeq cannot equal
#   sortKeyVS(vCons(str("aa"), .ValSeq), builtinV("len"))

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
# Exit: 1 (expected)
# Residual heap object 0: list(.ValSeq), rather than list(["aa"])

python3 differential_test.py
# cases=156
# python_mismatches=0
# k_exit=0
```

## Gate results

### Gate A — PASS

- A1: the module is loaded, the selected binding contains the exact translated
  body, and the body executes. The odd-filter body mutation is rejected.
- A2: there is no task-local operational bridge. The loop claim accounts for
  its binding and heap writes and preserves the other state.
- A3: module binding, lookup, argument evaluation, call/return, loop
  continuation, and allocation are executed by fixed semantics. The loop
  circularity is restricted to the exact body, scopes, and heap shape.
- A4: task-local function equations have exhaustive, disjoint cases and
  structurally descending recursion. The sole definedness lemma follows from
  fixed constructor equations and supplies no value.
- A5: `.ValSeq` and `["aa"]` are realizable precondition witnesses. The
  deliberate false-result claim fails with the expected unmet result.

### Gate B — PASS

- The formal domain is every finite list of strings, including duplicates,
  empty strings, and differing lengths. It excludes non-string elements exactly
  as the prompt does.
- The theorem is stronger than the prompt's contradictory final sentence
  allowing an assumption that all words have the same length; it supports the
  varied lengths required by the main contract and examples.
- `scanEven` formally characterizes the filter. The interpretation of
  `sortVS` as alphabetical sort and `sortKeyVS(..., len)` as stable ascending
  length sort is explicitly conditional on the supplied trusted contracts.
- Two stable passes—alphabetical first, length second—implement primary length
  order and alphabetical tie order.

### Gate C — PASS

- All unproved components are named in the trust ledger below.
- Both negative probes and all concrete evidence have existing artifacts,
  exact commands, observed exit statuses, and recorded residual/result
  summaries.
- The differential oracle independently uses one sort with key
  `(len(word), word)`, rather than reusing the implementation's two-sort
  construction or the K proof equations.

## Trust boundary

| Component | Kind and effect | Dependents | Evidence |
|---|---|---|---|
| Supplied `MPY` semantics | Fixed language model; affects all execution and state | Both claims | LLVM smoke execution, positive Haskell proofs, and negative probes |
| `sortVS` | Supplied trusted primitive; result-bearing alphabetical ascending sort | Final result | Contract in `reference-semantics/semantics/sort.k`; concrete insertion-sort leg; 156-case differential run |
| `sortKeyVS` | Supplied trusted primitive; result-bearing stable ascending keyed sort | Final result | Contract in `sort.k`; concrete real-key stable insertion-sort leg in `concrete.k`; 156-case differential run |

The K target theorem keeps both sorting terms explicit. Therefore K formally
proves the program-to-summary connection, while the human-facing ordering
conclusion is conditional on these named supplied contracts.

## Empirically supported facts

`smoke.py` exercises the prompt examples plus empty, duplicate, mixed-length,
tie-order, and all-odd inputs through LLVM/K and ends with `.K`, `NoExc`, and
exit code 0.

`differential_test.py` enumerates every list of length 0 through 3 over
`["", "a", "ab", "bb", "cccc"]`: 156 cases. Its independent Python oracle
filters by even length and performs one sort with `(length, word)` as the key.
It found zero Python candidate mismatches, and the generated exact-source K
assertion program exited 0. This is finite evidence for the supplied sorting
contracts, not a universal proof of them.

## Excluded behavior

- Termination and complexity are not proved; K reachability establishes
  partial correctness.
- Non-string list elements, malformed calls, exceptions, and behavior outside
  the supplied Python subset are outside the theorem.
- Input alias identity and mutation observations are not in the observable
  state. The theorem uses the reference semantics' permitted bare read-only
  list input representation; this function does not mutate that input.
- The alphabetical and stable-key sorting algorithms are not proved
  universally inside K; they remain the explicit trusted boundary above.
