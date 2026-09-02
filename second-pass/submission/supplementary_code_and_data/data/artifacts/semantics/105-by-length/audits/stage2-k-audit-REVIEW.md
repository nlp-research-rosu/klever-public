# Independent adversarial audit: HumanEval 105 `by_length`

The candidate implementation is extensionally correct on the intended
integer-list domain, its submitted `.mpy` is faithfully regenerated, and its
positive K claim cleanly reconstructs to `#Top`. The proof is nevertheless not
legitimate. Both proof-local loop summaries are operational bridges over an
arbitrary continuation, and both erase the Python-visible assignment to the
loop target. A machine-checked integer-list witness shows the fixed semantics
returns `2` and rejects `99`, while the candidate's extended theory proves
`99` for both exact loop bodies. This is a concrete false conclusion on the
intended input domain, not merely a missing explanation.

## 1. Input and provenance integrity

The rendered mode and mounted inputs are consistent:

- `/audit-input.json` declares `record_layout =
  legacy-selected-stage1`, condition `semantics`, and
  `semantics_mode = SUPPLIED_SEMANTICS`.
- `/reference/reference-semantics` exists as required. No generated-semantics
  route was used.
- The `audit_campaign` object in `/audit-input.json` is exactly equal to
  `/audit-campaign-lock.json`; its recorded SHA-256 is also correct.
- All records required for `legacy-selected-stage1` are real regular files:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace. `usage.json` is
  present and was inspected. The absence of `runtime-metrics.json` is
  permitted for this legacy-selected layout.
- All launcher-recorded direct file hashes checked by the independent script
  match. The retained candidate's independently recomputed standard pipeline
  tree digest is
  `340050c1e3add221cc9b2e1d1d071e55db3af34a69e3ce46b418aeb423408022`,
  exactly the workspace digest in both the invocation and stage result.
- The trace tree contains one regular JSONL file with 198 records; every
  record parses. The trace's standard tree digest matches `usage.json`, and
  the trace file hash matches both generation manifests. Generation prose,
  logs, and traces were treated only as untrusted historical claims.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to the
  trusted prompt and translator.
- A recursive type/name/content comparison of
  `/candidate/reference-semantics` and
  `/reference/reference-semantics` found no missing, additional, changed,
  mistyped, or symlinked entry. Their independently recomputed standard
  semantics-tree digest is
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the launcher-recorded manifest digest.
- The five required proof artifacts are present as real regular files.

The reproducible check and all hashes are in
[provenance_check.py](/audit-output/evidence/provenance_check.py) and
[01-provenance.log](/audit-output/evidence/01-provenance.log:18). It ended
`PROVENANCE_INTEGRITY_OK` at line 33. This audit found no infrastructure breach,
so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For every finite list of integers, retain precisely the elements from `1`
through `9` inclusive, preserving duplicates; sort those retained digits and
reverse the sorted order (equivalently, sort descending); then replace each
digit with `"One"` through `"Nine"`. Ignore all other integers. The empty input
returns an empty list.

The trusted canonical implementation sorts the whole integer input descending
and performs dictionary lookup under `try/except`; the submitted implementation
first filters `1 <= value <= 9`, then sorts descending and indexes a nine-name
table. These algorithms agree for every input in the stated integer-list
domain. The proof domain excludes non-integers; that is aligned with the prompt
and is not a material narrowing.

### Trusted translation

In clean scratch space, the exact command

```text
cd /tmp/audit-work/105-by-length/recon && python3 py2mpy.py solution.py > regenerated-solution.mpy
```

exited zero. `cmp -s regenerated-solution.mpy solution.mpy` exited zero. Both
files have SHA-256
`09a6bdd52e92d8f5740c0ed5e724754e39a82967171d9e719f0b13a441e7c742`.
See [02-fidelity.log](/audit-output/evidence/02-fidelity.log:1).

### Independent differential test

[differential_check.py](/audit-output/evidence/differential_check.py) imports
the trusted canonical entry point and the submitted entry point separately and
also compares both to a direct contract oracle. Its deterministic scope was:

- all three documented examples;
- explicit empty, singleton, duplicate, already ordered, reverse ordered,
  filter-boundary `0/1/9/10`, and very large integer cases;
- every list of length 0 through 5 over
  `[-2, 0, 1, 2, 8, 9, 10]`;
- 2,000 generated lists, seed `1052026`, lengths 0 through 100, ordinary values
  from `-50` through `50`, with periodic `±10**100`.

The generator itself is the preserved exact input specification. It exercised
21,621 cases, whose canonical compact-JSON digest is
`f6664d5a5d95fc083873850fcdb4100f33bb8ab29d8824f4076e736f688e0141`.
There were zero mismatches and exit status zero
([02-fidelity.log](/audit-output/evidence/02-fidelity.log:13)). This is finite
behavioral evidence, not a replacement for the K proof.

## 3. Clean proof reconstruction

No candidate-provided compiled definition or cache was copied. The scratch
directory began with no `runtime-kompiled` or `verification-kompiled`
([03-reconstruction.log](/audit-output/evidence/03-reconstruction.log:1)).
K 7.1.293 and Python 3.10.12 were used.

The exact fresh build/run sequence was:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 /audit-output/evidence/make_k_concrete_tests.py
krun audit-concrete.mpy --definition runtime-kompiled --output none
kompile verification.k --backend haskell \
  --main-module BY-LENGTH-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled \
  --spec-module BY-LENGTH-SPEC
```

The LLVM definition built with exit zero, and seven reviewer-authored K
assertions covering normal, empty, boundary, duplicate, negative, and large
integer inputs ran with exit zero. The exact generated assertion program is
[audit-concrete.mpy](/audit-output/evidence/audit-concrete.mpy).

The Haskell proof definition also built with exit zero. `spec.k` contains one
positive target claim; running the complete spec printed literal `#Top` and
exited zero. The output and per-command statuses are preserved in
[03-reconstruction.log](/audit-output/evidence/03-reconstruction.log:67),
with the positive `#Top` at line 105.

Thus the candidate's positive proof-execution claim is reproducible. This
establishes verification under the supplied plus proof-local theory; it does
not establish that the proof-local theory is sound.

## 4. Adequacy and real-program pinning

### Formal claim in plain language

The sole entry claim has no side condition beyond the sort of `IS:IntSeq`.
Consequently, it ranges over every finite mathematical integer sequence,
embedded as an unboxed Python list by `intVals`. It starts from the standard
empty module state with builtins at scope `-1`, no heap objects, no call stack,
no return, no exception, and exit code zero.

It calls a closure with parameter `arr` and then observes the returned heap
list. The required result is

```text
tableNames(revVS(sortVS(filterDigits(intVals(IS)))))
```

That is: filter to digits, use the supplied ascending-sort primitive, reverse
the sequence, and map each digit through the nine-name table. The claim leaves
the final heap and heap counter existentially unconstrained, which is
appropriate for a result-only contract, but the observed returned list itself
is exact rather than a free variable or implication.

A satisfying state is immediate: `IS = .IntSeq` with the literal initial cells
in the claim. The postcondition then denotes `[]`, and both Python
implementations return `[]`. For `IS = iCons(9, iCons(1, .IntSeq))`, it denotes
`["Nine", "One"]`, again matching both Python implementations. The documented
example and other ground substitutions were also executed as reviewer K
assertions in Stage 3.

### Constructor-level program identity

The entry claim does not load the complete `Module` term. Instead,
`byLengthClosure` denotes a closure over `byLengthBody`. This is an acceptable
pinning shape only if that body is mechanically the submitted function body.

[make_program_pinning_spec.py](/audit-output/evidence/make_program_pinning_spec.py)
extracts the third constructor argument of the `by_length` `FuncDef` directly
from freshly regenerated `solution.mpy`. It makes only the two parser-required,
semantically inert empty-production normalizations:
`ListExpr()` to `ListExpr(.Exprs)`, and the omitted `If` else-list to
`.Stmts`. It then emits reachability equalities for both `byLengthBody` and
`byLengthClosure`; the exact generated artifact is
[program-pinning-spec.k](/audit-output/evidence/program-pinning-spec.k).
Both claims normalized identically, printed `#Top`, and exited zero
([05c-program-pinning.log](/audit-output/evidence/05c-program-pinning.log:4)).

The first audit attempt used bare functional claims, which this Haskell backend
does not support; that backend diagnostic is preserved in the earlier logs and
was not treated as a candidate defect. The successful configured reachability
claims are the mechanical comparison.

### Body sensitivity

The actual executed `byLengthBody` term was changed so its first loop appends
`value + 1`, while the separate proof-local bridge pattern was deliberately
left unchanged. The exact mutated definition is
[body-mutated-verification.k](/audit-output/evidence/body-mutated-verification.k),
generated by
[make_body_mutation.py](/audit-output/evidence/make_body_mutation.py).
It built successfully. On input `[2]`, the stale original obligation
`["Two"]` failed with `WarnStuckClaimState`; the residual actual result encodes
`["Three"]`
([05b-pinning-body-sensitivity.log](/audit-output/evidence/05b-pinning-body-sensitivity.log:70)).
This confirms the entry really is sensitive to the body term it executes.

The real-program pin is therefore adequate. The defect is instead in the rules
used to summarize two operations inside that pinned body.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[RULE-INVENTORY.md](/audit-output/evidence/RULE-INVENTORY.md) inventories every
top-level `configuration`, `syntax`, `context`, `rule`, and `claim` from all 24
supplied semantics files, `verification.k`, and `spec.k`, with source location,
attributes, exact text, and per-entry disposition. The machine-generated totals
are:

- 949 entries: 708 rules, 234 syntax declarations, 5 contexts, 1
  configuration, and 1 claim;
- 928 supplied-fixed entries, 20 proof-local entries, and the target claim;
- 154 function declarations, 116 `total` declarations, 25 opaque
  `no-evaluators` symbols, 54 priority-bearing entries, 55 concrete entries,
  30 `owise` entries, and 4 macros;
- zero `functional`, `simplification`, or `anywhere` entries.

See [06b-rule-inventory.log](/audit-output/evidence/06b-rule-inventory.log:3).
The supplied entries are the selected fixed semantics and are byte-identical to
the trusted tree. Opaque fixed primitives remain explicit trust boundaries;
the inventory's “accepted fixed baseline” disposition does not claim that
those primitives were proved from CPython.

### Material construct map

| Submitted construct | Fixed declaration/execution path | Audit result |
|---|---|---|
| `Name`, statement sequence, literals | `syntax.k`; `core.k` load/sequence, lookup, literal rules | Correctly bound and ordered on the target path |
| list and string literals | `list.k` evaluation/allocation; `str.k` ASCII conversion | Correct for the nine ASCII names |
| assignment | `controls.k` current-scope update, plus heap allocation rules | Correct |
| function call/return | `call.k` closure frame rule; `functions.k` parameter binding, return, and pop | Actual body and binding are pinned |
| comparisons and `and` | `operators.k`, `int.k`, and short-circuit `bool.k` | Correct for integer inputs when actually executed |
| `append` | `call.k` method routing and `list.k` in-place heap write | Correct when actually executed |
| `sorted(..., reverse=True)` | `sort.k` allocation of `condRev(sortVS(...), true)` | `sortVS` is a supplied opaque trusted primitive in proof mode |
| subscript `names[value - 1]` | `subscript.k` dereference/indexing | Correct and in-bounds for real filtered digits, conditional on sort being a permutation |
| first and second `For` | `controls.k` iterator protocol and target binding | Preempted by the two rejected proof-local bridges |
| returned-list observation | proof-local `#observeList` reads the returned heap list | Sound post-execution observation |

Configuration cells, left-to-right argument evaluation, call frames, heap
allocation, method mutation, return unwinding, and the intended integer-only
guards were checked along this path. No generated helper semantics exists in
this supplied-semantics condition.

### Proof-local definitions other than the bridges

The 20 proof-local entries are fully listed as K-0929 through K-0948 in the
inventory:

- `byLengthBody` and `byLengthClosure` are truthful nullary definitional
  expansions, mechanically pinned in Stage 4.
- `intVals` is a terminating and exhaustive constructor embedding from
  `IntSeq`.
- The two guarded `filterDigits` equations are disjoint and mathematically
  correct for integer-headed sequences; their recursion descends.
  The `[total]` declaration is broader than these equations because `ValSeq`
  can contain non-integers. This is an evidence/totality limitation, not a
  false equation on the intended integer domain.
- `nameTable` is exactly the nine required strings.
- The `tableNames` equations correctly map an integer head through
  `valSeqAt(nameTable, I - 1)` and descend. Its `[total]` declaration is also
  broader than the supplied equations, and out-of-range indexing inherits the
  fixed semantics' explicitly underspecified total `valSeqAt`. Target uses are
  intended to contain only `1..9`.
- `#observeList` is a fresh proof observation. It runs after the call and reads
  rather than changes the returned heap list.
- There are no proof-local lemmas, auxiliary connection claims, simplification
  rules, or opaque symbols.

These truthful equations do not connect either source loop to the summary.
That connection is asserted only by the two ordinary rewrites below.

### Unsound operational bridge 1: filter loop

[verification.k](/candidate/verification.k:98) rewrites the exact first
`For` term directly to `.K` at priority 40 and replaces the `values` heap
object by `filterDigits(VS)`. Its complete match domain admits an arbitrary
continuation (`...`), arbitrary current-scope parent, arbitrary heap rest, and
every `VS:ValSeq` satisfying only that the current `values` binding names an
empty list.

Fixed execution additionally:

- iterates via `#iterNext`;
- assigns each yielded value to the name `value`;
- evaluates both guarded comparisons with Python short-circuit order;
- resolves and invokes the bound `values.append` method on accepted elements;
- preserves any exceptions/control effects from that work; and
- exposes the final loop-target binding to the following continuation.

The bridge writes the summarized list but performs none of the target binding,
evaluation, or control effects. No bridge-free universal connection theorem is
present, let alone one quantified over the bridge's arbitrary continuation and
state footprint.

The concrete false-conclusion witness uses the exact loop body with valid input
`[2]`, an initially empty `values`, an existing `value = 99`, and an immediate
`return value` continuation. Under the fixed semantics the loop binds
`value = 2`, so the function returns `2`. Under the bridge, the loop is deleted,
`value` remains `99`, and the function returns `99`.

### Unsound operational bridge 2: name-mapping loop

[verification.k](/candidate/verification.k:126) has the same defect. It
rewrites the exact second `For` directly to `.K`, replaces the empty `result`
list by `tableNames(VS)`, and admits an arbitrary continuation. It checks the
`names` table but does not perform the real loop-target assignments, name and
subscript evaluation, method calls, or their control/exception behavior.

The corresponding witness again uses valid input `[2]`, the exact nine-name
table, an empty result list, `value = 99`, and immediate `return value`. Fixed
execution appends `"Two"` and leaves `value = 2`; the bridge fabricates the
same list summary but leaves `value = 99`.

### Machine-checked false conclusions

The complete witness sources are
[bridge-witness-programs.k](/audit-output/evidence/bridge-witness-programs.k),
[bridge-witness-correct-spec.k](/audit-output/evidence/bridge-witness-correct-spec.k),
[bridge-witness-fixed-false-spec.k](/audit-output/evidence/bridge-witness-fixed-false-spec.k),
and
[bridge-witness-false-spec.k](/audit-output/evidence/bridge-witness-false-spec.k).
They were built in two fresh definitions:

1. A fixed-only definition proved both correct `=> 2` claims with `#Top`.
2. The fixed-only definition rejected the first `=> 99` claim with
   `WarnStuckClaimState`; its residual `<k>` is `2`.
3. A definition importing the candidate's two bridges proved both false
   `=> 99` claims with `#Top`.

All builds and checks exited as expected; see
[04-bridge-witnesses.log](/audit-output/evidence/04-bridge-witnesses.log:199)
and its summary at line 289. This directly satisfies the required unsoundness
witness standard on the intended integer-list domain. Exact source syntax and
correct summarized list values do not cure the lost control/state effect.
Priority only causes the bad bridges to preempt fixed execution; it is not a
justification.

## 6. Fresh non-vacuity test

The candidate did not supply a `spec-vacuity.k`; none was trusted.

The definitive reviewer mutation is
[spec-vacuity-ground.k](/audit-output/evidence/spec-vacuity-ground.k). It uses
the satisfiable original state with `IS = .IntSeq` (Python input `[]`) and
changes the required result from `[]` to `["Zero"]`.

The build-only command

```text
kprove spec-vacuity-ground.k --definition verification-kompiled \
  --spec-module BY-LENGTH-SPEC-VACUITY-GROUND --dry-run
```

exited zero. The actual proof command exited one with
`WarnStuckClaimState`; the residual `<k>` contains the real
`list(.ValSeq)`, which cannot unify with the false one-element destination.
The runner checked the build, nonzero proof status, warning, and empty-result
residual and exited zero
([07c-nonvacuity-ground.log](/audit-output/evidence/07c-nonvacuity-ground.log:1)).

An earlier universal version of the same wrong leading element exhausted the
backend with code 137 and no residual
([07-nonvacuity.log](/audit-output/evidence/07-nonvacuity.log)); per the audit
rules it is invalid evidence and is not counted as either non-vacuity or a
candidate defect. The successful ground witness is independent and
conclusive.

This gate shows that the entry postcondition constrains the result. It does not
show that the operational bridges used to derive that result are sound.

## 7. Proven versus assumed accounting

### What the reconstructed `#Top` actually establishes

Under the union of the supplied MPY theory and every rule in
`verification.k`, for every finite `IS:IntSeq`, the pinned `byLengthClosure`
can symbolically reach an observed list represented by
`tableNames(revVS(sortVS(filterDigits(intVals(IS)))))`, with the listed initial
cells and unconstrained final heap/allocation counter.

It is a partial-correctness statement in the selected semantics. Because the
extended theory contains the two machine-demonstrated false operational
bridges, this is not a sound reachability proof of the real generated program.

### Trust and assumption ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell/LLVM backends, and builtin integer/Boolean/map/string operations | All proof and execution | Ordinary toolchain trust; version independently observed |
| Supplied MPY configuration, evaluation, heap, call, iterator, list, and control rules | Binding, state, control, return | Fixed semantics selected by the benchmark; exact candidate copy verified |
| `sortVS` in `sort.k` (`function,total,symbol,no-evaluators`) | Final order and thus result | Supplied opaque trusted primitive. Proof mode is conditional/parametric in this named sort contract; seven fresh K executions and Python differential evidence are finite support, not a K proof of sorting |
| Fixed `valSeqAt` totalization outside in-bounds constructor cases | Name selected by each digit | Acceptable only on the intended `1..9` path, conditional on `sortVS` preserving the filtered digits |
| Translator and closure/body identity | Whether theorem concerns submitted code | Byte identity plus mechanically derived constructor claims; established |
| `intVals`, `filterDigits`, `nameTable`, `tableNames` equations | Formal input and postcondition summary | Equations are correct on reached integer/digit cases; broader `[total]` declarations documented as limitations |
| First-loop priority-40 bridge | Filtered list, loop binding, evaluation, control | Illegitimate. No connection theorem; fixed/extended witness proves a false `99` conclusion |
| Second-loop priority-40 bridge | Named result list, loop binding, subscript/call/control | Illegitimate. No connection theorem; fixed/extended witness proves a false `99` conclusion |
| Python differential test | Implementation/canonical/contract alignment for 21,621 cases | Reproducible finite evidence only |
| Fresh false postcondition and body mutation | Result discrimination and body sensitivity | Both produce expected stuck residuals; neither justifies the loop bridges |

The natural-language domain is not materially narrowed: `IntSeq` covers
arbitrary finite mathematical integer lists rather than finitely many sizes.
The returned value is genuinely constrained, and the program term is genuinely
pinned. Those positive facts rule out vacuity and substitution, but they do not
offset materially unsound proof rules.

Gate A (real-program soundness) fails. The proof-local bridge theory can prove
false behavior for exact source loops and valid integer input. Intent/domain
adequacy is otherwise aligned, and the evidence is reproducible; the supplied
opaque sort remains an explicit conditional trust boundary. Under the
benchmark decision rule, materially unsound semantics or proof rules require
`FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
