# Independent adversarial review: 115-max-fill

The candidate reconstructs cleanly and its generated implementation is correct on
the HumanEval domain.  Its successful K theorem is nevertheless not a legitimate
proof of that real execution.  The entry driver passes a proof-only
`list(symGrid(GS))`, not the fixed-semantics representation
`list(gridVals(GS))`.  Proof-local priority rules give the opaque `symGrid` and
`symRow` constructors their result-bearing iterator behavior.  The four
bridge-check claims prove corresponding one-step behavior for the real
`gridVals`/`rowVals` constructors, but do not prove a universal connection
between the two representations.  A fresh bridge-free universal connection
attempt gets stuck precisely when fixed semantics loses the `IntSeq` structure.

This is a real-program pinning failure under the required Kit Gate A procedure.
It is not a claim that the bridge equations produce a known wrong ground value:
the ground probes found the expected values and rejected an opposite result.
The narrower and decisive finding is that the candidate proves execution on a
substituted, locally axiomatized input representation without the required
machine-checked connection to actual fixed-semantics inputs.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1` and
`semantics_mode = SUPPLIED_SEMANTICS`.  `/reference/reference-semantics` is
present, so the trusted mounts agree with the rendered mode.  There is no audit
infrastructure breach.

The independent integrity program and complete bounded output are
[stage1_integrity.py](/audit-output/evidence/stage1_integrity.py) and
[stage1_integrity.log](/audit-output/evidence/stage1_integrity.log).  It checked:

- every required launcher, run, task, generation-result, invocation, metrics,
  prompt, output, last-message, usage, trace, candidate, and reference path is
  readable and has the required regular-file or directory type;
- `/audit-campaign-lock.json` equals the `audit_campaign` block and its SHA-256
  is `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
- all directly recorded file hashes match, including the canonical, prompt,
  translator, run/task/result manifests, invocation records, generation logs,
  prompt, metrics, usage, and the sole JSONL trace file;
- the independently reimplemented pipeline tree digest of `/candidate` is
  `3c7eafd486e896425b5a5848f734c8c3d03b0cf24c126afe0ff67a486f14d3c6`,
  matching the generation result's retained workspace digest;
- both trusted and candidate semantics pipeline tree digests are
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the launcher-recorded manifest digest;
- the generation trace tree digest is
  `a55b6e36cc6cd5dbd37b4ca8aae033803826d654f2d9da8a4edc4c34aaec0f33`,
  matching `usage.json`;
- recursive entry-type and byte comparison found no missing, additional,
  changed, mistyped, or symlinked entry between
  `/candidate/reference-semantics` and the trusted tree;
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
  trusted mounts, and no symlink exists below the candidate, trusted semantics,
  or generation-evidence trees.

All 578 structured trace lines parsed as JSON (`1 session_meta`,
`1 turn_context`, `1 world_state`, `168 event_msg`, and `407 response_item`).
The complete 42,774-line generation output was read and hashed; its historical
`#Top`, stuck states, errors, and final `KPROVE_PASSED` statement were treated
only as untrusted claims.  `usage.json` was present and inspected.  Historical
runtime metrics are absent, which is permitted for this legacy layout.

The required candidate sources are present.  Candidate-built
`kore-exec.tar.gz` and `__pycache__` were not trusted or reused.

## 2. Program fidelity and candidate-versus-canonical checks

The source contract in `/reference/prompt.py` is: for a rectangular grid with
1–100 nonempty rows, 1–100 entries per row, entries in `{0,1}`, and capacity
1–10, return the total number of bucket lowerings needed to empty each row.
Equivalently, return the sum over rows of
`ceil(number_of_ones_in_row / capacity)`.

The trusted canonical implementation computes
`sum(math.ceil(sum(row) / capacity) for row in grid)`.  The candidate computes
the same value with integer arithmetic:

```text
result += (sum(row) + capacity - 1) // capacity
```

For the documented bounded positive domain, these expressions are equivalent.
The candidate loop also behaves consistently on the requested empty extra
cases.

Fresh translation used the trusted translator:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -l solution.submitted.mpy solution.regenerated.mpy
```

Both commands exited 0; `cmp` produced no differences.  Exact records are
[regenerate_solution_mpy.log](/audit-output/evidence/regenerate_solution_mpy.log)
and
[compare_solution_mpy.log](/audit-output/evidence/compare_solution_mpy.log).

The independent differential program is
[differential_test.py](/audit-output/evidence/differential_test.py).  It imports
the trusted canonical and candidate entry points independently.  It exercised
all three examples, empty-grid and empty-row extras, minimum cases, ceiling
boundaries, 100×100 extrema, every binary rectangular grid through 3×3 for
every capacity 1–10, and 1,000 deterministic random valid grids across the full
dimension range.  All 7,834 cases agreed, with zero mismatches
([differential_test.log](/audit-output/evidence/differential_test.log)).

Stage 2 result: program fidelity passes.  Differential evidence is finite and
is not used as the K proof.

## 3. Clean proof reconstruction

The scratch setup is recorded by
[setup_scratch.sh](/audit-output/evidence/setup_scratch.sh) and
[setup_scratch.log](/audit-output/evidence/setup_scratch.log).  It copied only
candidate source artifacts and the trusted semantics/translator/reference
sources into `/tmp/audit-work/115-max-fill-audit`.  No candidate kompiled
definition or cache was copied.  The live toolchain is K 7.1.293.

Fresh concrete reconstruction:

| Command | Exit/result | Evidence |
|---|---:|---|
| `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | 0 | [stage3_kompile_runtime.log](/audit-output/evidence/stage3_kompile_runtime.log) |
| `krun concrete-tests.mpy --definition runtime-kompiled` | 0; final `.K`, `NoExc`, exit code 0 | [stage3_krun_examples.log](/audit-output/evidence/stage3_krun_examples.log) |

Fresh bridge definition and all four bridge claims:

```text
kompile verification.k --backend haskell \
  --main-module MAX-FILL-DATA --syntax-module MPY-SYNTAX \
  --output-definition bridge-check-kompiled
```

The build exited 0
([stage3_kompile_bridge.log](/audit-output/evidence/stage3_kompile_bridge.log)).
Each claim was selected and run separately; every command exited 0 and printed
`#Top`:

- `MAX-FILL-BRIDGE-SPEC.bridge-sum-empty`:
  [log](/audit-output/evidence/stage3_prove_bridge_sum_empty.log)
- `MAX-FILL-BRIDGE-SPEC.bridge-sum-step`:
  [log](/audit-output/evidence/stage3_prove_bridge_sum_step.log)
- `MAX-FILL-BRIDGE-SPEC.bridge-loop-empty`:
  [log](/audit-output/evidence/stage3_prove_bridge_loop_empty.log)
- `MAX-FILL-BRIDGE-SPEC.bridge-loop-step`:
  [log](/audit-output/evidence/stage3_prove_bridge_loop_step.log)

Fresh target definition:

```text
kompile verification.k --backend haskell \
  --main-module MAX-FILL-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

This exited 0
([stage3_kompile_verification.log](/audit-output/evidence/stage3_kompile_verification.log)).
`sum-fold` alone exited 0 with `#Top`
([log](/audit-output/evidence/stage3_prove_sum_fold.log)).  `fill-loop` needs
the `sum-fold` circularity, so its dependency-closed selection:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC \
  --claims MAX-FILL-SPEC.sum-fold,MAX-FILL-SPEC.fill-loop
```

exited 0 with `#Top`
([log](/audit-output/evidence/stage3_prove_fill_loop_with_sum_fold.log)).
The candidate's complete positive target command:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC
```

also exited 0 with `#Top`
([stage3_prove_max_fill_all_claims.log](/audit-output/evidence/stage3_prove_max_fill_all_claims.log)).
An initially isolated `fill-loop` diagnostic omitted its auxiliary because
`--claims` filters circularities; it was auditor-interrupted and is explicitly
not treated as a target result
([stage3_prove_fill_loop_isolated_interrupted.log](/audit-output/evidence/stage3_prove_fill_loop_isolated_interrupted.log)).

Stage 3 result: all dependency-closed positive claims reconstruct.  This
establishes verification under the candidate's extended theory, not validation
of that theory.

## 4. Adequacy and real-program pinning

### Claims in plain language

- `bridge-sum-empty` and `bridge-sum-step` say that fixed semantics takes one
  `sum` iterator-dispatch step for the empty and cons forms of the real
  `rowVals` representation.
- `bridge-loop-empty` and `bridge-loop-step` say the corresponding one-step
  fact for a `for` loop over the real `gridVals` representation.
- `sum-fold` says that `sum` over the proof-only `symRow(IS)` reaches the
  mathematical `rowTotal`.
- `fill-loop` is a circular loop invariant: for any remaining proof-only
  `symGrid(GS)`, positive `C`, and local accumulator `A`, the loop consumes
  `GS`, changes `result` to `fillTotal(A,GS,C)`, and records the modeled final
  `row` and `water`.
- `max-fill-correct` starts from the normal empty module state and says the
  `#runMaxFill(GS,C)` driver reaches exactly `maxFillSpec(GS,C)` for every
  algebraic `GridRows` and `C > 0`.

The formal domain is unbounded finite `GridRows` of arbitrary integers and any
positive capacity.  It therefore does not narrow the prompt's bounded binary,
rectangular domain.  Rectangularity and the upper bounds are not needed by the
algorithm.

### Function body and result constraint

The reviewer-authored
[program_pinning_check.py](/audit-output/evidence/program_pinning_check.py)
expands `MAX_FILL_LOOP_BODY`, extracts the `Module(FuncDef(...))` loaded by
`#runMaxFill`, and compares its constructor tokens to freshly regenerated
`solution.mpy`.  After deleting only the associative `.Stmts` identity, both
terms contain 135 tokens and are identical
([program_pinning_check.log](/audit-output/evidence/program_pinning_check.log)).
Thus the function binding and body—not merely its name—are exact.

The postcondition is not a free variable or implication: the final `<k>` value
is the concrete recursive function `maxFillSpec(GS,C)`.  A realizable witness is
`GS = gCons(iCons(1,.IntSeq),.GridRows)`, `C = 2`.  Both Python implementations
return 1
([ground_witness_python.log](/audit-output/evidence/ground_witness_python.log)),
and the corresponding ground K execution claim exits 0 with `#Top`
([ground_witness_kprove.log](/audit-output/evidence/ground_witness_kprove.log)).

The loaded body is therefore pinned and the claimed result is discriminating.
The remaining adequacy issue is the value supplied as `grid`: the driver calls
the exact body with `list(symGrid(GS))`, not with the fixed representation
`list(gridVals(GS))`.  Stage 5 audits that operational substitution.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule_inventory.md](/audit-output/evidence/rule_inventory.md) is the complete
generated inventory of the assembled `semantics.k`, all 23 supplied helper K
files, `verification.k`, and `spec.k`.  Its generator and command record are
[build_rule_inventory.py](/audit-output/evidence/build_rule_inventory.py) and
[build_rule_inventory.log](/audit-output/evidence/build_rule_inventory.log).
It contains 967 entries:

- 236 syntax declarations;
- 718 rules;
- 5 contexts;
- 1 configuration;
- 7 claims.

Attributes occur on 150 function entries, 111 total entries, 47 priority
entries, 35 concrete entries, 25 symbol entries, 22 `no-evaluators` entries,
26 `owise` entries, 5 macros, 2 strict entries, 1 seqstrict entry, and 2 token
entries.  There are no `[functional]` or simplification-rule entries.

The 928 fixed-semantics entries are byte-identical to the launcher-selected
supplied semantics.  Each is classified in the inventory as fixed rather than
as a proof extension.  Unused fixed rules cannot contribute to this proof.
The 22 fixed opaque/no-evaluator declarations are in float, sort, hash, or
other paths unused by `solution.mpy`.  No relevant execution value depends on
them.

The used fixed-semantics path is:

| Submitted construct/effect | Fixed declaration and behavior |
|---|---|
| `Module` and statement list | `syntax.k`; `core.k` `#loadAll`, statement sequencing, `.Stmts` |
| `FuncDef`, call frame, parameters, return | `functions.k` and `call.k`; closure binding, left-to-right arguments, scope/stack/ret restoration |
| `Name` | `core.k`; current-scope lookup followed by builtins scope |
| `Assign` and `AugAssign` | `controls.k`; local scope writes and `applyBin` update |
| `Int`, `+`, `-`, `//` | strict syntax, `operators.k`, and `int.k`; unbounded integers and Python-style `pyMod` floor division |
| `For` | `controls.k`; evaluate iterable once, `#loop`, `#iterNext`, target binding, body, loop label |
| list iteration | `list.k`; empty/cons iterator transitions |
| `Call(Name("sum"), row)` | `call.k` builtin resolution and `builtins.k` `#sumAcc/#sumCont` integer fold |
| final `Return(result)` | `functions.k`; ret state, frame pop, and restored caller continuation |

For `C > 0` and integer row elements, these relevant fixed rules preserve
evaluation order, scope updates, loop control, call/return control, and the
expected arithmetic.  The body allocates no collection; the unboxed
read-only-list convention is explicitly part of supplied `core.k`.  No
exceptional or zero-divisor branch is admitted by the entry precondition.

### Proof-local declarations and rules

Every proof-local inventory entry is assessed below; line numbers refer to
`/candidate/verification.k` and `/candidate/spec.k`.

- `verification.k:8-19`: `GridRows`, `rowVals`, and `gridVals` are typed
  algebraic representations with disjoint base/cons equations, full coverage,
  and structural descent.  These are truthful definitional summaries.
- `verification.k:24-41`: `rowSum`, `rowTotal`, `ceilDiv`, `fillTotal`, and
  `maxFillSpec` are structurally terminating mathematical summaries.  For
  `C > 0`, `ceilDiv(N,C)` is exactly the fixed `//` result for
  `N + C - 1`; `fillTotal` is the contract fold.  `ceilDiv` is declared
  `[total]` without guarding `C = 0`; its RHS is then undefined rather than a
  demonstrated false value.  This is a totality-evidence gap outside every
  target precondition, not a witnessed false conclusion and not the decisive
  finding.
- `verification.k:44-57`: `MAX_FILL_LOOP_BODY` is a syntax macro exactly equal
  to the regenerated loop body.
- `verification.k:70-74`: `symRow`, `symGrid`, `#typedSum`, and `#typedLoop`
  are fresh opaque proof-only constructors.  Their values influence loop
  exhaustion, each yielded row and integer, every `sum`, the accumulator, and
  the final postcondition.
- `verification.k:79-117`: these six rules are operational bridges.  The two
  priority-40 dispatch rules preempt generic fixed `#sumAcc`/`#loop` behavior
  for the proof-only values, and the four typed rules fabricate their empty
  and cons iterator transitions.  Their complete match admits an arbitrary
  continuation suffix through the `<k> ... </k>` frame, but changes only the
  active `<k>` cell.  It reads or writes no environment, scopes, heap,
  allocation, stack, return, exception, or exit state.  The four bridge claims
  quantify over arbitrary `K`, `T`, and `B`, so the local one-step context and
  control shape are adequate.  The missing obligation is value/representation
  connection over the entire recursive domain.
- `verification.k:119-128`: `finalRow` and `finalWater` have disjoint,
  descending equations and accurately summarize the last abstract iteration,
  conditional on the `symRow/symGrid` interpretation.
- `verification.k:137-154`: `#runMaxFill` is an exact source driver rather than
  a value summary.  Its body is mechanically pinned.  Its call argument,
  however, is the proof-only `list(symGrid(GS))`, which makes all target
  results depend on the bridges above.
- `spec.k:8-44`: the four bridge claims close under bridge-free
  `MAX-FILL-DATA` and correctly show one fixed-semantics step for each real
  base/cons constructor.  They do not mention `symRow` or `symGrid`, do not
  state a relation between symbolic and real representations, and leave the
  recursive tail as `rowVals`/`gridVals` where the operational bridges leave
  it as `symRow`/`symGrid`.  They are not universal connection theorems for
  the bridges' match domains.
- `spec.k:51-54`: `sum-fold` is a valid induction under the bridge-extended
  theory, but its starting value is `symRow`.
- `spec.k:58-88`: `fill-loop` is a result-bearing invariant under the same
  extended theory.  It starts from `symGrid` and calls `sum-fold` on
  `symRow`.
- `spec.k:91-109`: the target claim composes the exact body and the abstract
  invariant, constraining the result, but inherits the unconnected
  representation.

### Bridge experiments and Gate A finding

The bridge-free test definition
[bridge-free-symbolic.k](/audit-output/evidence/bridge-free-symbolic.k) and
claims
[spec-bridge-connection.k](/audit-output/evidence/spec-bridge-connection.k)
give a concrete operational witness:

1. Under fixed `MAX-FILL-DATA`,
   `#sumAcc(list(rowVals(.IntSeq)),0) => 0` exits 0 with `#Top`
   ([bridge_free_real_empty.log](/audit-output/evidence/bridge_free_real_empty.log)).
2. Merely declaring an opaque sequence, with no candidate bridge, leaves
   `#iterNext(list(symRowBF(.IntSeq))) ~> #sumCont(0)` stuck and exits 1
   ([bridge_free_opaque_empty_expected_fail.log](/audit-output/evidence/bridge_free_opaque_empty_expected_fail.log)).
3. Enabling the candidate bridge makes the corresponding
   `symRow(.IntSeq)` claim exit 0 with `#Top`
   ([bridge_enabled_empty.log](/audit-output/evidence/bridge_enabled_empty.log)).
4. The opposite ground interpretation for a one-element row is rejected:
   asking the bridged sum of `[1]` to be 0 exits 1 with the residual value 1
   ([bridge_enabled_wrong_one_expected_fail.log](/audit-output/evidence/bridge_enabled_wrong_one_expected_fail.log)).

Thus the bridge is result-bearing and genuinely supplies execution absent from
fixed semantics.  The ground cases support the intended interpretation; they
do not prove it universally.

The reviewer then attempted the required bridge-free universal theorem using
the real representations and the exact body.  The complete artifacts are
[real-verification.k](/audit-output/evidence/real-verification.k) and
[spec-real-universal.k](/audit-output/evidence/spec-real-universal.k).
The bridge-free Haskell definition builds successfully
([kompile_real_universal.log](/audit-output/evidence/kompile_real_universal.log)),
but `kprove` exits 1.  Its first universal `real-sum-fold` claim reaches:

```text
#iterYield(V, list(R)) ~> #sumCont(A) ~> K
rowVals(IS) == vCons(V, R)
```

with `V` no longer known to be an integer and `R` no longer connected to an
`IntSeq`.  The exact residual is
[prove_real_universal.log](/audit-output/evidence/prove_real_universal.log).
The candidate's typed bridge exists specifically to bypass this fixed-semantics
loss of structure.

No concrete false result was found for the bridge, so this review does **not**
label its equations mathematically false or claim an unsound-rule witness that
the evidence does not support.  The narrower evidence is conclusive: no
bridge-free universal connection theorem establishes that every execution on
`symGrid/symRow` is the real execution on `gridVals/rowVals`.  The successful
target therefore proves the exact body on a substituted operational input
model, not the real generated program under fixed semantics.  Under the
required Kit operational-bridge contract this fails Gate A and is a material
pinning defect, not a nonfatal documentation concern.

Finally, body sensitivity is positive.  The recorded mutation changes the
actual executed loop body from subtracting 1 to subtracting 2
([verification-body-mutation.patch](/audit-output/evidence/verification-body-mutation.patch),
[body_mutant_diff.log](/audit-output/evidence/body_mutant_diff.log)).  The
mutated definition builds, then its proof exits 1 on the exact mismatch between
the `-2` and `-1` `fillTotal` updates
([kompile_body_mutant.log](/audit-output/evidence/kompile_body_mutant.log),
[prove_body_mutant_expected_fail.log](/audit-output/evidence/prove_body_mutant_expected_fail.log)).
For `grid=[[1]]`, `capacity=2`, the mutant returns 0 while the claimed result is
1.

## 6. Fresh non-vacuity test

The fresh mutation is
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k).  It retains the
required `sum-fold` and `fill-loop` auxiliaries but changes the entry result to:

```text
maxFillSpec(GS, C) +Int 1
```

The witness `grid=[[1]]`, `capacity=2` satisfies the precondition and has real
result 1, while the mutation demands 2.  `kprove --dry-run` exits 0 and emits a
valid backend command, establishing that the mutation parses and builds
([spec_vacuity_dry_run.log](/audit-output/evidence/spec_vacuity_dry_run.log)).
The actual proof exits 1 with `WarnStuckClaimState`; the residual is exactly:

```text
fillTotal(0,GS,C) +Int 1 =/= fillTotal(0,GS,C)
```

See
[spec_vacuity_expected_fail.log](/audit-output/evidence/spec_vacuity_expected_fail.log).
This is the expected unmet result obligation, not a parser error, timeout,
unreachable mutation, or unrelated crash.

Stage 6 result: the candidate theorem is result-constraining and non-vacuous.
This does not repair the Stage 5 real-input connection failure.

## 7. Proven versus assumed accounting

What the successful candidate reachability proof establishes is precise:
conditional on the supplied semantics plus the proof-local operational meaning
assigned to `symGrid` and `symRow`, executing the exact submitted `max_fill`
body on `list(symGrid(GS))` with `C > 0` reaches
`fillTotal(0,GS,C)`.  As a partial-correctness result, it does not independently
claim Python termination outside the modeled finite algebraic inputs.

Trust and assumption ledger:

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 frontend, Haskell/LLVM backends, integer/map/list hooks | All parsing, rewriting, arithmetic, and proof closure | Normal low-level machine-checking trust boundary |
| Byte-identical supplied semantics | Evaluation order, scopes, calls, loops, arithmetic, return | Selected fixed semantics; relevant path audited and rebuilt |
| Trusted translator plus token comparison | Source-to-MPy and MPy-to-driver identity | Acceptable mechanical bridge; byte/token equality recorded |
| `rowSum`, `ceilDiv`, `fillTotal`, `maxFillSpec` | Intended mathematical result | Acceptable on `C > 0`; structurally defined and agrees with bounded prompt arithmetic |
| `symRow`, `symGrid`, `#typedSum`, `#typedLoop` bridges | Every row yielded, loop exhaustion, sums, final result | Illegitimate program-derived operational abstraction without a bridge-free universal connection theorem |
| Four bridge claims | One real constructor transition each | Valid local evidence, but insufficient to relate recursive symbolic executions to real values |
| Differential testing | Implementation/canonical agreement on 7,834 cases | Finite empirical support only; not universal proof |
| Ground and opposite-result probes | Satisfiability and value discrimination | Useful finite validation only |
| Informal structural-isomorphism argument | Intended meaning of symbolic sequences | Insufficient under Kit Gate A because the target depends on it and the machine connection is absent |

Gate accounting:

- Gate A, real-program soundness: **FAIL**.  Body identity, state footprint,
  context containment, body sensitivity, satisfiability, and non-vacuity pass,
  but the result-bearing operational abstraction lacks the required universal
  connection and the target starts from substituted values.
- Gate B, intent adequacy of the mathematical formula: **PASS conditional on
  the abstraction**.  The formal positive-capacity domain covers the source
  contract and the formula is correct.
- Gate C, evidence auditability: **PASS**.  Sources, commands, exits, bounded
  outputs, differential scope, bridge probes, mutation, and trust boundaries
  are preserved.  This cannot override Gate A.

The benchmark decision boundary assigns a proof of a substituted program or
execution model to `FAIL / NOT_LEGIT`.  Clean `#Top` reconstruction and strong
finite evidence do not supply the missing theorem.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
