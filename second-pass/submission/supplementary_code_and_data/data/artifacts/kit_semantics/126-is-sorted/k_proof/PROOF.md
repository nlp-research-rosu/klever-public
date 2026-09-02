VALIDATED
=========

## What is proven

Under the supplied MPY semantics, the proof establishes partial correctness of
the exact `is_sorted` closure in `solution.mpy`.

For every finite MPY list `list(VS)` for which `nonNegativeVals(VS)` is true,
calling the module binding named `is_sorted` returns
`sortedWithAtMostTwo(VS)`. The call performs normal name lookup, argument
binding, body execution, loop execution, return, and frame popping. The module
binding is preserved; the temporary result of `sorted` is allocated at heap
location 0; `heapLoc` advances from 0 to 1; and the environment, call stack,
return cell, exception cell, and exit code return to their stated final values.

The proof is a partial-correctness result. It does not separately claim
termination, resource bounds, or behavior outside the formal input domain.

## Formal claims and scope

`spec.k` contains two claims:

1. `SPEC.scan-loop` proves the loop invariant for an arbitrary remaining
   `ValSeq`, prior tuple value, repetition count, Boolean result, continuation,
   and framed semantics cells.
2. `SPEC.entry` proves the whole call from an exact module binding and exact
   function body to `sortedWithAtMostTwo(VS)`.

The formal input domain is exactly finite lists of nonnegative MPY integers.
`nonNegativeVals` rejects negative integers and every non-integer `Val`.

The observable entry result is the Boolean in `<k>`. The entry claim also
constrains every state cell: the module scope is unchanged, the callee scope is
removed, the sorted temporary remains in the heap, `heapLoc` is 1, the stack is
empty, `<ret>` is `noRet`, `<exc>` is `NoExc`, and the exit code is 0.

The program boundary starts at lookup and invocation of `is_sorted` with its
binding pinned to the exact closure body generated in `solution.mpy`. Module
loading of that already-pinned definition is outside the claim; lookup,
binding, every source statement, and return are inside it.

## Why the predicate matches the prompt

The supplied semantics defines `sortVS(VS)` as the trusted ascending
permutation produced by `sorted`. Conditional on that named contract,
`VS ==K sortVS(VS)` is true exactly when the input is already ascending.

`duplicateOK` starts with sentinel `-1` and count 0. The sentinel differs from
the first element because the formal domain is nonnegative. Equal adjacent
values increment the count, and a different value resets it to 1. The predicate
becomes false when a run reaches length 3. When the sorting conjunct is true,
all equal values are contiguous, so “no run has length 3” is equivalent to “no
value occurs more than twice.” If the input is not ascending, the sorting
conjunct is already false.

Thus `sortedWithAtMostTwo` states the prompt's ascending-order and
at-most-two-occurrences requirements.

## Proof obligations

- Base case: an empty remaining sequence leaves the prior value, count, result,
  and loop value unchanged; `duplicateOK` reduces to true.
- Inductive case: fixed MPY semantics binds the next value, constructs and
  compares singleton tuples, updates or resets `repeated`, sets `result` false
  exactly when the new count exceeds 2, stores the new singleton tuple, and
  returns to the same loop head. `SPEC.scan-loop` then applies to the tail.
- Whole-program discharge: fixed semantics computes the `sorted` comparison,
  initializes the loop state, applies the loop claim, returns the summarized
  Boolean, and pops the exact call frame.

## Proof-extension inventory

There are no proof-local operational bridges, priority rules, simplification
rules, opaque result oracles, or rewrites that replace MPY program execution.

### `nonNegativeVals`

- Class: definitional summary.
- Semantic role: input-domain predicate; it does not rewrite execution.
- Domain and coverage: all `ValSeq`; empty, integer-head, and `[owise]`
  non-integer-head cases are exhaustive and disjoint.
- Matched context / state footprint: pure term only; no continuation, binding,
  control, or state cells.
- Value influence: guards `SPEC.entry` and the `sortedWithAtMostTwo` equation.
- Value justification: structurally recursive, truthful equations; recursion
  descends on the sequence tail.
- Dependents: `SPEC.entry` and the human-facing contract.
- Control/value validation: no control effect; boundary and exhaustive
  differential witnesses include empty, zero, large integers, and duplicates.

### `nextRepeated`, `scanPrevious`, `scanRepeated`, and `scanValue`

- Class: definitional summaries.
- Semantic role: name final loop scalar values; none appears at the head of an
  MPY computation.
- Domain and coverage: all declared `Val`/`Int`/`ValSeq` arguments.
  `nextRepeated` splits on `V ==K P` versus its negation; the guards are
  complementary. Sequence equations split on empty versus `vCons`.
- Matched context / state footprint: pure terms; no state is read or changed.
- Value influence: the loop invariant's final local bindings and the
  `duplicateOK` recurrence.
- Value justification: exact one-iteration equations with structural descent.
- Dependents: `SPEC.scan-loop`, and through it `SPEC.entry`.
- Control/value validation: fixed loop execution closed independently with
  `#Top`; concrete and differential tests exercise equal and unequal cases.

### `duplicateOK` and `scanDuplicates`

- Class: definitional summaries.
- Semantic role: record whether the scanned suffix ever makes the adjacent run
  count exceed 2; they do not replace execution.
- Domain and coverage: constructor-complete over `ValSeq`.
  `duplicateOK` descends on the tail. `scanDuplicates` has one exhaustive
  equation and preserves an already-false accumulator by conjunction.
- Matched context / state footprint: pure terms only.
- Value influence: final result and postcondition.
- Value justification: the equations exactly mirror the source counter update
  and `repeated > 2` branch.
- Dependents: both K claims.
- Control/value validation: the loop claim proves the connection to fixed
  execution; the false-result mutation is rejected.

### `sortedWithAtMostTwo`

- Class: definitional summary.
- Semantic role: names the prompt-facing property; it does not rewrite program
  execution.
- Domain: guarded by `nonNegativeVals(VS)`, exactly the theorem domain. It is
  intentionally not declared total outside that guard.
- Matched context / state footprint: pure term only.
- Value influence: entry result.
- Value justification: conjunction of the supplied `sortVS` contract and the
  structurally defined duplicate scan.
- Dependents: `SPEC.entry`.
- Validation: the equivalence argument above, nine concrete K sorting cases,
  all prompt examples under K, and 97,666 independent CPython comparisons.

### `SPEC.scan-loop`

- Class: derived auxiliary reachability claim (loop circularity).
- Semantic role: summarizes fixed execution after independently proving its
  base and inductive cases.
- Matched context: the exact `#loop` target and exact translated loop body; an
  arbitrary active continuation is framed. The current scope is pinned to the
  five actual local bindings and `parent(0)`. All other semantics cells are
  explicitly framed.
- Justification scope / containment: the claim itself is universally proved by
  fixed semantics for exactly that framed context, so every use by
  `SPEC.entry` is within its match domain.
- State footprint: preserves `lst`; updates `previous`, `repeated`, `result`,
  and `value`; preserves scope location, heap, heap location, stack, return,
  exception, and exit-code cells.
- Value influence: supplies the entry result and final local state before
  return.
- Justification: focused `kprove` returned `#Top`, and the full proof returned
  `#Top`.
- Control validation: the loop body has no return, break, continue, exception,
  or frame effect. The claim consumes only the loop computation and preserves
  the arbitrary continuation.

### Supplied `sortVS`

- Class: trusted primitive imported from the fixed reference semantics, not a
  proof-local extension.
- Named contract: `sortVS(VS)` is an ascending permutation of an integer
  `ValSeq`, matching Python's `sorted` on the formal domain.
- Matched execution context: the supplied `sorted` rule applies after normal
  builtin lookup and argument evaluation and allocates
  `list(sortVS(VS))`.
- State footprint: reads the input sequence, writes one fresh heap entry, and
  advances `heapLoc`; binding and control remain governed by fixed semantics.
- Value influence: the initial `result`, final return value, and retained heap
  object.
- Dependents: `SPEC.entry` and the human interpretation of
  `sortedWithAtMostTwo`.
- Trust status: the K theorem is interpretation-parametric in the opaque
  symbolic value and explicitly returns a formula containing `sortVS`.
  Interpreting that formula as ascending order is conditional on the named
  contract.
- Evidence: the LLVM concrete rules passed nine direct sorting assertions and
  all program smoke cases. This finite evidence supports but does not
  universally prove the trusted contract.

## Exact commands and actual results

The reproducible command record is `prove.sh`. Its complete run exited 0.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 py2mpy.py sort_smoke.py > sort_smoke.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled > krun-smoke.out
krun sort_smoke.mpy --definition runtime-kompiled > krun-sort.out
python3 differential_test.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual results:

- Both `kompile` commands exited 0. They emitted only warnings originating in
  the supplied reference semantics.
- `krun smoke.mpy` exited 0; `krun-smoke.out` ends with
  `<exit-code> 0 </exit-code>` and stderr was empty.
- `krun sort_smoke.mpy` exited 0; `krun-sort.out` ends with
  `<exit-code> 0 </exit-code>` and stderr was empty.
- `python3 differential_test.py` printed
  `checked=97666 mismatches=0` and exited 0.
- The full `kprove` command printed `#Top` and exited 0, proving every claim in
  `spec.k`.
- A focused construction run,
  `kprove spec.k --definition verification-kompiled --spec-module SPEC
  --claims SPEC.scan-loop`, also printed `#Top` and exited 0.

The Gate A non-vacuity command was:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.entry-false-empty
```

It exited 1 as expected, emitted `WarnStuckClaimState`, and left
`true ~> .K` in `<k>` while the deliberately mutated destination required
`false`. The satisfiable witness was the empty nonnegative integer list.

## Gate results

### Gate A — PASS

- The exact program-defined body executes under fixed semantics.
- Binding, argument evaluation, allocation, loop control, return, and frame
  restoration are present in the entry claim.
- No proof-local rule skips execution or introduces abrupt control.
- All function equations have exhaustive/disjoint coverage over their declared
  use domain and structurally descend where recursive.
- The empty-list witness satisfies the precondition.
- The false-postcondition mutation was rejected with the expected residual.

### Gate B — PASS

- The formal domain matches the prompt: finite lists containing only
  nonnegative integers.
- The return predicate matches ascending order and permits one duplicate
  (multiplicity 2) but rejects multiplicity 3 or greater.
- The supplied model's bare unboxed list is its documented representation for
  read-only symbolic inputs. Python arbitrary-precision integer behavior is
  compatible with MPY `Int` on this program.
- The ascending-order interpretation is explicitly conditional on the fixed
  semantics' `sortVS` contract; this limitation is visible rather than hidden.

### Gate C — PASS

The trust ledger names `sortVS`, its exact effect, all dependent conclusions,
and the conditional result language. Every claimed artifact exists:

- `smoke.py` / `smoke.mpy`: the eight prompt examples plus the empty boundary;
  oracle is each explicit expected Boolean; LLVM `krun` exit 0.
- `sort_smoke.py` / `sort_smoke.mpy`: nine empty, sorted, reversed, permuted,
  duplicate, triple, and large-integer sorting cases; oracle is each explicit
  expected ascending list; LLVM `krun` exit 0.
- `differential_test.py`: every sequence of lengths 0 through 7 over values
  0 through 4, plus ten empty/sentinel/large/long boundaries. The independent
  oracle uses adjacent `<=` checks and `collections.Counter`, not the proof
  equations. Result: 97,666 checked, zero mismatches.
- `spec-vacuity.k`: false empty-list result mutation; exit 1 with a stuck
  true-versus-false result.

Finite tests are recorded only as evidence. They do not replace the symbolic
program proof or universally discharge the named `sortVS` trust contract.

## Trust boundary and excluded behavior

Formally established: execution of the exact source body returns the stated
K summary under the supplied semantics, and the loop summary is connected to
fixed execution.

Conditionally interpreted: `VS ==K sortVS(VS)` means the input is ascending,
under the supplied `sortVS` ascending-permutation contract.

Empirically supported: concrete `sorted` behavior on the recorded K cases and
the full implementation/property agreement on 97,666 CPython inputs.

Excluded: negative integers, non-integer list members, malformed calls,
alias-sensitive input mutations, exceptions or resource exhaustion, and any
claim of total correctness or complexity.
