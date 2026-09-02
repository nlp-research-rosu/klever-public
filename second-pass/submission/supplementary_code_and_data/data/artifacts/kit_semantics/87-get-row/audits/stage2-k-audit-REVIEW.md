# Independent adversarial review: 87-get-row

## Executive conclusion

The candidate contains a legitimate, freshly reconstructible
partial-correctness proof of the submitted program over the full HumanEval
domain of finite ragged integer lists and an integer target. The proof executes
the exact trusted-regenerated constructor bodies, constrains the returned
reference and heap, uses sound loop summaries, and survives independent
body/bridge sensitivity checks. A fresh false-result mutation is rejected for
the expected reachable obligation.

The qualification is the supplied semantics' result-bearing
`sortKeyVS(ValSeq, Val)`: symbolic K deliberately treats keyed sorting as an
opaque total primitive. The theorem returns an exact nested `sortKeyVS` term,
and the primitive's documented stable-sort interpretation is supported by
concrete semantics and finite differential evidence, but it is not universally
proved in K. This is a fixed, explicitly named semantics boundary—not a
candidate-added oracle—so it warrants `CONCERNS / LEGIT`, not failure.

## 1. Input and provenance integrity

I read `/audit-input.json` first. It declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem `87-get-row`, and the mounted
paths used below.

All required pipeline-v3 records are present, readable, regular
non-symlinked files or real directories:

- `/audit-campaign-lock.json`, `/run.json`, `/task.json`, and
  `/generation-result.json`;
- `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt` under
  `/generation-evidence`;
- the structured trace under `/generation-evidence/codex-trace`.

The campaign-lock JSON is exactly equal to the `audit_campaign` block, and its
SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every recorded regular-file hash checked by
[stage1_integrity.py](evidence/stage1_integrity.py) matches, including the run,
task, result, invocation, generation records, canonical source, prompt, and
translator. The pipeline-v3 tree algorithm independently reproduces:

- candidate workspace:
  `a351438ad2d9db2d296a7f77e05f32af041e1ae28770a0ca5189edf8630b7f80`;
- each supplied-semantics tree:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- structured trace:
  `dfc5a9b14151119374d673b3498aeab13966d6663d76dbe0282ab70e483a580c`.

See [stage1-integrity.log](evidence/stage1-integrity.log) and
[stage1-pipeline-tree-hashes.log](evidence/stage1-pipeline-tree-hashes.log).
The independently parsed trace contains one JSONL file and 869 valid records;
its generation-time `#Top` and final `VALIDATED` claims were treated only as
untrusted history
([stage1-trace-summary.log](evidence/stage1-trace-summary.log)).

The supplied-semantics boundary is intact. `/reference/reference-semantics`
exists as required. Candidate and trusted trees have the same 25 entries, with
no link or unsupported entry and zero path/type/content mismatches.
`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
trusted mounts. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py` and `/reference/canonical.py`: for a finite ragged
list of integer rows and integer `x`, return every zero-based `(row,column)`
whose value equals `x`; rows are ascending, while matching columns within each
row are descending. Empty outer and inner lists are allowed.

`solution.py` scans rows and columns left-to-right, appends a coordinate when
`value in (x,)`, sorts stably by `-column`, then sorts stably by `row`. On the
documented integer domain, singleton-tuple membership is equality. Stable
composition gives the required order.

Using the trusted `/reference/py2mpy.py` in scratch regenerated
`solution.mpy` byte-for-byte. Both submitted and regenerated files have SHA-256
`d584e692a61d6df3ea680279dece15d672ccefb8b75b86ad64928a1a25a5d1f4`;
`cmp` exited 0
([stage2-regeneration.log](evidence/stage2-regeneration.log)).

The reviewer-authored
[stage2_differential.py](evidence/stage2_differential.py) independently imports
the trusted canonical and generated entry points and also uses a third direct
contract oracle. It checked:

- three documented examples;
- nine empty, singleton, equality/inequality, repeated-match, ragged,
  negative, large-integer, and sort-order boundaries;
- 6,564 exhaustive small cases;
- 5,000 seeded matrices with up to eight rows and nine columns.

All 11,576 cases matched
([stage2-differential.log](evidence/stage2-differential.log)). I also replayed
the candidate's broader 196,923 exhaustive plus 2,000 seeded test suite with
zero mismatches
([stage7-candidate-differential-replay.log](evidence/stage7-candidate-differential-replay.log)).
These are finite fidelity evidence, not a replacement for the K proof.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/src`; no candidate
`*-kompiled` directory or cache was copied or used. The live tools are K
v7.1.293 (`kompile`, `kprove`, and `krun`).

Fresh concrete build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0. The reviewer smoke program covers empty, singleton, mismatch,
multiple matches, and multi-row ordering. Fresh `krun` reached `<k> .K </k>`,
`NoExc`, and exit code 0
([stage3-kompile-llvm.log](evidence/stage3-kompile-llvm.log),
[stage3-krun.log](evidence/stage3-krun.log)).

Fresh bridge-free connection build and proof:

```text
kompile --backend haskell shape-connection.k \
  --main-module SHAPE-CONNECTION --syntax-module ROW-MODEL-SYNTAX \
  --output-definition audit-shape-connection-kompiled
kprove shape-connection-spec.k \
  --definition audit-shape-connection-kompiled \
  --spec-module SHAPE-CONNECTION-SPEC
```

Both exit 0; proof output is `#Top`
([stage3-kompile-shape.log](evidence/stage3-kompile-shape.log),
[stage3-kprove-shape.log](evidence/stage3-kprove-shape.log)).

Fresh task build and proof:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module VERIFICATION-SYNTAX \
  --output-definition audit-verification-kompiled
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

Both exit 0; the five-claim spec prints `#Top`
([stage3-kompile-verification.log](evidence/stage3-kompile-verification.log),
[stage3-kprove-spec.log](evidence/stage3-kprove-spec.log)). The dependency-closed
`inner-loop,outer-loop` selection and each key claim also print `#Top`
([stage3-kprove-inner-outer.log](evidence/stage3-kprove-inner-outer.log),
[stage3-kprove-column-key.log](evidence/stage3-kprove-column-key.log),
[stage3-kprove-row-key.log](evidence/stage3-kprove-row-key.log)).

One diagnostic selection of `outer-loop` alone deliberately omitted its
`inner-loop` circularity and was interrupted after it made no progress; it is
not a positive target command. The correct dependency-closed and complete-spec
runs above pass. Likewise, attempts to evaluate a bare non-configuration K term
hit the backend's top-cell restriction, and a bare functional claim hit the
backend's documented unsupported form; the replacement `<k>` reachability
claim closes with `#Top`
([stage4-ground-rows-proof-cell.log](evidence/stage4-ground-rows-proof-cell.log)).
None of these diagnostics affects clean target reconstruction.

## 4. Adequacy and real-program pinning

### Plain-language claims

- `for-list-shape`: under the explicit list-shape equality, fixed `For(T,V,B)`
  takes exactly the proposed `#loop(list(rowContents(V)),T,B)` step, for an
  arbitrary continuation and framed state.
- `inner-loop`: iterating a row visits every value, advances the column once
  per element, and appends exactly `(row,column)` for equality with `x`.
- `outer-loop`: iterating all list-shaped rows composes the inner summary,
  advances the row once per row, and updates the coordinate list to
  `rowsAppend`.
- `column-key`: the submitted `_column_desc((RI,CI))` returns `0 -Int CI`.
- `row-key`: the submitted `_row_asc((RI,CI))` returns `RI`.
- `get-row`: from an empty heap and the exact three function bindings, calling
  `get_row(list(RS),X)` returns `ref(2)`, allocates exactly the scan list and
  two keyed-sort lists at 0, 1, and 2, advances `heapLoc` to 3, restores call
  control, and leaves exception/exit normal, provided `listRows(RS)`.

The entry precondition has no size bound. `listRows` accepts every finite
nested list; requiring `X:Int` matches the source target domain. Ground models
for every claim are recorded in
[stage4-precondition-witnesses.md](evidence/stage4-precondition-witnesses.md).

### Program identity

Trusted regeneration plus `kast --expand-macros` was followed by a structural
JSON KAST comparison. The expanded `GETROWBODY` is exactly the regenerated
`get_row` body. Each key closure's parameters and body are exactly its
submitted `FuncDef`, including environment 0. The three body hashes and exact
matches are in
[stage4-constructor-pinning.log](evidence/stage4-constructor-pinning.log);
the checking code is
[stage4_constructor_pinning.py](evidence/stage4_constructor_pinning.py).
Thus beginning the claim at an exact closure call is a constructor-level,
semantically inert normalization of module loading, not a substituted program.

The result is not free or tautological: the claim fixes returned `ref(2)`,
every result-bearing heap object, allocation count, control state, and normal
exit. A ground witness `[[2,1,2],[2],[1,2,1,2]], x=2` satisfies `listRows`;
both Python implementations return
`[(0,2),(0,0),(1,0),(2,3),(2,1)]`
([stage4-concrete-witness.log](evidence/stage4-concrete-witness.log)).

A material body mutation removes the append from the closure term actually
bound to `get_row`. Fresh reconstruction executes that mutated body, obtains
an empty scan result, and exits 1 with `WarnStuckClaimState` against the
required nonempty heap
([stage4-body-mutation-proof.log](evidence/stage4-body-mutation-proof.log)).

## 5. Rule-by-rule static soundness review

[stage5-rule-inventory-v2.tsv](evidence/stage5-rule-inventory-v2.tsv) is the
exhaustive 956-entry source inventory: 695 supplied and 17 local semantic
rules, 227 supplied and six local syntax blocks, five contexts, one
configuration, and five claims. It records each normalized item, source span,
attributes, origin, relevance, and review class. All `total`, `priority`,
`simplification`, `concrete`, `owise`, `symbol`, and `no-evaluators`
declarations are separately enumerated in
[stage5-special-attributes.log](evidence/stage5-special-attributes.log).

The detailed used-rule map and local rule-by-rule decisions are in
[stage5-static-review.md](evidence/stage5-static-review.md). Principal findings:

- `rowContents` and `listRows` have disjoint, exhaustive, descending equations.
- `advanceIndex` is total and structurally descending.
- `scanAppend` is total; its cons rules use complementary equality guards,
  both advance the column, and only the true branch appends the exact tuple.
- `rowsAppend` is intentionally partial; every use is protected by
  `listRows`, its empty/list-cons cases cover that domain, and recursion
  descends.
- All five macros are constructor aliases. They were mechanically matched to
  submitted bodies and add no runtime oracle.
- The only operational bridge is `verification.k:21-24`. Its guard equates
  `V` with `list(rowContents(V))`, making its RHS exactly fixed
  `controls.k:69`. Its bridge-free universal claim has the identical match
  domain, arbitrary continuation, and framed cells. Priority 40 only preempts
  an equivalent step.
- Binding, left-to-right evaluation, iteration, append mutation, integer
  increments, key calls, allocation, return, and exceptional/control state all
  follow fixed rules mapped in the detailed review.
- A bridge-free context witness iterates one element, records `"v" |-> 7`,
  then preserves/evaluates an immediate `Int(9)` suffix to 9; it prints `#Top`
  ([stage5-shape-context-proof.log](evidence/stage5-shape-context-proof.log)).
  A false bridge destination that drops the element reaches the real bind/body
  continuation and fails
  ([stage5-shape-bridge-negative.log](evidence/stage5-shape-bridge-negative.log)).

No candidate-local rule is unsound, so no false-conclusion witness is asserted
against one.

The fixed supplied tree contains several documented opaque primitives. Only
`sortKeyVS` affects this theorem. Symbolic proof does not unfold it; concrete
`MPY-CONCRETE` evaluates real key calls and stable integer insertion. All other
opaque symbols are outside this program's dependency graph.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh reviewer artifact is
[audit-false-result-spec.k](evidence/audit-false-result-spec.k). On
`[[5,5]], x=5`, the raw scan at `ref(0)` is
`[(0,0),(0,1)]`, but both Python implementations return the required
column-descending `[(0,1),(0,0)]`. The mutation changes the claimed return from
the real second-sort reference to raw `ref(0)`; the witness is demonstrably
false
([stage6-false-witness.log](evidence/stage6-false-witness.log)).

The mutated spec successfully parses/builds with `kprove --dry-run` (exit 0)
before execution
([stage6-mutation-build.log](evidence/stage6-mutation-build.log)). Actual:

```text
kprove audit-false-result-spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT-SPEC
```

It exits 1 with `WarnStuckClaimState`. The residual has `<k> ref(2) ~> .K </k>`
and the expected three heap objects, so failure is precisely the unmet
`ref(0)` result—not parsing, timeout, an unreachable mutation, or an unrelated
crash
([stage6-mutation-proof.log](evidence/stage6-mutation-proof.log)).

## 7. Proven versus assumed accounting

### Formally established

Under the freshly built supplied MPY theory, for every finite `RS:ValSeq` whose
heads are list values and every `X:Int`, if the exact submitted `get_row`
closure call terminates, it:

1. scans every row/column and builds exactly `rowsAppend(.ValSeq,RS,X,0)`;
2. allocates the fixed first keyed-sort term using the exact column-key
   closure;
3. allocates the fixed second keyed-sort term using the exact row-key closure;
4. returns that second allocation at `ref(2)`;
5. restores frame/control state and terminates without modeled exception.

The two key closures' integer results, both loop summaries, allocation effects,
and exact `For` connection are separately proved. The theorem covers the
source-contract domain without fixed sizes, examples, or bounded unrolling.

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler, Haskell prover, LLVM runtime | All machine results | Ordinary unavoidable toolchain trust; versions and fresh commands recorded. |
| Trusted translator `/reference/py2mpy.py` | Python-to-constructor identity | Accepted mounted input; byte regeneration and KAST body comparison independently check this instance. |
| Supplied MPY semantics | Binding, evaluation, heap, control, calls, iteration, sorting interface | Selected fixed semantics boundary; recursively byte-verified. Used rules were statically traced. It models a documented Python subset, not all CPython. |
| `sortKeyVS(ValSeq,Val)` in fixed `sort.k` | Entire final list ordering | Result-bearing opaque trusted primitive. The formal theorem is interpretation-parametric and returns the raw term; stable keyed-sort meaning is conditional on its named fixed contract. Concrete K plus 210,499 replayed/independent Python cases show zero mismatch, but finite evidence is not universal proof. This is the reason for `CONCERNS`. |
| Fixed `MPY-CONCRETE` keyed sorter | LLVM evidence only; absent from Haskell proof | Reviewed stable for this program's integer keys and exercised on boundaries. It supports but does not define symbolic `sortKeyVS`. |
| Prompt/canonical intent bridge | Human-facing coordinate property | Trusted sources plus independent oracle/differential evidence. Scan is formally proved; final ordering still inherits the named `sortKeyVS` contract. |
| Termination | Reachability theorem scope | Not proved or claimed; acceptable for requested partial correctness. Inputs are finite algebraic lists. |

No candidate-added opaque result, empirical rewrite, assumed helper body, or
task-answer rule contributes to closure. The fixed semantics comments mention
external sort notes/Lean evidence, but those were not mounted as trusted inputs
and were not credited here.

### Decision

This is not `FAIL`: every positive claim reconstructs; the real program body is
pinned; the domain is unrestricted over the source contract; poststate and
result are discriminating; and local extensions are sound. It is not an
unqualified `PASS` because the universal human-facing sorting interpretation
is outside the K theorem and rests on the fixed opaque `sortKeyVS` contract,
with only finite executable evidence in this audit. That is a non-fatal,
explicit trust-boundary limitation, so the proof remains legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
