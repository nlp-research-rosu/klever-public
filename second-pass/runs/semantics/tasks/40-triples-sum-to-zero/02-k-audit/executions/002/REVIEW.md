# Adversarial audit: 40-triples-sum-to-zero

## Outcome

The reconstructed K proofs are real, result-constraining proofs of the submitted
function for seven exact input lengths: 0, 1, 2, 3, 4, 5, and 6. They do not
prove the HumanEval contract, whose domain is arbitrary finite lists of
integers. No claim, invariant, induction, or sequence-tail variable covers a
list of length 7 or greater.

This is the Kit status `SOUND-BUT-LIMITED`: Gate A passes for the submitted
claims, Gate B fails on input-domain adequacy, and the bounded theorem has
reproducible Gate C evidence. Under the benchmark-specific decision boundary,
materially narrowing the HumanEval domain maps to `FAIL / NOT_LEGIT`, not
`CONCERNS / LEGIT`.

No audit infrastructure breach was found.

## 1. Input and provenance integrity

I read `/audit-input.json` before using candidate evidence. It declares
`record_layout = legacy-selected-stage1` and
`semantics_mode = SUPPLIED_SEMANTICS`. The mode is consistent with the mounts:
`/reference/reference-semantics` is present.

The following required records are present, regular, readable, and not
symlinks: `/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`,
`/generation-evidence/metrics.json`,
`/generation-evidence/codex-last.txt`,
`/generation-evidence/codex-output.log`,
`/generation-evidence/prompt.txt`, and the JSONL trace below
`/generation-evidence/codex-trace/`. The optional `usage.json` is present and
was inspected. `runtime-metrics.json` is absent, which is permitted for this
legacy-selected-stage1 layout; I did not reconstruct it.

The mounted `/audit-campaign-lock.json` is byte-hash
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching `/audit-input.json`, and its parsed object exactly matches the
`audit_campaign` block. All directly recorded file hashes match, including the
run/task/result/invocation records, generation prompt, metrics, usage, final
message, full output log, trusted prompt, translator, and canonical solution.
The generation-result hashes for every retained evidence file also match.

I independently reimplemented the pipeline content-manifest hash over the
mounted trees. The candidate tree digest is
`2e4a980035c1e3a1599f04e43d2d30a8c00fe9dd222e74638465e033db1b4e68`,
matching both the invocation and generation-result workspace hashes. The trace
tree digest is
`af5eb64f0ac3e8068e9f457b0d9c546bd4e2f1fd37524a082efa14d905367ea0`,
matching `usage.json`; all 259 JSONL records parse. The trace records the
candidate's bounded proof construction and prior aggregate `#Top`, but I used
those only as claims.

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. A recursive,
entry-type-sensitive comparison of `/candidate/reference-semantics` against
the trusted `/reference/reference-semantics` found the same 25 entries and
identical file hashes, with no missing, additional, changed, mistyped,
unsupported, or symlinked entry. Both independently produce the recorded
trusted manifest digest
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.

The required candidate proof artifacts—`solution.py`, `solution.mpy`,
`verification.k`, `spec.k`, and `prove.sh`—are present as regular files.

Evidence:

- `/audit-output/evidence/01_integrity.py`
- `/audit-output/evidence/01_integrity.log` — command
  `python3 evidence/01_integrity.py`, exit 0, `INTEGRITY_STATUS=PASS`
- `/audit-output/evidence/02_trace_summary.py`
- `/audit-output/evidence/02_trace_summary.log` — all generation tool calls
  and outputs summarized with bounded excerpts, exit 0

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt states: for a list of integers, return `True` exactly when
three elements at distinct positions sum to zero, otherwise return `False`.
There is no length restriction. The trusted canonical implementation at
`/reference/canonical.py:22` enumerates indices `i < j < k` and returns early
on a zero sum.

The submitted `/candidate/solution.py:1` implements the same three nested
index ranges and early return. Repetition of a value is allowed when it occurs
at different positions, as required by the documented `[1, 3, -2, 1]`
example. Python integers and the K `Int` sort are both unbounded for the
operations used here.

In a new `/tmp/audit-work/reconstruction` tree, I ran the trusted copied
translator:

`python3 py2mpy.py solution.py > solution.regenerated.mpy`

`cmp solution.regenerated.mpy solution.mpy` exited 0. Both files have SHA-256
`252f0f098f80b0578b66958658ec4d41bcbd78919a509d45dc018e941f0f8dc5`.

The reviewer-authored differential test imports the copied trusted canonical
entry point and copied submitted entry point under different module names. Its
oracle independently uses `itertools.combinations`, not either program's
three-loop implementation or the K helper equations. It checked:

- all five documented examples;
- 13 empty, length-boundary, duplicate-value, zero-placement, and huge-integer
  cases;
- 780 deterministic generated cases at lengths 0 through 12; and
- every list over `{-2,-1,0,1,2}` at lengths 0 through 7 (97,656 cases).

All 98,454 comparisons agreed; mismatch count was zero. This is finite program
fidelity evidence, not a universal proof.

Evidence:

- `/audit-output/evidence/03_program_fidelity.sh`
- `/audit-output/evidence/03_differential.py`
- `/audit-output/evidence/03_program_fidelity.log` — exit 0

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/reconstruction`. I did
not copy or use a candidate-built definition or cache. The supplied semantics
in scratch came from the trusted reference mount, after the recursive
candidate-versus-trusted comparison.

Using K 7.1.293, I regenerated the concrete harness with the trusted
translator, confirmed byte identity, and ran:

`kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled`

This exited 0. Then:

`krun concrete_tests.regenerated.mpy --definition runtime-kompiled`

exited 0 with `.K`, `NoExc`, and exit code 0. This freshly exercised module
loading, binding by the name `triples_sum_to_zero`, list allocation/dereference,
calls, all documented examples, `[0,0,0]`, and `[0,0]`.

The fresh proof definition command was:

`kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled`

It exited 0. The aggregate candidate target command exited 0 and printed one
standalone `#Top`. I then selected every claim independently using the correct
CLI spelling for `[label(...)]` claims:

`kprove spec.k --definition verification-kompiled --spec-module SPEC --claims <label> --output pretty`

Each of `empty`, `length-one`, `length-two`, `length-three`, `length-four`,
`length-five`, and `length-six` exited 0 and printed `#Top`.

My first independent-selection attempt used `SPEC.<label>`, which is the form
for bracket labels but not for `[label(...)]`. K rejected each with exit 113
and `Unused filtering labels`; these were parser/filter failures, not proof
attempts. They are preserved as
`05_kprove_*.invalid-selector.log`. I corrected the selector and did not count
the rejected runs.

Evidence:

- `/audit-output/evidence/05_reconstruct.sh`
- `/audit-output/evidence/05_reprove_individual.sh`
- `/audit-output/evidence/05_kompile_llvm.log` — exit 0
- `/audit-output/evidence/05_krun_concrete.log` — exit 0
- `/audit-output/evidence/05_kompile_haskell.log` — exit 0
- `/audit-output/evidence/05_kprove_batch.log` — `#Top`, exit 0
- `/audit-output/evidence/05_kprove_empty.log` through
  `/audit-output/evidence/05_kprove_length-six.log` — one `#Top` and exit 0
  in every file

## 4. Adequacy and real-program pinning

### Entry claims in plain language

Every claim fixes the complete initial configuration: module environment 0;
an empty module scope whose parent is the builtins scope; empty heap and stack;
allocation counters 1 and 0; `noRet`; `NoExc`; and exit code 0. There are no
extra `requires` clauses. The constructor annotations on list elements are the
preconditions.

| Label | Input precondition | Postcondition |
|---|---|---|
| `empty` | exactly `[]` | returned Boolean is `hasZeroTriple([])`, hence `false` |
| `length-one` | exactly `[A]`, `A:Int` | returned Boolean is `hasZeroTriple([A])`, hence `false` |
| `length-two` | exactly `[A,B]`, both `Int` | returned Boolean is `hasZeroTriple([A,B])`, hence `false` |
| `length-three` | exactly `[A,B,C]`, all `Int` | returned Boolean is `A+B+C == 0` |
| `length-four` | exactly four arbitrary `Int`s | returned Boolean is the existential zero-triple summary |
| `length-five` | exactly five arbitrary `Int`s | same existential summary |
| `length-six` | exactly six arbitrary `Int`s | same existential summary |

The postcondition is an equality-by-reachability to a determined Boolean term,
not a free RHS variable, implication, or tautology. The helper's structural
equations enumerate an initial element, every later second element, and every
still-later third element, so the summary means
`exists i<j<k: VS[i]+VS[j]+VS[k]=0`.

Each precondition is satisfiable. The ground witness `[0] * n` was substituted
for every `n = 0..6`. The K summary, canonical Python, and submitted Python all
agree: `false` at lengths 0, 1, and 2; `true` at lengths 3 through 6. See
`/audit-output/evidence/04_claim_witnesses.py` and the combined
`03_program_fidelity.log`.

### Real-program pinning

`/candidate/verification.k:30` rewrites the proof-only `#runTriples(VS)` entry
symbol to the fixed semantics' ordinary `#applyK(toCall(closureVal(...)))`.
It does not replace a loop, subscript, comparison, or result with a summary;
the complete submitted nested-loop body executes through the supplied
semantics.

I mechanically tokenized the regenerated `Module(FuncDef(...))` and the
embedded `closureVal` constructor. After removing only explicit `.Stmts` list
terminators that the `.mpy` parser inserts implicitly, the function name is
`"triples_sum_to_zero"`, the parameter is exactly `"l"`, the defining
environment is 0, and all 197 body-constructor tokens match. The expected and
actual normalized closure hashes are both
`175defd9a0ff2ddf0dd6c89723fc05010539db5807845010ae8b9f8ea3b1d039`.
See `/audit-output/evidence/06_constructor_pinning.py` and
`06_constructor_pinning.log`.

The proof entry omits module loading and name dispatch and passes the read-only
input as the semantics' legal bare `list(VS)` value rather than as a heap
reference. Those normalizations are inert for this body: the binding, body,
argument, and defining scope are fixed; the program only reads `l`; and fixed
semantics gives bare and dereferenced lists the same `len` and subscript
behavior. The fresh concrete harness separately exercised actual module
loading, name-based dispatch, and heap-list dereference.

An operational body-sensitivity test changed the embedded body's final
`Return(Bool(false))` to `Return(Bool(true))`. The mutated Haskell definition
built successfully, but the unchanged empty-list claim exited 1 with
`WarnStuckClaimState`; its residual contains returned `true` where the
postcondition reduces to `false`. Thus changing the term actually executed by
the claim invalidates the proof. Evidence is in
`/audit-output/evidence/verification-body-mutation.k`,
`spec-body-mutation.k`, and `08_body_mutation_{build,proof}.log`.

### Material adequacy failure

The source contract accepts arbitrary finite integer lists. `spec.k` has seven
separate closed `ValSeq` shapes and no claim with a symbolic tail. In
particular, a length-7 value cannot unify with the length-6 LHS because the
sixth tail is literally `.ValSeq`. Testing length 7 in Python does not extend
the K theorem. The candidate therefore proved a bounded unrolling, not the
unrestricted HumanEval domain.

## 5. Rule-by-rule static soundness review

The exhaustive derived inventory is
`/audit-output/evidence/07_rule_inventory.md`, with machine-readable full
blocks in `07_rule_inventory.json`. It inventories 944 top-level items from
the clean source:

- 229 syntax declarations;
- 702 semantic/equational rules;
- 7 reachability claims;
- 5 contexts; and
- 1 configuration.

The attributes comprise 147 function declarations, 107 `total`
declarations, 22 opaque `no-evaluators` symbols, 45 priority rules, 35
`concrete` occurrences, and 26 `owise` occurrences. There are no local
`functional` or `simplification` declarations. No generated-semantics helper
exists in this SUPPLIED_SEMANTICS submission.

### Submitted proof-local rules

`verification.k:10-24` adds exactly three functions and six equations:

- `hasZeroThird(S, REST)` checks each possible third value and structurally
  shortens `REST`;
- `hasZeroPair(A, REST)` chooses each second value and invokes
  `hasZeroThird` only on later values; and
- `hasZeroTriple(REST)` chooses each first value and invokes `hasZeroPair` on
  the tail.

Empty and nonempty constructors are disjoint. Each recursive call descends a
proper tail. The integer and Boolean equations are ordinary mathematics and
their domains cover every proof use (all `ValSeq` elements are constrained to
`Int`). The functions are not declared `total`; they need not fabricate a
result for non-integer `ValSeq` elements outside these claims. There are no
overlapping RHS disagreements, priority rules, opaque symbols, or
simplifications in the candidate extension.

`#runTriples` is a definitional entry launcher, not a result-bearing oracle.
Its complete accepted context is a `#runTriples(VS)` prefix with any
continuation suffix; it replaces that prefix with the exact ordinary call and
preserves the suffix. It neither returns abruptly nor skips fixed execution.
The call rule creates a local scope, binds `l`, pushes the continuation,
executes the body, and restores the caller's environment and scope on `#pop`.
The constructor comparison and body mutation above establish binding/body
sensitivity. All helpers influence only the expected postcondition, not the
program execution.

### Used fixed-semantics path

Every submitted constructor maps to supplied declarations and rules:

- `Module`, `FuncDef`, `Params`, `Name`, statement-list sequencing, closure
  application, parameter binding, `Return`, frames, and `#pop` are in
  `syntax.k`, `core.k`, `functions.k`, and `call.k`;
- `Call`, callee lookup, and left-to-right argument evaluation use `call.k`
  and core's `#evalArgs`;
- `len` and one-/two-argument `range` use `builtins.k`, `range.k`, and
  `vsLen`;
- each `For` uses `controls.k`'s iterator loop, positive-step `rangeObj`
  iteration, and target binding;
- `BinOp("+",...)` uses sequential strictness plus the integer addition rule;
- `Subscript` evaluates object then index and uses list `applyIndex`,
  `normIdx`, and `valSeqAt`;
- `Compare(...,"==",Int(0))` uses comparison contexts and integer equality;
  and
- strict `If` and Boolean literal rules select the return branch.

This enforces `0 <= i < j < k < len(l)`, so all used subscripts are in bounds.
The supplied `valSeqAt` is intentionally total/underspecified outside bounds,
but no proof path reaches such a case. The function mutates only local
`i/j/k` bindings; it performs no output, external call, list mutation, or
allocation in the proof representation. Return unwinds the loop
continuations and restores the exact cells required by the claim.

The 22 supplied opaque symbols are float operations, sorting, or MD5. None is
reachable from this integer-list program or its postcondition. Likewise,
unused supplied dict, string, set, tuple, comprehension, method, sorting, and
floating-point rules cannot match the submitted term. Relevant priority rules
only dereference real heap-list inputs in concrete execution or resolve normal
fixed-semantics dispatch; the proof-local module adds no priority.

I found no false candidate rule or material false fixed-semantics conclusion
on the intended integer-list paths. Accordingly, I make no unsoundness claim
requiring a false-conclusion witness. The defect is theorem scope, not a rule
that proves a false bounded result.

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation file (none was submitted). The fresh
`/audit-output/evidence/spec-vacuity.k` changes the length-three destination
from `hasZeroTriple([A,B,C])` to its Boolean complement
`notBool hasZeroTriple([A,B,C])`.

The state is satisfiable and the mutation is demonstrably false: for
`[0,0,0]`, both Python implementations and `hasZeroTriple` return `true`,
while the mutated target is `false`.

`kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY --dry-run`
exited 0, so parsing and KORE generation succeeded. The real mutation proof
then exited 1 with `WarnStuckClaimState`. Its residual shows returned `true`
under the satisfiable condition `0 == A +Int B +Int C`, followed by the normal
“cannot be rewritten further” prover error. This is the expected unmet result
obligation, not a parser error, timeout, missing import, or unrelated crash.

Evidence:

- `/audit-output/evidence/spec-vacuity.k`
- `/audit-output/evidence/09_vacuity_witness.py`
- `/audit-output/evidence/09_vacuity_witness.log` — exit 0
- `/audit-output/evidence/09_vacuity_dry_run.log` — exit 0
- `/audit-output/evidence/09_vacuity_proof.log` — exit 1 with the expected
  stuck residual

## 7. Proven versus assumed accounting

### What the K proof establishes

Conditional on K 7.1.293, its built-in theories, and the supplied MPY
semantics, the reconstructed reachability proof establishes partial
correctness of the constructor-identical submitted body for every integer
assignment to each exact input shape of length 0 through 6. At a successful
return it produces exactly the structurally defined zero-triple Boolean and
restores the specified control, environment, heap, allocation, exception, and
exit cells.

It establishes nothing for a list of length 7 or greater.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K compiler, Haskell prover/backend, and built-in `Int`/`Bool`/`Map`/`List` theories | all reachability results | Necessary low-level machine-checking trust; version and fresh commands recorded |
| Trusted supplied MPY semantics | all execution steps | Authorized fixed-semantics boundary; candidate copy is recursively identical; relevant rules statically reviewed |
| Trusted `py2mpy.py` translation | link from `solution.py` to `solution.mpy` | Acceptable: fresh byte-identical regeneration |
| Direct closure launcher versus module/name invocation | real-program pinning | Acceptable for this immutable read-only body: constructor match, exact binding/scope, fresh concrete name-dispatch execution, and rejected body mutation |
| `hasZeroTriple`/`hasZeroPair`/`hasZeroThird` as the English existential property | interpretation of returned Boolean | Truthful definitional summary by structural descent; independently supported by the combinations oracle, but differential tests remain finite evidence |
| Supplied opaque float/sort/MD5 primitives | none | Inert and unreachable; no claim depends on them |
| Canonical Python and combinations-based differential tests | empirical fidelity only | 98,454 finite checks; not used as a substitute for K proof |

There is no candidate oracle, uninterpreted result-bearing symbol,
proof-local `total` assertion, simplification lemma, operational shortcut, or
assumed loop invariant. The proof succeeds by finite symbolic execution of
seven bounded shapes. That is exactly why it is sound for those shapes and
inadequate for the unrestricted task.

### Gate and benchmark decision

- Gate A (real-program soundness for the submitted claims): **PASS**.
- Gate B (intent and input-domain adequacy): **FAIL** because lengths at least
  7 are excluded.
- Gate C (auditability of the bounded theorem): **PASS**.
- Kit status: **SOUND-BUT-LIMITED**.
- Benchmark mapping: a materially narrowed HumanEval source-contract domain
  is **FAIL / NOT_LEGIT**.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
