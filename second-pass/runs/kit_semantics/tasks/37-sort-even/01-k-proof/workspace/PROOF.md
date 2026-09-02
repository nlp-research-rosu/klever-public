VALIDATED

# What is proven

Under the supplied MPY semantics, the exact translated `sort_even` function is
partially correct for every symbolic `ValSeq` input.  If the call terminates,
it returns a fresh list whose odd-indexed values are those of the input and
whose even-indexed values are the supplied semantics' ascending
`sortVS` result for the input's even-index projection.

The source function does not mutate its argument.  The theorem observes the
returned reference, its list value, all allocations, module/function binding,
scope restoration, heap counter, call stack, return state, exception state,
and exit code.

# Formal claim

`SPEC.sort-even` starts from the complete initial MPY configuration, loads the
exact `FuncDef` represented in `solution.mpy`, looks up and calls
`sort_even(list(VS))`, and establishes:

```k
<k> ... => ref(0) </k>
<heap>
  .Map =>
  ( 0 |-> list(sortEvenResult(VS))
    1 |-> list(buildVS(VS, 0, vsLen(VS), 2))
    2 |-> list(sortVS(buildVS(VS, 0, vsLen(VS), 2))) )
</heap>
```

The result summary is defined by:

```k
sortEvenResult(VS)
  = fillEven(
      VS,
      sortVS(buildVS(VS, 0, vsLen(VS), 2)),
      0,
      evenCount(vsLen(VS)))
```

`fillEven` writes `valSeqAt(SORTED, I)` at index `2*I` for every
`0 <= I < STOP`; `setVSAt` leaves all other positions unchanged.
`evenCount(N)` is the exact MPY integer expression for `(N + 1) // 2`.

`SPEC-CONNECTION.loop-connection` is the universal bridge-free theorem for the
loop, exact remaining `Stmts` continuation, return, and frame pop.  It is
proved with module `VERIFICATION-NO-BRIDGE`, which does not import the
operational bridge.

# Proof-extension inventory

## `sortEvenBody` and `sortEvenLoopBody`

- **Class:** Definitional summary (syntax macros).
- **Semantic role:** Syntactic aliases only; macro expansion restores the exact
  translated AST before execution and replaces no semantic step.
- **Domain:** Their two nullary syntax occurrences.
- **Matched context / justification scope / containment:** Not operational
  patterns; each expands identically in every occurrence.
- **State footprint:** None.
- **Value influence:** They select the program body proved by both claims.
- **Value justification:** Direct textual correspondence with `solution.mpy`.
- **Justification:** Pure K macro expansion.
- **Dependents:** Both target claims, the connection theorem, and the bridge.
- **Control/value validation:** The `2*i+1` body mutation in
  `spec-body-mutation.k` is rejected with exit 1 and reaches `[9, 3]`, not the
  required `[3, 8]`.

## `evenCount(Int)`

- **Class:** Definitional summary.
- **Semantic role:** Names `(N + 1) // 2`; it does not replace execution.
- **Domain:** Every mathematical integer.
- **Matched context / justification scope / containment:** Function
  evaluation only; one unconditional equation covers the full domain.
- **State footprint:** None.
- **Value influence:** Determines how many even positions appear in the final
  result summary.
- **Value justification:** The equation uses `pyMod` and `/Int` exactly as the
  fixed MPY `//` rule for positive divisor 2.
- **Justification:** Algebraic expansion of the fixed integer rule.
- **Dependents:** `sortEvenResult` and `SPEC.sort-even`.
- **Control/value validation:** Concrete empty, odd-length, and even-length
  cases pass in both LLVM smoke execution and the Python differential suite.

## `fillEven(ValSeq, ValSeq, Int, Int)`

- **Class:** Definitional summary.
- **Semantic role:** Names the value produced by the remaining indexed writes;
  it never rewrites a program term.
- **Domain:** All two `ValSeq` arguments and all integer `I, STOP`.
- **Matched context / justification scope / containment:** Function terms only.
  Guards `I >= STOP` and `I < STOP` are disjoint and exhaustive.
- **State footprint:** None; it constructs a mathematical `ValSeq`.
- **Value influence:** Fully determines the returned list.
- **Value justification:** The step equation uses the fixed `setVSAt` and
  `valSeqAt` functions with the exact source indices and advances `I` by one.
- **Justification:** Base/step recurrence corresponding to zero or one fixed
  loop iteration.  The step terminates because `I` increases toward `STOP`.
- **Dependents:** `sortEvenResult`, the connection theorem, bridge, and target
  postconditions.
- **Control/value validation:** The bridge-free connection theorem proves the
  recurrence is exactly the fixed loop execution over its complete domain.

## `sortEvenResult(ValSeq)`

- **Class:** Definitional summary.
- **Semantic role:** Names the source-contract result without replacing
  execution.
- **Domain:** Every `ValSeq`.
- **Matched context / justification scope / containment:** Function terms only;
  the single unconditional equation covers every use.
- **State footprint:** None.
- **Value influence:** It is the entry claim's returned-list postcondition.
- **Value justification:** It composes the fixed slice operation, the named
  `sortVS` trust boundary, the exact even count, and `fillEven`.
- **Justification:** Direct formalization of “sort the even-index projection
  and write it back only at even indices.”
- **Dependents:** `SPEC.sort-even`.
- **Control/value validation:** The false-result mutation for `[5,6,3,4]` is
  rejected and exposes the actual `[3,6,5,4]` heap value.

## `SPEC-CONNECTION.loop-connection`

- **Class:** Derived lemma (auxiliary reachability theorem).
- **Semantic role:** Executes the exact fixed loop, return, and frame cleanup;
  it does not import or use the bridge it justifies.
- **Domain:** Arbitrary `CUR`, `SORTED`, `SLICE`, input `VS`, endpoint `C`,
  builtins scope, and old local `i`, with `I >= 0`.
- **Matched context:** Exact `#loop`, body, single remaining
  `(Return(...) .Stmts)` continuation, `#endcall`, environments 1 and 0,
  module and local scopes, heap locations 0/1/2, heap counter 3, one
  `frame(.K,0,1)`, `noRet`, `NoExc`, and exit code 0.
- **Justification scope / containment:** Exactly the same configuration and
  guard as the bridge; the theorem is slightly value-parametric in the
  preserved builtins, slice, and sorted heap values.
- **State footprint:** Reads the local bindings and sorted heap cell; updates
  heap cell 0; repeatedly rebinds local `i`; removes local scope 1; restores
  environment and scope counter; pops the frame; returns `ref(0)`; preserves
  heap cells 1/2, heap counter, module/builtins scope, return, exception, and
  exit states.
- **Value influence / justification:** Produces exactly
  `fillEven(CUR,SORTED,I,C)` by fixed execution.
- **Justification:** `kprove` under `VERIFICATION-NO-BRIDGE` prints `#Top`.
- **Dependents:** The operational bridge and therefore both main claims.
- **Control/value validation:** The exact `Stmts` continuation was derived from
  bounded fixed-semantics residuals; the `2*i+1` mutation fails independently.

## Exact loop operational rule in `VERIFICATION`

- **Class:** Operational bridge.
- **Semantic role:** At priority 40, replaces the proved loop region, return,
  and frame pop with the connection theorem's exact result.
- **Domain:** Exactly the complete match domain and `I >= 0` guard listed for
  `SPEC-CONNECTION.loop-connection`.
- **Matched context:** No continuation, stack, map, heap, control, exception,
  or exit wildcard is admitted.  `B`, `VS`, `SLICE`, `SORTED`, `CUR`, `I`,
  `C`, and the old local `i` are the theorem's universally quantified values.
- **Justification scope / containment:** Pattern-for-pattern equal to the
  bridge-free connection theorem.  Priority changes rule selection, not scope.
- **State footprint:** Identical to the connection theorem; all preserved and
  changed cells are explicit.
- **Value influence:** Determines heap cell 0 and returned `ref(0)`; introduces
  no fresh or opaque value.
- **Value justification:** `fillEven` equations plus the bridge-free universal
  connection theorem.
- **Justification:** `SPEC-CONNECTION.loop-connection`, proved before compiling
  and using this bridge.
- **Dependents:** `SPEC.loop-inv` and `SPEC.sort-even`.
- **Control validation:** Exact fixed-versus-bridge context comparison and
  rejected body mutation.
- **Value validation:** Fixed theorem equality and rejected false-result/body
  witnesses.

## Imported `sortVS(ValSeq)`

- **Class:** Trusted primitive supplied by the fixed reference semantics.
- **Semantic role:** Abstracts the ascending sort operation itself; this task
  proves the wrapper around it.
- **Domain:** Formally every `ValSeq`; the intended Python-level conclusion is
  conditional on elements being mutually sortable and on `sortVS` being their
  ascending permutation.
- **Matched context:** Only the supplied `sorted(list(...))` dispatch; no
  task-local rule broadens it.
- **Justification scope / containment:** The fixed semantics' named
  `sortVS` boundary.
- **State footprint:** Produces a new heap list; the input slice and original
  input are preserved.
- **Value influence:** Supplies every value written at an even result index.
- **Value justification:** Named external contract plus concrete insertion-sort
  rules under LLVM.
- **Justification:** Supplied semantics contract, LLVM smoke tests, and
  independent CPython differential tests.
- **Dependents:** `sortEvenResult`, both target claims, and the returned value.
- **Control/value validation:** Five K smoke cases and 19,536 Python cases,
  including lengths 0 through 6 over values `-2..2`, have zero mismatches.

# Exact commands and actual outputs

The complete output is preserved in `proof-run.log`; `prove.sh` contains the
exact commands.  The recorded clean run exited 0.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
python3 test_solution.py
```

Actual results: all commands exited 0; `krun` ended with `<k> .K </k>`,
`<exc> NoExc </exc>`, and exit code 0.  Python printed:

```text
Python differential tests: 19536 cases, 0 mismatches
```

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION-NO-BRIDGE --syntax-module MPY-SYNTAX \
  --output-definition verification-no-bridge-kompiled
kprove spec-connection.k \
  --definition verification-no-bridge-kompiled \
  --spec-module SPEC-CONNECTION
```

Actual connection-proof result:

```text
#Top
```

Exit code: 0.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual target-proof result:

```text
#Top
```

Exit code: 0.  This command proves every claim in `spec.k`.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`; the residual heap contains
`[3,6,5,4]` rather than the deliberately demanded `[5,6,3,4]`.

```bash
kprove spec-body-mutation.k \
  --definition verification-no-bridge-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`; the mutated body reaches
`[9,3]` rather than the required `[3,8]`.

# Gate results

## Gate A — PASS

- **A1:** The module load, function binding, call setup, allocations, and exact
  source body execute under the fixed semantics.  The only displaced loop
  region has an independently proved, bridge-free, universal connection
  theorem.  The material `2*i+1` body mutation is rejected.
- **A2:** The connection theorem and bridge explicitly agree on every read,
  write, preserved heap object, environment/scope change, frame pop, returned
  value, exception cell, and exit cell.
- **A3:** Lookup, argument evaluation, loop binding, exact
  `(Return(...) .Stmts)` continuation, abrupt return, and stack restoration are
  pinned.  No arbitrary continuation is framed.
- **A4:** `evenCount` and `sortEvenResult` each have one total equation.
  `fillEven` has disjoint, exhaustive `I >= STOP` / `I < STOP` guards and
  descends toward its base case.  No task-local false equation is admitted.
- **A5:** The initial state is realizable.  Concrete examples execute, the
  false-result mutation fails, and the body mutation changes the observed
  result and fails.

## Gate B — PASS

- **B1:** The formal input is a list value with arbitrary symbolic contents.
  The Python-level claim is for inputs whose elements are mutually sortable;
  this is the normal defined domain of the prompt's “sorted” requirement.
- **B2:** The supplied MPY model uses mathematical integers and does not model
  CPython `TypeError` behavior for incomparable mixed elements.  Those
  exceptional executions are excluded from the partial-correctness claim.
- **B3:** The wrapper property is formal: only `2*i` locations are updated from
  the sorted even projection.  “`sortVS` is the ascending permutation” is the
  explicit supplied-semantics trust boundary and is empirically supported, not
  re-proved here.
- **B4:** The implementation matches both prompt examples and all recorded
  representative tests; it returns a fresh list and preserves the input.

## Gate C — PASS

- **C1:** The trust ledger below names every unproved component and dependent.
- **C2:** `prove.sh`, all K specs, smoke input, Python differential test, and
  the complete `proof-run.log` exist.  Commands, domains, oracles, outputs, and
  exit statuses are recorded above.
- **C3:** Formal facts, conditional primitive meaning, finite evidence, and
  excluded exceptional behavior are separated explicitly.

# Trust boundary

| Component | Why outside this theorem | Effect | Dependents | Evidence |
|---|---|---|---|---|
| Supplied MPY semantics and K toolchain | Fixed foundation required by the task | All modeled execution and proof checking | Every claim | Successful LLVM/Haskell compilation, concrete execution, and two positive `#Top` proofs |
| `sortVS` ascending-permutation contract | Deliberately opaque symbolic primitive in the supplied semantics | Returned values at even indices | `sortEvenResult`, bridge theorem result, entry postcondition | Supplied concrete insertion-sort rules, five LLVM smoke cases, 19,536 CPython differential cases |
| `py2mpy.py` transliteration | Fixed supplied frontend | Program identity | `solution.mpy` and formal body macros | Successful regeneration; manual constructor-for-constructor comparison; body-sensitivity mutation |

# Empirically supported facts

`test_solution.py` uses an independent CPython oracle:

```python
expected = values[:]
expected[::2] = sorted(expected[::2])
```

It tests the prompt examples, additional boundary examples, and every list of
length 0 through 6 over `range(-2, 3)`: 19,536 cases and zero mismatches.
`smoke.mpy` independently runs five examples through the supplied LLVM
semantics, including empty, singleton, duplicates, negative values, odd
lengths, and even lengths.

These finite tests support the `sortVS` trust boundary and model adequacy; they
do not replace the universal K connection theorem.

# Excluded behavior

- CPython exceptions for lists containing mutually incomparable values.
- Floating-point, locale-dependent, custom-object, side-effecting comparison,
  and concurrency behavior not represented by the supplied MPY subset.
- Total-correctness/liveness claims beyond the Kit's partial-correctness scope.
- Any interpretation of `sortVS` other than the explicitly named ascending
  permutation contract; the wrapper theorem itself remains parametric in its
  returned `ValSeq`.
