# Adversarial proof review: 126-is-sorted

The candidate does not contain a legitimate partial-correctness proof of the
submitted program under the supplied semantics. Fresh reconstruction does
produce `#Top` for both submitted claims, and the submitted program is faithful
to the HumanEval contract on its promised domain. The decisive defect is in the
proof theory: `verification.k` adds (1) a task-specific rule that replaces one
complete loop-body execution with the desired recurrence and (2) a
whole-entry rule whose source, destination, and cells are the target entry
claim itself. Neither operational bridge has a bridge-free universal
connection theorem. The final `#Top` therefore follows under an axiom that
already states the target reachability result.

This review does **not** assert that either bridge equation is mathematically
false. No false conclusion witness was found for their narrowly matched
integer/plain-frame states, so they are not labeled false or globally
unsound. They are nevertheless illegitimate proof assumptions: they bypass
program execution and assume the correctness conclusion they are supposed to
establish.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`semantics_mode = SUPPLIED_SEMANTICS`, and problem `126-is-sorted`.
The required trusted supplied-semantics mount is present. This is not an
infrastructure-error case.

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, `/generation-result.json`, and every required
  `legacy-selected-stage1` generation record were present and readable.
  `usage.json` was also present. Historical `runtime-metrics.json` is absent,
  but that record is explicitly not required for this legacy layout.
- The `audit_campaign` object equals `/audit-campaign-lock.json` exactly, and
  the independently computed lock hash is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  matching `/audit-input.json`.
- Independent hashes of the run, task, stage result, invocation, metrics,
  usage, prompt, generation output, last message, and trace file match the
  launcher-recorded hashes. The structured trace contains 674 valid JSONL
  records and no invalid line.
- The candidate prompt and translator are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- Recursive `diff -r` of `/candidate/reference-semantics` and
  `/reference/reference-semantics` exits 0. Per-entry file hashes match, entry
  types match, and neither tree contains a symlink. There are no additional or
  missing entries in the candidate semantics tree.
- No candidate path is a symlink. Candidate caches, the candidate
  `kore-exec.tar.gz`, the candidate `.pyc`, and every candidate-provided claim
  about earlier execution were ignored for reconstruction.

The untrusted generation record says both claims printed `#Top`. The structured
trace also records that direct entry composition stalled and that an “exact
composed reachability rule” was then added. Those are only historical claims;
the audit below independently reproduces and evaluates the proof.

Evidence:

- [stage1_integrity.log](evidence/stage1_integrity.log)
- [stage1_candidate_manifest.log](evidence/stage1_candidate_manifest.log)
- [stage1_trace_summary.log](evidence/stage1_trace_summary.log)

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For a finite list of nonnegative integers, return `True` exactly when:

1. the list is in nondecreasing order; and
2. no integer occurs more than twice.

The empty list is permitted by the Python signature and natural contract and
returns `True`. Negative integers are expressly excluded.

### Candidate implementation

`solution.py` performs one pass. It maintains the preceding value, the current
equal-value run length, and a Boolean result. Initializing `previous` to zero is
valid on the promised nonnegative domain. On a sorted list, every repeated value
is contiguous, so rejecting an equal run of length three is equivalent to the
canonical implementation's global occurrence-count check. On an unsorted list,
both implementations return `False` independently of later repetitions.

The trusted translator regenerated `solution.mpy` byte-for-byte:

```text
submitted sha256:   50bbea9e74cff486c6dd53e951326b22fdec005065fc2f7f225388df2693d1fe
regenerated sha256: 50bbea9e74cff486c6dd53e951326b22fdec005065fc2f7f225388df2693d1fe
cmp exit: 0
```

The independent differential test compared the trusted canonical entry point
with the generated entry point on:

- all eight documented examples;
- 17 explicit empty, comparison-boundary, duplicate-boundary, order-boundary,
  zero, and large-integer cases;
- all 97,656 lists of lengths 0 through 7 over values 0 through 4; and
- 3,000 deterministic random lists of lengths 0 through 40 with nonnegative
  values below one billion.

All 100,681 cases matched. This is finite evidence, not a universal proof. As a
domain-boundary check, `[-1]` returns `True` in the canonical implementation but
`False` in the candidate; this is outside the explicitly promised domain and is
not treated as a contract defect.

Evidence:

- [stage2_differential.py](evidence/stage2_differential.py)
- [stage2_fidelity.log](evidence/stage2_fidelity.log)

## 3. Clean proof reconstruction

All source inputs needed for execution were copied to
`/tmp/audit-work/126-is-sorted-audit-003`. The semantics came from the trusted
mount, not a candidate-built definition. Three new definitions were built with
K 7.1.293:

| Target | Exact operation | Result |
|---|---|---|
| Concrete semantics | LLVM `kompile` of trusted `semantics.k`, main `MPY-KRUN` | exit 0 |
| Concrete submitted module | `krun solution.mpy` on that definition | exit 0; `.K`, `NoExc`, exit-code 0; closure contains submitted body |
| Loop proof base | Haskell `kompile verification.k`, main `IS-SORTED-VERIFICATION` | exit 0 |
| Loop claim | `kprove spec.k --spec-module IS-SORTED-LOOP-SPEC` | exit 0; `#Top` |
| Entry proof | Haskell `kompile verification.k`, main `IS-SORTED-WITH-LOOP-LEMMA` | exit 0 |
| Entry claim | `kprove spec.k --spec-module IS-SORTED-SPEC` | exit 0; `#Top` |

Thus the positive reconstruction gate succeeds as a **verification under the
submitted extended theory**. A `#Top` under that theory does not establish that
the added rules are valid consequences of the supplied semantics.

Exact command/output logs:

- [stage3_runtime_build.log](evidence/stage3_runtime_build.log)
- [stage3_runtime_solution.log](evidence/stage3_runtime_solution.log)
- [stage3_loop_build.log](evidence/stage3_loop_build.log)
- [stage3_loop_proof.log](evidence/stage3_loop_proof.log)
- [stage3_entry_build.log](evidence/stage3_entry_build.log)
- [stage3_entry_proof.log](evidence/stage3_entry_proof.log)

## 4. Adequacy and real-program pinning

### Claims in plain language

The loop claim in `/candidate/spec.k:6` says: from an isolated call frame with
Boolean `result = OK`, integer `previous = PREV`, integer `repeats = COUNT`,
and a remaining proof-carrier list `IS`, execute the real loop body, return the
Boolean scan recurrence, pop the frame, restore the caller continuation and
environment, and preserve unrelated cells.

Its precondition is satisfiable. One witness is:

```text
IS=.IntSeq, OK=true, PREV=0, COUNT=0, FRAME=SAVED=CURRENT=1,
CALLER=0, CONT=.K, STACK=.List, LOCALS=.Map, BASE=.Map,
PARENT=parent(0), NUMBER=0
```

Every freshness and no-duplicate-key requirement evaluates to true for this
witness.

The entry claim in `/candidate/spec.k:56` says: from the standard initial
configuration, directly call `isSortedClosure` on
`list(intsToVals(INPUT))`, and return
`scanResult(scanAll(true, 0, 0, INPUT))` while restoring all listed state.
`INPUT=.IntSeq` with the exact standard cells is a satisfying witness.

### Program identity

A reviewer-authored constructor comparison mechanically:

1. extracts the function binding and body from trusted regeneration;
2. extracts and expands `isSortedClosure` and `isSortedLoopBody`; and
3. erases only explicit empty `.Stmts` identity constructors.

The entry name, parameter, complete body, and loop body are
constructor-identical. This is a real-program term, not a substituted
algorithm. The lack of automatic source-to-proof regeneration is only a
maintenance observation for this immutable artifact.

Ground substitutions for `[]`, `[0]`, `[0,0]`, `[0,0,0]`, `[1,2,2]`,
`[1,2,2,2]`, `[1,0]`, and `[1,3,2,4,5]` agree among the K scan recurrence,
candidate Python, and canonical Python. Ground K recurrence claims also
normalize to `#Top`.

Evidence:

- [stage4_constructor_identity.py](evidence/stage4_constructor_identity.py)
- [stage4_constructor_identity_final.log](evidence/stage4_constructor_identity_final.log)
- [stage4_ground_compare.py](evidence/stage4_ground_compare.py)
- [stage4_ground_compare.log](evidence/stage4_ground_compare.log)
- [stage4_ground_kprove.log](evidence/stage4_ground_kprove.log)

### Execution pinning failure

Although the term is the real body, the entry proof does not execute its
material operations. `/candidate/verification.k:438-459` adds this
whole-configuration rule:

```text
#applyK(toCall(isSortedClosure), (list(intsToVals(INPUT)), .Vals))
  => scanResult(scanAll(true, 0, 0, INPUT))
```

with the same environment, scopes, allocation state, stack, return state, and
exception state as the entry claim. Apart from reducing the functional
`builtinsScope` spelling, this rule is the target entry claim
`/candidate/spec.k:56-76`. It has priority 10 and can close the claim directly.
There is no separate proof, in a definition that excludes this rule, that
establishes the rule from the supplied semantics and the independently proved
loop theorem.

A diagnostic definition with only this final rule removed built successfully.
Its entry proof did not reach either `#Top` or a stuck result before the
reviewer's 300-second bound (`timeout` exit 124). That timeout is **not** used
as a counterexample or candidate failure; it only shows that the fast
submitted closure path was removed.

A second diagnostic removed the one-iteration body summary at
`verification.k:322-350`. It built successfully, and the loop claim then exited
1 with `WarnStuckClaimState` at the first symbolic integer comparison. This
demonstrates that the submitted loop proof depends on the body summary. It does
not show that the summary equation is false.

Evidence:

- [stage4_bridge_dependence.sh](evidence/stage4_bridge_dependence.sh)
- [entry-summary-removed verification](evidence/stage4_verification_no_entry_summary.k)
- [body-summary-removed verification](evidence/stage4_verification_no_body_summary.k)
- [stage4_no_entry_summary_proof.log](evidence/stage4_no_entry_summary_proof.log)
- [stage4_no_body_summary_proof.log](evidence/stage4_no_body_summary_proof.log)
- [stage4_bridge_dependence_summary.log](evidence/stage4_bridge_dependence_summary.log)

## 5. Rule-by-rule static soundness review

The source-indexed exhaustive inventory covers:

- 227 supplied-semantics syntax declarations, five contexts, one
  configuration, and 695 supplied rules;
- seven candidate syntax declarations and 37 candidate rules;
- all 72 priority-bearing declarations, the one simplification, all 150
  function declarations, all 111 `total` declarations, both claims, and all
  22 explicit `no-evaluators` opaque declarations;
- no `[functional]` declaration (none exists).

Every declaration and complete rule block is listed by source and line in
[stage5_rule_inventory.md](evidence/stage5_rule_inventory.md). The supplied
tree is fixed and byte-identical to the trusted tree. Its rules were reviewed
file-by-file as follows:

| Supplied modules | Rules | Static disposition |
|---|---:|---|
| `syntax.k`, `semantics.k`, `iter.k` | 0 | Assembly, AST grammar, and iterator protocol declarations |
| `core.k` | 46 | Configuration, values, scope/heap behavior, evaluation sequencing, lookup, and structural helpers; used behavior is coherent |
| `call.k`, `functions.k`, `controls.k` | 70 | Call/frame lifecycle, assignment, branches, loop sequencing, return/pop; used control order and cell footprints are coherent |
| `int.k`, `bool.k`, `operators.k` | 39 | Integer/Boolean operations and ordered evaluation; used comparisons and `+` agree with Python integers |
| `list.k`, `tuple.k`, `range.k`, `subscript.k` | 94 | Iterable/collection support; only the list/iterator shape is material here |
| `str.k`, `set.k`, `methods.k` | 115 | Unused by this submitted program |
| `builtins.k`, `sort.k`, `dict.k` | 184 | Unused by this submitted program |
| `float.k` | 121 | Unused; contains the documented opaque/concrete float trust boundary |
| `comprehension.k`, `assert.k`, `concrete.k` | 26 | Unused in the proof; concrete module only supports the independent LLVM run |

The supplied semantics is deliberately partial. Its documented opaque float,
sort, MD5, and total-but-underspecified out-of-bounds operations, plus omitted
exceptions for unsupported cases, do not occur in `solution.mpy` and do not
influence either claim. No supplied opaque symbol reaches a branch or final
result here.

### Construct coverage for `solution.mpy`

| Program construct | Declaration/execution path |
|---|---|
| `Module`, `FuncDef`, `Params`, statement sequencing | `syntax.k`; `core.k:124-127`; `functions.k:14-16` for concrete loading |
| `Name`, `Int`, `Bool` | `syntax.k`; `core.k:130-151,193-205`; proof-local exact lookup/guard accelerators |
| function call and frame | `core.k:183-191`, `call.k:69-75`, `functions.k:63-90`; proof-local call specialization |
| `Assign`, `AugAssign` | `controls.k:9-31`; proof-local plain-frame direct instances |
| `For` and iteration | `controls.k:65-75`; proof-local `intsToVals` iterator equations |
| three `If`/`Compare` guards | `syntax.k`, `operators.k`, `int.k`, `controls.k`; proof-local disjoint direct guard pairs |
| `Return` and cleanup | `functions.k:78-90`; proof-local exact Boolean-local return and frame cleanup |

### Candidate extensions

| Lines in `verification.k` | Class and rule-by-rule disposition |
|---|---|
| 7-32 | Two syntax macros and their expansions. Definitional only; constructor identity is mechanically established. |
| 36-62 | Specialized call-frame creation. A narrowed operational accelerator for the exact closure; it matches argument binding/order and relevant cells, although no independent connection theorem is supplied. |
| 66-193 | Lookup, parameter/target binding, assignment, and augmented-assignment direct instances. Each duplicates the supplied map operation on a plain or exactly keyed frame. Specific and generic overlaps agree; priority only selects a more decidable form. |
| 198-205 | Direct return of the known Boolean local. It agrees with fixed lookup followed by strict `Return` and `#pop` on its guard, including the abrupt discard of the active in-call suffix. |
| 210-301 | Six guard rules. `<` versus `>=`, `==` versus `=/=`, and `>` versus `<=` are pairwise disjoint and exhaustive over K integers; branches agree with supplied integer comparison and `If`. |
| 304-306 | Map-delete simplification. Under `N` absent from `BASE`, deleting the disjoint `N |-> S` entry yields `BASE`; mathematically valid. |
| 309-317 | `intsToVals` is an uninterpreted structural carrier, not a result oracle. Its two iterator rules are constructor-exhaustive over `IntSeq` and yield exactly the represented integers in order. |
| 322-350 | **Program-derived operational bridge.** It skips all four real loop-body statements and directly updates `result`, `previous`, and `repeats` to the desired recurrence. The recurrence appears truthful on the matched Int/Bool plain-frame domain, but no bridge-free universal connection theorem proves this complete state transition. Removing it exposes the genuine stuck execution. |
| 354-381 | `nextRepeats`, `scanAll`, `scanResult`, and `isSortedContract`. Guards are disjoint/exhaustive, structural recursion descends on `IntSeq`, and the equations are ordinary mathematics. |
| 390-435 | Imported loop lemma. Its text equals the separately closed loop claim, so reusing it compositionally would be acceptable only if that loop proof had passed Gate A. It inherits the unproved body-bridge dependency. |
| 438-459 | **Whole-entry operational bridge and circular theorem assumption.** Its complete matched configuration and conclusion are the target entry claim. There is no bridge-free derivation. This rule alone is enough to make the target theorem provable under the extended theory. |

No false conclusion witness is claimed for lines 322-350 or 438-459. The
review defect is narrower and decisive: these program-derived operational
bridges have no independent universal connection theorem, and the latter
literally installs the target theorem as a rewrite rule. Finite tests, truthful
comments, priority, and an apparently correct equation cannot replace that
proof obligation.

## 6. Fresh non-vacuity test

The reviewer created a new spec that negates the result-bearing destination:

```text
notBool scanResult(scanAll(true, 0, 0, INPUT))
```

The original entry configuration and every cell are unchanged. `INPUT =
.IntSeq` is a concrete satisfying witness: the correct scan result is `true`,
while the mutation demands `false`.

- `kprove ... --dry-run` exited 0, showing that the mutation parses and builds.
- The actual `kprove` exited 1 with `WarnStuckClaimState`.
- The residual is the expected unmet condition:
  `notBool scanResult(...) #Equals scanResult(...)`.
- There was no parser error, missing import, timeout, or unrelated crash.

The proof is therefore result-constraining and non-vacuous. This does not
validate how the correct result was obtained: the whole-entry rule first
produces the scan result, and the mutation correctly refuses its negation.

Evidence:

- [stage6_spec_vacuity_audit.k](evidence/stage6_spec_vacuity_audit.k)
- [stage6_mutation_dry_run.log](evidence/stage6_mutation_dry_run.log)
- [stage6_mutation_proof.log](evidence/stage6_mutation_proof.log)
- [stage6_nonvacuity_summary.log](evidence/stage6_nonvacuity_summary.log)

## 7. Proven versus assumed accounting

### What the successful K runs establish

Under the theory consisting of the supplied semantics **plus every rule in
`verification.k`**, K establishes:

1. the loop reachability claim from the stated symbolic loop-head frame to the
   mathematical scan result; and
2. the standard entry configuration's reachability to that scan result.

This is not a proof that fixed semantics executes the submitted body to that
result. The loop proof assumes the one-step body transition, and the entry
proof assumes its entire source-to-destination reachability as a rule.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K integer, Boolean, map, list, and reachability machinery | Values, conditions, state, proof engine | Ordinary accepted K trust base |
| Byte-identical supplied semantics | Program execution model | Required fixed semantics; integrity passes |
| Supplied opaque float/sort/MD5/OOB symbols | None in this program or postcondition | Inert for this theorem |
| `intsToVals` plus its two iterator equations | Formal representation of arbitrary integer-list inputs | Acceptable structural proof carrier; not result-bearing |
| Proof-local direct lookup/bind/assign/guard/return rules | Symbolic execution mechanics | Narrow and extensionally consistent on their guards; no false witness found |
| `nextRepeats`/`scanAll`/`scanResult` | Final mathematical result | Truthfully and exhaustively defined |
| Loop-body summary rule | Branches, three locals, loop invariant, returned value | Unacceptable program-derived operational bridge without a bridge-free connection theorem |
| Imported loop lemma | Complete loop and call-frame cleanup | Conditional on the invalidated loop proof theory |
| Whole-entry summary rule | Entire returned value and all target reachability | Illegitimate circular assumption of the target theorem |
| Constructor identity script | Source-to-proof term identity | Reproducible mechanical evidence; does not prove execution |
| Differential and ground tests | Python equivalence and finite summary examples | Strong finite evidence only; not a universal K connection theorem |

### Gate and benchmark decision

- **Gate A — real-program soundness: FAIL.** The body summary and whole-entry
  summary replace program-defined execution without independent universal
  connection proofs. The final bridge is the target theorem itself.
- **Gate B — intent adequacy: conditional PASS only.** If the scan recurrence
  had been derived soundly, it covers arbitrary finite `IntSeq` inputs and
  agrees with the full promised nonnegative-integer HumanEval domain. The
  candidate does not materially narrow the contract domain.
- **Gate C — evidence auditability: PASS as evidence accounting.** Commands,
  hashes, differential scope, term comparison, proof runs, bridge-deletion
  diagnostics, and mutation residuals are reproducible. They do not repair
  Gate A.

Under the benchmark decision boundary, a proof that installs the result-bearing
loop transition and the exact target entry theorem as operational rules is not
a legitimate partial-correctness proof, even when the implementation and the
assumed equations appear extensionally correct.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
