# Independent adversarial review: 43-pairs-sum-to-zero

The candidate contains a legitimate partial-correctness proof. I reconstructed
the proof from source using the trusted supplied semantics, checked that the
entry claim executes the regenerated program, audited every relevant K rule,
and independently made a reachable false result obligation fail. Candidate
reports, caches, compiled definitions, and prior traces were not used as proof.
`evidence/00_command_ledger.md` indexes the exact reviewer commands, raw tool
statuses, and bounded logs.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, and problem
`43-pairs-sum-to-zero`. The campaign block is byte-for-byte equal to the block
in `/audit-campaign-lock.json`, and the recorded lock hash equals the mounted
file's SHA-256.

I read and independently checked all required pipeline-v3 records:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured trace. All are regular
readable entries, all launcher-declared file hashes match, and the one JSONL
trace contains 599 parseable records with no malformed line. The provenance
and trace checks are recorded in:

- `evidence/01_integrity_check.py` and `01_integrity_check.log`
- `evidence/01_trace_summary.py` and `01_trace_summary.log`
- `evidence/01_generation_record_excerpt.log`

The mounted candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. A recursive type, path, and
content comparison found no missing, added, changed, mistyped, or symlinked
entry between `/candidate/reference-semantics` and
`/reference/reference-semantics`. Their independently computed pipeline tree
digest is
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
matching the authoritative manifest. The candidate tree and generation-trace
pipeline digests also match their manifests. The audit-input record additionally
contains secondary tree digests made with an undeclared serialization; these
were recorded but were not misinterpreted as pipeline digests.

The trusted semantics mount is present as SUPPLIED_SEMANTICS requires. There is
no mode/mount contradiction and no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract in `/reference/prompt.py:3` is: for any finite list of
integers, return `True` exactly when two distinct list positions hold values
whose sum is zero. The canonical function in `/reference/canonical.py:23`
directly checks every index pair.

The generated function in `/candidate/solution.py:1` scans each value. For a
nonzero value `x`, a counted `-x` must occur at a different position because
`x != -x`; for zero, two occurrences are explicitly required. Thus the
different algorithm preserves the distinct-position condition.

Using only the trusted translator, I regenerated `solution.mpy` in
`/tmp/audit-work/review-43`. It is byte-identical to the submitted file; both
have SHA-256
`705488ab5666c76d3425e85842150600c95483a0d7bfcb95711f5451a7848c3e`.
See `evidence/02_translation_identity.log`.

The independent differential script `evidence/02_differential.py` imports the
trusted canonical and generated entry points and also uses an independent
index-pair oracle. It checked:

- all five documented examples;
- 15 empty, singleton, zero, duplicate, sign, and large-integer boundaries;
- all 19,531 lists of lengths 0 through 6 over `{-2,-1,0,1,2}`;
- 2,500 deterministic generated lists of lengths 0 through 30, including
  unbounded Python integers.

All 22,051 comparisons agreed, covering 18,858 true and 3,193 false cases.
The command exited 0; see `evidence/02_differential.log`. This testing supports
the source-to-contract bridge but is not treated as the K proof.

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work/review-43`, replaced the
candidate's semantics copy with the trusted mounted semantics, and did not copy
or use any candidate `*-kompiled` directory or cache. The installed toolchain is
K 7.1.293. The following fresh commands and gates succeeded:

| Reconstruction gate | Result | Evidence |
|---|---:|---|
| `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition review-runtime-kompiled` | exit 0 | `03_kompile_llvm.log` |
| translate and `krun` 11 reviewer concrete assertions | `.K`, `NoExc`, exit-code 0; shell exit 0 | `03_concrete_tests.py`, `03_krun_concrete.log` |
| `kompile --backend haskell connection-definition.k --main-module CONNECTION-DEFINITION --syntax-module MPY-SYNTAX --output-definition review-connection-kompiled` | exit 0 | `03_kompile_connection.log` |
| `kprove connection-spec.k ... --claims CONNECTION-SPEC.int-equality` | `#Top`, exit 0 | `03_kprove_connection_int_equality.log` |
| `kprove connection-spec.k ... --claims CONNECTION-SPEC.int-unary-minus` | `#Top`, exit 0 | `03_kprove_connection_int_unary-minus.log` |
| `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition review-verification-kompiled` | exit 0 | `03_kompile_verification.log` |
| `kprove spec.k ... --claims SPEC.loop-invariant` | `#Top`, exit 0 | `03_kprove_loop_invariant.log` |
| `kprove spec.k --definition review-verification-kompiled --spec-module SPEC` | `#Top`, exit 0 | `03_kprove_all_target_claims.log` |

The last command is the valid entry-theorem reconstruction: it keeps the entry
claim and its auxiliary circularity active and proves all claims in `SPEC`.
One reviewer diagnostic selected the entry label alone, thereby removing the
loop circularity and causing symbolic unrolling; I interrupted that diagnostic
and did not count it as evidence. Its exact disposition is preserved in
`evidence/03_entry_selection_diagnostic.md`.

The only compiler messages were warnings in fixed supplied semantics. No
positive proof relied on a timeout, cached definition, or candidate log.

## 4. Adequacy and real-program pinning

### Entry and helper claims in plain language

The loop claim at `/candidate/spec.k:9` accepts arbitrary finite integer
sequences `FULL` and `REM`, a Boolean incoming `found`, and the exact translated
loop body. It says normal loop completion changes `found` to:

`incoming found OR some element of REM has a distinct-position inverse in FULL`.

It leaves `l = list(FULL)`, permits the real loop's final value of `x`, and
frames the rest of the state. The precondition is satisfiable, including
`FULL = REM = .ValSeq`.

The entry claim at `/candidate/spec.k:41` starts in a completely fixed clean
configuration, requires every element of arbitrary finite `FULL` to be an
integer, loads the function, looks it up by its real name, calls it with
`list(FULL)`, and assigns the return to `$result`. It ends normally with clean
heap, stack, return, exception, and exit cells. Its postcondition at line 81
requires the actual `$result` map entry to equal
`anyInverse(FULL,FULL)`. The result is therefore neither free nor tautological,
and the theorem is equivalence-valued rather than a one-way implication.

### Mechanical program pinning

`evidence/04_constructor_pinning.sh` extracted the function from the trusted
regeneration and from the entry claim, normalized only explicit `.Stmts`
sequence units, and parsed both with fresh `kast`. The resulting KORE terms have
the same SHA-256,
`d569747bd5d07dee66796a71c53f7487daa52c9448080c58fbc43b51fd6476fb`,
and compare byte-for-byte (`CONSTRUCTOR_COMPARE_EXIT=0`). See
`evidence/04_constructor_pinning.log`. Every assignment, guard, `count` call,
unary minus, loop, and return is present in the claim term.

The precondition has many witnesses. Reviewer ground claims reduce the property
to false for `[]`, true for `[1,-1]`, false for `[0]`, and true for `[0,0]`;
all close with `#Top` in `evidence/04_ground_substitution.log`. These values
match both Python functions and the independent oracle.

The symbolic entry uses the supplied semantics' permitted unboxed
`list(ValSeq)` representation for a read-only input. The program performs no
mutation or identity observation on `l`; concrete tests also execute ordinary
parsed list expressions and agree. This representation changes no material
operation or control effect for this function.

## 5. Rule-by-rule static soundness review

`evidence/05_rule_inventory.py` generated the exhaustive inventory
`evidence/05_rule_inventory.md`: 945 logical source blocks covering all 24
byte-verified supplied `.k` files and every candidate proof source imported by
the positive claims. It contains 928 fixed-supplied and 17
candidate-controlled entries: 704 rules, 231 syntax declarations, 5 contexts,
4 claims, and 1 configuration. Attributes such as `function`, `total`,
`functional`, `opaque`, `concrete`, `owise`, priority, strictness, macros, and
simplification are separately classified.

The exact material fixed-semantics slice is mapped in
`evidence/05_static_review.md`: syntax and configuration; module loading and
lookup; left-to-right statements and arguments; function installation,
parameter binding, frame push/pop, and return; assignment, `if`, `for`, and
target binding; list iteration and `list.count`; integer comparisons and unary
minus. The fixed rules implement the real evaluation order and all material
state changes. Unused fixed entries have absent constructors, operator tags,
callables, value sorts, or control markers; notably, no unused opaque
float/sort/md5 helper is reachable.

Every candidate-controlled declaration/rule has this disposition:

| Inventory IDs | Construct | Static disposition |
|---|---|---|
| 929–931 | total `intProj` | Disjoint exhaustive projection; its arbitrary non-integer result is excluded by every bridge guard and the entry domain. |
| 932–933 | total `hasInverse` | Exact distinct-position characterization: two zeros, or one occurrence of `-x` when `x` is nonzero. |
| 934–936 | total `anyInverse` | Constructor-disjoint structural recursion and finite disjunction over the list. |
| 937–939 | total `allInts` | Constructor-disjoint structural domain predicate. |
| 940 | integer equality simplification | Pure, guarded to injected integers, agrees with the fixed integer rule, and has a bridge-free universal connection theorem. |
| 941 | integer unary-minus simplification | Pure, guarded to injected integers, agrees with the fixed integer rule, and has a bridge-free universal connection theorem. |
| 942–943 | connection claims | Universal lemmas built without importing the simplification bridges. |
| 944 | loop circularity | Matches the exact real loop and summarizes precisely the body-written bindings while framing material state. |
| 945 | entry claim | Exact real binding/body/call with a constrained Boolean result and normal final state. |

The two simplifications accelerate existing fixed semantic computations; they
do not encode the task answer or replace an unmodeled operation with an oracle.
As an additional adversarial check, reviewer claims demanded the opposite
ground equality and unary-minus results against the bridge-free connection
definition. Both built, became stuck on the concrete wrong value, and exited 1:
`evidence/05_bridge_wrong_equality.log` and
`05_bridge_wrong_unary_minus.log`.

I found no unsound rule. Consequently there is no false-conclusion witness to
attribute to any rule; the full inventory gives the narrower reachability and
trust disposition for every entry.

## 6. Fresh non-vacuity test

I did not rely on `/candidate/spec-vacuity.k`. The reviewer-authored
`evidence/06_false_result.k` loads and calls the exact real function from a
clean, satisfying empty-list state, but falsely demands `$result = true`.

The mutation first passed `kprove --dry-run` with exit 0
(`06_false_result_dry_run.log`), establishing that it parses, imports, and
builds. The actual proof then exited 1 with `WarnStuckClaimState`
(`06_false_result_proof.log`). Its residual final configuration is otherwise
normal and contains `$result |-> false`; the failure is exactly the unmet
result obligation, not a parser error, missing import, timeout, unreachable
state, or unrelated crash. This demonstrates both precondition satisfiability
and result sensitivity.

## 7. Proven versus assumed accounting

The successful reachability proof establishes this partial-correctness theorem:
for every finite semantic list whose elements are mathematical integers, if the
submitted `pairs_sum_to_zero` function terminates normally from the specified
clean state, its Boolean return is true exactly when two distinct positions
contain additive inverses. In fact the fixed structural loop rules also drive
all such finite inputs to completion, but termination is not claimed as a
separate total-correctness theorem.

The proof/trust ledger is:

| Boundary | Status and reason |
|---|---|
| Candidate entry and loop reachability claims | Formally reconstructed with fresh Haskell definitions and `#Top`. |
| Equality/minus proof bridges | Formally justified by independently closed, bridge-free universal connection claims; negative opposites were rejected. |
| Candidate recursive property functions | Audited as disjoint, exhaustive, terminating mathematical definitions; no opaque answer oracle. |
| Submitted program term | Mechanically constructor-identical to trusted regeneration. |
| Python rewrite versus the HumanEval contract | Elementary distinct-position argument plus broad differential evidence; testing is corroboration, not proof. |
| Supplied MPY semantics | Mandated trusted baseline, byte-verified; every material rule was statically reviewed and concrete behavior was freshly exercised. |
| K engine, SMT reasoning, and builtin integer/Boolean/list/map operations | Ordinary low-level proof-system trust boundary. No candidate-controlled primitive substitutes for these. |
| Unboxed read-only input value | Explicitly supported by the supplied semantics and observationally adequate here because the program neither mutates nor observes input identity. |
| Candidate prose, prior `#Top`, caches, mutation logs, and generation trace | Not assumed. |

The proof is sound, result-constraining, pins the real regenerated program, and
covers the unrestricted finite list-of-integers source domain. No material
adequacy gap or illegitimate assumption remains.

VERDICT: PASS
LEGITIMACY: LEGIT
