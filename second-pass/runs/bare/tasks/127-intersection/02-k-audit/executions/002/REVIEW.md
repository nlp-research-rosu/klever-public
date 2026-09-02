# Independent adversarial review: 127-intersection

## Audit conclusion

The candidate is **not a legitimate proof**, despite successful fresh
reconstruction, correct program behavior, exact program pinning, and a
discriminating postcondition. The whole-program proof imports an unsound
operational loop bridge at `verification.k:71-89`. On the reachable state
`length=5, divisor=2`, fixed semantics increments `divisor` to 3 before
returning `YES`; the bridge returns the same value while falsely preserving
`divisor=2`. A fresh fixed-semantics claim asserting that false preserved state
fails with a concrete residual, while the bridge-enabled definition proves the
same false claim as `#Top`.

This is not inferred from candidate logs. It was reproduced independently from
source in fresh LLVM and Haskell definitions. The decisive evidence is
`evidence/stage4.log`, with the two witness specs in
`evidence/fixed-state-witness.k` and `evidence/bridge-state-witness.k`.

## 1. Input and provenance integrity

The launcher declares:

- problem `127-intersection`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, the required invocation and metrics
records, `usage.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and
all 242 JSONL records in the structured trace. I treated their contents only as
generation claims.

No infrastructure breach was found:

- The campaign lock JSON exactly equals the `audit_campaign` block, and its
  SHA-256 is the value recorded in `/audit-input.json`.
- Every required regular file for `legacy-selected-stage1` is present and
  readable. `runtime-metrics.json` is absent, but historical runtime metrics
  are explicitly not required for this layout. `usage.json` is present and was
  inspected.
- No symlink occurs under `/candidate`, `/reference`, or
  `/generation-evidence`.
- All directly recorded file hashes match. Every generation output listed by
  `/generation-result.json`, including the sole trace JSONL, also matches.
- An independent retained-tree hash of `/candidate` is
  `2126c63067804427b5eabecf2c25e89f90b2029b2b97e89bd9aa8cbcfafac8b3`,
  matching both `invocation.json` and `generation-result.json`. The independently
  hashed trace tree matches `usage.json`.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
  `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py`.
- `/reference/reference-semantics` is absent, as required by
  `GENERATED_SEMANTICS`.

The candidate's `__pycache__`, `kore-exec.tar.gz`, `prove.log`, and all
generation traces were ignored as proof authority. Full checks, hashes, trace
record counts, and the exact command are preserved in
`evidence/integrity_check.py`, `evidence/stage1.sh`, and
`evidence/stage1.log`.

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For closed integer intervals `(A,B)` and `(C,D)`, with `A <= B` and `C <= D`,
let

`L = min(B,D) - max(A,C)`.

The function must return `"YES"` exactly when `L` is prime, and `"NO"`
otherwise. Thus disjoint, touching, and degenerate intersections return
`"NO"`. The prompt's example establishes geometric length `end-start`, not a
count of integer points.

The trusted canonical implementation computes those max/min endpoints and
tests the resulting positive length for primality. The candidate computes the
same endpoints with branches and performs trial division while
`divisor*divisor <= length`. On the documented domain of two integer pairs,
these algorithms agree.

### Translation identity

Running the trusted `/reference/py2mpy.py` over the scratch copy of
`solution.py` produced a file byte-identical to submitted `solution.mpy`.
Both hashes are
`50e2785172fe16e32b01bf02041d6aa4672707b205cafd12b2bc30c201f3627e`.

### Independent differential testing

`evidence/differential.py` separately imports the trusted canonical entry point
and the generated entry point. It also uses an independently written primality
oracle whose loop guard avoids copying the candidate expression. It covers:

- all documented examples (including the differing but compatible third
  examples in the trusted prompt and canonical docstring);
- degenerate, disjoint, touching, and lengths 0, 1, 2, 3, 4, 5, 9, 101, and
  121;
- a complete grid of 23,409 valid interval pairs with endpoints from -8 to 8;
- 5,000 deterministic generated valid pairs with endpoints from -10,000 to
  10,000;
- all four order partitions used by the K entry claims.

All 28,431 cases agree among candidate Python, trusted canonical Python, and
the independent oracle. Commands, exit status 0, branch counts, and zero
mismatches are in `evidence/stage2.sh` and `evidence/stage2.log`.

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/candidate-src`.
Candidate-built definitions, caches, the bundled backend archive, and
candidate proof logs were not copied or used.

The installed independent tools report K version 7.1.293. The final clean
reconstruction used new output paths:

1. LLVM:

   `kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX --backend llvm --output-definition /tmp/audit-work/build-concrete/semantic-v2-kompiled`

   Exit 0.

2. Bridge-free loop definition:

   `kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition /tmp/audit-work/build-proof/loop-v2-kompiled`

   Exit 0.

3. Loop claim:

   `kprove spec.k --definition /tmp/audit-work/build-proof/loop-v2-kompiled --spec-module LOOP-CORRECTNESS-SPEC --output pretty`

   Exit 0, exactly one `#Top`.

4. Whole-program definition:

   `kompile verification.k --main-module VERIFICATION-WITH-LOOP-LEMMA --syntax-module MPY-SYNTAX --backend haskell --output-definition /tmp/audit-work/build-proof/verification-v2-kompiled`

   Exit 0.

5. All four entry claims:

   `kprove spec.k --definition /tmp/audit-work/build-proof/verification-v2-kompiled --spec-module SPEC --output pretty`

   Exit 0, exactly one `#Top` for the complete four-claim module.

For generated-semantics validation, 18 fresh LLVM executions covered normal
and boundary inputs, zero/nonzero loop iterations, prime/composite square
boundaries, every source branch partition, and every used operator. Every run
exited 0 and agreed with both Python implementations.

The first reviewer semantics harness had an over-escaped result regular
expression; it mislabeled valid final K values as unparsed. I corrected only
that reviewer script and reran the entire build and proof pipeline at new
definition paths. The successful final run is `evidence/stage3.log`; the
superseded harness run remains visible as
`evidence/stage3-initial-regex-error.log`. Exact scripts and individual logs are
under `evidence/stage3.sh`, `evidence/semantics_differential.py`,
`evidence/kompile-*.log`, and `evidence/kprove-*.log`.

Stage 3 result: **PASS** for reconstruction and positive closure. A `#Top`
under the submitted theory is not yet a soundness verdict.

## 4. Adequacy and real-program pinning

### Plain-language claims

The loop claim at `spec.k:10-27` says: for any integers `N >= 2` and `D >= 2`,
executing the submitted trial-division loop with local `length=N`,
`divisor=D`, and the exact trailing `return "YES"` reaches
`primeResult(N,D)`. It permits the final divisor to be an existential
`?_VD`; it does not say the divisor is preserved.

The four entry claims at `spec.k:37-91` all assume valid intervals. They
partition all inputs by `C <= A` versus `C > A`, and `D >= B` versus `D < B`:

| Claim | Extra precondition | Claimed returned value |
|---|---|---|
| C02 | `C <= A`, `D >= B` | `lengthResult(B-A)` |
| C03 | `C <= A`, `D < B` | `lengthResult(D-A)` |
| C04 | `C > A`, `D >= B` | `lengthResult(B-C)` |
| C05 | `C > A`, `D < B` | `lengthResult(D-C)` |

These are exactly
`lengthResult(min(B,D)-max(A,C))`. Each final `<functions>` and `<env>` map is
existential, but the returned `<k>` value is constrained.

### Satisfiable witnesses

The loop precondition is satisfied by `N=5,D=2` and an environment containing
those bindings. Entry witnesses are:

- C02: `(0,5),(-2,7)`, result `"YES"` from length 5;
- C03: `(0,5),(-2,3)`, result `"YES"` from length 3;
- C04: `(0,5),(2,7)`, result `"YES"` from length 3;
- C05: `(0,5),(2,4)`, result `"YES"` from length 2.

Both Python implementations and fresh K execution return those values; see the
four `spec_case_*` lines in `evidence/stage3.log`.

### Mechanical program identity and sensitivity

`solutionProgram` is not an oracle: it is intended as a definitional alias for
the full translated body. `evidence/make_program_checks.py` reads the trusted
regeneration verbatim and only makes the translator's four omitted empty
statement lists explicit as `.Stmts`. A reachability identity claim between
that generated term and `solutionProgram` closes with `#Top`; K reports it as
trivial after normalization. This is recorded in `evidence/stage4.log`.

A separate body-sensitivity mutation changes the actual final return in the
program term from `"YES"` to `"NO"`. On intervals `(0,2),(0,2)`, the mutated
definition builds successfully and the expected-`YES` proof fails with
`WarnStuckClaimState`; its residual contains the mutated program's final
`strVal("NO")`. Thus the entry proof is tied to the executed body rather than
only to an external source filename.

Stage 4 result: **PASS** for domain coverage, result constraint, real-program
pinning, and body sensitivity. Soundness of the proof-local operational bridge
fails in Stage 5.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is in `evidence/rule-inventory.md`. The mechanical
scan found:

- 33 ordinary rules and 8 evaluation contexts in `semantic.k`;
- 9 rules in `verification.k`;
- 5 claims in `spec.k`;
- four local `[function]` declarations;
- no local `total`, explicit `functional`, opaque, `simplification`,
  `anywhere`, macro, or alias declarations;
- one priority rule, at `verification.k:71-89`.

The raw scan and counts are in `evidence/stage5.sh` and
`evidence/stage5.log`.

### Generated semantics

Every constructor in `solution.mpy` maps to declared syntax and an executable
rule: module/function/list handling, name assignment and lookup, both
conditionals, the reconstructed while loop, return control, tuple construction
and indexing, integer literals and strings, `+`, `-`, `*`, `%`, and `<`, `<=`,
`>`, `==`. The configuration contains exactly computation, function bindings,
and local environment state. Argument and binary operand evaluation are
left-to-right. The one function is loaded under its actual `"intersection"`
binding, and `invoke` executes the exact stored body.

The semantics is deliberately minimal. It does not model unused Python
constructs, which is permitted in generated-semantics mode. Its return rule is
broad as a reusable language rule, but on every reachable submitted-program
state the entire remaining computation is the current top-level function
continuation, so no target control or observable state is lost. Unbounded K
integers match Python integers for the used operations; modulo is guarded by a
nonzero divisor and the submitted program has divisor at least 2.

No false semantic conclusion witness was found for the submitted domain.

### Definitional proof functions

`primeResult` has three disjoint equations: exhausted search, found divisor,
and advance divisor. On its used domain `N>=2,D>=2`, their guards are exhaustive
and recursion advances toward an exhausted or factor branch.
`intersectionResult` and `lengthResult` split disjointly at length 2.
`intersectionResult` is unused by the entry claims. `solutionProgram` is the
mechanically checked exact constructor alias. These symbols are defined by
equations; none is an unconstrained result-bearing oracle.

### Unsound priority bridge P09

The whole-program definition adds:

`verification.k:71-89`

This rule matches the exact submitted while loop and exact final
`Return(Str("YES"))` suffix, reads `length=N` and `divisor=D`, rewrites the
whole `<k>` cell to `primeResult(N,D)`, and leaves all other cells unchanged.
Priority 40 makes it preempt ordinary while execution.

The bridge-free loop claim is a valid result connection theorem, but it does
**not** justify P09's state transition. Its postcondition explicitly rewrites

`"divisor" |-> (intVal(D) => ?_VD:Value)`.

P09 instead preserves `intVal(D)`. The following independently executed
witness establishes a concrete false conclusion:

1. Start at the exact matched loop with `length=5`, `divisor=2`, and the exact
   final `return "YES"` continuation. This state is reachable for valid
   intervals having overlap length 5.
2. Under the bridge-free `VERIFICATION` definition, concrete/symbolic
   execution tests 2, finds it does not divide 5, increments to 3, exits, and
   returns `YES`. A claim demanding final `divisor=2` exits 1 with
   `WarnStuckClaimState`; the residual visibly has `divisor |-> intVal(3)`.
3. Under `VERIFICATION-WITH-LOOP-LEMMA`, the same false claim exits 0 and
   prints `#Top`, because P09 returns `primeResult(5,2) = YES` while leaving
   `divisor=2`.

The exact commands, statuses, and residual are in `evidence/stage4.log`.
This compares result, control, and the affected state cell over a satisfiable
ground witness. It is not merely an evidence gap: it is a demonstrated false
reachability conclusion enabled by the bridge on the intended domain.

The entry claims existentially forget their final environment, so this
specific false state is hidden from their postconditions and the returned
value happens to remain correct. That does not make the rule sound. The
whole-program proof imports and uses an operational rule stronger than its
bridge-free theorem, and the extended theory can prove a false reachable
configuration. Under the required Gate A and benchmark decision boundary, this
is a material proof-rule unsoundness.

Stage 5 result: **FAIL**.

## 6. Fresh non-vacuity test

The candidate supplied no authoritative vacuity result, so I created
`evidence/spec-vacuity-fresh.k`. It runs the original pinned program on
`(0,2),(0,2)`, a satisfying input whose intersection length is the prime 2,
but changes the required return from the true `"YES"` to the false `"NO"`.

- `kprove ... --dry-run` exits 0, establishing that the mutation and imports
  build.
- The actual `kprove` exits 1 with `WarnStuckClaimState`.
- The residual is the completed original program with `strVal("YES")`, exactly
  the unmet result obligation.

The artifact, exact commands, statuses, and bounded residual are in
`evidence/stage6.sh` and `evidence/stage6.log`.

Stage 6 result: **PASS**. The proof is result-constraining and non-vacuous; its
failure is operational-rule soundness, not a tautological postcondition.

## 7. Proven versus assumed accounting

### What the successful K runs establish

Under bridge-free `semantic.k` plus the definitional equations in
`VERIFICATION`, the successful loop claim establishes partial correctness of
the exact trial-division loop: from `N>=2,D>=2`, its returned value is
`primeResult(N,D)`, with its final divisor deliberately existential.

Under the stronger, bridge-enabled `VERIFICATION-WITH-LOOP-LEMMA`, the four
successful entry claims establish that, for all unbounded integer endpoints
with `A<=B` and `C<=D`, the pinned program returns the corresponding
`lengthResult` in each exhaustive endpoint-order partition. This formal
statement constrains the return and leaves final local maps existential.

Because the stronger definition contains P09, that second statement is proved
inside an unsound operational extension and is not accepted as a legitimate
proof of the real program.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 reachability engine and built-in `INT`, `BOOL`, `STRING`, and `MAP` domains | Arithmetic, maps, rewriting, and proof checking | Ordinary low-level trusted computing base; acceptable. |
| Trusted `/reference/py2mpy.py` | Source-to-constructor identity | Launcher-trusted and byte-matched; regeneration is exact. Acceptable. |
| Candidate-generated `semantic.k` | Meaning of every executed constructor | Audited rule by rule and differentially exercised, but it remains a generated model rather than CPython itself. Its used subset is faithful; acceptable for `GENERATED_SEMANTICS`. |
| Standard number-theoretic fact that a composite `N>=2` has a divisor at most `sqrt(N)` | Connects recursive `primeResult(N,2)` to the natural-language word “prime” | Informal ordinary mathematics, supported by the transparent exhaustive equations; acceptable intent bridge, not an opaque oracle. |
| Trusted canonical Python and independent oracle tests | Finite program/intent and semantics evidence | Empirical only; they do not replace the K proof. |
| `solutionProgram` | Program identity | Definitional and mechanically constructor-checked; acceptable. |
| P09 at `verification.k:71-89` | Replaces real loop execution; affects return, control, and local state | **Illegitimate.** Its result is connected, but its preserved divisor state is false and exceeds the proved theorem. |

There are no external calls, allocation, heap, I/O, exceptions, concurrency,
opaque result symbols, or unmodeled used constructors. Wrong types, malformed
pairs, and invalid endpoint ordering are outside the documented/formal domain.
The result is a partial-correctness assessment, not a separate total-termination
theorem.

Gate accounting:

- Gate A, real-program soundness: **FAIL**, because P09 enables the concrete
  false state conclusion above.
- Gate B, intent adequacy considered independently: **PASS**; the four claims
  cover all valid integer endpoints and express the correct result.
- Gate C, evidence auditability considered independently: **PASS**; fresh
  builds, tests, mutations, commands, statuses, and residuals are preserved.

The Gate A failure controls the benchmark decision. A correct implementation,
fresh `#Top`, exact source pin, and successful non-vacuity mutation cannot
legitimize an unsound operational proof rule.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
