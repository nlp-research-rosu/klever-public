# Independent adversarial audit: 57-monotonic

This is a completed seven-stage audit of the mounted candidate. I treated all
candidate prose, generation records, traces, caches, and prior `#Top` reports as
untrusted. All execution used fresh source copies below `/tmp/audit-work`; all
reviewer-authored evidence is below `/audit-output/evidence`.

The candidate does rebuild and its two claims do print `#Top`. The claims also
pin the submitted function and reject a false result mutation. Those facts do
not make the proof legitimate: claim closure depends on a proof-local,
priority-45 operational bridge that replaces every list equality with an
unconstrained `sortEquality` oracle, plus two unproved simplification rules
that state the task's decisive ascending/descending equivalences. The
candidate supplies no bridge-free universal connection theorem. A fixed-only
connection attempt fails, the target proof fails when the bridge is removed,
and an ordinary list-equality witness shows that the bridge admits conclusions
opposite to fixed semantics.

## 1. Input and provenance integrity

Status: PASS. There is no audit-infrastructure breach.

- `/audit-input.json` declares `record_layout =
  legacy-selected-stage1`, problem `57-monotonic`, condition `semantics`, and
  `semantics_mode = SUPPLIED_SEMANTICS`. The trusted
  `/reference/reference-semantics` tree is present, as required for this mode.
- I read `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`,
  `/generation-evidence/metrics.json`,
  `/generation-evidence/usage.json`,
  `/generation-evidence/codex-last.txt`,
  `/generation-evidence/codex-output.log`,
  `/generation-evidence/prompt.txt`, and the sole structured JSONL trace below
  `/generation-evidence/codex-trace/`. Historical `runtime-metrics.json` is not
  required by this legacy layout. The trace records the candidate's claimed
  build and proof, but I did not rely on it.
- `/audit-campaign-lock.json` is byte-hashed to
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the hash recorded in `/audit-input.json`, and its parsed object is
  exactly the `audit_campaign` block.
- Every required mount and record is a readable real file/directory.
  Independent SHA-256 checks match all launcher-recorded per-file hashes,
  including the canonical source, manifests, generation prompt, output log,
  metrics, usage record, and trace file. An independently implemented
  length-delimited tree digest is
  `7e00720e21c941d33e805f83d6daad99add244d704abebd58b1bb97d1c4ec205`
  for `/candidate`, matching the generation result and invocation;
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`
  for the trusted semantics, matching the audit record; and
  `0c4b1ba7fc3f31bdeb6db8cd35805cdcdb07551b6a59cb34fe78c12e15b8a2f5`
  for the trace tree, matching `usage.json`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounted versions. Recursive type/path/content comparison of candidate and
  trusted `reference-semantics/` finds the same 25 entries and no symlink,
  missing, added, changed, or mistyped entry.
- All required proof artifacts (`solution.py`, `solution.mpy`,
  `verification.k`, `spec.k`, and `prove.sh`) are present as real files.

Reproduction: [provenance checker](/audit-output/evidence/provenance_check.py)
and [stage-1 log](/audit-output/evidence/stage1-provenance.log).
The exact command was:

```text
python3 /audit-output/evidence/provenance_check.py
```

It exited 0 and printed `PROVENANCE_CHECK=PASS`.

## 2. Program fidelity and candidate-versus-canonical checks

Status: PASS.

The source contract says that `monotonic(l)` returns true exactly when the list
elements are monotonically increasing or monotonically decreasing. Equality is
allowed, as demonstrated by the conventional meanings of those words and by
the canonical implementation. The three documented examples are increasing
(`True`), neither direction (`False`), and decreasing (`True`).

The trusted canonical implementation returns true iff
`l == sorted(l) or l == sorted(l, reverse=True)`. Candidate `solution.py`
returns that exact expression directly; eliminating the canonical function's
`if`/final-`False` statements is behavior-preserving. It does not narrow the
input domain relative to the canonical implementation.

The trusted regeneration command was:

```text
python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
cmp /tmp/audit-work/regenerated-solution.mpy /candidate/solution.mpy
```

Both commands exited 0, establishing byte identity.

The independent differential oracle imports `/reference/canonical.py` and
`/candidate/solution.py` separately. It tests 23 named cases, all integer lists
of lengths 0 through 7 over values `-2..2` exhaustively, and 5,000
deterministically generated integer lists of lengths 0 through 30. The named
set includes the examples, empty/singleton/two-element boundaries, equality,
both monotone directions, both ways to cease being monotone, large integers,
floats, strings, booleans, and an unorderable mixed list whose exception class
is compared. It checked 102,679 inputs across all three logical branches and
found zero mismatches.

Reproduction: [differential script](/audit-output/evidence/differential_test.py)
and [stage-2 log](/audit-output/evidence/stage2-program-fidelity.log). The
script exited 0 and printed `DIFFERENTIAL_TEST=PASS`. This is finite
implementation-fidelity evidence, not a universal proof.

## 3. Clean proof reconstruction

Status: mechanical reconstruction PASS; semantic legitimacy is decided in
stage 5.

I copied sources to `/tmp/audit-work/candidate`, did not copy or use any
candidate-compiled definition/cache, and built new definitions under
`/tmp/audit-work/fresh-build`. The installed live toolchain is K
`v7.1.293`.

The exact substantive commands and results were:

```text
kompile /tmp/audit-work/candidate/reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/fresh-build/runtime-kompiled
# exit 0

krun /tmp/audit-work/fresh-build/concrete-program.mpy \
  --definition /tmp/audit-work/fresh-build/runtime-kompiled
# exit 0; final .K, NoExc, exit-code 0

kompile /tmp/audit-work/candidate/verification.k \
  --backend haskell --main-module MONOTONIC-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/fresh-build/verification-kompiled
# exit 0

kprove /tmp/audit-work/candidate/spec.k \
  --definition /tmp/audit-work/fresh-build/verification-kompiled \
  --spec-module MONOTONIC-SPEC
# #Top; exit 0

kprove /tmp/audit-work/candidate/spec-claim1.k \
  --definition /tmp/audit-work/fresh-build/verification-kompiled \
  --spec-module MONOTONIC-SPEC-CLAIM1
# #Top; exit 0

kprove /tmp/audit-work/candidate/spec-claim2.k \
  --definition /tmp/audit-work/fresh-build/verification-kompiled \
  --spec-module MONOTONIC-SPEC-CLAIM2
# #Top; exit 0
```

The isolated specs reproduce each submitted claim verbatim in a separate
module, so the final two commands independently establish that each positive
target closes. The compiler warnings concern unused variables and
non-exhaustive fixed-semantics functions outside this program; they are not
build failures.

Reproduction: [clean rebuild driver](/audit-output/evidence/run_clean_rebuild.sh),
[concrete test program](/audit-output/evidence/concrete_program.py),
[isolated claim 1](/audit-output/evidence/spec-claim1.k),
[isolated claim 2](/audit-output/evidence/spec-claim2.k), and
[complete build/proof log](/audit-output/evidence/stage3-clean-rebuild.log).

## 4. Adequacy and real-program pinning

Status: PASS for identity, claim coverage, satisfiability, result constraint,
and body sensitivity.

Plain-language claims:

1. For any symbolic `ValSeq VS` satisfying `nondecreasing(VS)`, load the
   submitted module, call `monotonic(list(VS))`, and terminate normally with
   return value `true`.
2. For any `VS` satisfying `notBool nondecreasing(VS)`, execute the same call
   and terminate normally with return value `nonincreasing(VS)`.

Because `nondecreasing(VS)` has sort `Bool`, those preconditions partition the
formal domain. Together the postconditions are exactly
`nondecreasing(VS) orBool nonincreasing(VS)`, not a free result, implication,
or tautology.

The `<k>` cell starts with `#loadAll(monotonicProgram)` and then calls the
newly bound `monotonic` closure. A mechanical constructor-token comparison
between trusted-regenerated `solution.mpy` and the right-hand side of
`monotonicProgram` found exactly 89 equal tokens. This checks the function
name, parameter, docstring statement, short-circuit `or`, both comparisons,
both `sorted` calls, and the `reverse=True` keyword. No program-defined helper
is summarized.

The initial configuration is realizable: module environment 0 has an empty
scope with builtins parent `-1`, the builtin scope is present, the heap and
stack are empty, allocation counters are at their initial values, and there is
no return or exception. Witnesses include:

| Claim branch | Input | ND | NI | Formal/Python result |
|---|---:|---:|---:|---:|
| claim 1 | `[]` | true | true | true |
| claim 1 | `[1,1,3]` | true | false | true |
| claim 2 | `[3,2,2,-1]` | false | true | true |
| claim 2 | `[1,3,2]` | false | false | false |

Trusted canonical and candidate Python agree on all four substitutions.
Reproduction: [pinning checker](/audit-output/evidence/pinning_check.py) and
[stage-4 pinning log](/audit-output/evidence/stage4-pinning.log).

The body-sensitivity mutation changes the constructor term actually executed
by the claim to `Return(Bool(false))`; it does not merely edit an unused source
file. With the original first postcondition, `kprove` exits 1 with
`WarnStuckClaimState` and a residual `<k> false </k>` versus expected `true`.
Reproduction: [body mutation](/audit-output/evidence/spec-body-mutation.k) and
[body-sensitivity log](/audit-output/evidence/stage4-body-sensitivity.log).

The claims quantify over all K `ValSeq` elements even though the fixed
`sortVS` trust comment specifically describes integer sorting (with some
concrete string support). Thus the claims are not a finite-size proof or an
explicit domain narrowing. They should not, however, be read as a faithful
theorem about every possible Python object list; unsupported/mixed comparison
exceptions are outside this small supplied language.

## 5. Rule-by-rule static soundness review

Status: FAIL.

### Exhaustive inventory

The line-addressed inventory covers `reference-semantics/semantics.k`, all 23
supplied helper K files, `verification.k`, and `spec.k`: 26 files, 945 records
comprising 706 rules, 231 syntax declarations, 5 contexts, 1 configuration,
and 2 claims. It identifies 150 function declarations, 111 `total`
declarations, all 23 `no-evaluators` declarations, all priority/concrete/owise
attributes, and both simplification rules. There are no `[functional]`
declarations. See the [inventory generator](/audit-output/evidence/k_rule_inventory.py)
and [complete inventory](/audit-output/evidence/stage5-k-rule-inventory.md).

Of those records, the candidate adds four syntax declarations and eleven
rules in `verification.k`; the other semantic declarations/rules are the
byte-verified supplied baseline. I reviewed the supplied rules by dependency
and constructor head. Rules for floats, dictionaries, sets, comprehensions,
loops, slices, methods, and other unused constructs are syntax-disjoint from
this program and cannot contribute to claim closure. The material path is:

- AST syntax for `Module`, `FuncDef`, `Params`, `Expr`, `Str`, `Return`,
  `BoolOp`, `Compare`, `CmpOp`, `Call`, `Name`, `KwArg`, and `Bool`;
- the configuration, `#loadAll`, statement sequencing, string evaluation and
  discarded docstring expression;
- function definition, exact name lookup, left-to-right call argument
  evaluation, parameter binding, frame push/pop, and return;
- builtin lookup for `sorted`, fresh-list allocation, `sortVS`, `condRev`,
  `revVS`, and `revVSAcc`;
- left-to-right short-circuit `or`, list dereference/comparison, and the final
  Boolean return.

Those fixed rules preserve the expected bindings and ordering: the call first
resolves the actual `sorted` builtin, evaluates its list and keyword arguments,
allocates the sorted result, then compares values. The sorted calls' heap
allocations occur before the proof-local equality bridge. Return restores the
caller environment and empties the stack; the claims require `NoExc` and exit
code 0. I found no separate fixed-semantics bypass on this used path.

The material fixed opaque boundary is
`sortVS(ValSeq)` at
`/reference/reference-semantics/semantics/sort.k:18`. The supplied semantics
names it as ascending sort and gives concrete insertion-sort rules for LLVM.
Trusting that primitive does not automatically prove the theorem relating
equality with that primitive to the candidate's newly defined adjacency
predicates.

### Candidate extension inventory and judgments

| Extension | Class and complete domain | Judgment |
|---|---|---|
| `monotonicProgram` and its equation (`verification.k:8-36`) | Definitional summary, no state/control replacement | Sound. Exact constructor identity is mechanically checked. |
| `nondecreasing` (`:40-45`) | Total recursive definition over all constructor `ValSeq` | Sound as a definition. Empty, singleton, and length-at-least-two cases are disjoint and exhaustive; recursion descends by one element. Its comparisons may remain opaque on unsupported `Val`, but it does not invent a value for them. |
| `nonincreasing` (`:41,47-50`) | Same class and domain | Sound for the same reasons. |
| `sortEquality` declaration (`:55-56`) | New total, symbolic, no-evaluators Boolean | Concerning by itself and materially unsafe with the next rule. Outside two later shapes its value is unconstrained. |
| `<k> Compare(list(A), CmpOp("==", list(B))) => sortEquality(A,B) ... </k> [priority(45)]` (`:57-61`) | Operational bridge over **every** evaluated list equality, arbitrary continuation, and all framed cells | Unsound over its complete match domain. It preempts fixed `Compare -> applyCmp` and structural list equality, yet supplies no equation fixing most `A,B`. Concrete false-conclusion witness below. |
| `sortEquality(VS, sortVS(VS)) => nondecreasing(VS) [simplification]` (`:62-64`) | Result-bearing derived lemma over all `VS` | This is the task's ascending correctness equivalence, admitted as an axiom. It is plausible ordinary mathematics for a correctly sorted finite integer sequence, but no bridge-free universal theorem derives it from fixed semantics. It is therefore an unjustified, proof-closing answer lemma, not a validated derivation. |
| descending `sortEquality` rule (`:66-71`) | Result-bearing derived lemma over all `VS` | Same defect for `VS == reverse(sorted(VS))` iff adjacent nonincrease. Its pattern is syntactically distinct from the ascending one; where their intended meanings overlap, both predicates agree. The defect is missing derivation, not a demonstrated contradictory overlap. |
| `isMonotonic` (`:74-76`) | Definitional summary | Sound and exhaustive, but unused by either submitted claim and irrelevant to closure. |

The bridge's state footprint is only the `<k>` computation after both
operands have become values; it does not itself discard continuation, pop a
frame, or mutate the heap. An arbitrary continuation would be acceptable if
the replacement Boolean were exactly fixed list equality. It is not.
Priority 45 ensures this is not a dormant rule.

### Required false-conclusion witness

The bridge matches ordinary equalities unrelated to `sorted`. Under fixed
semantics:

- `[] == []` is `true`;
- `[1,2] == [2,1]` is `false`.

The reviewer program asserts those results. The fixed Haskell definition
terminates with `.K`, `NoExc`, exit code 0. Under the bridge-enabled proof
definition, `krun` exits 111 and displays branches that assign both truthful
and opposite values to the corresponding ground `sortEquality` terms. In
particular, the residual admits
`true #Equals sortEquality(vCons(1,vCons(2,.ValSeq)),
vCons(2,vCons(1,.ValSeq)))`, even though fixed structural equality is false,
and it admits `false #Equals sortEquality(.ValSeq,.ValSeq)`, even though empty
lists are equal. These are concrete symbolic false-conclusion witnesses for
the operational rule's complete match domain, not merely an unreachable-case
argument.

See [list-equality witness](/audit-output/evidence/list_equality_probe.py) and
[bridge audit log](/audit-output/evidence/stage5-bridge-audit.log), especially
the fixed run (exit 0) and bridge-enabled run (exit 111).

### Missing connection and proof dependence

The candidate contains no auxiliary connection claim at all. I constructed
the bridge-free universal ascending obligation using only fixed semantics and
an independently named adjacency definition:

```text
Compare(list(VS), CmpOp("==", list(sortVS(VS))))
  => connectionNondecreasing(VS)
```

Its definition builds, but `kprove` exits 1 with `WarnStuckClaimState`; the
residual is fixed equality `VS ==K sortVS(VS)` versus
`connectionNondecreasing(VS)`. See
[connection definition](/audit-output/evidence/connection-verification.k),
[connection claim](/audit-output/evidence/connection-spec.k), and the end of
the [bridge log](/audit-output/evidence/stage5-bridge-audit.log).

I also removed the bridge and its two equations while leaving the exact
program and the two intended predicates intact. That definition builds, but
the original target claims exit 1 with `WarnStuckClaimState` at
`VS ==K sortVS(VS)` / `VS ==K revVSAcc(sortVS(VS), .ValSeq)`. This establishes
that the submitted `#Top` depends on the offending extension. See
[bridge-free definition](/audit-output/evidence/verification-no-bridge.k),
[bridge-free spec](/audit-output/evidence/spec-no-bridge.k), and
[dependency log](/audit-output/evidence/stage5-no-bridge.log).

Finite Python/LLVM agreement cannot supply the missing universal theorem.
Consequently Gate A (real-program soundness of proof extensions) fails.

## 6. Fresh non-vacuity test

Status: PASS, but it cannot cure the stage-5 failure.

No candidate-provided vacuity artifact was trusted. The fresh mutation changes
claim 1's required return from `true` to `false` while retaining its
`nondecreasing(VS)` precondition and executing the exact original program.
`VS = [1,2]` is a satisfying witness: its precondition is true and both Python
implementations return true, so the mutation is genuinely false.

Commands and results:

```text
kprove /tmp/audit-work/candidate/spec-vacuity-review.k \
  --definition /tmp/audit-work/fresh-build/verification-kompiled \
  --spec-module MONOTONIC-SPEC-VACUITY-REVIEW --dry-run
# exit 0: the mutation parses/builds

kprove /tmp/audit-work/candidate/spec-vacuity-review.k \
  --definition /tmp/audit-work/fresh-build/verification-kompiled \
  --spec-module MONOTONIC-SPEC-VACUITY-REVIEW
# exit 1; WarnStuckClaimState; residual final <k> true, requested false
```

Reproduction: [false mutation](/audit-output/evidence/spec-vacuity-review.k),
[driver](/audit-output/evidence/run_nonvacuity.sh), and
[stage-6 log](/audit-output/evidence/stage6-nonvacuity.log). This shows the
submitted claim constrains the result and is not vacuous.

## 7. Proven versus assumed accounting

The successful reconstructed reachability proof establishes the following
statement **only in the candidate-extended K theory**:

- for arbitrary formal `VS`, if candidate-defined `nondecreasing(VS)` holds,
  execution reaches normal return `true`;
- otherwise, execution reaches normal return
  `nonincreasing(VS)`;
- the stack is empty, return state is reset, no exception is present, and exit
  code is 0; final scopes/heap/allocation counter are existentially framed.

It is a partial-correctness result: it does not independently prove
termination. More importantly, the result is conditional on the exact
proof-local axioms that already replace the two result-bearing comparisons by
the desired predicates.

Trust ledger:

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell and LLVM backends | All builds, executions, and reachability results | Ordinary toolchain trust. Fresh builds avoid candidate caches. |
| Byte-verified supplied MPY semantics | Binding, evaluation order, calls, allocation, comparisons, return/control | Authorized fixed semantics for this benchmark. Used-path rules were reviewed. |
| Trusted `sortVS` primitive | Values returned by both `sorted` calls; therefore both branches and final result | Acceptable as a named low-level fixed-semantics boundary for integer sorting, with concrete LLVM and finite Python evidence. It does not entail the candidate's new equality lemmas inside K. |
| Candidate `sortEquality` bridge and two simplifications | Directly determine both comparisons and close both claims | Illegitimate. The bridge is false/unconstrained on its full match domain, and the two task-specific result equations have no bridge-free universal connection proof. |
| Recursive ND/NI definitions and their identification with the English contract | Formal postcondition and human-facing monotonicity | Ordinary adjacent-order mathematics; concrete witnesses and the canonical implementation agree. This is not the source of failure. |
| Trusted translator plus reviewer constructor-token comparison | Source-to-`solution.mpy` and `solution.mpy`-to-claim identity | Adequate program-pinning evidence. |
| Differential tests | Candidate/canonical implementation bridge and finite evidence for normal/boundary behavior | 102,679 zero-mismatch cases; empirical only, not a substitute for the missing K connection theorem. |

Gate summary:

- Gate A, real-program proof-extension soundness: **FAIL**.
- Gate B, intent/domain adequacy: the split claims express the intended
  monotonicity result on the material integer-list domain and do not impose a
  finite bound; unsupported general Python object behavior remains outside the
  supplied language.
- Gate C, evidence auditability: **PASS** for the evidence actually claimed
  here; every command, status, mutation, and witness is preserved.

The decisive Gate-A defect is material, not a documentation concern. The
candidate's `#Top` is obtained only after importing an overbroad
result-bearing oracle and axiomatizing the task's key conclusion. Under the
benchmark decision boundary, that is not a legitimate partial-correctness
proof of the real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
