VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every finite modeled string whose code
sequence contains only ASCII lowercase letters (`97`–`122`) and ASCII spaces
(`32`), loading `solution.mpy`'s exact `histogram` function body and calling it
returns `histogramResult(CS)`.

`histogramResult(CS)` is a dictionary whose keys are exactly the distinct
non-space letters attaining the greatest occurrence count in `CS`, and whose
value at each key is that count. The empty or all-space input returns the empty
dictionary. Dictionary key order is first-occurrence order, although the prompt
does not observe order.

This is a K reachability proof of partial correctness. It does not separately
claim termination.

## Formal claim

`SPEC.histogram` starts from the complete initial MPY configuration and:

1. executes `#loadAll(Module(FuncDef(...)))` with the exact translated function
   body;
2. resolves `Name("histogram")` from the module scope;
3. calls it on `str(CS)`;
4. executes both outer loops, both inner counting loops, dictionary updates,
   return, and call-frame cleanup under the fixed semantics; and
5. reaches `histogramResult(CS)`.

Its precondition is `validHistogramInput(CS)`. The final configuration restores
the module environment, empty stack, `noRet`, `NoExc`, exit code `0`, empty
heap, and heap location `0`. The module scope contains the loaded closure.

The four loop claims establish:

- `SPEC.first-count-loop`: the first inner loop changes `count` from `N` to
  `countHistogramCode(REM, TARGET, N)`.
- `SPEC.second-count-loop`: the identical second-pass inner loop has the same
  count result while preserving its current dictionary.
- `SPEC.first-loop`: the first outer loop changes `max_count` from `M` to
  `maxHistogramCount(REM, ORIG, M)`.
- `SPEC.second-loop`: the second outer loop changes
  `dictV(KS, VS)` to `buildHistogram(REM, ORIG, M, KS, VS)`.

## Proof-extension inventory

There are no trusted primitives, opaque values, operational bridge rules,
priority rules, or rules that intercept calls, loops, lookup, return, or
dictionary operations in `verification.k`.

### `validHistogramInput`

- Class: definitional summary (domain predicate).
- Semantic role: constrains the theorem domain; it does not replace execution.
- Domain: every `IntSeq`.
- Matched context / justification scope / containment: pure function arguments
  only; no configuration context.
- State footprint: none.
- Value influence: entry-claim applicability only.
- Value justification: exhaustive empty/cons equations; the cons equation
  accepts exactly code `32` or codes `97`–`122` and recurses on the tail.
- Dependents: `SPEC.histogram`.
- Validation: constructor coverage is complete, cases do not overlap, and
  recursion strictly decreases the first argument.

### `countHistogramCode`

- Class: definitional summary.
- Semantic role: names the accumulator result of either exact inner loop; it
  does not rewrite source computation.
- Domain: every `IntSeq`, target `Int`, and accumulator `Int`.
- Matched context / justification scope / containment: pure arguments only.
- State footprint: none.
- Value influence: inner-loop `count`, then maximum selection and dictionary
  values.
- Value justification: the empty equation returns the accumulator; the cons
  equation adds one exactly when the head code equals the target, then recurses
  on the tail.
- Dependents: both count-loop claims, `maxHistogramCount`, and
  `buildHistogram`.
- Validation: empty/cons coverage is total and disjoint; recursion strictly
  decreases the input sequence. LLVM tests and the independent Python oracle
  agree on all recorded cases.

### `maxHistogramCount`

- Class: definitional summary.
- Semantic role: names the result of the exact first outer loop.
- Domain: every remaining/original `IntSeq` pair and integer accumulator.
- Matched context / justification scope / containment: pure arguments only.
- State footprint: none.
- Value influence: the maximum used by the second loop.
- Value justification: empty/cons equations mirror the source's space test and
  strict-greater-than update using `countHistogramCode(ORIG, C, 0)`.
- Dependents: `SPEC.first-loop`, `histogramResult`.
- Validation: total empty/cons coverage, a total Boolean conditional, and
  strict structural descent.

### `buildHistogram`

- Class: definitional summary.
- Semantic role: names the result of the exact second outer loop.
- Domain: every remaining/original `IntSeq`, integer maximum, and two
  `ValSeq`s representing the current dictionary.
- Matched context / justification scope / containment: pure arguments only.
- State footprint: none.
- Value influence: the final result.
- Value justification: the empty equation returns `dictV(KS, VS)`; the cons
  equation skips spaces, and otherwise applies the supplied total `dPutK` and
  `dPutV` exactly when the letter's count equals the maximum.
- Dependents: `SPEC.second-loop`, `histogramResult`.
- Validation: total empty/cons coverage, strict structural descent, and no
  partial `dictSet` abstraction.

### `histogramResult`

- Class: definitional summary.
- Semantic role: composes the two exact folds; it does not replace execution.
- Domain: every `IntSeq`.
- Matched context / justification scope / containment: pure argument only.
- State footprint: none.
- Value influence: final postcondition.
- Value justification: its single equation starts the maximum fold at `0` and
  the dictionary fold at two empty sequences.
- Dependents: `SPEC.histogram` and the false-result mutation.
- Validation: unconditional and terminating through the two structural folds.

### Loop circularities

- Extensions: `SPEC.first-count-loop`, `SPEC.second-count-loop`,
  `SPEC.first-loop`, and `SPEC.second-loop`.
- Class: derived reachability lemmas (loop invariants).
- Semantic role: exact execution theorems for source loop heads; no
  fixed-semantics rule is replaced in `verification.k`.
- Domain: the variables and exact local-scope shapes stated in each claim,
  with `L` absent from the framed outer scope map.
- Matched context: exact `#loop` term, exact target and body, arbitrary trailing
  continuation via the `<k> ... </k>` frame, current environment `L`, exact
  relevant local bindings, framed outer scopes, and explicitly preserved
  `scopeLoc`, heap, heap location, stack, return, exception, and exit-code
  cells.
- Justification scope / containment: each claim proves the same framed context
  it accepts. Phase values `1` and `2` distinguish the two syntactically
  identical inner loops.
- State footprint: inner loops write only `candidate` and `count`; the first
  outer loop additionally writes `letter` and `max_count`; the second outer
  loop additionally writes `letter` and `result`. Temporary final locals are
  existential because they are unobserved. All other cells and relevant
  bindings are preserved.
- Value influence: inner summaries determine counts; outer summaries determine
  the maximum and returned dictionary.
- Value justification: the exhaustive equations above and fixed-semantics
  execution of every loop body.
- Dependents: the two outer claims depend on their phase-specific inner claim;
  `SPEC.histogram` depends on all four.
- Control validation: the exact loop bodies contain no `break`, `continue`,
  return, exception, allocation, or output. The claims consume only the loop
  prefix and preserve their arbitrary continuation.
- Value validation: no fresh opaque value occurs. All result-bearing values are
  fixed by total equations.
- Validation: both focused inner claims and the all-claims run printed `#Top`
  and exited `0`.

## Exact commands and actual outputs

The complete reproducible sequence is in `prove.sh`. Its final run exited `0`.

```bash
python3 py2mpy.py solution.py > solution.mpy
diff -u solution.mpy <(python3 py2mpy.py solution.py)
```

Output: none. Exit: `0`.

```bash
python3 concrete_tests.py
python3 differential_test.py
```

Output:

```text
cases: 21850
mismatches: 0
```

Both exited `0`.

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled
```

`kompile` exited `0` with warnings originating in the supplied semantics.
`krun` exited `0` with `.K`, `NoExc`, and `<exit-code> 0 </exit-code>`. The
five assertions are the five prompt examples.

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.first-count-loop
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.second-count-loop
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Actual positive proof outputs and exits:

```text
#Top  Exit: 0
#Top  Exit: 0
#Top  Exit: 0
```

The final command proves all five claims in `spec.k`.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1`, `WarnStuckClaimState`. For the ground input `"a"`, the
residual contains:

```text
dictV(vCons(str(iCons(97, .IntSeq)), .ValSeq), vCons(1, .ValSeq))
```

The deliberately false destination expected the same key with value `2`.

```bash
krun body_mutation_tests.mpy --definition runtime-kompiled
```

Actual result: exit `1`, `AssertionError`, and `<exit-code> 1 </exit-code>`.
The mutation changes the second-pass comparison from `==` to `!=`; the prompt
example `"b b b b a"` no longer returns `{"b": 4}`.

## Gate results

- Gate A — PASS. The exact program-defined body executes under fixed
  semantics. There are no operational bridges or opaque result-bearing
  abstractions. All total functions have exhaustive, disjoint constructor
  equations and strict descent. The ground `"a"` precondition is satisfiable,
  the false-result mutation is rejected, and the body mutation changes
  behavior.
- Gate B — PASS. The formal domain includes all strings described by the
  prompt under the supplied ASCII model: lowercase single-letter tokens and
  spaces, including the empty string. The theorem also defines harmless
  behavior for extra spacing and adjacent lowercase characters. The recursive
  summaries definitionally count occurrences, select the maximum, and retain
  all ties, matching the prompt examples and intended property.
- Gate C — PASS. Every proof extension and assumption is listed here; commands,
  artifacts, input scopes, oracles, outputs, and negative probes are
  reproducible. Formal, conditional, empirical, and excluded conclusions are
  separated below.

## Trust boundary

- The supplied read-only `reference-semantics/` definition is trusted as the
  intended model of the accepted Python subset. Every target claim depends on
  it for value, binding, control, state, and exception behavior.
- K v7.1.293, its Haskell prover/backend, LLVM backend, and SMT reasoning are
  trusted implementation components.
- The prompt's “lowercase letters” is interpreted as ASCII `a`–`z`, matching
  the supplied string semantics and examples.
- There are no proof-local trusted primitives and no unproved external value
  contracts.

## Empirically supported facts

- `concrete_tests.py` and `concrete_tests.mpy` check all five prompt examples.
  CPython and LLVM/`krun` both exit `0`.
- `differential_test.py` uses `collections.Counter` as an independent oracle;
  it does not reuse the K fold equations. It exhaustively checks every string
  of length `0` through `7` over `"abc "` (21,845 strings), then the five prompt
  examples. Output: `cases: 21850`, `mismatches: 0`.
- `body_mutation_tests.py` / `.mpy` provide the body-sensitivity witness and
  fail as expected after changing the second comparison.
- Finite tests support the semantic-model and intent checks; they are not used
  as a universal proof.

## Excluded behavior

- Inputs containing non-ASCII characters or characters other than lowercase
  ASCII letters and space are outside the formal precondition.
- The proof is about the supplied MPY semantics, not all of CPython.
- Termination, performance, resource bounds, and behavior under memory or
  backend failure are not claimed.
- Temporary locals (`letter`, `candidate`, `count`, and proof-distinguishing
  `phase`) are not part of the observable result.
