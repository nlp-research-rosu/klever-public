# Independent adversarial audit: HumanEval 68 `pluck`

The candidate contains a legitimate partial-correctness proof of the submitted
program over the full material source-contract domain. I reconstructed the
definitions from source, proved the target afresh, mechanically pinned the
claim body to the trusted translation, reviewed all local and supplied rules,
and rejected a fresh false result obligation. Candidate prose, prior compiled
definitions, traces, and prior `#Top` outputs were not used as proof authority.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `68-pluck`, and condition
`kit-semantics`. The infrastructure boundary is internally consistent:
`/reference/reference-semantics` exists as required.

I checked all pipeline-v3 records required by the prompt:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the one JSONL file under the structured trace tree.

All required paths are real regular files/directories. Parsing every structured
trace line produced 430 valid records. The campaign-lock JSON exactly equals
the `audit_campaign` block and its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
the value recorded in `audit-input.json`.

Independent file hashing matched the launcher records for the run/task/result
manifests, invocation and metric records, usage, generation prompt/log/last
message, canonical source, trusted prompt, and translator. The independently
recomputed pipeline-v3 candidate-tree digest is
`7468c92f7f709c726ce7ecde098338ae5c6f67513c719d40afe9df7229322dbc`,
matching `generation-result.json`; the trace-tree digest is
`1550290bda0a63be916371a9d80df108bcebcdf84d90749f94341808a55768ab`,
matching `usage.json`.

The candidate prompt and translator are byte-identical to the trusted mounted
copies. A recursive type/content comparison of candidate and trusted
`reference-semantics/` returned no difference; neither tree contains a symlink
or special entry. Their independently recomputed pipeline tree digest is
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
also the task-manifest semantics digest. There is no supplied-semantics
integrity failure and no audit-infrastructure breach.

Evidence: `evidence/provenance_check.py`, `evidence/01-provenance.log`.
Generation records were read and integrity-checked, but their assertions about
validation and prior proof results were treated only as untrusted claims.

## 2. Program fidelity and canonical comparison

The trusted contract says: for a list of non-negative integer nodes, return
`[smallest_even_value, first_index_of_that_value]`; return `[]` if the list is
empty or has no even value. The examples explicitly include the empty list.
The stated maximum length is 10,000.

`solution.py` implements a left-to-right scan. It starts with sentinel `-1`,
replaces the selection on the first even value or a strictly smaller even
value, preserves the prior index on ties, and returns the selected pair or
`[]`. This agrees with the canonical `filter`/`min`/`index` implementation.

Trusted regeneration:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

exited 0. Both MPY files have SHA-256
`082523bd6cbff0ee455c5d2fce9b039824d288bb15ca1547b1d9c8f66fc6a6a1`.
See `evidence/02-translate.log`.

The reviewer-authored differential script imported `/reference/canonical.py`
and the scratch copy of the generated implementation independently. It checked:

- all four documented examples;
- empty, singleton odd/zero/even, first-selection, smaller-replacement,
  equal-tie, and odd-preservation branch boundaries;
- very large non-negative Python integers;
- four length-10,000 boundaries;
- all 137,257 lists over values 0 through 6 and lengths 0 through 6;
- 2,000 deterministic random lists of lengths 0 through 300 with values up to
  \(10^{12}\).

All 139,273 cases matched both the natural-language oracle and canonical
implementation. This is finite fidelity evidence, not a substitute for the K
proof. Evidence: `evidence/differential_test.py`,
`evidence/03-differential.log`.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/68-pluck`; no
candidate-provided kompiled directory or cache was copied or referenced.
K version 7.1.293 was available.

The clean proof definition was built with:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0 (`evidence/04-kompile-proof.log`).

The loop circularity was then independently selected:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.pluck-loop
```

It printed `#Top` and exited 0 (`evidence/05-kprove-loop.log`).

The unmodified complete target proof was:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC
```

It printed `#Top` and exited 0 (`evidence/07-kprove-all.log`). This invocation
contains both `pluck-loop` as the needed circularity and `pluck-entry` as the
entry theorem, so every positive claim is included.

A diagnostic attempt selecting only `pluck-entry` was interrupted while
actively unrolling after more than 13 minutes: that selector also removes
`pluck-loop` from the selected circularity set and is not the candidate's
proof. It is neither a positive nor negative datum; the exact explanation and
partial log are preserved in `evidence/06-entry-selector-diagnostic.md` and
`evidence/06-kprove-entry.log`.

For independent concrete reconstruction, I also built a new LLVM
`MPY-KRUN` definition and ran six normal/boundary assertions. The final state
had `.K`, `NoExc`, empty stack, and exit code 0. See
`evidence/14-translate-runtime-witness.log`,
`evidence/15-kompile-runtime.log`, and
`evidence/16-krun-runtime-witness.log`.

## 4. Adequacy and real-program pinning

### Claims in plain language

`pluck-loop` applies at a nonempty list-loop head. Its precondition says the
current index is non-negative and every remaining element, including the
current head, is a non-negative integer. It executes the exact loop body and
states that:

- `smallest` becomes the recursive `scanBest` fold;
- `smallest_index` becomes the corresponding `scanBestIndex` fold;
- `index` advances once per remaining element;
- `value` may be whatever the last iteration bound/assigned;
- the loop disappears while the trailing continuation and unmentioned cells
  remain framed.

`pluck-entry` starts from the standard module/builtin scopes, empty heap and
stack, and a call to the closure bound as `"pluck"`. Its precondition
`allNonNegative(INPUT)` covers every finite `ValSeq` made solely of
non-negative K integers. Its destination requires normal call completion,
return reference 0, heap location 0 containing
`resultList(scanBest(...), scanBestIndex(...))`, heap counter 1, no pending
return/exception, empty stack, and exit code 0.

### Mechanical program pinning

The trusted translation is a `Module(FuncDef("pluck", Params("arr"), BODY))`.
The entry claim starts after the semantically inert module-load step by fixing
the module binding to `closureVal("arr", BODY, 0)`. I mechanically extracted
that closure body from `spec.k`, reconstructed the corresponding module
program, and parsed both it and `solution.mpy` with the fresh definition.
After normalizing only the concrete/internal spellings of empty K lists, the
two parsed KORE terms were byte-identical, both with SHA-256
`2300c9d0b2a64c57bd4d09fb91c03547a6053d85195fb70f49191f9eabb1de2f`.
See `evidence/pinning_extract.py`, `evidence/09-pinning-extract.log`, and
`evidence/12-constructor-compare.log`.

Fresh LLVM module loading independently produced that same closure binding.
Thus the claim does not prove a substituted algorithm: it pins the exact
trusted translation's name, parameter, definition scope, constructor body,
call path, and return path.

### Satisfiability and concrete substitutions

The entry precondition is satisfiable; examples include `.ValSeq`, `[0]`,
`[1,3]`, `[4,2,3]`, and `[2,2]`. I substituted these values into the claimed
recursive result. All five ground summary claims printed `#Top` and exited 0:

```text
[]        -> []
[0]       -> [0,0]
[1,3]     -> []
[4,2,3]   -> [2,1]
[2,2]     -> [2,0]
```

These values also match both Python implementations in the independent
differential run. Evidence: `spec-ground-summaries.k` in scratch and
`evidence/13-ground-summary-proof.log`.

The result is not free or implied only one way: the returned reference and
exact heap payload are constrained functions of `INPUT`. The recursive
definitions embody the minimum-even/first-index property: strict replacement
selects the first even and only a later strictly smaller even; structural
induction over the finite sequence gives the stated contract.

## 5. Rule-by-rule static soundness review

The source-ordered exhaustive inventory is
`evidence/k-rule-inventory.md`; its generator and command record are
`evidence/k_inventory.py` and `evidence/08-inventory.log`. It enumerates all 26
K source files, 237 syntax declarations, 717 rules (238 operational and 479
pure/equational), 45 priority rules, 155 function-syntax declarations, 117
`total` declarations, 23 opaque/no-evaluator declarations, six proof-local
simplification rules, and both claims. There are no `functional`
declarations.

The detailed constructor map, per-file disposition, proof-local rule table,
evaluation-order analysis, state footprint, overlap analysis, and claim review
are in `evidence/static-review-matrix.md`.

The material findings are:

- The submitted term uses only module/function loading, plain closure calls,
  local assignment, integer operations/comparisons, list iteration, `If`,
  `Return`, and list allocation. Fixed rules preserve left-to-right evaluation,
  scope/stack lifecycle, allocation, exceptions, and abrupt return.
- None of the 23 fixed opaque symbols (float, sort, MD5, and related
  primitives) is reachable from this integer/list program. `MPY-CONCRETE` is
  not imported into the proof module.
- All fixed priority alternatives are either the faithful special case or
  pattern/guard-disjoint from the reachable plain integer/list state. There is
  no proof-local priority or operational rule.
- `verification.k` contains 22 pure equations and ten syntax declarations.
  `allNonNegative`, `shouldTake`, `nextBest`, `nextBestIndex`, `scanBest`,
  `scanBestIndex`, `afterIndex`, and `resultList` have exhaustive constructors
  or complementary/disjoint guards and structurally decreasing recursion.
- `projectIntTotal` is opaque only outside the integer sort. Every target use is
  guarded by `isInt` through `allNonNegative`/the loop precondition. Its
  guarded cast laws fix its accepted-domain value.
- The guarded `applyBin("+", Val, Int)` simplifier is a pure derived lemma, not
  a `<k>` operational bridge. On its complete guard, `Val` denotes an `Int`,
  and its RHS agrees with the fixed typed integer-addition rule.

I compiled a separate proof definition that omitted the candidate's
`applyBin` simplifier. In it, universal typed and explicit guarded-cast
connection claims, the projection identity, and a ground projection claim all
printed `#Top` and exited 0
(`evidence/17-kompile-projection-base.log`,
`evidence/19-projection-typed-connection-proof.log`). A first diagnostic
formulation left the downcast implicit and stayed stuck because fixed K could
not refine a dynamic `Val` solely from `isInt`; that narrower evidence gap is
preserved in `evidence/18-projection-connection-proof.log` and is discharged
by the explicit casted theorem. It is not a false-rule witness.

Opposite ground interpretations `projectIntTotal(7) = 8` and
`applyBin("+",7,0) = 8` both built and were rejected with the actual residual
value 7 (`evidence/20-projection-wrong-dry-run.log`,
`evidence/21-projection-wrong-proof.log`,
`evidence/25-wrong-addition-proof.log`).

No inventoried proof-local rule admits a false conclusion on the intended
domain. In particular there is no answer-encoding operational rewrite,
unconstrained result oracle, call/loop/return bypass, fabricated state, or
exception/control mismatch.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh reviewer mutation
`/tmp/audit-work/68-pluck/spec-audit-false-value.k` executes the exact real
body on satisfying input `[4,2,3]` but changes the result value obligation from
the true `[2,1]` to the false `[4,1]`.

Its dry run:

```text
kprove spec-audit-false-value.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-AUDIT-FALSE-VALUE --dry-run
```

exited 0, establishing successful parsing/build
(`evidence/23-fresh-false-value-dry-run.log`). The real proof command exited 1
with `WarnStuckClaimState`. Its residual was a normally completed call with
heap `0 |-> list(vCons(2,vCons(1,.ValSeq)))`, exactly the true `[2,1]`, which
could not unify with mutated `[4,1]`
(`evidence/24-fresh-false-value-proof.log`). This is the expected unmet
result obligation, not a parser error, crash, timeout, or unreachable mutation.

As separate body-sensitivity evidence, I reran the inspected opposite-comparison
body under the fresh definition. It exited 1 with a normally completed residual
heap `[4,0]`, not the original `[2,1]`
(`evidence/22-candidate-body-mutation-clean.log`). The changed constructor was
inside the closure actually executed by that claim.

## 7. Proven versus assumed accounting

The successful reachability proof establishes:

> For every finite algebraic list whose elements are non-negative K integers,
> if the exact submitted `pluck` call terminates under the supplied MPY
> semantics from the stated standard initial state, it completes normally and
> returns `[]` iff no even value is present; otherwise it returns the smallest
> even value and the least index at which that value occurs.

The theorem is unbounded in symbolic list length. It therefore covers the
prompt's empty case and all lengths through 10,000 (and proves the same property
for larger finite lists). It does not materially narrow the HumanEval domain.

Trust/assumption ledger:

- **Supplied MPY semantics and K builtin theories.** Trusted at the benchmark's
  supplied-semantics boundary, after exact tree-integrity verification. The
  rule review additionally checked every material path and established that
  unused opaque primitives cannot influence this theorem.
- **K 7.1.293 compiler, Haskell prover, LLVM executor, and reachability-logic
  implementation.** Ordinary machine-checking trust. All definitions used for
  audit results were freshly built.
- **Trusted `py2mpy.py` as the Python-to-MPY bridge.** The submitted MPY is its
  byte-identical output. Translator correctness for these AST constructors is
  an external front-end assumption, supported by direct source inspection,
  parsed-term pinning, concrete MPY execution, and Python differential tests.
- **Guarded K sort projection laws.** These affect the result but are fixed on
  every accepted input by `isInt`, the partial downcast, the static-Int
  collapse, and the bridge-free typed/casted connection proof. The opaque
  non-integer interpretation is outside the entry precondition.
- **Summary-to-English reading.** The scan equations themselves are the formal
  postcondition; the minimum-even/first-index interpretation follows by the
  stated elementary structural induction. Differential testing supplies broad
  finite corroboration only.
- **Partial correctness.** No separate liveness, time-complexity, or
  termination theorem is claimed. Negative/non-integer nodes, Python `bool`
  values as nodes, arbitrary ambient heaps/aliases, and behavior outside the
  supplied MPY subset are excluded.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C
(auditability/trust evidence) all pass. The fresh proof is result-constraining,
pins the real generated body, covers the full material source-contract domain,
and has no material semantic or proof-rule soundness gap.

VERDICT: PASS
LEGITIMACY: LEGIT
