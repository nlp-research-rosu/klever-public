# Independent adversarial audit: 126-is-sorted

## Decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted translated program under the supplied MPY semantics.
Fresh reconstruction proved the loop circularity and the full entry theorem,
the submitted Python and MPY artifacts are faithful, and reviewer-authored
false-result and changed-body probes were rejected for the intended reasons.

The verdict is `CONCERNS / LEGIT`, rather than an unconditional pass, because
the Haskell proof deliberately leaves the supplied builtin `sortVS` opaque.
The K theorem proves the program result in terms of that fixed external
primitive. Its interpretation as the actual ascending permutation—and
therefore the last bridge to the English contract—is a named assumption
supported by ordinary mathematics and finite fresh concrete tests, not a
machine-checked theorem in this proof.

This review does not rely on the candidate’s `#Top`, compiled definitions,
`PROOF.md`, logs, trace, or final report.

## 1. Input and provenance integrity

### Infrastructure and rendered-mode check

The rendered mode is `SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, as required; there is no mode/mount
contradiction and therefore no infrastructure breach. The live toolchain is K
v7.1.293 ([toolchain-version.log](evidence/toolchain-version.log)).

The candidate’s `reference-semantics/` and trusted
`/reference/reference-semantics/` have identical recursive path sets, entry
types, sizes, and bytes. There are no missing or additional entries and no
symlinks. The candidate prompt and translator are byte-identical to their
trusted mounts:

| Artifact | SHA-256 | Result |
|---|---|---|
| `prompt.py` | `050a2b9defc209aa64d0777939ff3387ee7db918434d818789eab7b36578b7ca` | candidate = trusted |
| `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | candidate = trusted |
| supplied semantics tree | recursive manifest and byte diff | candidate = trusted |

All required candidate artifacts are ordinary files or, for the semantics,
ordinary directories. No required artifact is missing, changed, mistyped,
extra within the supplied-semantics tree, or symlinked. Candidate-provided
`runtime-kompiled/`, `verification-kompiled/`, and `__pycache__/` exist but
were ignored and never copied into the fresh reconstruction.

Evidence: [stage1_integrity.sh](evidence/stage1_integrity.sh) and
[stage1-integrity.log](evidence/stage1-integrity.log).

### Untrusted generation claims

`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, the
structured JSONL trace, and `PROOF.md` were read only as claims. They report a
successful generation, two positive `#Top` results, mutation failures, and
differential counts. None of those reports is used as proof evidence here. The
bounded provenance record, sizes, and hashes are in
[stage1-untrusted-claims.log](evidence/stage1-untrusted-claims.log).

**Stage 1 result: PASS.**

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and canonical behavior

For a finite list of nonnegative integers, `is_sorted` must return `true`
exactly when:

1. every adjacent pair is nondecreasing; and
2. no integer occurs more than twice.

Thus two equal occurrences are allowed, while a third occurrence makes the
result false. The trusted canonical implementation first counts every value,
rejects a count greater than two, and then checks adjacent `<=`.

The submitted `solution.py` uses a different but equivalent algorithm on the
intended domain: it initializes the result with
`lst == sorted(lst)`, scans every element, and forces the result to false if
that element’s count exceeds two. For integer lists, equality with the
ascending sort is equivalent to nondecreasing order.

### Translation identity

The trusted `/reference/py2mpy.py` regenerated `solution.mpy` from the
submitted `solution.py`. The regenerated and submitted MPY files are
byte-identical:

```text
solution.py              f85923d01385f7f1282a600f8938658b1d828b38c0d64382e7b5d8f1cc01545c
solution.mpy             d011eee3dce343389eac2165a93d67231e7c859869890db485da9f7d51d216e5
regenerated-solution.mpy d011eee3dce343389eac2165a93d67231e7c859869890db485da9f7d51d216e5
```

Evidence:
[stage2_translation.sh](evidence/stage2_translation.sh) and
[stage2-translation.log](evidence/stage2-translation.log).

### Independent differential test

The reviewer-authored test imports the trusted canonical entry point and the
generated entry point independently. Its oracle uses adjacent comparisons and
`Counter`, not `sorted` equality or repeated `list.count`. The 20,480 unique
inputs include:

- all eight documented examples;
- empty, singleton, order-direction, exactly-two, exactly-three, and
  exactly-four multiplicity boundaries;
- zero and 100-digit nonnegative integers;
- every list over `0..4` of lengths `0..6`;
- 939 additional deterministic random lists of lengths through 30.

All canonical, generated, and independent-oracle results were Boolean and
equal; mismatches were zero. The complete JSONL input corpus has SHA-256
`9cfdd953e5eac96ed884b77b10d0290dc805ac6bf885cfb937cbef4356036052`.

Evidence:
[stage2_differential.py](evidence/stage2_differential.py),
[stage2-inputs.jsonl](evidence/stage2-inputs.jsonl), and
[stage2-differential.log](evidence/stage2-differential.log).

**Stage 2 result: PASS.**

## 3. Clean proof reconstruction

Only source files and the candidate’s byte-identical supplied-semantics tree
were copied to `/tmp/audit-work/scratch`. No candidate definition, KORE file,
cache, or Python bytecode was reused.

### Fresh builds

| Command purpose | Definition | Exit | Evidence |
|---|---|---:|---|
| LLVM concrete build | `runtime-fresh-kompiled` | 0 | [stage3-kompile-runtime.log](evidence/stage3-kompile-runtime.log) |
| Haskell proof build | `verification-fresh-kompiled` | 0 | [stage3-kompile-verification.log](evidence/stage3-kompile-verification.log) |

The runtime compiler repeated fixed-baseline warnings about globally
non-exhaustive total functions. The warned functions are off the submitted
program path and are accounted for in Stage 5; they are not candidate-added
rules.

### Fresh positive proofs

The loop circularity was selected and proved independently:

```text
kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant
#Top
EXIT_STATUS: 0
```

Evidence:
[stage3-kprove-loop-invariant.log](evidence/stage3-kprove-loop-invariant.log).

The complete spec, containing the entry target together with the auxiliary
loop circularity it requires, also proved:

```text
kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC
#Top
EXIT_STATUS: 0
```

Evidence: [stage3-kprove-full-spec.log](evidence/stage3-kprove-full-spec.log).
This is the positive entry-proof command: filtering to the entry label alone
removes its circularity and changes the proof problem. For transparency, that
diagnostic-only filtered run was interrupted while actively searching and is
not verdict evidence; see
[stage3-isolated-entry-diagnostic.md](evidence/stage3-isolated-entry-diagnostic.md).

Both required positive targets therefore close in the fresh reconstruction
with literal `#Top` and exit 0.

**Stage 3 result: PASS.**

## 4. Adequacy and real-program pinning

### Plain-language meaning of each claim

`SPEC.loop-invariant` has no explicit `requires`. Its starting state says:
inside the real `is_sorted` call, with full original list `INPUT`, Boolean
local `RESULT`, and remaining iterator `REST`, execute the real loop from that
point, then execute the real `Return(result)` and `#endcall`. The destination
is `scanCounts(INPUT, RESULT, REST)`, with the local scope removed and the
caller restored. The claim fixes the exact module and local bindings, sorted
heap object, heap counter, one caller frame, return cell, exception cell, and
exit code.

`SPEC.is-sorted` requires `nonNegativeInts(INPUT)`: `INPUT` is a finite
`ValSeq`, every element has K sort `Int`, and every integer is at least zero.
It loads the exact submitted function definition into the empty module scope,
resolves and calls that closure on `list(INPUT)`, and returns

```text
scanCounts(INPUT, INPUT ==K sortVS(INPUT), INPUT)
```

while fixing the final module binding, one sorted-list heap allocation,
restored scope counter, empty stack, `noRet`, `NoExc`, and exit code zero.

### Actual program and control-flow pinning

`isSortedFunctionBody` expands constructor-for-constructor to the submitted
`solution.mpy`: the sorted equality assignment, initial `current = 0`, real
`For`, real count/threshold `If`, and real `Return`. The entry `<k>` loads that
body and calls its actual module binding. There is no rule that replaces the
function call, loop, count, or return with an oracle. The auxiliary loop claim
matches the actual `#loop` control point and an exact trailing continuation;
it does not accept an arbitrary suffix.

The postcondition has no fresh or unconstrained result variable. It fixes the
returned Boolean to a total structural summary connected to real loop
execution by the focused claim. A reviewer-authored changed-body claim
successfully parsed, executed the changed body to `false`, and failed against
the requested `true`, proving body sensitivity:

- build/dry run exit 0:
  [stage4-body-sensitivity-dry-run.log](evidence/stage4-body-sensitivity-dry-run.log);
- proof exit 1 with `WarnStuckClaimState`, residual `false`:
  [stage4-body-sensitivity-proof.log](evidence/stage4-body-sensitivity-proof.log);
- source:
  [audit-body-sensitivity.k](evidence/audit-body-sensitivity.k).

### Satisfiable witnesses and concrete substitution

The empty list satisfies the entry precondition, as do all five ground cases
below:

| Input | Formal ground summary | Canonical | Generated | Fresh K |
|---|---:|---:|---:|---:|
| `[]` | true | true | true | true |
| `[0,0]` | true | true | true | true |
| `[0,0,0]` | false | false | false | false |
| `[1,0]` | false | false | false | false |
| `[0,10^40]` | true | true | true | true |

The concrete harness’s first function AST is identical to `solution.py`.
Fresh LLVM execution ended with `.K`, `NoExc`, exit code zero, and exactly
those five result bindings. Evidence:
[stage4_ground_checks.py](evidence/stage4_ground_checks.py),
[stage4-ground-python.log](evidence/stage4-ground-python.log),
[stage4_concrete.mpy](evidence/stage4_concrete.mpy), and
[stage4-ground-krun.log](evidence/stage4-ground-krun.log).

**Stage 4 result: PASS.**

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The source-level inventory contains every `configuration`, `context`, local
`syntax`, `rule`, and `claim` in the supplied semantics, helper K files,
`verification.k`, and `spec.k`: 946 items total. The assembly
`reference-semantics/semantics.k` has zero local declarations/rules; it only
requires files and assembles modules.

The inventory includes 148 function-tagged declarations, 109 total
declarations, 45 priority-tagged items, 35 concrete-tagged items, 27 `owise`
items, 25 symbols, 22 `no-evaluators` items, and six macro-tagged items. There
are zero `functional` and zero `simplification` items. It gives source,
line span, complete text, tags, origin, and a disposition for every item.

Evidence:
[stage5_inventory.py](evidence/stage5_inventory.py),
[stage5-rule-inventory.md](evidence/stage5-rule-inventory.md), and
[stage5-inventory.log](evidence/stage5-inventory.log).

Items K-0001 through K-0928 are byte-identical members of the trusted selected
semantics. In this supplied-semantics mode they define the fixed language
level rather than candidate proof extensions. Each is individually marked as
such in the inventory. This is not a claim that the complete MPY subset is
CPython: reachable model boundaries are still accounted for below, and the
exact paths used by this program were reviewed in detail.

Items K-0929 through K-0946 are all proof-local declarations, rules, and
claims. Every one has an individual hand decision and justification in
[stage5-proof-local-review.md](evidence/stage5-proof-local-review.md). All are
sound:

- the two macros exactly name submitted source constructors;
- `nonNegativeInts` has exhaustive, disjoint empty/int/non-int cases;
- `nextCountResult` has disjoint and exhaustive `> 2`/`<= 2` guards;
- `countArgument` has exact `ref(0)` and `owise` coverage and is used only in
  the loop claim’s pinned heap context;
- `scanCounts` has exhaustive empty/cons cases and strictly descends on the
  tail;
- `intendedSorted` is a definition of the exact initial result plus scan;
- the loop and entry reachability claims pin complete configurations.

There are no proof-local priority rules, simplification equations, opaque
symbols, or operational `<k>` bridge rules. No proof-local rule replaces
program execution. No inventoried rule is labeled unsound, so no
unsound-rule false-conclusion witness is applicable.

### Used constructs, cells, evaluation, and control

[stage5-used-construct-map.md](evidence/stage5-used-construct-map.md) maps every
construct in `solution.mpy` to its syntax and rules: module loading, function
definition and closure binding, lookup, left-to-right calls, assignments,
sorted allocation, list equality, integer comparison, for/list iteration,
target binding, method dispatch and argument dereference, `count`, `if`, and
return/frame pop.

The used path preserves:

- the fixed ten-cell configuration;
- callee-before-argument and left-to-right argument evaluation;
- local/module/builtin binding and shadowing;
- one sorted-list heap allocation and monotone heap counter;
- exact loop order and local updates;
- actual return, frame removal, environment restoration, no exception, and
  zero exit code.

Reachable priorities only ensure heap-object dereference before generic
dispatch. All are trusted-baseline rules and none bypasses the submitted
body. The fresh body-sensitivity failure corroborates this static conclusion.

The fixed-semantics compiler warned about `mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and `valSeqAt` totality. None is reachable from this AST
on the formal integer-list domain. The narrower fact is recorded as an
off-path model limitation; the warnings are not mislabeled as unsound
candidate rules.

### Result-bearing opacity: `sortVS`

Only one supplied opaque symbol is reachable: K-0773,
`sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]`.
The builtin `sorted` rule allocates `list(sortVS(INPUT))`. The Haskell proof
does not establish that `sortVS` is the ascending permutation. It is an
externally trusted boundary, not a program-derived abstraction:

- `sorted` is a fixed builtin outside `is_sorted`;
- the proof is interpretation-parametric and states the exact result in terms
  of `sortVS`;
- the report’s English conclusion is explicitly conditional on its ascending
  permutation contract;
- no opposite-interpretation or connection theorem is incorrectly claimed.

The LLVM definition has concrete insertion-sort equations. An independently
generated 348-case corpus—named boundaries plus every list over `0..3` of
length through four—was executed in nine bounded batches. Every batch
translated and ran with `NoExc`, exit cell zero, and zero assertion failures.
Evidence:
[stage5_k_differential_batched.py](evidence/stage5_k_differential_batched.py),
[stage5-k-batched-inputs.jsonl](evidence/stage5-k-batched-inputs.jsonl),
[stage5-k-differential-batched.log](evidence/stage5-k-differential-batched.log),
and [stage5-k-batches](evidence/stage5-k-batches/).

An initial single oversized 348-case generated AST caused the Java parser to
be killed with exit 137 before execution. This is preserved in
[stage5-k-differential.log](evidence/stage5-k-differential.log) as an
infrastructure event, not candidate evidence. The same input corpus then
passed in bounded batches.

**Stage 5 result: PASS for real-program soundness, with a documented
intent-bridge limitation.**

## 6. Fresh non-vacuity test

The candidate’s `spec-vacuity.k` was not reused. The reviewer-authored
[audit-nonvacuity.k](evidence/audit-nonvacuity.k) uses concrete input `[0,0]`.
That input satisfies `nonNegativeInts`; the formal summary, both Python
implementations, and fresh K execution all return `true`. The mutation changes
the result-constraining destination to `false`.

The mutation parsed and compiled successfully under `--dry-run` with exit 0:
[stage6-nonvacuity-dry-run.log](evidence/stage6-nonvacuity-dry-run.log).
The real proof then exited 1 with `WarnStuckClaimState`. Its residual is the
complete expected final configuration with:

```text
<k> true ~> .K </k>
```

while the target requires `false`. This is an expected unmet result obligation,
not a parser error, missing import, timeout, unreachable mutation, or unrelated
crash. Evidence:
[stage6-nonvacuity-proof.log](evidence/stage6-nonvacuity-proof.log).

**Stage 6 result: PASS.**

## 7. Proven versus assumed accounting

### Precisely what the reachability proof establishes

Under the selected MPY theory, for every finite K `ValSeq INPUT` consisting
only of integers `>= 0`, the actual submitted body is loaded, bound, called,
and symbolically executed. As a partial-correctness statement, any covered
terminating execution reaches:

```text
scanCounts(INPUT, INPUT ==K sortVS(INPUT), INPUT)
```

as the returned Boolean, with the final scopes, allocation, heap counter,
stack, return cell, exception cell, and exit code fixed by `SPEC.is-sorted`.
The universal loop claim establishes that fixed loop execution implements
`scanCounts`; this connection is proved, not assumed.

Conditional on the external contract that `sortVS(INPUT)` is the ascending
permutation of an integer sequence:

- `INPUT == sortVS(INPUT)` exactly characterizes nondecreasing order; and
- the structural scan returns true exactly when no occurring integer has
  multiplicity greater than two.

Those facts give the natural-language contract. The proof is partial
correctness and does not separately prove total termination or resource bounds.

### Trust ledger

| Boundary | Status and influence | Assessment |
|---|---|---|
| Supplied MPY semantics | Trusted mounted language model; controls all value, state, allocation, binding, exception, and control behavior | Acceptable by the rendered `SUPPLIED_SEMANTICS` condition; candidate copy is byte-identical. Used paths were also reviewed and concretely exercised. |
| `sortVS` ascending-permutation meaning | Opaque in Haskell; determines the initial list equality, final Boolean, and sorted heap value | Concerning but legitimate external builtin boundary. The formal theorem is parametric/conditional, and 348 fresh LLVM cases support but do not prove the contract. |
| `py2mpy.py` correctness | Connects `solution.py` to the K AST | Acceptable with limitation: trusted translator is byte-identical and regeneration gives exact submitted MPY, but translator correctness is not proved in K. |
| Canonical-to-English alignment | Trusted reference implementation plus prompt interpretation | Supported by direct source inspection and 20,480 independent differential/oracle cases; finite testing is not universal proof. |
| Mathematics of the structural scan | Tail recursion and threshold reasoning connect the K summary to “multiplicity at most two” | Acceptable ordinary mathematical argument; the stronger and essential program-to-summary connection is machine-checked by the loop claim. |
| K v7.1.293 compiler, Haskell/LLVM backends, and host | Trusted computing base for build, proof, and execution | Necessary proof-checker boundary; positive/negative reconstruction results are reproducible in the logs. |

There is no proof-local trusted primitive, opaque program-derived value,
execution-bypassing rewrite, or empirical bridge presented as a universal K
theorem. Differential evidence supports only the tested Python/K behavior and
the external sort interpretation.

### Gate summary

- **Gate A, real-program soundness: PASS.** Exact body, binding, control,
  state, universal loop connection, result constraint, body sensitivity, and
  non-vacuity all pass.
- **Gate B, intent adequacy: LIMITED BUT LEGIT.** The formal input domain
  matches the prompt and the implementation matches the canonical behavior,
  but the final ascending-sort bridge is conditional on opaque `sortVS`.
- **Gate C, trust and evidence auditability: PASS.** Every boundary and
  dependent result is named; scripts, complete deterministic input corpora,
  commands, statuses, and bounded outputs are preserved. Finite evidence is
  not overstated.

The opacity is a documented evidence/intent limitation, not a false rule, free
result, substituted program, or missing proof. It therefore warrants
`CONCERNS / LEGIT` under the requested decision boundary.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
