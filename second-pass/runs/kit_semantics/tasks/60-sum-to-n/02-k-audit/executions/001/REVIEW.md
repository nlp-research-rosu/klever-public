# Independent adversarial audit: 60-sum-to-n

## Audit outcome

The candidate contains a legitimate partial-correctness proof of the submitted
program over the full modeled integer domain. I rebuilt both K definitions from
source, independently reran the claims, checked the translated program and
entry configurations constructor-for-constructor, reviewed the proof-local
theory and every supplied-source record, and rejected a fresh false result
claim after real execution. The decision does not rely on the candidate's
`PROOF.md`, compiled directories, logs, or prior `#Top`.

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` is a readable regular file and declares:

- `record_layout = pipeline-v3`
- `problem_id = 60-sum-to-n`
- `condition = kit-semantics`
- `semantics_mode = SUPPLIED_SEMANTICS`
- `mount_reference_semantics = true`

All launcher-declared `container_paths` resolve to real regular files or real
directories. The required pipeline-v3 records are present and readable:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured JSONL trace. No required
record is a symlink or special file.

The independent checker
`evidence/integrity_check.py` recomputed all declared regular-file SHA-256
values. The run, task, result, invocation, metrics, runtime metrics, usage,
generation prompt/output/last message, canonical source, trusted prompt,
translator, and campaign-lock hashes all match `/audit-input.json`.
`/audit-campaign-lock.json` is exactly equal as a JSON object to the
`audit_campaign` block, and its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The task manifest equals the audit manifest after removing the launcher's
additional `config` field, whose value separately matches the declared config.

The structured trace consists of one declared JSONL file with 311 parseable
records. Its file SHA-256 is
`d1eafe93e5872fa1e13cdba128fe8156b27fe5b97757ed77f6916cb498d7838f`;
its independently reconstructed pipeline tree hash is
`749932cf7f16f2a5edd88873ee75414019a14452ad5bee32a18f7d2dac13c32e`,
matching `usage.json`. The mounted candidate's pipeline tree hash is
`e5d3e652af2aa929b8c27947a6d9f4ad152b595731c3f083dfd8be4ee1c8a14c`,
matching the workspace hash in both the invocation and generation result.
Exact values and status 0 are in `evidence/stage1_integrity.log`.

### Supplied-semantics boundary

The rendered mode and mounts agree: `/reference/reference-semantics` exists.
I recursively compared it with `/candidate/reference-semantics`, rejecting
links and special entries and comparing every relative entry and every byte.
Both contain the same 24 regular K files, no missing or additional entry, and
no symlink. Their independently computed framed tree hash is
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
matching the trusted semantics manifest hash. The candidate `prompt.py` and
`py2mpy.py` are likewise byte-identical to their trusted mounts. This baseline
does not bless `verification.k`; that file is audited below as proof-local
theory.

The required candidate proof artifacts are real nonempty regular files:
`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
`PROOF.md`. Candidate-built `runtime-kompiled`,
`verification-kompiled`, and `__pycache__` were never copied into or used by
the reconstruction.

### Untrusted generation claims

I read the generation records, 20,029-line text log, and structured trace only
as provenance evidence. They claim a successful final `./prove.sh`, `#Top`,
2,001 differential tests, and two rejected mutations. They also record earlier
interrupted diagnostics and the eventual dependency on the loop circularity.
`evidence/summarize_generation_trace.py` and
`evidence/stage1_generation_trace_summary.log` give a bounded inventory of all
51 structured function calls, event counts, assistant messages, and claimed
markers. None substitutes for the fresh work below.

Stage 1 result: **PASS; no infrastructure breach**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

`/reference/prompt.py` says that `sum_to_n(n: int)` sums the integers from 1
through `n`, with examples:

- 30 maps to 465;
- 100 maps to 5050;
- 5 maps to 15;
- 10 maps to 55;
- 1 maps to 1.

The trusted canonical implementation is `sum(range(n + 1))`. Thus, for an
integer `n > 0`, it returns the inclusive triangular sum; for `n <= 0`, the
Python range is empty and it returns 0.

The candidate implementation initializes `total = 0`, repeatedly adds the
current positive `n` and decrements `n`, then returns `total`. It follows the
same two branches for every integer. It is a different algorithm but not a
contract change.

### Trusted regeneration

In `/tmp/audit-work/reconstruction`, I copied the candidate source proof
artifacts, the trusted translator, and the trusted supplied-semantics sources.
I ran:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp regenerated-solution.mpy solution.mpy
```

Both commands exited 0. Both `.mpy` files have SHA-256
`31e7bf9a0696667a2704263df1005e67c104bbf4ecbe95a641af446f2b425341`.
See `evidence/stage2_translation_and_pinning.log`.

### Independent differential test

`evidence/differential_test.py` separately imports the trusted canonical entry
point and the scratch candidate entry point. It covers all five examples,
negative values, the guard-adjacent values `-1`, `0`, `1`, and `2`, additional
small boundaries, 400 deterministic generated integers in
`[-10000, 10000]`, and large signed powers of ten. The exact command was:

```text
python3 /audit-output/evidence/differential_test.py
```

It exited 0 with 426 cases and zero mismatches. Boundary results, inputs, and
status are in `evidence/stage2_differential.log`. These tests support the
implementation-to-canonical bridge; they are not used as a universal proof.

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

### Clean build inputs and toolchain

The scratch reconstruction initially contained only source files and the
trusted supplied-semantics tree. The K tools are independently installed at
`/usr/bin/kompile`, version 7.1.293; Python is 3.10.12. See
`evidence/tool_versions.log`.

### Concrete definition and execution

I created the reviewer-authored `evidence/concrete_smoke.py`, translated it
with the trusted translator, and ran:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-smoke.mpy --definition runtime-kompiled
```

LLVM compilation exited 0. Its warnings concern supplied, unused,
non-exhaustive total helpers for strings, floats, and subscript access; none is
reachable from this program. Concrete execution checked `-3`, `-1`, `0`, `1`,
`2`, `5`, `30`, and `100`, exited 0, and finished with `<k> .K </k>`,
`<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`. Logs are
`evidence/stage3_llvm_build.log` and `evidence/stage3_krun.log`.

### Proof definition and all positive claims

I built a new Haskell definition:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0; its only warnings are unused pattern variables in the supplied
`str.k`. The log is `evidence/stage3_haskell_build.log`.

The actual required target command was:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

It printed `#Top` and exited 0, proving all three claims together. I also
checked the claim dependencies explicitly:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC \
  --claims SPEC.sum-loop

kprove spec.k --definition verification-kompiled --spec-module SPEC \
  --claims SPEC.sum-to-n-empty-range

kprove spec.k --definition verification-kompiled --spec-module SPEC \
  --claims SPEC.sum-loop,SPEC.sum-to-n-positive
```

Each printed `#Top` and exited 0. The positive entry selection intentionally
retains its auxiliary loop circularity. A diagnostic selection of the positive
entry alone excludes that circularity and begins unrolling; I interrupted that
non-representative diagnostic rather than misclassifying it. The complete
proof and the dependency-correct filtered command both close. Decisive logs
are `evidence/stage3_kprove_all.log`,
`evidence/stage3_kprove_sum_loop.log`,
`evidence/stage3_kprove_empty.log`, and
`evidence/stage3_kprove_positive_with_aux.log`.

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.sum-loop` starts at the exact internal `#while` head reached from the
submitted `While` statement. For arbitrary integer accumulator `S` and
remaining integer `N >= 0`, it says the loop terminates its normal path with
local `n` changed from `N` to `0` and `total` changed from `S` to
`S + sumToN(N)`. The continuation and all omitted cells are framed.

`SPEC.sum-to-n-empty-range` starts with an exact call to the submitted closure
for every `N <= 0`. It requires the normal post-load module binding, fresh
frame allocator, empty heap and stack, no pending return or exception, and
exit code 0. It constrains the returned integer to 0.

`SPEC.sum-to-n-positive` has the same exact call state for every `N >= 1` and
constrains the returned integer to `sumToN(N)`, which reduces to
`N*(N+1)/2`.

The two entry preconditions are satisfiable, disjoint, and exhaustive over K
integers. They do not use fixed sizes, bounded unrolling, a free result, an
implication-only postcondition, or an impossible premise.

### Exact body and control-flow pinning

`evidence/claim_term_compare.py` strips only whitespace, extracts the function
body from the freshly regenerated `solution.mpy`, constructs the exact
`closureVal`, and requires exactly two occurrences in `spec.k`. It found both
and also found the exact internal loop term. This is a constructor-level
comparison, not a source-text resemblance test. The command exited 0; see
`evidence/stage2_translation_and_pinning.log`.

The entry claims begin after module loading, which is allowed here: trusted
regeneration plus the mechanical comparison establishes the same function
name, one parameter, body, and defining module frame. No typing-only runtime
operation was removed. The formal call still performs lookup, argument
evaluation, parameter binding, both assignments, every guard comparison, each
loop iteration, return, and frame restoration under fixed semantics.

`evidence/used_construct_map.md` maps every constructor in `solution.mpy` to
its declaration and material rule path. In particular, the helper claim's
`#while` is not a substituted algorithm: `controls.k` rewrites the submitted
`While(C,B)` to that exact stable internal term before every guard evaluation.

### Satisfying witnesses and substitutions

I used `N=-3` for the empty claim and `N=5` for the positive claim.
`evidence/entry_witnesses.py` computes:

```text
N=-3: formal=0, canonical=0, candidate=0
N=5:  formal=15, canonical=15, candidate=15
```

I also created exact ground K call claims in `evidence/spec-witnesses.k`.
Together they print `#Top` and exit 0. Exact commands and output are in
`evidence/stage4_entry_witnesses.log`.

### Body sensitivity

The reviewer-authored `evidence/spec-body-sensitivity-reviewer.k` changes the
program term actually executed by the claim: `total += n` becomes
`total -= n`. It does not merely edit an external source file. Its dry run
exited 0. For `N=2`, proof execution reached `<k> -3 ~> .K </k>` and rejected
the original expected result 3 with `WarnStuckClaimState`, exit 1. See
`evidence/stage5_body_sensitivity_dry_run.log` and
`evidence/stage5_body_sensitivity_proof.log`.

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/inventory_k.py` inventories every source statement beginning with
`module`, `imports`, `configuration`, `syntax`, `context`, `rule`, or `claim`
in all 24 supplied K files, `verification.k`, and `spec.k`. The complete
ledger is `evidence/rule_inventory.tsv`; its SHA-256 is
`b3546da20e37ce0223af35f06855fcf3d622dc5901abc6e8669714e10073dbd8`.
It contains 1,052 records:

- 697 rules;
- 228 syntax declarations;
- five contexts;
- one configuration;
- three claims;
- 28 module and 90 import records.

The flags inventory identifies 146 function declarations, 111 `total`
declarations, no `functional` declaration, 25 `symbol` declarations, 22
`no-evaluators` declarations, 45 priority-bearing records, no simplification
rule, 35 concrete records, 26 `owise` records, and the strictness/macro
declarations. Counts and the exact extraction command are in
`evidence/rule_inventory_summary.log`.

`evidence/disposition_inventory.py` attaches a disposition and reason to every
one of the 1,052 records. The full output is
`evidence/rule_dispositions.tsv`, with summary in
`evidence/rule_dispositions_summary.log`. It marks 92 fixed-semantics records
as material and reviewed, 25 fixed opaque primitives as target-inert, and the
remaining fixed records as unreachable from the submitted constructors. This
is an exhaustive record-level accounting; full-language behavior for unused
floats, collections, sorting, hashing, and methods is not silently attributed
to this theorem.

### Proof-local theory

There are exactly three proof-local executable declarations:

1. `syntax Int ::= sumToN(Int) [function, total]`.
2. `sumToN(N) => N *Int (N +Int 1) /Int 2` for `N >= 0`.
3. `sumToN(N) => 0` for `N < 0`.

This is a definitional mathematical summary, not an operational bridge. It
never matches a `Call`, `While`, `#while`, assignment, return, environment,
stack, or other configuration term. Its value affects the loop post-state and
positive entry postcondition, but fixed execution is connected to it by the
proved loop claim.

The guards are pairwise disjoint and exhaustive over integers. Both right-hand
sides are true on their guards: the product of consecutive integers is even,
so division by 2 is exact for `N >= 0`; an empty downward loop returns 0 for
`N < 0`. There is no recursive descent, overlap, unconstrained oracle, priority
interaction, task-answer rewrite over program syntax, or fabricated state.
There is no proof-local opaque symbol, simplification lemma, or operational
rewrite.

### Material fixed-semantics path

The material path has the following checked behavior:

- The configuration starts in module scope 0 with a real builtins parent,
  empty heap/stack, no return/exception, and monotonically fresh locations.
- Module load and statement sequencing preserve source order; `FuncDef`
  installs a closure containing the exact translated body.
- `Call` evaluates the callee before arguments, lookup selects the concrete
  `"sum_to_n"` binding, argument evaluation is left-to-right, and frame
  creation binds `n` in a fresh current scope.
- `Assign` evaluates its right-hand side before the current-scope write.
  `AugAssign` reads the existing local and applies mathematical integer `+`
  or `-`. The priority cell/ref alternatives are guarded by `$cells` or
  `isRefV` and are inapplicable to these plain integer locals.
- `Compare` evaluates both operands in order and dispatches `>` on integers to
  K's integer comparison. Integer truth is nonzero truth.
- `While` reaches `#while`, evaluates the guard on every iteration, sequences
  both body statements, and either loops or leaves normally. The circularity
  matches this exact recurring control state.
- `Return` evaluates the local value, sets the return state, discards only the
  remainder of the callee body, pops the frame, restores the caller
  environment and allocator, and reinstates the saved continuation. There is
  no heap allocation, output, exception, or other observable state effect in
  this program.

The clean ground and symbolic runs confirm the complete state transition, not
only the final arithmetic value.

### Opaque and unused supplied declarations

The fixed semantics contains opaque or concrete-only primitives for floats,
sorting, keyed sorting, and MD5. The disposition ledger names every one,
including `sortVS`, `sortKeyVS`, `md5hexCodes`, and the float operator family.
No submitted constructor can reach them, and no claim or proof-local equation
mentions them. They therefore cannot influence control, state, result, or the
postconditions here. Likewise, LLVM's non-exhaustiveness warnings concern
unused domains.

I found no materially unsound rule on the intended execution path. Consequently
there is no soundness allegation requiring a false-conclusion witness. For
unused fixed-language records, the precise limitation is that this audit does
not revalidate the entire supplied Python subset; integrity and target
unreachability, rather than an unsupported global soundness claim, are
recorded.

Stage 5 result: **PASS**.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The fresh mutation is
`evidence/spec-fresh-vacuity.k`. It uses the unchanged exact closure and the
satisfying positive input `N=2`, but requires the false result 4; the actual
result is 3.

First, the mutation built successfully:

```text
kprove spec-fresh-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-FRESH-VACUITY --dry-run
```

This exited 0 and emitted the concrete `kore-exec` invocation; see
`evidence/stage6_fresh_vacuity_dry_run.log`.

Then:

```text
kprove spec-fresh-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-FRESH-VACUITY
```

executed the function to `<k> 3 ~> .K </k>`, emitted
`WarnStuckClaimState` because the destination could not be met, and exited 1.
This is the expected unmet result obligation, not a parser error, timeout,
missing import, unreachable mutation, or unrelated backend crash. The complete
bounded residual is in `evidence/stage6_fresh_vacuity_proof.log`.

Stage 6 result: **PASS**.

## 7. Proven-versus-assumed accounting

### What the K proof establishes

Under the supplied MPY semantics and the exact post-load closure binding, for
every K integer `N`:

- if `N <= 0`, any terminating call of the submitted `sum_to_n` body returns
  0 with the specified caller cells restored;
- if `N >= 1`, any terminating call returns
  `N * (N + 1) / 2` with the specified caller cells restored.

The auxiliary circularity establishes the fixed loop's accumulator relation
for arbitrary initial integer `S` and arbitrary `N >= 0`. The entry
preconditions partition the entire formal integer domain. Ordinary integer
mathematics identifies the positive formula with the inclusive sum from 1 to
`N`; the empty-range branch matches the trusted canonical implementation.

This is a partial-correctness theorem. It does not separately prove a liveness
or resource-bound theorem, though the source loop plainly decreases a positive
integer by one.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted `/reference/reference-semantics` and its K integer/map/list hooks | All concrete and symbolic execution | Acceptable supplied-semantics boundary; byte integrity and the complete material path were independently checked |
| K 7.1.293 parser, kompilers, LLVM/Haskell backends, and reachability engine | Build, concrete runs, `#Top`, mutation rejection | Standard machine-checking trust boundary; fresh builds and opposing outcomes reduce artifact/caching risk |
| Trusted `/reference/py2mpy.py` | Source-to-`.mpy` and source-to-claim identity | Explicit task trust boundary; fresh output is byte-identical and constructor comparison pins both entry bodies |
| Post-load entry configuration instead of symbolic module loading | Entry theorem | Acceptable mechanical intent bridge: exact function name, parameter list, body, and defining frame are pinned; module loading is also exercised concretely |
| Proof-local `sumToN` equations | Loop and positive result | Not opaque or assumed: exhaustive truthful equations plus the fixed-execution loop claim connect the value |
| Mathematical triangular-number identity | Human-language “sum 1 to n” interpretation | Ordinary mathematics; the K loop relation establishes the same recurrence and finite differential tests support the implementation bridge |
| Python differential oracle | Canonical equivalence on 426 sampled values | Finite empirical evidence only; not substituted for the symbolic K theorem |
| Supplied float/sort/MD5 opaque symbols | None | Inert and unreachable; no target conclusion depends on them |

No proof-local trusted primitive, empirical oracle rule, abrupt operational
bridge, or same-symbol circular oracle contributes to closure.

### Gate accounting and exclusions

- Gate A, real-program soundness: **PASS**. Exact bodies execute; no
  operational bridge exists; proof equations are sound; result and body
  mutations discriminate.
- Gate B, intent adequacy: **PASS**. The claims cover every modeled integer,
  not finitely many cases or bounded unrolling, and match both contract
  branches.
- Gate C, trust/evidence auditability: **PASS**. Reviewer-authored artifacts,
  commands, exit statuses, bounded outputs, rule ledger, witnesses, and
  assumptions are preserved under `/audit-output/evidence`.

Excluded are non-integer inputs, Python annotation enforcement, machine
resource exhaustion, and a separate total-correctness theorem. Manual
duplication of the immutable closure term in `spec.k` is an artifact-maintenance
observation, not a pinning defect: trusted regeneration and the independent
mechanical comparison establish identity for this candidate.

VERDICT: PASS
LEGITIMACY: LEGIT
