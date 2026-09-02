# Independent adversarial review: 147-get-max-triples

The candidate contains a legitimate partial-correctness proof of the submitted
program over the full stated domain of positive integers. I independently
reconstructed the proof from source, checked program identity, reviewed every
source-level K declaration/rule, and obtained discriminating failures from both
an executed-body mutation and a false postcondition. The generation transcript,
candidate prose, prior builds, and reported `#Top` were not used as proof
authority.

## 1. Input and provenance integrity

`/audit-input.json` is readable and declares:

- problem `147-get-max-triples`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance and a mounted supplied-semantics baseline.

The mode and mounts agree: `/reference/reference-semantics` exists. There is no
infrastructure contradiction.

I read the required launcher and generation records:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- all 226 JSONL events in the sole structured trace at
  `/generation-evidence/codex-trace/2026/07/23/`;
- the present legacy records `legacy-metrics.json` and
  `legacy-run-input.json`.

Historical `runtime-metrics.json` is absent, which is allowed for the declared
legacy-selected-stage1 layout. All layout-required records are present and
readable. The trace is valid JSONL with 226 records, and every one of its 51
tool calls has a paired output. These records merely report the generator's
work; none is trusted as proof evidence.

The campaign-lock object is exactly equal to the `audit_campaign` object in
`/audit-input.json`. Its independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which equals the launcher-recorded hash. Direct hashes of the run manifest,
task manifest, stage result, invocation, metrics, usage, prompt, final answer,
output log, and trace entry also equal their recorded file hashes. See
[provenance_check.log](evidence/provenance_check.log),
[generation_trace_summary.log](evidence/generation_trace_summary.log), and
[generation_output_index.log](evidence/generation_output_index.log).

Candidate input integrity passed:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (`d1dd4d...75b7`);
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (`406485...db16`);
- recursive path/type/link inventories of the candidate and trusted
  `reference-semantics/` trees are identical;
- `diff -qr --no-dereference` reports no content difference;
- neither semantics tree contains a symlink;
- every file in both semantics trees was independently hashed, with identical
  per-path hashes.

All required candidate proof artifacts exist and are regular readable files.
The candidate's `.pyc` is untrusted and was neither needed nor copied. Full
candidate artifact hashes are in
[candidate_artifact_hashes.log](evidence/candidate_artifact_hashes.log).
There is no provenance or mount breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For positive integer `n`, form the length-`n` array
`a_i = i^2 - i + 1` for indices `1 <= i <= n`. Return the number of index
triples `i < j < k` for which `a_i + a_j + a_k` is divisible by 3.

The candidate uses the closed form:

```text
z = floor((n + 1) / 3)
choose(z, 3) + choose(n - z, 3)
```

This is correct for the full contract, not just tested sizes:

1. For `i` congruent to `0, 1, 2` modulo 3, `i^2-i+1` is respectively
   congruent to `1, 1, 0`.
2. A triple drawn from residues only in `{0,1}` sums to 0 modulo 3 exactly
   when it has either zero or three residue-1 members.
3. Among `1..n`, the residue-0 array values occur at indices
   `i == 2 (mod 3)`, of which there are `z = floor((n+1)/3)`.
4. Therefore the valid triples are exactly all triples from those `z` indices
   plus all triples from the other `n-z` indices.

The trusted translator regenerated `solution.mpy` byte-for-byte:

```text
5a0b502c9645b094e28af71a4accb31a8ac0ec8fd5c81947ca3fa6c994b63979
```

An independent differential program imports both the trusted canonical entry
point and the generated entry point. It also uses a third, independently
written direct-combination oracle. It checked:

- the documented `n=5` example;
- the empty `n=0` case (explicitly outside the positive-input contract);
- every integer `0..64`, thereby crossing every modulo-3 branch boundary and
  the choose-three thresholds;
- 100 deterministic random draws with seed 147 (deduplicated into that
  range);
- representative values `8`, `20`, `32`, `48`, and `64`.

There were 65 unique inputs and zero mismatches. The exact script, scope,
oracle, command, and output are in
[differential_test.py](evidence/differential_test.py) and
[stage2_program_fidelity.log](evidence/stage2_program_fidelity.log). The
differential run is finite corroboration; the four-step residue/counting
argument above establishes the general source-contract bridge.

## 3. Clean proof reconstruction

I created `/tmp/audit-work/147-get-max-triples-clean` from source files only.
No candidate `*-kompiled` directory, cache, or `.pyc` was copied. The scratch
inventory is in [setup_scratch.log](evidence/setup_scratch.log).

The toolchain was K `v7.1.293`. I freshly built:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled

kompile verification.k \
  --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled -I .
```

The LLVM execution of the translated six-assertion concrete program ended with
`.K`, `NoExc`, and exit code 0. See
[kompile-llvm.log](evidence/kompile-llvm.log) and
[krun-concrete.log](evidence/krun-concrete.log).

I then selected and ran every positive target claim independently:

| Claim | Exit | Exact success signal |
|---|---:|---|
| `SPEC.residue-0` | 0 | `#Top` |
| `SPEC.residue-1` | 0 | `#Top` |
| `SPEC.residue-2` | 0 | `#Top` |
| `SPEC.get-max-triples-correct` | 0 | `#Top` |

The exact commands and complete bounded outputs are in
[stage3_reconstruction.log](evidence/stage3_reconstruction.log) and the four
`evidence/kprove-*.log` files. The residue claims close by arithmetic
simplification. The entry claim symbolically executes the call and body; it
emits some `DecidePredicateUnknown` warnings during intermediate simplification
but still exits 0 with `#Top`. Those warnings are not stuck states or omitted
claims.

## 4. Adequacy and real-program pinning

### Claim meanings

| Claim | Plain-language precondition and postcondition |
|---|---|
| `residue-0` | For every K integer `Q` (no requires clause), `(3Q)^2-3Q+1` modulo 3 is 1. |
| `residue-1` | For every K integer `Q`, `(3Q+1)^2-(3Q+1)+1` modulo 3 is 1. |
| `residue-2` | For every K integer `Q`, `(3Q+2)^2-(3Q+2)+1` modulo 3 is 0. |
| `get-max-triples-correct` | For every K integer `N > 0`, from the completely specified empty heap/stack/no-exception configuration with `get_max_triples` bound to the submitted closure, calling it with `N` returns `tripleCount(N)` and restores all framed cells. |

All preconditions are satisfiable. `Q=-3..3` witnesses all three residue
claims. `N=1,2,3,4,5,8,20,64` witness the entry precondition. For each listed
`N`, the formal summary, generated Python, trusted canonical Python, and direct
contract oracle agree. See
[adequacy_witness.py](evidence/adequacy_witness.py) and
[adequacy-witness.log](evidence/adequacy-witness.log).

The entry theorem pins the real program:

- trusted regeneration links `solution.py` to `solution.mpy`;
- a mechanical token-level constructor comparison extracts the
  `FuncDef("get_max_triples", Params("n"), ...)` body from `solution.mpy` and
  compares it with the expansion of `getMaxTriplesBody`;
- both sequences contain 195 constructor tokens and are identical
  ([compare_program_term.py](evidence/compare_program_term.py));
- the claim's scope maps the exact name `"get_max_triples"` to a one-parameter
  closure containing that exact body, and the `<k>` cell performs an ordinary
  `Call(Name("get_max_triples"), ...)`;
- the module contains only this function definition, so entering through the
  mechanically identical bound closure omits no module-level material
  operation or control effect.

The postcondition is not a free variable, tautology, or one-way implication.
`tripleCount` is a fully defined arithmetic term. A separate concrete K claim
substituting `N=5` and the ground result `1` also exits 0 with `#Top`; see
[spec-witness.k](evidence/spec-witness.k) and
[kprove-entry-n5.log](evidence/kprove-entry-n5.log).

Body sensitivity also passed. I changed the program term actually stored in the
claim's closure so that its `Return` adds one. I rebuilt that mutant definition.
Its attempted proof against the unchanged result exits 1 with
`WarnStuckClaimState`; the residual explicitly compares
`tripleCount(N)+1` with `tripleCount(N)` under `N>0`. This is an execution-body
mutation, not a change to an unused external source file. See
[verification-body-mutant.k](evidence/verification-body-mutant.k),
[spec-body-mutant.k](evidence/spec-body-mutant.k), and
[kprove-body-mutant.log](evidence/kprove-body-mutant.log).

There are no loops or helper-function calls in the submitted body, hence no
loop/helper claims needing control-flow alignment.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I inventoried every source header beginning `syntax`, `rule`, `claim`,
`configuration`, or `context`, retaining the complete multi-line source blocks
and attributes. The inventory covers 26 K files and 940 headers:

- 699 rules;
- 231 syntax declaration blocks (all continuation alternatives are retained in
  the numbered source);
- five contexts;
- one configuration;
- four claims.

Every entry has a file/line, attributes, target-reachability classification,
and assessment in [K-INVENTORY.md](evidence/K-INVENTORY.md). The complete
numbered source is preserved in
[K-SOURCES-NUMBERED.txt](evidence/K-SOURCES-NUMBERED.txt), and every special
attribute occurrence is indexed in
[K-SPECIAL-ATTRIBUTES.txt](evidence/K-SPECIAL-ATTRIBUTES.txt).

| Source | Headers | Target role and rule-by-rule disposition |
|---|---:|---|
| assembled `semantics.k` | 0 | Imports only; proof imports `MPY`, concrete run imports `MPY-KRUN`. |
| `syntax.k` | 16 | Used declarations/strictness for `Int`, `Name`, `BinOp`, `Assign`, `Return`, `Call`, `FuncDef`, `Stmts`; order is left-to-right. |
| `core.k` | 84 | Used configuration, sequencing, lookup, argument evaluation, literals, dispatch declarations, and list helpers reviewed faithful. |
| `functions.k` | 19 | Used parameter binding, return, frame pop, environment restoration reviewed faithful. |
| `call.k` | 24 | Used callee lookup, argument evaluation, and exact closure dispatch reviewed faithful; no local interception applies. |
| `controls.k` | 37 | Only ordinary local-name assignment is reached; it updates the current frame exactly. |
| `int.k` | 17 | Reached `+`, `-`, `*`, floor `//`, and `pyMod`; divisors are fixed positive 3 and 6. |
| `operators.k` | 12 | Reached ordinary `BinOp` dispatch; no reference/deref priority rule applies. |
| `iter.k`, `range.k` | 1, 8 | Unused by the submitted closed-form body; no target influence. |
| `bool.k` | 14 | Unused by the target execution. |
| `float.k` | 155 | All float/opaque boundaries unused; none occurs in a target term or result. |
| `str.k`, `set.k` | 33, 18 | Unused by the target execution. |
| `list.k`, `tuple.k`, `subscript.k` | 32, 25, 57 | Unused by the target execution. |
| `comprehension.k` | 10 | Canonical Python uses a comprehension, but the submitted program and theorem do not; no candidate substitution is hidden because the optimized submitted body is independently validated against the contract. |
| `methods.k` | 102 | Unused by the target execution. |
| `builtins.k` | 175 | Builtin scope is present, but no builtin is called by the submitted body. |
| `sort.k` | 25 | Opaque sorting boundaries are unused. |
| `assert.k` | 3 | Used only in the independent LLVM smoke program, not in the symbolic target theorem. |
| `dict.k` | 40 | Unused by the target execution. |
| `concrete.k` | 21 | LLVM-only deep equality/keyed-sort rules; absent from the Haskell proof path and unused by the concrete body. |
| `verification.k` | 8 | Four local syntax/function declarations and four equations, reviewed individually below. |
| `spec.k` | 4 | The four target claims, independently executed and audited above. |

Across the source there are 149 syntax declarations carrying `function`, 107
carrying `total`, 22 explicit `no-evaluators` opaque declarations, 45 priority
attributes, 29 `owise` attributes, and 39 `concrete` attributes. There are no
explicit `functional` or `simplification` attributes. These counts and the
compiler warnings are preserved in
[final_evidence_check.log](evidence/final_evidence_check.log).

The LLVM compiler reports six non-exhaustive-totality warnings:
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. These are
real limitations of the supplied partial Python model, not proof-local rules.
None of the six symbols is reachable from this body, precondition,
postcondition, or target arithmetic. The 22 opaque symbols similarly concern
floats, sorting, and MD5 only; no opaque value can influence this theorem.
Consequently they create no false target conclusion or result-bearing oracle
for this proof.

### Construct-to-rule map and state/control audit

| Submitted construct | Declaration and reached behavior |
|---|---|
| `FuncDef`/`Params`/`Module` | `syntax.k`; module binding is mechanically supplied as the exact closure. No module side effect exists. |
| `Call` | `call.k`: evaluate callee, then argument; exact `closureVal` dispatch pushes a frame. |
| `Name` | `core.k`: lookup starts at `<env>` and finds the exact local binding before builtins. |
| `Int` | `core.k`: literal becomes the corresponding K mathematical integer. |
| `BinOp` | `syntax.k` `seqstrict(2,3)`, then `operators.k` dispatch and `int.k` arithmetic; left-to-right evaluation is preserved. |
| `Assign` | RHS strictness, then `controls.k` writes the current scope. |
| `Return` | expression strictness, then `functions.k` stores the return, discards the remaining callee body, pops the exact saved frame, and restores environment/scope state. |
| statement sequence | `core.k` executes the head and retains the tail in the continuation. |

The body allocates nothing, performs no external call, raises no modeled
exception, and mutates only locals in the fresh call frame. Frame creation and
pop restore `<env>`, `<scopes>`, `<scopeLoc>`, `<stack>`, and `<ret>`;
`<heap>`, `<heapLoc>`, `<exc>`, and `<exit-code>` remain unchanged. The claim
pins all of these cells.

### Proof-local extension audit

| Extension | Classification | Domain/context | Value/control justification |
|---|---|---|---|
| `getMaxTriplesBody` | Definitional body abbreviation | One unguarded `Stmts` equation; expands wherever the name occurs | Exact 195-token constructor identity with the translated submitted body; it skips no operation. Body mutation is rejected. |
| `chooseThree(C)` | Definitional mathematical summary | All K integers; used as a count only for nonnegative `C` | Exact floor-division arithmetic. One terminating equation, no overlap, no opaque value. It does not rewrite program syntax. |
| `zeroResidues(N)` | Definitional mathematical summary | All K integers; counting interpretation used under `N>0` | Exact `floor((N+1)/3)` arithmetic. One terminating equation, no overlap, no operational interception. |
| `tripleCount(N)` | Definitional postcondition summary | All K integers; theorem requires `N>0` | Composition of the two preceding truthful equations. It occurs on the target side, not as an execution oracle. |

There is no proof-local priority rule, ordinary operational bridge, opaque
symbol, `total` declaration, simplification rule, or unconstrained fresh value.
The residue claims are not axioms needed by the entry claim: selecting the
entry claim alone still gives `#Top`. The program independently computes the
arithmetic that the target-side definitions denote.

I found no unsound rule affecting the theorem and therefore have no false-rule
witness to report. The narrower unused totality/coverage gaps are documented
as such rather than mislabeled unsoundness.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; no candidate mutation was trusted.
I authored a fresh mutation that keeps the actual submitted closure and complete
initial configuration but changes the ground `N=5` result obligation from the
true value `1` to the false value `2`.

First, `kprove --dry-run` parsed and built the mutation successfully with exit
0. The actual proof then:

- executed the submitted body to the ground K result `1`;
- failed to unify it with destination `2`;
- emitted `WarnStuckClaimState`;
- emitted the expected “cannot be rewritten further” prover error;
- exited 1.

This is a reached, meaningful unmet result obligation, not a parser error,
missing import, timeout, or unrelated crash. See
[spec-vacuity.k](evidence/spec-vacuity.k),
[kprove-vacuity-dry-run.log](evidence/kprove-vacuity-dry-run.log), and
[kprove-vacuity.log](evidence/kprove-vacuity.log).

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY semantics, for every mathematical integer `N > 0`, an
ordinary call to the exact submitted `get_max_triples` closure from the stated
clean configuration reaches:

```text
chooseThree(floor((N+1)/3))
+ chooseThree(N - floor((N+1)/3))
```

with the same environment, scope store, heap, allocation counters, empty
stack, no pending return, no exception, and exit code 0. It also universally
establishes the three residue identities in `spec.k`.

This is a partial-correctness reachability result. It is not a proof of the
entire CPython language or of unused semantics modules.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser/compiler/Haskell prover and mathematical `Int` hooks | All machine-checking | Standard unavoidable checker trust; exact versions and outputs recorded. |
| Trusted `/reference/py2mpy.py` | Python-to-constructor identity | Acceptable launcher-provided bridge; byte identity is independently re-established. |
| Supplied MPY rules for call, scopes, integer expressions, assignment, and return | Entry execution | Acceptable for this target after rule/control/state review and concrete execution. |
| Elementary residue/combinatorial argument from `tripleCount` to the English contract | Intent adequacy | Acceptable and complete over all positive integers; independently written above, supported but not replaced by differential testing. |
| Finite Python differential run | Implementation/intent corroboration on `0..64` | Empirical support only; not treated as a universal proof. |
| 22 float/sort/MD5 opaque symbols and six unused totality gaps | No target claim | Explicitly outside the dependency cone; they affect neither control nor result here. |
| Termination outside the proved execution/model and behavior for non-positive inputs | None | Outside the source contract; `n=0` was tested only as a robustness boundary. |

Gate A (real-program soundness) passes: exact body, faithful reached rules,
result-constraining target, body sensitivity, and false-postcondition rejection.
Gate B (intent adequacy) passes: `N>0` is exactly the source domain and the
summary counts precisely the contract's triples without a finite bound. Gate C
(trust/evidence auditability) passes: commands, sources, positive outputs,
ground witnesses, differential scope, and negative residuals are preserved.
The evidence manifest is [SHA256SUMS](evidence/SHA256SUMS).

VERDICT: PASS
LEGITIMACY: LEGIT
