# Independent adversarial review: 136-largest-smallest-integers

## Executive finding

The candidate contains a legitimate, non-vacuous K partial-correctness proof of the submitted program over arbitrary finite sequences of mathematical integers. I rebuilt both definitions from source, ran all three positive claims, checked the theorem's program term against trusted regeneration at the KAST constructor level, reviewed every local declaration and rule, and made both an executed-body mutation and a false-postcondition mutation fail for the expected proof reason.

The result is `CONCERNS / LEGIT`, rather than `PASS`, because two intent/model bridges remain outside the candidate's machine-checked theorem:

1. The universal claim uses the generated semantics' proof-oriented `pyIntList(IntSeq)` value, while source list literals evaluate to the separate `pyList(List)` value. Both loop paths transparently bind and execute the same submitted body one element at a time, and concrete executions agree, but the candidate has no universal theorem relating those two representations. An auditor-only attempt to prove that bridge compiled and then got genuinely stuck on symbolic representation case splitting.
2. The identification of `#negFold`/`#posFold` with “greatest negative”/“least positive” is a short, transparent mathematical induction, but is not itself stated as a separate K theorem.

Neither limitation narrows the formal domain to fixed sizes, introduces an oracle, bypasses a material program operation, or supplies a false conclusion witness on the intended integer-list domain.

All reviewer-authored scripts, inputs, mutations, and bounded logs are under `/audit-output/evidence/`; their SHA-256 index is `/audit-output/evidence/evidence_manifest.sha256`.

## 1. Input and provenance integrity

The launcher declares:

- `record_layout`: `pipeline-v3`
- condition: `bare`
- semantics mode: `GENERATED_SEMANTICS`
- problem: `136-largest-smallest-integers`

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`, `/generation-result.json`, all required pipeline-v3 records under `/generation-evidence`, and the one 437-record JSONL trace. I treated the generation report and its prior `#Top` statements only as untrusted history.

Integrity results:

- Every required record is a real regular file, and every required tree is a real directory.
- No symlink occurs under `/candidate`, `/generation-evidence`, or `/reference`.
- `/audit-campaign-lock.json` is JSON-identical to the `audit_campaign` block and has the recorded hash `ad5dfcc...d745`.
- All launcher-recorded regular-file hashes match, including the run/task/result/invocation records, metrics, runtime metrics, usage, prompt, trace JSONL, canonical solution, trusted prompt, and translator.
- The structured trace parses completely as JSONL.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to `/reference/prompt.py` and `/reference/py2mpy.py`.
- `/reference/reference-semantics` is absent, as required in `GENERATED_SEMANTICS`.
- An independent implementation of the pipeline-v3 canonical tree digest gives candidate hash `8043e15c...0bd9`, exactly matching both `generation-result.json` and `invocation.json`. The trace tree similarly matches `usage.json` at `ff6f37e5...ac74`.

`/audit-input.json` also contains launcher-local directory-digest fields (`candidate_tree_sha256=cd3f2ac9...b331` and `generation_codex_trace_sha256=5ed96c5d...76e6`) whose serialization algorithm is not declared in any mounted record. I recorded them without equating them to the pipeline-v3 canonical workspace/tree digest. The independently checkable per-file evidence maps and canonical pipeline tree digests all match.

Evidence: `/audit-output/evidence/stage1_integrity.py` and `stage1_integrity.log` (`STAGE1_INTEGRITY: PASS`, exit 0).

No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py` and `/reference/canonical.py`: for a finite list of integers, return `(a, b)`, where `a` is the greatest integer strictly below zero and `b` is the least integer strictly above zero. Use `None` when the corresponding class is absent. Zero is in neither class.

`solution.py` implements one left-to-right loop with two optional accumulators:

- on a negative value, initialize or increase `largest_negative`;
- on a positive value, initialize or decrease `smallest_positive`;
- return both accumulators as a tuple.

That algorithm is faithful on the intended domain and does not mutate the input.

### Trusted regeneration

In scratch I ran:

```text
python3 py2mpy.py solution.py > regenerated.solution.mpy
cmp -s regenerated.solution.mpy solution.mpy
```

Both commands exited 0. Both MPY files have SHA-256 `39d22a1f...f26d`.

### Independent differential test

`/audit-output/evidence/differential_test.py` imports the trusted canonical and candidate entry points independently. The preserved input set `/audit-output/evidence/differential_inputs.json` has SHA-256 `bcbde5a1...3982` and contains:

- 14 explicit example/boundary/branch cases;
- every sequence of length 0 through 5 over `[-3, 3]` (19,608 cases);
- 1,000 deterministic seeded cases of lengths 0 through 60 containing small, 12-digit, and up to 100-digit integers.

Total: 20,622 inputs, zero mismatches, exit 0. The initial reviewer script had a reporting-line Python syntax error before either implementation ran; that audit-harness mistake is preserved separately as `stage2_initial_script_error.log`, and the corrected successful run is `stage2_program_fidelity.log`.

No program/canonical divergence was found.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/reconstruction`; I did not copy or use candidate `semantic-kompiled`, `verification-kompiled`, cache files, or bytecode.

Observed toolchain: K `v7.1.293`.

Fresh builds:

```text
timeout 900 kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/reconstruction/audit-semantic-kompiled

timeout 900 kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/reconstruction/audit-verification-kompiled
```

Both exited 0.

Fresh LLVM executions of regenerated `solution.mpy` all exited 0:

| Input | final `<k>` value | steps | trusted Python |
|---|---|---:|---|
| `[2,4,1,3,5,7]` | `pyTuple(pyNone,pyInt(1))` | 6 | `(None, 1)` |
| `[]` | `pyTuple(pyNone,pyNone)` | 0 | `(None, None)` |
| `[0]` | `pyTuple(pyNone,pyNone)` | 1 | `(None, None)` |
| `[-6,-1,-9,4,2]` | `pyTuple(pyInt(-1),pyInt(2))` | 5 | `(-1, 2)` |
| `[-2,-1]` | `pyTuple(pyInt(-1),pyNone)` | 2 | `(-1, None)` |
| `[2,1]` | `pyTuple(pyNone,pyInt(1))` | 2 | `(None, 1)` |

The positive command:

```text
timeout 900 kprove spec.k \
  --definition /tmp/audit-work/reconstruction/audit-verification-kompiled \
  --spec-module SPEC
```

printed `#Top` and exited 0 for the three-claim spec. A semantically inert labeled copy was also used to select the setup and invariant individually; both printed `#Top`. The end-to-end target, with its setup and invariant dependencies available, also printed `#Top`. See `stage3_reconstruction.log`, `spec-labeled.k`, and `stage3_each_claim.log`.

This independently establishes the candidate's positive verification result.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. **Setup claim, `spec.k:10`.** With arbitrary `IS`, empty environment, and zero steps, `run(solutionProgram, Value(pyIntList(IS)))` reaches the exact submitted loop body with the return statement as continuation. The parameter and two initialized sentinels have the expected bindings. It makes no final-result claim.
2. **Loop invariant, `spec.k:43`.** Starting at that exact loop with arbitrary remaining finite sequence `IS`, optional-integer accumulators `N` and `P`, an existing loop-variable binding, any disjoint residual map, and any step count, termination returns exactly `pyTuple(#negFold(IS,N), #posFold(IS,P))`. Final environment and step count are existentially framed.
3. **End-to-end claim, `spec.k:77`.** For every finite `IntSeq IS`, with empty environment and zero steps, running the submitted function returns exactly `pyTuple(#negFold(IS,pyNone), #posFold(IS,pyNone))`.

None of the claims has an unsatisfiable `requires` clause. Concrete witnesses recorded in `stage4_pinning.log` include:

- setup/end entry: `IS=nil`, `.Map`, steps 0;
- loop invariant: `IS=icon(-2,icon(3,nil))`, `N=P=pyNone`, `_OLD=pyInt(99)`, `_REST=.Map`, `_S=0`;
- nonempty end entry: `IS=icon(-2,icon(3,icon(0,nil)))`, `.Map`, steps 0.

The last witness executes to `pyTuple(pyInt(-2),pyInt(3))`, matching both Python implementations. The empty witness executes to `(None,None)`.

### Mechanical program identity

The trusted translator regeneration is byte-identical to submitted `solution.mpy`. I then expanded both:

- the regenerated MPY file as sort `Program`; and
- `solutionProgram` from `verification.k`

through the clean definition using `kast --expand-macros --output json`. The two 13,272-byte KAST files are byte-identical with SHA-256 `7f8f3925...c5d`. Thus the spec executes the same function name, parameter, statement sequence, conditions, assignments, and return body as the regenerated program. Evidence: `solution-file.kast.json`, `solution-macro.kast.json`, and `stage4_pinning.log`.

The postcondition is result-constraining: the final `<k>` value is an exact tuple of fully defined folds, not a right-only free variable, existential result, tautology, or implication.

### Executed-body sensitivity

In a separate scratch definition I changed the actual `solutionProgram` macro to return `(smallest_positive, largest_negative)` while leaving the spec obligations unchanged. That mutated definition compiled successfully. `kprove` exited 1 with `WarnStuckClaimState`; even the `IS=nil` setup destination no longer unified with execution. This changes the constructor term executed by the claim, not merely external `solution.py`.

Evidence: `/audit-output/evidence/body-mutation/verification.k`, `stage4_body_sensitivity.log`, and `body_mutation_kprove.raw.log`.

## 5. Rule-by-rule static soundness review

There are exactly three local K source files and no additional helper K source: `semantic.k`, `verification.k`, and `spec.k`. The complete declaration-start inventory and hashes are in `stage5_rule_inventory.log`.

### Local syntax and configuration inventory

`semantic.k` declares:

- `Program`: `Module(Stmts)`;
- sequence sorts `Stmts` and `Exprs`;
- `Params(String)` and `CmpOp(String,Expr)`;
- free sequence `IntSeq`: `nil` and `icon(Int,IntSeq)`;
- statements: `FuncDef`, `Assign`, `For`, `If`, and `Return`;
- expressions: `Name`, `Int`, `NoneVal`, `Compare`, `ListExpr`, `TupleExpr`, and internal `Value`;
- optional integers: `pyInt` and `pyNone`;
- values: `OptInt`, `pyBool`, `pyList`, `pyIntList`, and `pyTuple`;
- `KResult ::= PyVal`;
- K items: `run`, `start`, `exec`, `bind`, `store`, `branch`, `compareLeft`, `compareRight`, `tupleLeft`, `tupleRight`, `makeList`, `listValue`, `loop`, `iterate`, `iterateIntSeq`, `bindIteration`, and `iterationDone`.

The configuration has only the state used by this program: `<k>`, `<env>` map, and `<steps>` integer. No heap, allocation, I/O, exception, or global-state cell is needed by the submitted body.

`verification.k` adds six `[function,total]` symbols—`#negFold`, `#posFold`, `#negStep`, `#posStep`, `#negCandidate`, `#posCandidate`—and the `[macro]` program symbol `solutionProgram`.

There are no local `functional` declarations, opaque symbols, priorities, `[simplification]` rules, `[concrete]` rules, or `owise` rules.

### All 41 operational rules in `semantic.k`

| Lines | Rules | Assessment |
|---|---:|---|
| 79–83 | 2 `run`/`start` | Evaluate the supplied argument, bind the sole parameter in a fresh function environment, and execute the exact body. `start` ignores the textual `_F`, but the pinned module has exactly one function with the correct mechanically checked name/body. |
| 85–89 | 2 `bind` | Existing-key update and absent-key insertion are disjoint by `in_keys`; both preserve the rest of the map. |
| 91–92 | 2 `exec` | Empty sequence terminates; nonempty sequence executes its head before its tail. |
| 94–98 | 4 literal/value/name | Correctly inject integers, `None`, internal values, and deterministic environment lookup. Every actual lookup is bound. |
| 100–105 | 3 assignment/store | Evaluate RHS before store; existing/absent map cases are disjoint and complete for the actual assignments. |
| 107–118 | 6 comparison | Left operand before right operand; integer `<`/`>` use K mathematical integers; the two `is None` outcomes cover the actual `OptInt` values and are disjoint. |
| 120–125 | 3 conditional | Evaluate the guard, then execute exactly one branch for `pyBool(true/false)`. |
| 127–131 | 3 tuple | Left-to-right evaluation followed by exact pair construction. |
| 133–140 | 5 list literal | Empty, singleton, and multi-element construction preserve order. The singleton/general syntactic overlap has the same RHS when the residual expression list is empty, so it is coherent. |
| 142–147 | 3 `for` dispatch | Evaluate the iterable and select either ordinary `pyList` iteration or symbolic `pyIntList` iteration. |
| 148–159 | 4 iteration | Both list representations have empty and head/tail rules; each head is bound, the real body executes, the step marker executes, and only then does iteration continue on the strict tail. |
| 160–164 | 2 iteration binding | Existing/absent cases are disjoint and preserve the map. |
| 165–166 | 1 step counter | Increments once after each completed iteration. |
| 169 | 1 return | Evaluates the final top-level return expression and discards the remaining top-level statement sequence. This is exact at the sole return site used by the candidate. |

All material evaluation and control effects of the submitted body execute. The return rule is only validated for the actual final top-level return placement; this generated language is not a claim to model nested returns or arbitrary Python programs. I found no false conclusion witness reachable from the submitted program on the intended integer-list domain, so I record the broader-language limitation rather than an unsoundness finding.

### All 11 rules in `verification.k`

- Four fold equations: `#negFold` and `#posFold`, each on `nil` and `icon`.
- Three negative equations: unconditional `#negStep`, plus `#negCandidate` for `pyNone` and `pyInt`.
- Three positive equations: unconditional `#posStep`, plus `#posCandidate` for `pyNone` and `pyInt`.
- One `solutionProgram` macro equation.

The fold equations recurse on the strict `IntSeq` tail. Candidate equations cover both `OptInt` constructors. Negative and positive guards are implemented by total built-in Boolean conditionals. There is no pairwise conflicting overlap and all `[total]` declarations cover their complete declared sorts. Starting from `pyNone`, the negative fold retains exactly the maximum encountered value below zero and the positive fold retains exactly the minimum encountered value above zero.

The program macro is a definitional syntax abbreviation, not an operational bridge; its exact expansion equality was machine checked in Stage 4.

### Construct coverage and representation boundary

Every constructor in `solution.mpy`—`Module`, `FuncDef`, `Params`, `Assign`, `Name`, `NoneVal`, `For`, `If`, `Compare`, `CmpOp`, `Int`, `Return`, and `TupleExpr`—has the declarations and rule chain listed above. The entry harness additionally exercises `Value` and `pyIntList`. Stage 3 exercised all branch outcomes and both list iteration paths.

`pyIntList(IntSeq)` is an unbounded inductive encoding of finite integer lists, not a finite-size restriction. Its two loop rules do not summarize or oracle-call the body; they bind each integer and execute the unchanged body. Nevertheless, the semantics also has a distinct `pyList(List)` representation for evaluated list literals. The candidate does not contain a machine-checked universal equivalence theorem between these encodings.

I attempted an auditor-only theorem using total conversion `#asPyList : IntSeq -> List`. The definition compiled, but the proof exited 1 with `WarnStuckClaimState`: K could not split a symbolic `IS` hidden under `#asPyList` into empty/head cases. This is an honest evidence gap, not a candidate target failure and not evidence of a false semantic rule. See `list-representation-bridge/` and `stage7_list_bridge.log`.

## 6. Fresh non-vacuity test

The candidate provided no trusted non-vacuity artifact. I created `/audit-output/evidence/spec-vacuity.k`, renamed its module `SPEC-VACUITY`, and changed only the end-to-end result obligation from:

```text
pyTuple(#negFold(IS,pyNone), #posFold(IS,pyNone))
```

to:

```text
pyTuple(#posFold(IS,pyNone), #negFold(IS,pyNone))
```

For satisfying input `IS=icon(-2,icon(3,nil))`, the real result is `(-2,3)` while the mutation requires `(3,-2)`.

Results:

- fresh Haskell definition build: exit 0;
- mutated-spec `kprove --dry-run`: exit 0;
- mutated proof: exit 1 with `WarnStuckClaimState`;
- residual: actual `pyTuple(#negFold(...),#posFold(...))` could not imply the swapped obligation.

There was no parser error, missing import, timeout, or unrelated crash. Evidence: `stage6_nonvacuity.log` and `nonvacuity_kprove.raw.log`.

The proof is result-discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Relative to the rebuilt generated semantics and K's imported domains, for every finite `IntSeq IS`:

```text
run(exact-submitted-program, Value(pyIntList(IS)))
```

from empty environment and zero steps, if it terminates, has final `<k>` value:

```text
pyTuple(#negFold(IS,pyNone), #posFold(IS,pyNone))
```

The auxiliary setup and generalized loop claims establish that result by executing the initialization, each guard, each conditional assignment, every iteration, and the exact return expression. The theorem does not constrain the final environment or step counter, and it is a partial-correctness theorem rather than a separately stated total-termination theorem.

### Trust ledger

| Boundary | Influence | Assessment/evidence |
|---|---|---|
| K `v7.1.293`, Haskell/LLVM backends, reachability engine | Entire proof/execution | Trusted toolchain boundary; independently rebuilt, positive and negative outcomes recorded. |
| Imported `domains.md` modules for `Int`, `Bool`, `String`, `Map`, `List`, K sequencing, and `#if` | Arithmetic comparisons, state, sequencing, helper evaluation | Standard K primitive boundary; no candidate override. |
| Trusted `py2mpy.py` | Source-to-constructor translation | Launcher hash matches; fresh translation is byte-identical. |
| Generated `semantic.k` as a Python-subset model | All program execution | Exhaustively reviewed for every used construct; six concrete K/Python comparisons and 20,622 Python differential cases support adequacy. It is not a universal CPython formalization. |
| `solutionProgram` macro | Program identity | Not assumed: expansion is byte-identical at KAST level to regenerated MPY. |
| `#negFold`/`#posFold` meaning | Human-facing greatest-negative/least-positive contract | Transparent, terminating equations and ordinary induction; supported by differential tests, but no separate K theorem states the extrema characterization. |
| `pyIntList` as the external finite integer-list encoding | Formal input-domain interpretation | Covers arbitrary length and integer magnitude and executes every element; ordinary `pyList` path agrees concretely. Universal cross-representation bridge attempt remained stuck, so this is the principal non-fatal concern. |
| Opaque symbols/oracles | None | No opaque or unconstrained result-bearing symbol exists. |

### Gate assessment

- **Gate A — real-program soundness: PASS.** Clean `#Top`, exact constructor identity, no execution bridge or oracle, satisfiable starts, executed-body sensitivity, and false-result rejection.
- **Gate B — intent adequacy: PASS.** The formal `IntSeq` domain is arbitrary and finite, with unbounded mathematical integers; it is not examples-only or bounded unrolling. The result equations match the source contract.
- **Gate C — trust/evidence auditability: CONCERN.** The generated-semantics-to-Python interpretation and especially the `pyIntList`/`pyList` representation relation remain partly informal/empirical; the auditor-only universal bridge did not close. This does not invalidate the sound theorem over the declared unbounded representation.

There is no material domain narrowing, substituted body, vacuity, failed positive reconstruction, or witnessed false rule on the intended domain. The proof is therefore legitimate, with the documented non-fatal validation limitation.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
