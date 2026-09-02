VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, for every K integer `N >= 0`,
loading the exact translated definition of `tri`, resolving its module binding,
and calling it with `N` returns `ref(0)`.  Heap location `0` contains
`list(triResult(N))`, where `triResult(N)` is the ordered sequence of values at
indices `0` through `N`.

This is a partial-correctness result in the sense of the Kit workflow.  The
proof executes the program-defined function, loop body, list mutation, name
lookups, call frames, and return rules from the fixed semantics.

The proof also establishes:

- `triValue(0) = 1`;
- `triValue(1) = 3`;
- for even `N >= 2`, `triValue(N) = 1 + N / 2`; and
- for odd `N >= 3`,
  `triValue(N) = triValue(N-1) + triValue(N-2) + triValue(N+1)`.

Thus the execution summary has the recurrence meaning stated in `prompt.py`.

## Formal claims

`spec.k` contains six claims:

1. `SPEC.tri-loop` is the circularity for the exact source `while` loop.  With
   current index `I`, bound `N`, and arbitrary existing prefix `P`, it changes
   the heap list to `triComplete(P,I,N)` and changes `i` to `N+1`.
2. `SPEC.tri-entry` loads and calls the exact translated function from the
   initial MPY configuration and constrains the returned reference, heap,
   scopes, allocation counters, stack, return state, exception state, and exit
   code.
3. `SPEC.tri-at-zero` and `SPEC.tri-at-one` establish the base values.
4. `SPEC.tri-at-even` establishes the prompt's even clause.
5. `SPEC.tri-at-odd-recurrence` establishes the prompt's odd recurrence.

The formal input domain is exactly integer `N >= 0`.

## Proof-extension inventory

### Exact-AST macros

- **Extensions:** `triLoopCondition`, `triLoopBody`, `triFunctionBody`, and
  `triDefinition`.
- **Class:** Definitional summary, syntax-only.
- **Semantic role:** Parse-time aliases; they expand to constructors and do not
  rewrite runtime execution.
- **Domain and matched context:** The exact constructor trees written in
  `verification.k`, with no guards, frames, or operational wildcards.
- **Justification scope and containment:** Their expansions match
  `solution.mpy`, including binding names, branch order, append calls,
  increment, and return.
- **State footprint and value influence:** None by themselves; after expansion,
  fixed MPY rules perform all state and value changes.
- **Dependents:** `SPEC.tri-loop` and `SPEC.tri-entry`.
- **Validation:** `solution.mpy` is regenerated from `solution.py`; the
  changed-body probe replaces the body with `return [2]` and is rejected.

### `triValue`

- **Class:** Definitional summary.
- **Semantic role:** Names the mathematical integer appended at an index; it
  does not match or replace a program term.
- **Domain:** All integers.  `I < 0` is totalized to `0`.  For `I >= 0`, the
  disjoint `pyMod(I,2) = 0` and `pyMod(I,2) = 1` cases are exhaustive.
- **Matched context:** Pure `Int` terms only; no continuation, binding, or
  configuration cells.
- **State footprint:** None.
- **Value influence:** Determines each element in `triComplete`, the final
  result, and the recurrence claims.
- **Value justification:** The nonnegative equations are the closed forms used
  by the source branches.  The four value/recurrence claims all close under
  K's integer theory.
- **Dependents:** The loop claim, entry claim through `triComplete`, and all
  four mathematical claims.
- **Validation:** The false-result probe is rejected, and the independent
  recurrence oracle has zero mismatches over `0..100`.

### `triComplete` and `triResult`

- **Class:** Definitional summaries.
- **Semantic role:** `triComplete(P,I,N)` appends `triValue(I)` through
  `triValue(N)` to prefix `P`; `triResult(N)` starts that fold at the empty
  sequence and index `0`.
- **Domain:** All `ValSeq` prefixes and all integer `I,N`.  Guards `I > N` and
  `I <= N` are disjoint and exhaustive.
- **Matched context:** Pure sequence and integer terms only.
- **State footprint:** None.
- **Value influence:** Fixes the complete returned list.
- **Value justification and descent:** The base returns `P`; the step appends
  exactly one value and increments `I`.  Measure `N-I+1` decreases on every
  recursive step in the active domain.
- **Dependents:** `SPEC.tri-loop` and `SPEC.tri-entry`.
- **Validation:** The loop proof closes from an arbitrary `P`, and the ground
  false-result probe exposes `[1,3,2,8]` rather than the requested mutant
  `[1,3,2,9]`.

### `SPEC.tri-loop`

- **Class:** Derived reachability lemma/circularity.
- **Semantic role:** Proves fixed-semantics execution of the exact loop; it is
  not an operational rewrite in `verification.k`.
- **Domain:** `N >= 0`, `0 <= I <= N+1`, arbitrary prefix `P`.
- **Matched context:** Exact `#while(triLoopCondition,triLoopBody)`, arbitrary
  trailing continuation, environment `L`, the exact local bindings
  `i`, `n`, and `values`, parent scope `0`, heap location `H`, and framed
  unrelated scope/heap entries.  Other configuration cells are preserved.
- **Justification scope and containment:** The claim itself is machine-checked
  over every framed continuation and every state satisfying its guards.
- **State footprint:** Reads `i`, `n`, `values`, and heap list `H`; writes only
  `i` and heap list `H`.  The append result `noneV` is discarded by the source
  expression statement.  No exception, output, return, or allocation is
  abstracted by the claim.
- **Value influence:** Supplies the final heap list used by the entry claim.
- **Dependents:** `SPEC.tri-entry`.
- **Control/value validation:** The focused loop command prints `#Top`; the
  complete-spec proof uses the circularity while still executing normal lookup,
  branch, append, increment, continuation, frame-pop, and return semantics.

### Mathematical claims

- **Extensions:** `SPEC.tri-at-zero`, `tri-at-one`, `tri-at-even`, and
  `tri-at-odd-recurrence`.
- **Class:** Derived lemmas.
- **Domain:** Their explicit ground or parity guards.
- **Semantic role and state footprint:** Pure arithmetic; they replace no
  execution and touch no state.
- **Justification:** K simplification plus the integer solver proves each claim.
- **Dependents:** Intent validation; the execution claims do not assume them.

There are no proof-local operational bridges, priority rules, simplification
axioms, opaque result oracles, or trusted primitives.

## Exact commands and actual outputs

The complete reproducible command record is `./prove.sh`.  Its final recorded
run exited `0`.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
```

Output: no diagnostics; exit `0`.

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Output: `kompile` exited `0` with supplied-semantics exhaustiveness/unused
variable warnings.  `krun` exited `0` with final `<k> .K </k>`,
`<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>` after all six assertions.

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual positive proof output:

```text
#Top
```

Both commands exited `0`.  `kprove` also emitted four `WarnTrivialClaim`
messages for arithmetic claims normalized during claim simplification.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1`, `WarnStuckClaimState`; residual heap
`[1,3,2,8]` does not unify with the deliberately false `[1,3,2,9]`.

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit `1`, `WarnStuckClaimState`; the changed body produces
`[2]`, which does not unify with `[1]`.

```bash
python3 oracle_test.py
```

Actual output and exit:

```text
Differential domain: integers 0..100
Oracle: forward evaluation of the prompt recurrence
Mismatches: 0
```

Exit `0`.

## Gate results

### Gate A — PASS

- **A1:** The exact program body executes under fixed semantics.  The material
  body mutation is rejected with its actual heap value visible.
- **A2:** There is no operational bridge.  The entry theorem constrains every
  operational cell, and the loop theorem enumerates its read/write footprint.
- **A3:** Fixed rules perform binding, left-to-right evaluation, branch
  selection, method dispatch, frame control, and return.  No opaque value or
  abrupt-control shortcut exists.
- **A4:** Summary guards are exhaustive and disjoint; `triComplete` has a
  decreasing measure.
- **A5:** `N=3` is a realizable witness.  The false postcondition is rejected
  with exit `1`.

### Gate B — PASS

- **B1:** The theorem domain, K integers `N >= 0`, matches the prompt's stated
  input domain.
- **B2:** The relevant model uses unbounded mathematical integers and mutable
  heap lists, matching the material Python behavior for this task.  No float,
  text, external state, or implementation-defined operation is used.
- **B3:** Separate machine-checked claims prove that the execution summary has
  the prompt's base, even, and odd-recurrence meaning.
- **B4:** The implementation and formal intent agree, including the example
  `tri(3) = [1,3,2,8]`.

### Gate C — PASS

- All proof files, negative probes, concrete smoke program, output logs, and
  exact commands exist in the current directory.
- The independent oracle evaluates the prompt recurrence forward and does not
  reuse `triValue` or `triComplete`.
- Formal proof, finite evidence, trust assumptions, and exclusions are
  separated here.

## Trust boundary

The theorem is conditional on the supplied read-only MPY semantics,
`py2mpy.py` preserving the CPython AST constructor structure, K's Haskell
backend and integer solver, and the K reachability-logic implementation.  Those
components are outside this theorem.  No proof-local trusted primitive is used,
and none of the supplied semantics' opaque sort/float/digest primitives occurs
on the target execution path.

## Empirically supported facts

- LLVM execution of six ground cases (`n=0..5`) terminates with all assertions
  satisfied.
- CPython differential execution against a separately written forward
  recurrence has zero mismatches for all `n=0..100`.
- These finite checks support translation/model adequacy; they do not replace
  the universal K proof.

## Excluded behavior

- Negative integers and non-integer Python inputs are outside the formal
  precondition.
- The proof establishes partial correctness, not a separate liveness theorem.
- Behavior outside the supplied MPY subset and equivalence of the entire MPY
  semantics to all CPython behavior are not claimed.
- Warnings in unrelated supplied float/string/subscript helpers do not occur on
  this program's execution path.
