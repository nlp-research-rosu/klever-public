# Independent adversarial audit — 102-choose-num

Outcome: **PASS / LEGIT**. I reconstructed the supplied-semantics proof from source, proved each target independently, mechanically pinned the proof's closure body to the trusted regeneration of the submitted program, audited every local and fixed K sentence, and obtained the expected failures from both a false-result mutation and a material body mutation. Candidate prose, generation logs, and the prior `#Top` were not used as proof authorities.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`, condition `semantics`, and `semantics_mode = SUPPLIED_SEMANTICS`. The trusted `/reference/reference-semantics` mount is present, so the rendered mode and mounts are consistent.

I read `/audit-input.json` first, then inspected `/audit-campaign-lock.json`, `/run.json`, `/task.json`, `/generation-result.json`, all required legacy-selected-stage1 generation records (`invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace), and the present `usage.json`. The trace consists of 188 valid JSONL records. The historical layout does not require absent runtime metrics.

Integrity results:

- The `audit_campaign` object equals `/audit-campaign-lock.json` structurally, and its actual SHA-256 is the recorded `ad5dfcc...d745`.
- All launcher-declared container paths and required records are readable real files/directories, not symlinks.
- Mounted `canonical.py`, prompt, translator, run/task/result records, invocation metrics, usage, final text, output log, prompt, and trace file all have their recorded file hashes.
- An independent manifest-style tree hash of `/candidate` is `7d836d...3569`, exactly the retained workspace hash in `/generation-result.json`.
- Independent tree hashes match for the trusted semantics (`4e0639...89f`), candidate semantics (`4e0639...89f`), and generation trace (`8c80d8...8f4d`).
- `cmp` shows that candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted mounts.
- `diff -r --no-dereference` between trusted and candidate `reference-semantics/` exits 0. There are no missing, additional, changed, mistyped, or symlinked entries.
- Required candidate proof artifacts (`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, and `prove.sh`) are present as regular files.

Evidence: [stage1_integrity.log](/audit-output/evidence/stage1_integrity.log), [stage1_tree_hashes.py](/audit-output/evidence/stage1_tree_hashes.py), and [stage1_tree_hashes.log](/audit-output/evidence/stage1_tree_hashes.log).

There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

On the integral domain implied by the request for an “even integer” and by the trusted canonical implementation, the contract is: for positive integers `x` and `y`, return the largest even integer in the inclusive interval `[x, y]`; return `-1` when the interval contains no even integer. The two documented examples are `(12, 15) -> 14` and `(13, 12) -> -1`.

The candidate implements an equivalent branch decomposition:

- even `y`: return `y` exactly when `y >= x`;
- odd `y`: return `y - 1` exactly when `y - 1 >= x`;
- otherwise return `-1`.

For integer endpoints this is algebraically equivalent to the canonical program. In the odd case, `x < y` is equivalent to `x <= y - 1`, which accounts for the only syntactic branch difference.

### Trusted regeneration and differential execution

Running the trusted `/reference/py2mpy.py` over the scratch copy of `solution.py` exits 0 and produces a file byte-identical to submitted `solution.mpy` (both SHA-256 `e7231f...f226`).

The independent differential test imports `/reference/canonical.py` and the scratch candidate entry point. It covers:

- both prompt examples;
- the smallest positive endpoint;
- singleton, reversed/empty, and adjacent intervals;
- every even/odd and in-range/out-of-range branch boundary;
- the full grid `1 <= x,y <= 200`;
- 5,000 deterministic generated pairs up to `10^12`.

All 45,015 inputs matched. Every branch class had over 11,000 executions; mismatch count was zero. This finite test supports implementation/canonical fidelity but is not substituted for the K proof.

Evidence: [differential_test.py](/audit-output/evidence/differential_test.py) and [stage2_fidelity.log](/audit-output/evidence/stage2_fidelity.log).

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work`, ignored candidate `__pycache__`, and used newly named output definitions. No candidate K definition or cache was present or reused. The available independent toolchain is K `v7.1.293`, matching the campaign lock.

Fresh builds:

- `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` — exit 0.
- `kompile verification.k --backend haskell --main-module CHOOSE-NUM-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` — exit 0.

Evidence: [stage3_runtime_build.log](/audit-output/evidence/stage3_runtime_build.log) and [stage3_proof_build.log](/audit-output/evidence/stage3_proof_build.log).

I then selected every target by its compiled qualified label. Each command exited 0 and printed exactly one line equal to `#Top`:

| Target | Exit | `#Top` |
|---|---:|---:|
| `CHOOSE-NUM-SPEC.all-positive-inputs` | 0 | 1 |
| `CHOOSE-NUM-SPEC.even-upper-in-range` | 0 | 1 |
| `CHOOSE-NUM-SPEC.even-upper-before-range` | 0 | 1 |
| `CHOOSE-NUM-SPEC.odd-upper-predecessor-in-range` | 0 | 1 |
| `CHOOSE-NUM-SPEC.odd-upper-no-even-in-range` | 0 | 1 |

The initial unqualified `--claims` attempt was rejected as an unused filter before proof execution and is preserved in [stage3_positive_claims.log](/audit-output/evidence/stage3_positive_claims.log). The successful independent invocations are in [stage3_positive_claims_qualified.log](/audit-output/evidence/stage3_positive_claims_qualified.log).

As an independent concrete check of the rebuilt LLVM definition, a reviewer-authored translated harness executed nine assertions spanning both prompt examples, all four claim partitions, the smallest positive input, and large/reversed boundaries. `krun` exited 0 with final `.K`, `NoExc`, and exit code 0. Evidence: [k_concrete_cases.py](/audit-output/evidence/k_concrete_cases.py), [k_concrete_cases.mpy](/audit-output/evidence/k_concrete_cases.mpy), and [stage3_concrete_execution.log](/audit-output/evidence/stage3_concrete_execution.log).

Compiler warnings concern non-exhaustive fixed-semantics functions for unused float/list/subscript constructs and unused variables in `strLt`; none lies on the submitted integer program's dependency path.

## 4. Adequacy and real-program pinning

### Plain-language claims and satisfiable states

Each claim starts from the exact standard configuration: environment 0; empty module scope with the fixed builtins parent; `scopeLoc = 1`; empty heap and stack; `noRet`; `NoExc`; and exit code 0.

| Claim | Precondition | Required result | Satisfying witness |
|---|---|---|---|
| `all-positive-inputs` | `X > 0` and `Y > 0` | `Y - pyMod(Y,2)` if that value is at least `X`, else `-1` | `(12,15) -> 14` |
| `even-upper-in-range` | positive, even `Y`, `X <= Y` | `Y` | `(1,2) -> 2` |
| `even-upper-before-range` | positive, even `Y`, `X > Y` | `-1` | `(3,2) -> -1` |
| `odd-upper-predecessor-in-range` | positive, odd `Y`, `X < Y` | `Y - 1` | `(1,3) -> 2` |
| `odd-upper-no-even-in-range` | positive, odd `Y`, `X >= Y` | `-1` | `(3,3) -> -1` |

For every witness, the claimed result, trusted canonical result, and candidate Python result agree. Evidence: [claim_witnesses.py](/audit-output/evidence/claim_witnesses.py) and [stage4_claim_witnesses.log](/audit-output/evidence/stage4_claim_witnesses.log).

### Mechanical program pinning

The claim does not load the whole module; it invokes a proof-only `#chooseNum(X,Y)` adapter. This is permitted only if the adapter contains the same binding and body as the real entry point.

The mechanical comparison establishes:

- trusted regeneration contains exactly one `Module(FuncDef("choose_num", Params("x","y"), BODY))`;
- the adapter calls `closureVal(("x","y"), BODY, 0)`;
- parameters match exactly;
- after normalizing only the surface spelling of empty `.Stmts`, both constructor bodies hash to `3bda02...bb1`;
- the closure's defining environment is 0, which is exactly where the fixed `FuncDef` rule would bind this sole module function.

Thus the adapter bypasses only the mechanically determined module-load/name-lookup setup. It does not substitute an algorithm, helper, oracle, or summary for the function body. Evidence: [program_pinning_check.py](/audit-output/evidence/program_pinning_check.py) and [stage4_program_pinning.log](/audit-output/evidence/stage4_program_pinning.log).

The underlying call allocates a temporary scope, binds `x` then `y`, executes the submitted body, unwinds on `Return`, deletes the temporary scope, and restores `env`, `scopeLoc`, stack, and `ret`; heap, exception, and exit-code cells are unchanged. The adapter itself rewrites only `<k>` and preserves the suffix. A fresh continuation probe observes the returned `2`, continues to add `100`, and proves `102` with `#Top`: [audit-context-probe.k](/audit-output/evidence/audit-context-probe.k), [audit-context-probe-spec.k](/audit-output/evidence/audit-context-probe-spec.k), and [stage5_context_probe.log](/audit-output/evidence/stage5_context_probe.log).

A material mutation of the term actually executed by the claim—changing the even/in-range return from `Y` to `Y - 2`—builds but makes the original universal result get stuck with a failed implication and exit 1. This is genuine body sensitivity, not an edit to an unused external source file. Evidence: [audit-verification-body-mutant.k](/audit-output/evidence/audit-verification-body-mutant.k), [audit-spec-body-mutant.k](/audit-output/evidence/audit-spec-body-mutant.k), [stage4_body_mutant_build.log](/audit-output/evidence/stage4_body_mutant_build.log), and [stage4_body_mutant_proof.log](/audit-output/evidence/stage4_body_mutant_proof.log).

There are no loop/helper claims; the submitted program is straight-line conditional code.

## 5. Rule-by-rule static soundness review

The exhaustive lexical inventory covers all 26 K source files used in this audit: supplied `semantics.k` and every helper, candidate `verification.k`, and `spec.k`. It records the complete normalized sentence, source bounds, attributes, hash, dependency disposition, and assessment for every entry.

Inventory totals:

- 937 outer sentences: 229 syntax declarations, 697 rules, 5 contexts, 1 configuration, and 5 claims;
- 146 function declarations, 108 carrying `total`, 0 carrying `functional`;
- 4 macro declarations;
- 45 priority rules;
- 22 `no-evaluators` opaque declarations;
- 0 simplification rules.

The full enumeration is [rule_inventory.md](/audit-output/evidence/rule_inventory.md), generated by [build_rule_inventory.py](/audit-output/evidence/build_rule_inventory.py). It classifies 66 fixed sentences as relevant and individually checked, all five claims as targets, four local proof sentences by role, and the remaining fixed sentences as unreachable from this submitted constructor term.

### Used-construct mapping

| Submitted construct | Declaration and operative rules |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; load/sequencing in `core.k`; closure binding in `functions.k:14-16` |
| `Call(closureVal(...), X, Y)` | `call.k:20-21,69-74`; left-to-right argument loop `core.k:185-191` |
| `Name("x")`, `Name("y")` | `core.k:130-154`; current-frame lookup after parameter binding |
| `Int` | `core.k:194` |
| `UnaryOp("-", ...)` | `operators.k:10`; `int.k:7` |
| `BinOp("%", ...)` | sequential strictness in `syntax.k`; dispatch `operators.k:12`; `int.k:15,19-20` |
| `BinOp("-", ...)` | same dispatch; `int.k:13` |
| `Compare(..., "==", ...)` | left-then-right contexts `operators.k:15-17`; `int.k:26` |
| `Compare(..., ">=", ...)` | same contexts; `int.k:25` |
| `If` | strict guard declaration; `controls.k:51-54`; integer truthiness from `core.k:199,202` |
| `Return` | strict expression evaluation and `functions.k:78-90` frame unwind |

This map covers every constructor in `solution.mpy` and the entry adapter's real call.

### Candidate-local extension decisions

1. `#chooseNum(Int,Int)` is a fresh invocation constructor. Its sole rule expands it to the exact submitted closure call. It does not preempt a fixed-semantics rule or invent a value. Its broad K suffix is preserved, as confirmed by the continuation probe.
2. `largestEvenInRange(Int,Int)` is a nonrecursive `[function,total]` definitional summary. Its single unconditional equation covers every integer pair and has no overlap.
3. The summary equation computes `C = Y - pyMod(Y,2)` and returns `C` iff `X <= C`, otherwise `-1`. For positive integer `Y`, the fixed `pyMod(Y,2)` is 0 or 1; hence `C` is even, `C <= Y`, no larger even integer is at most `Y`, and `X <= C` is exactly interval membership. This is ordinary integer mathematics, not an execution shortcut.
4. No candidate-local opaque symbol, simplification, priority rule, lemma, circularity, or trusted claim exists.

There is no circular abstraction: the program executes fixed `%`, subtraction, comparison, branching, and return rules; `largestEvenInRange` appears only as a fully defined postcondition summary.

### Fixed-semantics overlap, priority, and unused boundaries

On the reachable fragment:

- operand evaluation is left-to-right (`seqstrict`/contexts and the call argument loop);
- integer operator cases are sort-specific and deterministic;
- true/false branch guards are disjoint and exhaustive;
- the generic call rule's `owise` status does not select any special interception for a direct `closureVal`;
- the cell-parameter priority rule is inapplicable because the new frame is an ordinary empty scope;
- return/pop restores all exposed call state exactly;
- no allocation, mutation, exception, output, iterator, loop, float, collection, sort, digest, or external-state rule is reachable.

All fixed priority rules and totality declarations are enumerated in the inventory. The 22 named `no-evaluators` symbols—`md5hexCodes`, float abstractions (`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`), and `sortVS`/`sortKeyVS`—are unreachable. Symbolic concrete-only helpers such as `floorFI`, `toF`, and `ceilF`, and warned partial-total functions such as `mapStrVS` and `valSeqAt`, are likewise unreachable. None can influence a branch, return, state cell, or postcondition here.

I found no proof-relevant false rule and therefore make no unsupported unsoundness allegation. In particular, there is no rule encoding the task answer, fabricating a used operation, or replacing the submitted body.

## 6. Fresh non-vacuity test

No candidate mutation was trusted. I created a fresh spec whose universal postcondition requires:

`actual result = largestEvenInRange(X,Y) + 2`.

This is demonstrably false at satisfying input `(X,Y) = (1,2)`: the real and claimed-good result is 2, while the mutation requires 4.

- `kprove ... --dry-run` parses and builds the mutation successfully, exit 0.
- The real proof run exits 1, prints no `#Top`, reports `WarnStuckClaimState`, and explicitly says the implication check failed.
- The residual includes the unmet result equality (for the even branch, `Y = if X <= Y then Y else -1 fi + 2`), so this is not a parser error, missing import, timeout, unrelated crash, or unreachable mutation.

Evidence: [audit-spec-vacuity.k](/audit-output/evidence/audit-spec-vacuity.k), [stage6_vacuity_build.log](/audit-output/evidence/stage6_vacuity_build.log), and [stage6_vacuity_proof.log](/audit-output/evidence/stage6_vacuity_proof.log).

The proof is result-constraining and non-vacuous.

## 7. Proven versus assumed accounting

### Precisely established

Under the supplied K definition, for every K integer `X > 0` and `Y > 0`, execution of the exact submitted `choose_num` closure from the stated initial configuration reaches a normal returned integer equal to:

`Y - pyMod(Y,2)` when `X <= Y - pyMod(Y,2)`, and `-1` otherwise.

The four additional claims independently establish the corresponding exhaustive parity/range cases. This is a partial-correctness result; the concrete straight-line execution also terminates, but no broader total-correctness claim is needed.

### Trust ledger

| Boundary | Influence | Dependents | Assessment/evidence |
|---|---|---|---|
| Supplied MPY semantics and K built-in Int/Bool/Map/List hooks | evaluation, control, call state, arithmetic | all claims | Acceptable fixed campaign boundary; candidate copy is recursively identical to trusted mount; reachable rules statically reviewed |
| K toolchain/backend `v7.1.293` | compilation and reachability closure | all machine results | Acceptable campaign-locked tool boundary; fresh reconstruction performed |
| Trusted `py2mpy.py` | source-to-`solution.mpy` constructor translation | program identity | Acceptable designated translator; byte-identical regeneration |
| Manual entry adapter | selects bound entry and supplies symbolic arguments | all claims | Acceptable under the benchmark's constructor-comparison rule; exact parameters/body/env checked, continuation and body sensitivity tested |
| Integer interpretation of “positive numbers” | theorem domain | adequacy | Acceptable: parity/evenness and trusted canonical behavior make integral endpoints the coherent HumanEval domain; arbitrary Python floats and other non-Int values are explicitly outside the theorem |
| Formula-to-“greatest even” interpretation | human-facing intent | adequacy | Elementary integer argument given above; supported by all four formal case claims |
| Differential and concrete tests | finite fidelity evidence only | translator/program bridge | 45,015 Python comparisons plus nine fresh K executions; not used as a universal proof |
| Imported opaque/partial unused symbols | none on this program | no target | Acceptable because dependency analysis shows no value/control/state/postcondition influence |

Candidate generation logs, final prose, concrete tests, and any historical `#Top` establish nothing beyond untrusted claims; none was used in place of the reconstructed K proof.

Validation gates:

- Gate A (real-program soundness, result constraint, non-vacuity): PASS.
- Gate B (intent and domain adequacy): PASS.
- Gate C (trust and reproducible evidence): PASS.

The immutable candidate lacks automatic source-to-proof regeneration, but the required trusted regeneration plus mechanical constructor comparison closes the identity question for this submission. That is an artifact-maintenance observation, not a theorem defect.

VERDICT: PASS
LEGITIMACY: LEGIT
