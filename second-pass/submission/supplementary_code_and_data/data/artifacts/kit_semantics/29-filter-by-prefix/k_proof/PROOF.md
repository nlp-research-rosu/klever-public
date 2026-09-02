VALIDATED

## What is proven

Under the supplied MPY semantics, for every finite semantic list whose elements
are strings and every semantic string prefix, the translated
`filter_by_prefix` function returns a fresh list containing exactly the input
elements whose code sequences start with the prefix, in their original order
and with duplicates preserved.

This is a partial-correctness result.  The reachability claims do not themselves
state a termination theorem.

The proved source boundary is the exact module translated into `solution.mpy`:
the no-op `typing.List` import, the `filter_by_prefix(strings, prefix)`
definition, its two initial assignments, its `for` loop and `startswith`
condition, `append`, and `return`.  The proof observes the returned reference,
the complete returned list in the heap, frame cleanup, stack, return state,
exception state, allocation counter changes, and relevant scopes.

## Formal claims

`SPEC.filter-loop` states the loop invariant at the actual continuation emitted
by statement sequencing:

```k
#loop(list(INPUT), Name("string"), filterLoopBody)
~> (Return(Name("result")) .Stmts):Stmts
~> #endcall
```

Starting with accumulator `ACC`, prefix `P`, and `allStrings(INPUT)`, it returns
the result reference after changing the referenced heap list to
`filterPrefixAcc(ACC, INPUT, P)` and performing the exact return/frame cleanup.

`SPEC.filter-program` starts from the initial MPY configuration, loads
`filterByPrefixProgram`, calls the target with `list(INPUT)` and `str(PREFIX)`,
and ends at `ref(0)` with:

```k
0 |-> list(filterPrefixAcc(.ValSeq, INPUT, PREFIX))
```

Its precondition is `allStrings(INPUT)`.  The prefix is syntactically a
semantic string.  Non-list and non-string inputs are outside the claim.

The invariant obligations are:

- Base: an empty remaining list leaves `ACC` unchanged.
- Step/keep: `startsWith(P, stringCodes(V))` appends the current string and
  recurs on the tail.
- Step/drop: the complementary condition leaves the accumulator unchanged and
  recurs on the tail.
- Whole program: loading, call binding, allocation, initialization, and the
  exact loop head establish the invariant with an empty accumulator.

## Program identity

`solution.mpy` is regenerated with:

```bash
python3 py2mpy.py solution.py > solution.mpy
```

Both `solution.mpy` and the expanded proof macro are parsed with the final
compiled definition:

```bash
kast solution.mpy \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --output kore > program-source.kore
kast \
  --expression 'filterByPrefixProgram' \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore > program-macro.kore
cmp program-source.kore program-macro.kore
```

Actual result: both files are 4,214 bytes and `cmp` exited 0.

## Proof-extension inventory

### Exact AST macros

- Extension: `filterLoopBody`, `filterFunctionBody`, and
  `filterByPrefixProgram` in `verification-core.k`.
- Class: definitional syntax aliases.
- Semantic role: compile-time names for exact MPY AST terms; they do not
  replace runtime execution.
- Domain/context: closed macro terms only.
- State footprint/value influence: none by themselves; their expansions select
  the program body proved by the claims.
- Justification and validation: expanded KORE is byte-identical to the parsed
  `solution.mpy`.  The unconditional-append body mutation is rejected.
- Dependents: both target claims and the loop-connection claim.

### String-domain definitions

- Extension: `stringCodes`, `isStringVal`, and `allStrings` in `domain.k`.
- Class: definitional summaries.
- Semantic role: define the formal `List[str]` domain and expose a string's
  semantic code sequence.
- Domain: all `Val` and `ValSeq` terms.  `stringCodes(str(S)) = S`; its `owise`
  case returns `.IntSeq`.  `isStringVal(V)` is
  `V ==K str(stringCodes(V))`.  `allStrings` is the structural fold of that
  predicate.
- Coverage/overlap/descent: the string and `owise` projection cases are
  disjoint and total; the list cases are constructor-disjoint and the recursive
  call is on the tail.
- State footprint: none.
- Value influence: the projection determines the normalized iterator value,
  summary branch, and returned list element.
- Value justification: for every value admitted by `isStringVal`, the
  bridge-free `CONNECTION-SPEC.string-iterator-normalization` proves that fixed
  iteration returns exactly `str(stringCodes(V))`.
- Dependents: iterator normalization, `filterPrefixAcc`, the loop theorem, and
  both target claims.
- Validation: fixed/extended witnesses use `"a"` and `""`; the opposite
  iterator value is rejected.

### Result summary

- Extension: `filterPrefixAcc` and its three equations in
  `verification-core.k`.
- Class: definitional summary.
- Semantic role: names the mathematical stable prefix filter; it never occurs
  in a program redex and does not skip execution.
- Domain: total over all `(ACC, INPUT, P)`.  The off-domain totalization maps a
  non-string value through `stringCodes`; the theorem itself requires
  `allStrings(INPUT)`.
- Coverage/overlap/descent: the empty/cons cases are disjoint.  The two cons
  guards are `startsWith(...)` and its Boolean negation, so exactly one applies.
  Each recursive equation strictly shortens `INPUT`.
- Matched context/state footprint: mathematical terms only; no cells,
  continuation, binding, exception, or allocation state.
- Value influence: fixes the final heap list and therefore the returned value.
- Value justification: on `allStrings`, each input head equals
  `str(stringCodes(V))`; the equations retain it exactly when the same
  `startsWith` predicate used by fixed method semantics is true.
- Dependents: loop connection, loop bridge, and both target claims.
- Validation: concrete MPY assertions, keep/drop fixed-vs-extended witnesses,
  a rejected wrong-loop result, and the independent CPython differential test.

### Iterator normalization

- Extension: the priority-40 `#iterNext(list(vCons(V, REST)))` rule in
  `verification-core.k`.
- Class: operational bridge.
- Semantic role: replaces one fixed iterator step only when
  `isStringVal(V)`; it yields `str(stringCodes(V))`.
- Complete matched context: the exact iterator redex with any trailing `<k>`
  continuation (`...`), guarded by `isStringVal(V)`.  Every other configuration
  cell is framed and unchanged.
- Justification scope: `CONNECTION-SPEC.string-iterator-normalization`, compiled
  from `domain.k`, which imports MPY but does not import this bridge.  Its
  `CONT:K` is universally quantified and its omitted cells are completed as
  unchanged frames.
- Context containment: the bridge and theorem accept the same iterator term,
  guard, arbitrary continuation, and state frame.
- State footprint: reads no cell other than `<k>`; writes no heap, scope,
  stack, return, exception, output, or allocation state.
- Value/control influence: supplies the loop element and preserves the entire
  continuation.
- Value justification: the bridge-free theorem proves fixed iteration's `V`
  equals `str(stringCodes(V))` under the exact guard.
- Dependents: loop-connection theorem and thus the loop bridge and target
  claims.
- Control/value validation: the universal theorem prints `#Top`; fixed and
  extended ground witness modules both print `#Top`; the wrong `"a" -> ""`
  interpretation exits 1 with `WarnStuckClaimState`.

### Scope-deletion normalization

- Extension:
  `((1 |-> _:Scope) SC)[1 <- undef] => SC` under
  `notBool (1 in_keys(SC))`.
- Class: derived lemma.
- Semantic role: normalizes the built-in map update after fixed function-pop
  execution; it does not replace Python code.
- Domain/overlap: all maps with key `1` absent from `SC`.  The guard makes the
  equation exactly the built-in deletion law; no competing proof-local equation
  exists.
- State footprint/value influence: mathematical map term only; it exposes the
  already-computed caller scope and does not affect the returned list.
- Dependents: loop-connection theorem.
- Validation: both bridge-free loop connection and fixed ground loop witnesses
  reach `SC` and print `#Top`.

### Loop, return, and frame-cleanup summary

- Extension: the priority-40 full-configuration rule in `verification.k`.
- Class: operational bridge.
- Semantic role: summarizes the remaining loop, exact return statement,
  `#endcall`, and frame pop.
- Complete matched context: exact `filterLoopBody`; exact statement-list return
  continuation; environment `1`; closed four-local frame with `strings`,
  `prefix`, `result`, and `string`; scope location `2`; result heap object;
  heap location; exact `frame(.K, 0, 1)` stack; `noRet`; `NoExc`; and
  `allStrings(INPUT)`.
- Justification scope:
  `LOOP-CONNECTION-SPEC.filter-loop-connection`, compiled from
  `verification-core.k`.  That definition does not import the loop bridge.  It
  depends only on fixed MPY semantics, definitions above, the derived map law,
  and the separately connected iterator normalization.
- Context containment: the theorem and bridge have the same term, continuation,
  bindings, guard, cells, frames, and result.  The statement-list continuation
  was explicitly checked against the real bounded execution trace.
- State footprint: reads `<k>`, environment, local bindings, heap accumulator,
  stack, return and exception state; writes the result heap list, restores
  caller environment and scope location, deletes the callee scope, empties the
  stack frame, and returns `ref(H)`.  It preserves heap location, exception,
  exit code, generated counter, and the framed heap/scope remainders exactly as
  the theorem does.
- Value/control influence: determines every remaining branch and append, the
  returned reference/list, return control, stack pop, and frame cleanup.
- Value justification: the bridge-free universal connection theorem executes
  fixed `startswith`, append, loop control, return, and pop to the identical
  summary value and state.
- Dependents: `SPEC.filter-loop` under the final theory and
  `SPEC.filter-program`.
- Control/value validation: universal connection `#Top`; fixed and extended
  keep/drop ground witnesses both `#Top`; wrong-loop output rejected; the
  unconditional-append program-body mutant is not matched by the bridge and is
  rejected after fixed execution.

No proof-local opaque primitive or unconstrained result-bearing oracle remains.

## Exact proof and execution record

The complete reproducible command sequence is executable as:

```bash
./prove.sh
```

Important positive commands and actual results:

```bash
kompile --backend haskell domain.k \
  --main-module STRING-SEQUENCE-DOMAIN \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC
# Actual: #Top, exit 0

kompile --backend haskell verification-core.k \
  --main-module VERIFICATION-CORE \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-connection-kompiled
kprove loop-connection-spec.k \
  --definition loop-connection-kompiled \
  --spec-module LOOP-CONNECTION-SPEC
# Actual: #Top, exit 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
# Actual: #Top, exit 0; both claims selected

kprove bridge-witness-fixed.k \
  --definition loop-connection-kompiled \
  --spec-module BRIDGE-WITNESS-FIXED
# Actual: #Top, exit 0

kprove bridge-witness-extended.k \
  --definition verification-kompiled \
  --spec-module BRIDGE-WITNESS-EXTENDED
# Actual: #Top, exit 0
```

Concrete execution used the required LLVM modules:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty \
  --output-file concrete-tests.out
```

Actual result: `.K`, `NoExc`, exit code `0`.  The assertions cover the prompt's
empty-list and mixed-list examples plus empty-prefix behavior.

The supplied semantics emits unused-variable and LLVM non-exhaustiveness
warnings in unrelated generic helpers.  All required builds and positive proof
commands exit 0.

## Negative and mutation evidence

All probes are preserved as source and output artifacts and are checked by
`prove.sh`.

- `BRIDGE-WITNESS-NEGATIVE.wrong-iterator-value`: input `"a"` was changed to
  expected output `""`.  Exit 1; `negative-iterator.out` contains
  `WarnStuckClaimState` and the actual yielded code `97`.
- `BRIDGE-WITNESS-NEGATIVE.wrong-loop-value`: a matching `"abc"` element was
  changed to expected empty output.  Exit 1; `negative-loop.out` contains
  `WarnStuckClaimState` and the actual singleton `"abc"` heap list.
- `SPEC-VACUITY.wrong-empty-result`: the realizable input `(["abc"], "a")`
  was assigned an empty postcondition.  Exit 1; `vacuity.out` contains
  `WarnStuckClaimState` and the actual singleton `"abc"` result.
- `SPEC-BODY-MUTANT.unconditional-append-mutant`: the loop body was materially
  changed to append every element.  On `(["abc", "bcd"], "a")`, exit 1;
  `body-mutant.out` contains `WarnStuckClaimState` and the actual two-element
  result.  This demonstrates body sensitivity and that the loop bridge does not
  match the mutant.

## Gate results

### Gate A — PASS

- A1: parsed `solution.mpy` and expanded proof program are KORE-identical.
  Program-defined execution is either run by fixed semantics or covered by an
  exact auxiliary execution theorem.  The body mutant is rejected.
- A2: both operational bridges have enumerated state footprints and
  bridge-free connection theorems with identical outputs and preserved cells.
- A3: the iterator theorem quantifies over every continuation.  The loop theorem
  pins the exact continuation, stack, bindings, control effects, and cleanup
  used by the bridge.  Fixed/extended witnesses agree.
- A4: definitional equations have disjoint or complementary cases, total
  declarations have complete coverage, recursion descends, and the map lemma is
  guarded by key absence.
- A5: the `(["abc"], "a")` witness is realizable under both CPython and MPY
  execution; the false postcondition and wrong-value probes are rejected.

### Gate B — PASS

- B1: `allStrings(INPUT)` plus `str(PREFIX)` matches the prompt's
  `List[str]` and `str` domain without a length bound.
- B2: MPY strings are integer code sequences and concrete string literals are
  ASCII-only.  The formal prefix property is structural over arbitrary
  `IntSeq`, so this representation difference does not change the proved
  filtering relationship.  Unsupported non-string behavior is excluded.
- B3: `filterPrefixAcc` is a formally defined stable filter using the exact
  fixed-semantics `startsWith` predicate; its human-facing meaning is not an
  opaque assumption.
- B4: the implementation matches both prompt examples, retains order and
  duplicates, and handles the empty prefix correctly.  The extra initialization
  of the loop variable has no observable result effect.

### Gate C — PASS

- Every proof-local definition, lemma, bridge, supporting theorem, dependency,
  mutation, command, and output artifact is listed above and exists in the
  workspace.
- `python3 differential_test.py` used an independent slicing oracle over 4,392
  cases, including exhaustive short `a`/`b` words/lists, empty values,
  duplicates, Unicode examples, and extra prefixes.  Actual result:
  `mismatches: 0`.
- Concrete LLVM assertions and all mutation results are reproducible from
  `prove.sh`.  Finite tests are reported only as evidence; universal bridge
  equivalence comes from the connection claims.

## Trust boundary

Trusted components are the user-supplied MPY semantics as the Python model, the
fixed `py2mpy.py` translator, K's compiler/parser, Haskell prover, LLVM backend,
SMT/built-in integer/Boolean/map theories, and the host tools used by
`prove.sh`.  The KORE identity comparison checks that the theorem uses the
translator's exact output; it does not independently re-prove the translator or
the supplied semantics against CPython.

There is no additional opaque proof-local primitive.  The two operational
bridges are not merely trusted: each has a universal connection theorem over
its complete match domain.

## Empirical evidence and excluded behavior

Empirically supported facts are the three LLVM concrete assertions and 4,392
CPython differential cases.  They supplement but do not replace the universal K
claims.

Excluded behavior includes inputs outside `List[str]` and `str`, Python
features absent from the supplied MPY subset, resource exhaustion, concurrency,
and a separate total-correctness/termination theorem.  The theorem is about the
supplied semantics and its integer-code-sequence string model, not all of
CPython.

The runner outcome is `KPROVE_PASSED` because every required positive target and
connection proof printed `#Top` and exited 0.  This execution marker is separate
from the `VALIDATED` proof-quality headline above.
