# Independent adversarial audit: HumanEval 90 `next_smallest`

The candidate contains a legitimate partial-correctness proof of the submitted
program for the full material docstring domain: every arbitrary finite list of
K/Python integers. I rebuilt both definitions from copied source, proved the
dependency-complete two-claim spec, reconstructed the exact translated program
term, audited every proof-local equation, and rejected fresh false result and
body mutations. I did not rely on candidate-compiled definitions, `PROOF.md`,
logs, or its prior `#Top`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`, condition
`kit-semantics`, and `semantics_mode: SUPPLIED_SEMANTICS`. The required
`/reference/reference-semantics` mount exists, so the rendered mode and trusted
mounts do not conflict.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, every required JSON/text record in
`/generation-evidence`, and the structured 392-record JSONL trace. All are
regular readable files/directories, no required record is missing, the trace
has no invalid JSON record, and its session id is the invocation/result session
id. Generation prose and traces were treated only as untrusted claims.

The campaign lock is structurally identical to the `audit_campaign` block and
has the recorded SHA-256. Direct SHA-256 checks match every launcher-recorded
file hash: lock, run/task/result/invocation manifests, metrics, runtime metrics,
usage, prompt, generation last/output, canonical, trusted prompt, and
translator. The sole trace file has the exact hash recorded in both invocation
and result manifests. Evidence: `evidence/stage1-basic-integrity.log` and
`evidence/stage1-trace-and-lock.log`.

There are no symlinks under `/candidate` or either semantics tree. Candidate
`prompt.py` and `py2mpy.py` are byte-identical to the trusted mounts. Recursive
`diff --no-dereference` reports no missing, extra, changed, or mistyped entry in
the 24-file candidate supplied-semantics tree. Independently generated
normalized per-file manifests are identical, with 24 equal hashes. Evidence:
`evidence/stage1-tree-manifests.log`,
`evidence/candidate-semantics-files.sha256`, and
`evidence/trusted-semantics-files.sha256`. Stage 1 passes; there is no
infrastructure breach.

## 2. Program fidelity and differential checks

The trusted docstring says: for a list of integers, return its second-smallest
element, or `None` if none exists. `[1,1] -> None` determines that “second” means
the second **distinct** value. The four documented results are `2`, `2`,
`None`, and `None`. The canonical implementation `sorted(set(lst))[1]` is a
consistent witness of that reading.

`/candidate/solution.py` is a one-pass implementation maintaining a smallest
and second-distinct-smallest value with presence flags. Every branch matches
the stated contract; it does not mutate the input. The trusted command
`python3 py2mpy.py solution.py` reproduced submitted `solution.mpy` byte for
byte (both SHA-256
`d50c03b82c246ac26874ef0ca7badc663d13a1ba922ac325f5caf13a3d46f313`).
Evidence: `evidence/stage2-mpy-regeneration.log`.

The reviewer-authored `evidence/differential_test.py` separately imports the
generated and trusted canonical entry points and uses an independent one-pass
docstring oracle. It checks all four examples, 13 branch/boundary cases,
all 960,800 lists of lengths 0--7 over integers -3--3, and 20,000 seeded lists
of lengths 0--100 with integers up to 80 decimal digits. All 980,817 cases
matched, with no input mutation. Evidence: `evidence/stage2-differential.log`.
This is finite fidelity evidence, not a replacement for the proof. Stage 2
passes with no docstring/canonical conflict or relevant divergence.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/review-90`, used the trusted
semantics copy, and did not copy or consult candidate definitions/caches for
execution. The live tools are K 7.1.293 and Python 3.10.12
(`evidence/stage3-tool-versions.log`).

Fresh builds succeeded:

- LLVM `MPY-KRUN` from trusted `reference-semantics/semantics.k`, exit 0
  (`evidence/stage3-kompile-llvm.log`).
- Haskell `VERIFICATION` from `verification.k`, exit 0
  (`evidence/stage3-kompile-haskell.log`).

The loop claim alone printed `#Top` and exited 0
(`evidence/stage3-kprove-loop.log`). The dependency-complete command
`kprove spec.k --definition verification-kompiled-fresh --spec-module SPEC`
proved both the loop circularity and whole-function target, printed `#Top`, and
exited 0 (`evidence/stage3-kprove-all-claims.log`). A diagnostic selecting only
`SPEC.next-smallest` was interrupted after about 21 minutes because that option
removes its separately declared loop circularity and therefore unrolls an
unbounded loop; it is not the candidate's target proof and is recorded in
`evidence/stage3-kprove-next-smallest.log` rather than misclassified as failure.

Fresh LLVM execution used ten reviewer-authored assertions over an AST-identical
copy of the exact submitted function. It ended with `.K`, `NoExc`, exit code 0,
and empty stack (`evidence/stage3-krun-concrete.log`). Stage 3 passes.

## 4. Adequacy and real-program pinning

The loop claim at `/candidate/spec.k:8` says: for any finite all-integer suffix,
executing the actual translated `#loop` and exact loop body terminates that loop
and updates the four accumulator bindings according to `scanVS`, with `x` equal
to the suffix's last integer. A satisfying state is the empty suffix with
`HA=HB=false` and `A=B=X0=0`; arbitrary accumulator states are also allowed and
the summary remains operationally exact.

The entry claim at `/candidate/spec.k:29` says: from the complete initial MPY
configuration, load `solutionProgram`, bind `next_smallest` to
`nextSmallestBody`, and call it on any `list(VS)` satisfying `allInts(VS)`; the
returned `<k>` value must equal `nextSmallestSpec(VS)`. It pins environment,
module/builtins scopes, allocation counters, heap, stack, return/exception, and
exit state. The postcondition is equality to a determined value, not a free
variable, tautology, or implication. Empty and `[1,2]` sequences are explicit
satisfying inputs.

Trusted regeneration first established source-to-MPY identity. I then parsed
that exact MPY `Module` with K and inserted its canonical constructor tree into
a reviewer identity claim. Under a fresh auxiliary definition,
`solutionProgram` and that exact tree are identical and the claim printed
`#Top`/exit 0 (`evidence/stage4-constructor-pinning-final.log`; the two earlier
logs record harmless reviewer-harness parser/structure iterations). This is a
mechanical constructor-level comparison, not reliance on source filenames.

Ground whole-function K claims for `[3,1,2] -> 2` and `[1,1] -> noneV` printed
`#Top`; generated Python and canonical Python returned the same values
(`evidence/stage4-ground-substitution.log`). A material reviewer mutation changed
`Assign(second,x)` to `Assign(second,smallest)` inside the function term actually
executed by `solutionProgram`. It rebuilt successfully, and the original proof
failed on the loop implication with exit 1
(`evidence/stage4-body-mutation-kompile.log` and
`evidence/stage4-body-mutation-kprove.log`). Stage 4 passes.

## 5. Rule-by-rule static soundness review

`evidence/k_rule_inventory.py` generated the exhaustive
`evidence/k-rule-inventory.txt`: 978 captured records across all 24 supplied K
files, `verification.k`, and `spec.k` (243 syntax, one configuration, five
contexts, 727 rules, two claims), with function/total/functional,
`no-evaluators`, priority, ordinary, simplification, concrete/symbolic, owise,
strictness, and macro attributes identified. The assertion that captured count
equals lexical declaration-start count passed. Detailed adjudication is in
`evidence/static-soundness-review.md`.

The selected supplied model's used path correctly provides module loading and
sequencing; lexical lookup; call argument order; frame allocation, binding,
return, deletion and restoration; assignment; branch truthiness and
short-circuit order; finite list iteration; integer addition/comparison; and
`None`. The actual program uses no list mutation, exceptions, output, closures
escaping frames, or unmodeled construct. Its ASCII docstring does not hit the
supplied string model's non-ASCII boundary. Unused supplied rules cannot
contribute to this claim; they remain part of the launcher-selected fixed-model
trust boundary, not candidate proof extensions.

All 48 `verification.k` records (inventory 931--978) were checked. The program
aliases are exact constructor subterms. `allInts` is complete structural
recursion. The sole `no-evaluators` helper, `projectIntTotal`, is unconstrained
off-domain but is used only under `isInt`; its guarded equations fix it to the K
sort projection on every theorem input. The three guarded `applyBin/applyCmp`
rules are exactly the fixed integer equations after sort refinement and do not
touch control or cells. `scanStep` has six disjoint, exhaustive cases matching
the source branches. `scanVS` and `lastInt` structurally descend; their non-int
totalization cases are disjoint and unreachable under `allInts`. Field
projections are exact. `nextSmallestSpec` is a fully defined fold, not an opaque
oracle or operational interception.

The fold invariant is: `A` is the prefix minimum when `HA`; `HB` holds exactly
when a distinct larger prefix value exists; then `B` is the least such value.
Each of the six `scanStep` cases preserves it, including moving the old minimum
to `B` when a new minimum arrives. Consequently the summary returns precisely
the second-smallest distinct integer or `noneV`. No candidate `<k>` rule,
priority bridge, fresh result, task-answer axiom, overlap inconsistency, or
non-descending recursion exists. There is therefore no soundly supported false
conclusion witness for any candidate rule. Stage 5 passes.

## 6. Fresh non-vacuity test

I did not use the candidate's `spec-vacuity.k`. The fresh
`evidence/fresh-false-spec.k` preserves the real loop circularity but changes the
whole-function result obligation to unconditional `noneV`. It is demonstrably
false for satisfying input `[1,2]`, for which both Python implementations return
2. The mutation parsed/built, reached the final result-bearing branch, emitted
`WarnStuckClaimState` with residual `scanSecond(scanVS(...))` under
`scanFoundSecond(...) == true`, and exited 1. Evidence:
`evidence/stage6-fresh-false-kprove.log` and
`evidence/stage6-fresh-false-validation.log`. This is the expected unmet
obligation, not a parser error, timeout, unrelated crash, or unreachable probe.
Stage 6 passes.

## 7. Proven versus assumed accounting

Formally established under the supplied MPY semantics: for every arbitrary
finite `ValSeq` whose elements are K `Int`, loading and calling the exact
trusted-regenerated submitted module executes its real body and returns
`nextSmallestSpec(VS)`; the loop transition is summarized by the proved
circularity. The equations and elementary invariant establish that this value
is the docstring's second-smallest distinct integer, or `noneV` if absent.

Trust ledger:

- K 7.1.293's parser, kompiler, Haskell backend/prover, reachability logic, and
  hooked unbounded integer/Boolean/map/list operations are foundational trusted
  machinery. They affect all formal conclusions and were version-pinned and
  freshly exercised.
- The 24-file supplied semantics is the launcher-mandated fixed execution
  model. Its used rules affect value, control and state as described in Stage 5.
  Candidate/trusted trees are byte-identical; no candidate rule modified it.
- `/reference/py2mpy.py` is the trusted empirical/source bridge from the Python
  AST to MPY constructors. It affects program identity; byte regeneration plus
  parsed constructor identity support it. The K theorem begins at the MPY term,
  not CPython bytecode.
- `projectIntTotal` is not an assumed result: on every formal input its guarded
  equations fix it to the K `Int` projection. Its arbitrary off-domain
  interpretation has no positive dependent claim.
- The summary-to-English step uses the explicit inductive invariant above and
  ordinary integer-order mathematics. It is inspectable and has broad finite
  differential support, but differential testing itself proves no universal
  fact.
- Fidelity of the submitted Python program to intended CPython behavior is
  independently supported by 980,817 tests. Exotic non-list containers,
  non-integers (including floats/NaN), exceptions, and implementation-specific
  behaviors are outside the explicit “list of integers” contract. K `Int` is
  unbounded, so size and sign are not narrowed. Python `bool` is a subclass of
  `int`, but ordinary docstring language distinguishes booleans from integers;
  the supplied K model also represents `Bool` separately. Excluding booleans
  is therefore not a material source-contract narrowing.
- The theorem is a partial-correctness result. Neither candidate prose nor
  differential evidence substitutes for the reconstructed K proof.

All three validation gates pass: real-program soundness, intent/domain
adequacy, and reproducible trust/evidence accounting. There is no material
representation gap, undocumented narrowing, canonical/docstring contradiction,
or non-fatal limitation requiring a concerns verdict.

VERDICT: PASS
LEGITIMACY: LEGIT
