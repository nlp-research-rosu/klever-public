# Independent adversarial review: `0-has-close-elements`

## Decision summary

The candidate’s implementation is faithful to the HumanEval task, its submitted
`.mpy` is the trusted translator’s exact output, and all five positive proof
rungs reconstruct cleanly from source. The final claim is also
result-constraining: an independently authored negated-result mutation parses,
builds, and is rejected with the expected implication residual.

Those facts do not make the proof legitimate. Four operational bridges in
`verification.k` are materially broader than the claims said to justify them.
Fresh fixed-versus-extended witnesses show each broad rule proving a false
conclusion. The most direct failure is the entry bridge at
`/candidate/verification.k:197`: it rewrites a textual
`Call(Name("has_close_elements"), ...)` without looking up the name or executing
the selected closure. I changed the actual translated entry body to
`return False`, mechanically proved that the changed constructor term is the
term loaded by the claim, and reran the final theorem. It still printed `#Top`.
For the satisfying input `[0.0, 0.0], 1.0`, that changed program returns
`False`, while the trusted canonical, the original candidate, and the claimed
all-pairs result are `True`.

Therefore the reconstructed `#Top` is closure in a materially unsound extended
theory, not a legitimate partial-correctness proof of the submitted program.

## 1. Input and provenance integrity

### Declared layout and semantics boundary

`/audit-input.json` declares:

- `record_layout = legacy-selected-stage1`;
- `condition = semantics`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- mounted paths through its `container_paths` map, rather than the host-only
  provenance paths.

The trusted `/reference/reference-semantics` tree is present, as required for
this mode. This is not a mode/mount contradiction, so the audit proceeds to a
candidate verdict.

### Launcher and generation records

All records required for `legacy-selected-stage1` are regular, readable files:

- `/audit-input.json`, `/audit-campaign-lock.json`;
- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`,
  `/generation-evidence/metrics.json`,
  `/generation-evidence/codex-last.txt`,
  `/generation-evidence/codex-output.log`,
  `/generation-evidence/prompt.txt`;
- `/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T20-31-25-019f8c99-51a5-7a12-811f-3c0052ef1541.jsonl`.

`usage.json` is present and was inspected. The historical runtime-metrics record
is absent, which is permitted for this declared legacy layout. The additional
legacy records `legacy-run-input.json` and `legacy-metrics.json` are present,
readable, and match the hashes in `invocation.json`.

The campaign object in `/audit-campaign-lock.json` is canonically equal to the
`audit_campaign` object in `/audit-input.json`; the lock file itself has the
recorded SHA-256
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-recorded single-file hash checked independently matched,
including the run/task/result records, canonical, prompt, translator,
generation prompt, usage, logs, and the single trace file.

The structured trace has 695 JSONL records, zero malformed records, 136 tool
calls, and 136 tool outputs. The complete generation output was streamed and
hashed: 83,795 lines and SHA-256
`d0096d91ffffd02db5d9d9a7a9723ef38e95dc73022aaa845488d89f7b211600`.
These generation materials are treated only as untrusted historical claims.
The checks are reproducible in:

- `/audit-output/evidence/01-provenance.log`
- `/audit-output/evidence/01b-tree-hashes.log`
- `/audit-output/evidence/01-candidate-files.sha256`
- `/audit-output/evidence/inspect_generation.pl`
- `/audit-output/evidence/hash_trees.py`

The reviewer-authored aggregate tree hash in `01b-tree-hashes.log` deliberately
uses its documented path/type/content scheme; it is not presented as an
inference of the launcher’s unspecified aggregate-tree algorithm. Exact
recorded file hashes and complete per-file manifests are the integrity checks.

### Candidate-versus-trusted inputs

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. Their hashes
match the audit manifest.

A recursive, no-dereference comparison of
`/candidate/reference-semantics` and
`/reference/reference-semantics` found no missing, additional, changed,
mistyped, or linked entry. A sorted per-file SHA-256 manifest is identical for
the two trees. No symlink or unsupported entry occurs anywhere in the mounted
candidate tree. The supplied-semantics integrity gate therefore passes.

The required proof deliverables—`solution.py`, `solution.mpy`,
`verification.k`, `spec.k`, and `prove.sh`—are all present. Candidate caches,
compiled material, `kore-exec.tar.gz`, logs, and prior `#Top` statements were
not reused.

**Stage 1 result: PASS. No audit-infrastructure breach.**

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt asks whether a list of floats contains any two distinct
positions whose absolute numerical difference is **strictly less than** the
given float threshold. It has no list-length bound and gives:

- `[1.0, 2.0, 3.0], 0.5 -> False`;
- `[1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3 -> True`.

The trusted canonical loops over every pair of indices, excludes equal indices,
computes `abs(elem - elem2)`, and returns `True` on the first distance strictly
below the threshold.

The candidate uses an equivalent one-sided traversal. For the element at
position `i`, `start` is `i + 1`, and `is_close_to_any` ignores every position
before `start`; it therefore checks each unordered pair exactly once. Empty and
singleton lists return `False`; zero or negative thresholds cannot satisfy the
strict comparison; duplicates return `True` only for a positive threshold.

### Trusted regeneration

The exact command

```text
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/case/regenerated-solution.mpy
```

exited 0. The regenerated file is byte-identical to
`/candidate/solution.mpy`; both have SHA-256
`fdcfe6fa45a3f0c3095f26e402bb739c403800bc3412df619a41bdb449c33307`.

### Independent differential

`/audit-output/evidence/differential.py` imports scratch copies of the trusted
canonical and candidate sources and uses a third oracle:
`itertools.combinations(numbers, 2)` plus
`math.fabs(left - right) < threshold`. It does not reuse the K summary
equations.

The preserved scope is 21 named cases plus 2,000 deterministic generated cases
(seed `0xC105E`). It includes both examples, empty/singleton inputs, equality
and adjacent floating-point values at the strict threshold, duplicates,
zero/negative thresholds, negative values, early/late/non-adjacent matches,
large finite values, subnormals, signed zero, infinities, NaN elements, and a
NaN threshold. Complete inputs are in
`/audit-output/evidence/differential-inputs.json`.

Result:

```text
total=2021
property_true=842
property_false=1179
mismatches=0
```

Commands, hashes, and exit codes are in
`/audit-output/evidence/02-fidelity.log`.

**Stage 2 result: PASS. The Python implementation is faithful on the intended
domain, and the submitted constructor program is exactly regenerated.**

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/case`; the supplied
semantics came from the trusted reference mount. All output definitions were
built below `/tmp/audit-work/build`. No candidate-provided definition or cache
was read by `kompile`, `krun`, or `kprove`.

The live toolchain reports K version `7.1.293`. The reviewer rebuilt:

1. LLVM `MPY-KRUN` from trusted `reference-semantics/semantics.k`;
2. five Haskell definitions, successively rooted at
   `VERIFICATION-BASE`, `VERIFICATION-WITH-INNER`,
   `VERIFICATION-WITH-HELPER`, `VERIFICATION-WITH-OUTER`, and
   `VERIFICATION-WITH-ENTRY`.

A reviewer-generated concrete program consists of the exact candidate source
plus 12 normal/boundary assertions. Trusted translation and LLVM execution both
exited 0. The concrete cases include both examples, empty/singleton, strict
equality and just-inside boundaries, duplicate/zero/negative thresholds,
negative values, a last-only pair, and a non-adjacent pair.

Every positive proof target was then run independently:

| Proof definition | Spec module | Exit | Exact success output |
|---|---|---:|---|
| `base-kompiled` | `SPEC-INNER` | 0 | one `#Top` |
| `inner-kompiled` | `SPEC-HELPER` | 0 | one `#Top` |
| `helper-kompiled` | `SPEC-OUTER` | 0 | one `#Top` |
| `outer-kompiled` | `SPEC-ENTRY` | 0 | one `#Top` |
| `entry-kompiled` | `SPEC` | 0 | one `#Top` |

No positive log contains a prover error. Exact commands, bounded compiler
output, status codes, and success counts are in
`/audit-output/evidence/03-reconstruction.log`; the concrete generator is
`/audit-output/evidence/make_concrete_cases.py`.

**Stage 3 result: the verification-execution gate passes. This establishes only
closure under the submitted extensions, not their soundness.**

## 4. Adequacy and real-program pinning

### Plain-language meaning and satisfiability of the eight claims

The formal domain is an arbitrary finite `FloatSeq` and an arbitrary K
`Float` threshold. There is no finite-size bound.

| Claim | Precondition and postcondition in plain language | Satisfying example |
|---|---|---|
| `SPEC-INNER`, empty | In a helper frame, an empty remaining iterator followed by the exact cleanup/return leaves `found=false`, resets `index=0`, and resets `other=number`. | `A=0.0`, `ALL=.FloatSeq`, `T=1.0`, `START=0`, `I=0`, `Q=0.0` with the displayed frames. |
| `SPEC-INNER`, `I < START` | Skip the current element and return `closeSkip(A,R,T,I+1,START)`. | one-element remainder, `I=0`, `START=1`. |
| `SPEC-INNER`, `I >= START` | Compare the current element and OR that result with the remaining suffix. | one-element remainder, `I=0`, `START=0`. |
| `SPEC-HELPER` | Applying the exact `helperClosure()` returns `closeSkip(A,ALL,T,0,START)`. | empty list, `A=0.0`, `T=1.0`, `START=0`. |
| `SPEC-OUTER`, empty | The empty outer iterator returns false after the exact cleanup. | `ALL=.FloatSeq`, `T=1.0`. |
| `SPEC-OUTER`, nonempty | The head helper result is ORed with the recursive all-pairs result for the tail. | singleton list, `A=0.0`, `T=1.0`, `START=1`. |
| `SPEC-ENTRY` | Applying the exact `entryClosure()` returns `hasPairs(ALL,ALL,T,1)`. | empty list and `T=1.0`. |
| final `SPEC` | Load `solutionModule()`, call `has_close_elements`, and return `hasPairs(ALL,ALL,T,1)`. | empty list and `T=1.0`; a true-result witness is `[0.0,0.0]`, `T=1.0`. |

The result is not a free variable or tautology. `hasPairs` is a total recursive
Boolean summary over `ALL` and `T`. The ground/structural checks in
`/audit-output/evidence/ground-summary.k` establish the empty and singleton
results and reduce a two-element sequence to `near(A,B,T)`. They print `#Top`
in `/audit-output/evidence/04c-pinning-completed.log`. For
`ALL=[0.0,0.0]`, `T=1.0`, the summary is true by its equations and the
`0.0` distance comparison; both Python implementations and concrete LLVM
execution return `True`.

### Constructor-level program identity

`kast` parsed the exact regenerated `solution.mpy` through `MPY-SYNTAX` and
produced `/audit-output/evidence/solution.normalized.kterm`.
`pinning-original.k` claims that `solutionModule()` is this complete normalized
module term, including both function bindings and both bodies. It prints
`#Top` against the fresh base definition. Thus manual whitespace and empty-list
surface syntax are normalized mechanically; the claimed module is the
translated candidate module, not a merely similar handwritten body.

### Body-sensitivity failure

Program-term pinning is not enough because the final bridge ignores the binding
and body after loading them. The fresh body-sensitivity experiment made the
following material change:

```python
def has_close_elements(numbers: List[float], threshold: float) -> bool:
    return False
```

The trusted translator generated
`/audit-output/evidence/solution-body-mutated.mpy`.
`kast` normalized that exact file, and the diff in
`/audit-output/evidence/04d-body-sensitivity-final.log` shows that the entry
`FuncDef` body changed from the submitted loop to `Return(Bool(false))`.
`verification-body-mutated.k` changes `entryBody()` to exactly that constructor.
The independent `PINNING-BODY-MUTATED` claim prints `#Top`, proving that
`solutionModule()` in this experiment is the changed translated module term.

Despite that changed executed term, the same universal final reachability shape
in `body-mutation-spec.k` also prints `#Top`. The concrete witness is:

```text
numbers=[0.0, 0.0] threshold=1.0
canonical=True
original=True
mutated=False
```

This is not the invalid experiment of editing only an external source while
leaving the proof term fixed. The normalized loaded module, its K constructor
definition, and the compiled proof definition all changed and were mechanically
pinned before the false-program proof was run.

The cause is `/candidate/verification.k:197-203`: the high-priority rule
rewrites the textual call directly to `hasPairs` while mentioning no
`<scopes>` binding at all. It can fire after `#loadAll` even when the loaded
closure has the false body. Therefore the final claim does not execute the
submitted entry body in the theorem-critical step.

**Stage 4 result: FAIL. The surface module is pinned, but the result proof is
body-insensitive and can establish the claimed result for a substituted false
program.**

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The complete machine-readable inventory is
`/audit-output/evidence/05-rule-inventory.tsv`. It contains 972 entries:

- 241 local syntax declarations;
- 717 rules;
- 5 contexts;
- 1 configuration;
- 8 reachability claims.

It covers every K file in the supplied reference tree plus `verification.k` and
`spec.k`. The inventory records source, line, complete normalized declaration,
attributes, materiality, and assessment. Attribute accounting includes 159
`function`, 121 `total`, 25 `no-evaluators`, 55 `concrete`, 30 `owise`,
priority 39/40/45 rules, strictness, macros, and all named opaque symbols. No
local `simplification` or `functional` declaration is present. Generation and
hashes are in `/audit-output/evidence/05-rule-inventory.log`.

The 928 supplied-semantics inventory entries are the fixed selected semantics.
Rules in modules unused by the submitted program cannot affect this execution.
The target-path modules were additionally traced through the actual constructor
term:

| Used construct | Declaration and material fixed rules |
|---|---|
| `Module`, statement sequencing | `syntax.k:61`; `core.k:124-127` |
| `ImportFrom("typing",...)` | `syntax.k:43`; no-op `controls.k:35-44` |
| `FuncDef`, parameters, closures | `syntax.k:53-60`; `functions.k:14-16`; `call.k:69-74`; `functions.k:63-90` |
| `Name` lookup and arguments | `core.k:131-152`, `core.k:189-191`; `call.k:20-21` |
| `Assign`, `AugAssign` | `controls.k:9-31`; integer `+` in `int.k` |
| `For`, target bind, break | `controls.k:69-74`, `controls.k:85-91`; typed iterator rules at `verification.k:91-95` |
| `If`, `Compare` | `controls.k:52-54`; `operators.k:15-17`; integer `>=` in `int.k`; float `<` in `float.k:50-52` |
| float subtraction and `abs` | `float.k:54-56`, `float.k:103-105`, generic call dispatch |
| `Return` and frame pop | `functions.k:78-90` |
| `Int`, `Bool`, `Float` literals | `core.k:194-196`; `float.k:20-21` |

The fixed configuration tracks `<k>`, environments/scopes, allocation, frames,
return state, exceptions, and exit code. On the actual path, evaluation is
left-to-right; function calls bind arguments in a fresh scope and restore the
caller; loop and break continuations are explicit. Fresh LLVM execution agrees
with Python on the preserved normal/boundary cases.

The LLVM build warns that several fixed-semantics `total` functions are not
syntactically exhaustive over unrelated values (`mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and `valSeqAt`). None is reachable from this program term.
No false target-path conclusion witness was found for a supplied rule, so these
are recorded as fixed-semantics/unused limitations, not mislabeled as candidate
unsoundness.

### Candidate definitions that are locally acceptable

The body constructors, closure constructors, `solutionModule()`, and
`solutionScope()` at `verification.k:7-85` expand to the exact translated
terms. Mechanical pinning checks them.

`FloatSeq` is a proof-only typed representation. Its two priority-40 iterator
rules cover exactly empty and `fCons` sequences and yield the same head/tail
behavior as list iteration. The program uses no other operation on this
representation, so this narrow representation boundary is adequate for the
claimed list domain.

`near`, `closeSkip`, and `hasPairs` are ordinary terminating definitions.
`closeSkip` recurses on the tail; its integer guards `I < START` and
`I >= START` are disjoint and exhaustive. `hasPairs` also recurses on the tail.
Their equations do not overlap inconsistently. `near` is exactly
`floatLt(absF(subF(A,B)),T)`, the term built by the fixed execution.

### Materially unsound operational bridges

The following are not derived lemmas. They are operational rules imported into
later proof definitions. Each accepts a strictly larger context than its
preceding reachability claim, and no bridge-free universal connection theorem
justifies that larger domain.

1. **Inner-loop body oracle (`verification.k:130-145`).**

   The proved `SPEC-INNER` claims start at `#loop`, contain the exact
   `helperLoopBody()` and exact cleanup/return suffix, pin a function frame, and
   cover structural cases. The imported rule instead matches
   `For(Name("other"), list(ALL), _B)` for **any** `_B`, any continuation hidden
   by `...`, and without the proved stack/cleanup context.

   False witness: one float element, `START=2`, and body
   `Assign(found,true)`. Fixed execution writes `found=true`; `closeSkip` skips
   the sole element and is false. `base-kompiled` rejects the false claim with
   `WarnStuckClaimState` and exit 1; `inner-kompiled`, after adding this rule,
   prints `#Top`. See modules and paired commands in
   `/audit-output/evidence/bridge-witnesses.k` and
   `/audit-output/evidence/04-adequacy-and-bridges.log`.

2. **Helper textual-call binding oracle (`verification.k:151-161`).**

   This rule matches the spelling `Name("is_close_to_any")` and four local
   values, but never looks up that name in scope 0 or checks that the selected
   closure is `helperClosure()`. It also bypasses ordinary callee and argument
   evaluation.

   False witness: bind `is_close_to_any` to a closure returning `true` and call
   it with an empty float list, whose `closeSkip` summary is false. Fixed
   `inner-kompiled` reaches `true` and rejects the false destination (exit 1,
   stuck); `helper-kompiled` prints `#Top`. The arguments are within the formal
   float/list domain.

3. **Outer-loop body oracle (`verification.k:178-191`).**

   The proved outer claims use the exact `outerLoopBody()` and exact
   cleanup/return continuation. The imported rule accepts any `_B`, frames its
   continuation, and fabricates `hasPairs` state.

   False witness: a singleton float list and body
   `Assign(found,true)`. The fixed loop sets `found=true`; a singleton has no
   pair, so `hasPairs` is false. `helper-kompiled` rejects the claim with a
   stuck residual; `outer-kompiled` prints `#Top`.

4. **Entry textual-call binding/body oracle (`verification.k:197-203`).**

   The preceding `SPEC-ENTRY` claim proves an exact
   `#applyK(toCall(entryClosure()),...) ~> #proofDone` configuration. The
   imported rule instead accepts a textual `Call`, arbitrary continuation,
   and no scopes binding. Its matched domain is not contained in the claim’s
   justification domain.

   False binding witness: bind `has_close_elements` to a closure returning
   `true` and use a singleton list, whose `hasPairs` summary is false. Fixed
   `outer-kompiled` rejects; `entry-kompiled` prints `#Top`.

   The independently translated `return False` body-sensitivity experiment in
   Stage 4 is an additional real-program witness for this rule. It proves the
   wrong all-pairs result for `[0.0,0.0],1.0`.

The priority attributes only make these bridges preempt fixed semantics; they
do not supply the missing equivalence, binding proof, state preservation, or
context containment.

`verification.k:163-172` is another attempted helper `#applyK` shortcut with an
arbitrary `_BODY` and weakly framed continuation. It has no universal
connection theorem. A fresh arbitrary-body witness was tried against the
before/after definitions, but the proposed rule did not match and both runs
failed on the fixed `true` result. In compliance with the required witness
standard, this review labels it **unjustified or dead**, not unsound. The failed
probe and residual are preserved in `04b-adequacy-completed.log`.

**Stage 5 result: FAIL. Four local rules are concretely unsound over their
declared match domains and materially taint the target proof.**

## 6. Fresh non-vacuity test

No candidate vacuity artifact was relied on. The fresh
`/audit-output/evidence/spec-vacuity.k` changes the final result obligation from

```text
hasPairs(ALL, ALL, T, 1)
```

to

```text
notBool hasPairs(ALL, ALL, T, 1)
```

This is demonstrably false for the satisfying witness
`ALL=[0.0,0.0]`, `T=1.0`: the true program result is `True`, while the mutated
destination is `False`.

`kprove --dry-run` exited 0, so the mutation parsed and built. Actual `kprove`
exited 1, printed one `WarnStuckClaimState`, printed no `#Top`, and exposed the
expected unmet condition:

```text
hasPairs(ALL, ALL, T, 1)
#Equals
notBool hasPairs(ALL, ALL, T, 1)
```

This is a meaningful proof failure, not a parser error, timeout, missing import,
or unrelated crash. Exact commands and bounded output are in
`/audit-output/evidence/06-fresh-non-vacuity.log`.

**Stage 6 result: PASS. The final claim constrains its result, but this does not
repair its lack of dependence on the program body.**

## 7. Proven-versus-assumed accounting

### What the successful runs actually establish

The clean `#Top` runs establish that, in the theory consisting of the supplied
MPY semantics plus all imported candidate rules, the displayed configurations
reach the candidate summaries. In particular, the final run establishes that a
term spelled as the target call rewrites to `hasPairs`.

Because that theory contains demonstrated false operational rules and proves
the same result for a mechanically pinned `return False` replacement, this is
not a sound theorem about execution of `solution.mpy`. Differential testing,
the truth of the Python implementation, and a failed false-postcondition probe
cannot substitute for the missing real-program connection.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| Trusted prompt, canonical, and translator mounts | Source contract, executable oracle, source-to-constructor bridge | Hash-checked; translator output byte-identical. Acceptable trusted input. |
| Supplied MPY semantics | All operational behavior | Integrity-identical to trusted reference and freshly rebuilt. It is the selected semantics level. |
| K Float primitives `subF`, `absF`, `floatLt` | Pair predicate and final Boolean | Opaque (`no-evaluators`) for symbolic proof with concrete LLVM rules. The theorem is structurally parametric in these exact primitives; finite LLVM/Python tests support, but do not universally prove, the Python IEEE bridge. Acceptable named boundary for an otherwise sound structural theorem. |
| Candidate `FloatSeq` and its two iterator rules | Representation of arbitrary finite float lists | Exact empty/head-tail behavior; only iteration is used. Mechanically and concretely exercised. Non-fatal representation boundary. |
| `near`, `closeSkip`, `hasPairs` | Final result | Truthful, guarded, terminating equations. Structural ground claims close. |
| Manual `solutionModule()`/scope definitions | Program identity | Exact normalized constructor pinning closes for both original and mutated bodies. Maintenance is manual but identity is established for this immutable candidate. |
| Inner/outer loop bridges | Control, variable state, return summary | Illegitimate. They accept arbitrary bodies and continuations; paired false witnesses close only with the extensions. |
| Helper/entry textual-call bridges | Binding, call evaluation, selected body, result | Illegitimate. They bypass lookup/body execution; paired false witnesses and the translated body mutation expose wrong results. |
| Rule at `verification.k:163` | Potential helper-call execution shortcut | No connection theorem and no demonstrated match in the attempted witness. Recorded as unjustified/dead, not used as the basis for the unsoundness verdict. |
| Differential and concrete tests | Implementation/intent and finite float bridge | 2,021 Python cases and 12 LLVM assertions, zero mismatches/failures. Finite evidence only. |
| Partial-correctness interpretation | Termination | K reachability establishes partial correctness. The program’s finite list loops terminate informally; termination is not the claimed K theorem. |

### Gate accounting and benchmark decision

- **Kit Gate A, real-program soundness: FAIL.** Four witnessed operational
  bridges are false over their match domains, and the final proof is insensitive
  to a material, mechanically pinned entry-body replacement.
- **Kit Gate B, intent adequacy: conditionally adequate in isolation.** The
  formal list/threshold domain is unbounded and `hasPairs` expresses all
  distinct position pairs with a strict threshold. There is no finite-size
  narrowing. This cannot rescue Gate A.
- **Kit Gate C, evidence auditability: PASS for the reviewer evidence.** Scripts,
  complete deterministic inputs, exact commands, bounded logs, status codes,
  normalized terms, mutations, and rule inventory are preserved under
  `/audit-output/evidence/`.

Under the benchmark’s decision boundary, a proof that relies on materially
unsound operational rules and proves a substituted false program is
`FAIL / NOT_LEGIT`, even though every submitted positive command reconstructed
to `#Top` and the result mutation was correctly rejected.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
