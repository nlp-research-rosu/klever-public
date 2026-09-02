# Independent adversarial review: 70-strange-sort-list

The candidate program appears extensionally correct, and both submitted positive
claims can be reconstructed to `#Top`. The submitted end-to-end proof is
nevertheless not legitimate. Its decisive step is an ordinary priority rewrite
that replaces the program's while loop with the desired summary. The separately
proved loop claim does not justify that rule over its full match domain. Fresh
fixed-versus-extended and body-sensitivity experiments produce concrete false
conclusions.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `70-strange-sort-list`;
- condition `semantics`;
- `semantics_mode: SUPPLIED_SEMANTICS`;
- `record_layout: legacy-selected-stage1`.

The trusted `/reference/reference-semantics` mount is present, so the rendered
mode and mounts agree. There is no infrastructure breach.

I read the launcher-owned audit input before the candidate. I then inspected
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, `/generation-evidence/invocation.json`,
`metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and every record in the structured trace. Runtime metrics are not
required for this legacy-selected layout and were not reconstructed.

The reproducible integrity command was:

```bash
script -q -e -c '/audit-output/evidence/01_integrity_checks.sh' \
  /audit-output/evidence/01_integrity_checks.log
```

It exited 0. Material results:

- The campaign-lock JSON is exactly equal to the `audit_campaign` block.
- Its SHA-256 is the declared
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- All file hashes checked against `/audit-input.json` match, including the run,
  task, result, invocation, metrics, usage, generation log, generation prompt,
  canonical, prompt, and translator.
- The sole JSONL trace file has SHA-256
  `3062ab55421f22aafd45f528eb389aa15574111cea56ef55a732b0bcfc2d9c58`,
  matching the per-file generation manifest.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounted copies.
- Recursive `diff --no-dereference --recursive` reports the candidate and
  trusted supplied-semantics trees identical. The deterministic per-file
  manifests agree. Neither tree contains a symlink, additional entry, missing
  entry, or mistyped entry.
- No candidate symlink was found.

The complete structured trace was independently parsed by
`evidence/01_trace_inventory.py`: 464 of 464 JSONL records parsed, with zero
malformed records. It inventories 87 command/poll calls, 19 patches, and all
messages and statuses in `evidence/01_trace_inventory.log`. The generation
records claim two `#Top` results and 5,000 tests; those claims were not used as
proof evidence.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract in `/reference/prompt.py` is: for a list of integers,
return a new list by repeatedly taking the minimum remaining integer, then the
maximum remaining integer, alternating until empty. The examples include
`[1,2,3,4] -> [1,4,2,3]`, four equal values unchanged, and the empty list.

The trusted `/reference/canonical.py` implements that description by mutating a
working list with alternating `min`/`max` removal. Candidate
`/candidate/solution.py` instead sorts a copy and traverses it with indices
`i//2` from the low side for even `i` and
`len(ordered) - i//2 - 1` from the high side for odd `i`. This is a different
but valid algorithm. It accepts the full documented list-of-integers domain; it
does not impose a size bound or restrict integer magnitude.

The exact fidelity command was:

```bash
script -q -e -c '/audit-output/evidence/02_program_fidelity.sh' \
  /audit-output/evidence/02_program_fidelity.log
```

It exited 0. Trusted regeneration produced SHA-256
`e3821adc6c256d846d6fd09bdfcc56196e564a2aac16acfe791dfb352b1535ee`
for both submitted and regenerated `solution.mpy`; `cmp` reports byte identity.

The independent differential script is
`evidence/02_differential.py`. It imports the trusted canonical and candidate
entry points independently and uses separate input copies. Its documented
scope is:

- 12 prompt, empty, singleton, even/odd branch-boundary, duplicate, negative,
  reverse-order, and arbitrary-precision cases;
- all 19,531 lists of lengths 0 through 6 over `{-2,-1,0,1,2}`;
- 5,000 seeded lists of lengths 0 through 64 with values in
  `[-10^12,10^12]`.

All 24,543 cases matched, with zero mismatches. This is finite fidelity evidence,
not a universal proof.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/task70`. No candidate
kompiled directory, cache, prior KAST, or prior proof output was copied or used.
Tool versions were K 7.1.293 and Python 3.10.12
(`evidence/03_tool_versions.log`).

Fresh concrete build:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

python3 py2mpy.py /audit-output/evidence/03_concrete_tests.py \
  > audit-concrete-tests.mpy

krun audit-concrete-tests.mpy --definition audit-runtime-kompiled
```

All commands exited 0. The seven reviewer-authored K cases exercise empty,
singleton, size 2/3/4, duplicates, and negative integers. The final
configuration has `.K`, `NoExc`, and exit code 0. Evidence:
`03_compile_runtime.log`, `03_translate_concrete.log`, and
`03_krun_concrete.log`.

Fresh loop-definition build and target proof:

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-base-kompiled

kprove spec.k \
  --definition audit-verification-base-kompiled \
  --spec-module LOOP-SPEC \
  --claims LOOP-SPEC.loop-invariant
```

Both commands exited 0; the proof printed `#Top`. Evidence:
`03_compile_verification_base.log` and `03_loop_proof.log`.

Fresh extended-definition build and target proof:

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.function-correct
```

Both commands exited 0; the proof printed `#Top`. Evidence:
`03_compile_verification.log` and `03_function_proof.log`.

These are the only two positive target claims in `spec.k`, so every submitted
positive target was rerun. Compiler warnings concern incomplete evaluation of
some supplied, mostly unused total functions and unused variables; none is a
failed build. A clean `#Top` establishes closure only under the compiled theory,
which includes the rule rejected in Stage 5.

## 4. Adequacy and real-program pinning

### Plain-language claims

The loop claim starts with the exact loop condition/body, environment 1,
builtins at scope `-1`, a sorted sequence `S` at heap location `HO`, an
accumulator `strangePrefix(S,I,N)` at `HR`, and `0 <= I <= N = vsLen(S)`. It
claims the loop reaches empty computation with `i=N` and accumulator
`strangePrefix(S,N,N)`, preserving the other named cells.

This precondition is satisfiable. For example:

- `S=.ValSeq`, `I=N=0`;
- `HO=0`, `HR=1`;
- `LIST=list(.ValSeq)`;
- result heap entry `.ValSeq`;
- the exact scopes, locations, return, exception, and exit cells shown in the
  claim.

The function claim has no `requires` clause. For every `INPUT:ValSeq`, it calls
the closure with parameter `lst`, definition environment 0, and
`strangeBody()`. It claims return value `ref(1)`, ordered list
`sortVS(INPUT)` at heap location 0, result list
`strangeResult(sortVS(INPUT))` at location 1, two allocations, no exception,
and exit code 0. `INPUT=.ValSeq` and `INPUT=vCons(1,.ValSeq)` are immediate
satisfying entry states.

### Constructor-level identity

`evidence/04_pinning_compare.py` extracts the submitted `FuncDef`, recursively
expands `strangeBody`, `strangeCondition`, and `strangeLoopBody`, normalizes
only whitespace and the parser-equivalent empty `ListExpr(.Exprs)`, and compares
constructor strings. The authoritative rerun is
`04_pinning_compare_v3.log`:

```text
translated-body-sha256=12f3151a...65fe24b
expanded-macro-sha256=12f3151a...65fe24b
PINNING_COMPARISON=PASS
```

It also checks that the entry claim calls precisely
`closureVal(("lst",.ParamNames),strangeBody(),0)` with `list(INPUT)`.
Thus the immutable original entry term is the submitted function body, not a
substituted function. `04_pinning_compare.log` was an initial superseded scanner
run whose comment remover mistakenly treated the string operator `"//"` as a
comment; the corrected v2/v3 script and full printed terms fix that reviewer
bug.

### Ground substitutions and result constraint

`evidence/04_ground_substitution.py` directly evaluates the concrete
`sortVS` insertion equations and the alternating-prefix equations for four
satisfying inputs. For `[4,1,3,2]` it obtains
`sortVS=[1,2,3,4]` and `strangeResult=[1,4,2,3]`, equal to both Python
implementations. Empty, negative/duplicate, and all-equal cases also agree
(`04_ground_substitution.log`).

The returned value is not a free variable: the claim fixes `ref(1)` and the
complete heap value at location 1. Stage 6 independently confirms this by
rejecting a false empty result.

Mechanical pinning and result constraint are therefore adequate for the
original text. They do not cure the execution-bypassing proof rule used to get
from that body to the result.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_rule_inventory.py` scans the fresh source tree and records the
complete text, source line, attributes, per-sentence disposition, and reason for
every local K sentence. The full 354 KB result is
`evidence/05_rule_inventory.log`. Counts:

```text
sentences=945
syntax_declarations=233
rules=706
priority_rules=46
simplification_rules=3
opaque_or_symbol_declarations=26
rejected_sentences=1
```

No local `functional` declaration is present. The inventory includes the
configuration and all contexts, macros, functions, total declarations, opaque
symbols, concrete rules, owise rules, priority rules, simplifications, and the
task-local operational rule.

The recursively identical supplied tree is the selected fixed semantics. I
reviewed every source file. Its clauses fall into these audited groups:

- `syntax.k`: constructor grammar and strictness declarations.
- `core.k`, `call.k`, `functions.k`, `controls.k`: configuration, left-to-right
  evaluation, scope lookup, allocation, calls/returns, assignments, branches,
  and while control.
- `operators.k`, `int.k`, `builtins.k`, `list.k`, `subscript.k`, `sort.k`:
  the material integer/list operations.
- `assert.k`, `bool.k`, `comprehension.k`, `concrete.k`, `dict.k`, `float.k`,
  `iter.k`, `methods.k`, `range.k`, `set.k`, `str.k`, and `tuple.k`: fixed
  support that is constructor- or sort-disconnected from this program, except
  for imported shared declarations. No unused clause can match the target
  control terms or contribute to either target closure.

The material source-to-rules map is:

| Submitted construct | Selected declarations/rules |
|---|---|
| module/function/call/return | `syntax.k`; `core.k` load/sequence; `functions.k` frame/bind/return/pop; `call.k` callee/argument dispatch |
| `sorted(lst)` | name lookup in `core.k`; call dispatch; non-key `sorted` rule and `sortVS` in `sort.k`; allocation in `core.k` |
| assignments and empty list | `controls.k` assignment; `list.k` `ListExpr`/`toList`; allocation |
| while/if | strict comparison plus `controls.k` `While`, `#while`, `#whileCond`, `#branch`, and loop label |
| `len(ordered)` | reference dereference in `call.k`; `applyBuiltin("len")`, `seqLen`, and `vsLen` |
| `%`, `//`, `-`, `+`, `<`, `==` | dispatch in `operators.k`; integer equations and `pyMod` in `int.k` |
| list indexing | reference dereference, `Subscript`, `applyIndex`, `normIdx`, and `valSeqAt` in `subscript.k` |
| `result.append` | attribute/call routing and the in-place heap append rule in `list.k` |
| `i += 1` | `AugAssign` in `controls.k` and integer addition |

Evaluation order, object allocation, calls, stack restoration, and the
`ordered`/`result` heap updates align on this target. Divisors are the constant
2. Under `0 <= I < N`, even index `I//2` and odd index
`N-I//2-1` are both in bounds, so the deliberately opaque out-of-bounds part of
total `valSeqAt` is not used.

The supplied `sortVS` is an explicit trust boundary:
`sort.k` leaves it opaque for symbolic proofs and gives concrete insertion-sort
equations for execution. The operational `sorted` rule and the postcondition
share this symbol. That is not a proof that `sortVS` is a sorted permutation;
the seven K cases, ground substitutions, and 24,543 Python differentials are
only finite evidence. This would be a non-fatal trust limitation if the proof
otherwise passed Gate A.

### Task-local rules

All task-local declarations are inventoried individually.

- `strangeCondition`, `strangeLoopBody`, and `strangeBody` are syntax macros.
  Mechanical comparison establishes their exact source identity.
- `strangePick` is total because `pyMod(I,2)==0` and its negation cover all
  integers; it is unused by either target.
- `strangePrefix` is opaque only at symbolic positive indices, but its base and
  guarded even/odd append equations agree with the actual iteration. The parity
  guards are disjoint. On reachable `I>=0`, the equations inductively
  characterize the sequence used by the loop claim.
- `strangeResult(S) = strangePrefix(S,vsLen(S),vsLen(S))` is a truthful
  definitional summary.
- `0 <=Int vsLen(S) => true [simplification]` follows from the algebraic
  `ValSeq` length and is valid for the target.
- The ordinary while-summary rule at `/candidate/verification.k:94` is
  rejected.

### Rejected operational bridge

The rule matches:

- `#while(strangeCondition(),strangeLoopBody())` with an arbitrary continuation
  because the `<k>` cell has `...`;
- environment 1 and the named local bindings;
- an arbitrary `BS:Scope` at location `-1`;
- ordered and accumulator heap entries;
- fixed scope/heap locations, return, exception, and exit cells;
- any omitted stack cell.

It rewrites the loop directly to completion, sets `i=N`, and fabricates the
final `strangePrefix`, under the invariant equation and range guards. Its
`priority(30)` lets it preempt fixed while execution.

The only purported justification is the `LOOP-SPEC` claim. That claim is proved
against `VERIFICATION-BASE`, but it has the exact empty K continuation and
requires `-1 |-> builtinsScope`. It is not a bridge-free universal connection
theorem over arbitrary continuations, arbitrary stacks, or arbitrary
`BS:Scope`. The candidate added the broader statement as an axiom instead of
proving it. Priority does not supply the missing equivalence.

Two independent witnesses make the defect concrete.

1. **False conclusion in the original theory's accepted domain.**
   `evidence/05_bridge_witness.k` supplies an integer list `[1]`, valid invariant
   state, and an empty root scope lacking `len`. This state satisfies every
   guard and cell pattern of the candidate rule.

   Under fixed `VERIFICATION-BASE`:

   ```bash
   kprove bridge-witness.k \
     --definition audit-verification-base-kompiled \
     --spec-module BRIDGE-WITNESS-BASE \
     --claims BRIDGE-WITNESS-BASE.missing-len-fixed
   ```

   exits 1 and gets stuck at `#look("len",-1)`. Under `VERIFICATION`, the
   identical termination/no-exception claim:

   ```bash
   kprove bridge-witness.k \
     --definition audit-verification-kompiled \
     --spec-module BRIDGE-WITNESS-EXTENDED \
     --claims BRIDGE-WITNESS-EXTENDED.missing-len-bridge
   ```

   exits 0 with `#Top`. The rule therefore concludes successful loop completion
   in a state where fixed semantics cannot even evaluate its condition.
   Evidence: `05_bridge_witness_base.log` and
   `05_bridge_witness_extended.log`.

2. **False result on an actual entry-domain input after a real body change.**
   `evidence/04_verification_body_mutation.k` changes the actual even branch to
   append `ordered[0]`. This is not an external-source-only mutation.
   Constructor comparison against the trusted translation of
   `evidence/04_mutated_program.py` gives identical changed-body hashes
   `8ce1e444...ba7ea` (`04_body_mutation_pinning_compare.log`).

   For the intended input `[1,2,3]`, CPython and fresh K concrete execution of
   that body return `[1,3,1]`, not `[1,3,2]`
   (`04_body_mutation_python.log`, `04_body_mutation_krun.log`). The genuine
   loop claim against fixed semantics exits 1 with an unmet append equation:

   ```bash
   kprove spec.k \
     --definition body-mut-base-kompiled \
     --spec-module LOOP-SPEC \
     --claims LOOP-SPEC.loop-invariant
   # exit 1, WarnStuckClaimState
   ```

   Yet the end-to-end proof with the ordinary summary axiom still exits 0 and
   prints `#Top`:

   ```bash
   kprove spec.k \
     --definition body-mut-verification-kompiled \
     --spec-module SPEC \
     --claims SPEC.function-correct
   # exit 0, #Top
   ```

   Evidence: `04_body_mutation_loop_proof.log` and
   `04_body_mutation_function_proof.log`. The same macro name changes both the
   program loop and the bridge's LHS, while the bridge's desired RHS is
   unchanged. Thus the end-to-end theorem is insensitive to a material change
   in the program operation it claims to summarize.

These witnesses meet the false-conclusion requirement. The first refutes the
original rule over its own match domain. The second demonstrates a false claimed
result for a real source-contract input and shows why no valid
execution-to-summary connection was established.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; none was trusted. I created
`evidence/06_spec_vacuity.k`, which keeps the actual closure, return reference,
allocations, and all final cells, but falsely requires the result list to be
empty for every `INPUT`. `INPUT=vCons(1,.ValSeq)` satisfies the entry
precondition and has nonempty intended output `[1]`.

The mutation first built successfully:

```bash
kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.false-empty-result \
  --dry-run
# exit 0
```

The actual proof command:

```bash
kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.false-empty-result
```

exited 1 with `WarnStuckClaimState`. The residual is the expected unmet
obligation:

```text
.ValSeq
#Equals
strangePrefix(sortVS(INPUT), vsLen(sortVS(INPUT)), vsLen(sortVS(INPUT)))
```

Evidence: `06_vacuity_dry_run.log` and `06_vacuity_proof.log`. This is meaningful
non-vacuity evidence. It establishes that the postcondition constrains the
result; it does not validate the unsound route used to derive that result.

## 7. Proven versus assumed accounting

What the successful K runs actually establish is:

1. Under supplied MPY semantics plus the task-local mathematical summaries, the
   exact-context loop claim closes without assuming the ordinary loop-summary
   rewrite.
2. Under the *extended* theory that additionally assumes the ordinary
   loop-summary rewrite, the exact submitted closure reaches the stated
   `strangeResult(sortVS(INPUT))` heap configuration.
3. The second statement is not a partial-correctness theorem about fixed
   execution because its essential extension is false on its match domain and
   bypasses a body-sensitive computation.

Trust ledger:

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 compiler/prover and built-in integer/map/list logic | All builds and reachability reasoning | Ordinary accepted toolchain boundary |
| Byte-identical supplied MPY semantics | Binding, evaluation, state, calls, lists, control | Accepted selected-semantics boundary for the used fragment; concrete and static checks found no material target mismatch |
| Opaque symbolic `sortVS` plus concrete insertion rules | Ordered list, every selected value, final result | Conditional and empirically supported, not universally proved; non-fatal concern by itself |
| Total opaque `valSeqAt` outside constructor/in-bounds cases | Potential selected values | Acceptable here because the loop guard makes every used index in bounds; OOB behavior is excluded |
| `strangePrefix` / `strangeResult` equations | Loop invariant and postcondition | Acceptable mathematical summaries for reachable nonnegative indices; the exact loop claim provides their fixed-context execution connection |
| Ordinary priority loop-summary rule | Entire loop control, index update, result heap, and end-to-end closure | Illegitimate operational bridge; context containment and body sensitivity fail |
| Mechanical source pinning | Identity of immutable function term | Strong artifact evidence, not semantic correctness |
| Differential and ground tests | Python implementation equivalence and finite sort/summary cases | Finite empirical support only; never substituted for the K proof |

Gate results:

- Gate A, real-program soundness: **FAIL**. The end-to-end `#Top` depends on an
  unsound execution-bypassing rule with explicit false witnesses.
- Gate B, intent/domain adequacy: the candidate program and formal parameters do
  not narrow the unrestricted list-of-integers contract, and the stated summary
  is the intended alternating low/high result conditional on `sortVS`.
  This cannot rescue Gate A.
- Gate C, trust/evidence: reproducible evidence is present, but `sortVS` remains
  an explicit finite-evidence trust boundary. This also cannot rescue Gate A.

The candidate's program may be correct, and its exact loop invariant is useful
partial proof progress. The required end-to-end partial-correctness proof of the
real generated program is not established. Per the benchmark decision boundary,
materially unsound proof rules require `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
