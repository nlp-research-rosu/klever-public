# Independent adversarial review: HumanEval 31 (`is_prime`)

The candidate’s three written claims are reproducible and individually sound, and
the proof macros exactly contain the submitted function body. However, the
candidate does not contain a reachability claim proving the required result for
any `N >= 2`. Its `entry-large-prefix` claim stops immediately after removing the
initial `if` and leaves the assignment, loop, and return as residual code.
`isPrimeSpec` is never used in a claim. The separately proved loop lemma is not
imported into or machine-composed with an entry theorem. This is a material
missing target theorem, so the successful `#Top` results do not constitute the
requested partial-correctness proof.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- record layout `legacy-selected-stage1`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- problem `31-is-prime`;
- complete input provenance.

The trusted `/reference/reference-semantics` mount is present, so it is
consistent with the rendered mode. The campaign block in `/audit-input.json`
is semantically identical to `/audit-campaign-lock.json`; the lock’s independently
computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record.

All records required by `legacy-selected-stage1` are present, regular/readable,
and non-symlinked: `/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the structured trace. `usage.json` is also present.
`runtime-metrics.json` is absent, but historical runtime metrics are explicitly
not required for this layout. The single trace contains 755 valid JSONL records
with no parse error, and its raw hash matches both the invocation and result
records.

Every raw file hash recorded by the launcher for the campaign lock, canonical,
prompt, translator, run/task/result/invocation records, metrics, usage,
generation prompt/output/final message, trace, and legacy extra records was
independently recomputed and matched. Reviewer-defined, per-file manifests for
the complete candidate, reference, and generation-evidence trees are preserved
in `evidence/*-tree-manifest.tsv`; all three trees have zero symlinks.

The candidate prompt and translator are byte-identical to their trusted mounts.
The candidate `reference-semantics/` has exactly the same 25 entries, entry
types, paths, and file bytes as the trusted tree. There are no missing,
additional, changed, mistyped, or symlinked semantics entries. The independent
manifest aggregate is
`51c71872287731bc1458ed960ef68fb8126adae2af5e488b22b5549c1a8e69ec`
for both trees.

Evidence:

- `evidence/stage1_check.py`
- `evidence/stage1_integrity.log` (exit 0)
- `evidence/mounted_tree_manifests.py`
- `evidence/mounted_tree_manifests.log` (exit 0)
- `evidence/mounted-tree-hash-summary.json`

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt’s contract is: for an integer `n`, return `True` exactly
when `n` is prime and `False` otherwise. The prompt examples cover prime,
composite, and `n < 2` cases. The trusted canonical implementation rejects
`n < 2`, then tests integer divisors. Its use of `range` establishes the
intended HumanEval input domain as Python integers; an “empty” collection case
does not apply to this scalar function.

The submitted implementation is a standard equivalent algorithm: reject
`n < 2`, then test divisors from 2 while `divisor * divisor <= n`. It uses
Python’s unbounded integers, so there is no multiplication-overflow discrepancy.

In clean scratch space, the trusted translator regenerated `solution.mpy`
byte-for-byte:

- submitted SHA-256:
  `870a9890935eca71a5ef2604103b07f703ec76b9fd3fcae0600d75d3d8964e7d`;
- regenerated SHA-256: the same value;
- `cmp` exit: 0.

The independent differential test imported both the trusted canonical module
and submitted module and also used a separately implemented `math.isqrt`
primality oracle. It checked all seven prompt examples, explicit branch and
square boundaries, every integer from -100 through 5000, and 2,000
deterministically generated integers in `[-100000, 100000]`. There were 7,046
unique inputs and zero mismatches. The exact input list is preserved with
SHA-256
`e152999eaf7752865185f8005155187e5b4467c91fe2c3c236c707d144c1f82e`.

A separate K boundary harness executed the exact submitted body under the fresh
LLVM definition for negative values, 0, 1, the 2/3/4/5 boundaries, square
composites, primes, and the large prompt example. It terminated with `.K`,
`NoExc`, and exit code 0.

Evidence:

- `evidence/differential_test.py`
- `evidence/differential_inputs.json`
- `evidence/stage2_fidelity.log` (exit 0)
- `evidence/k_boundary_tests.py`
- `evidence/stage4_k_boundaries.log` (exit 0)

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/31-is-prime-audit`.
Candidate-provided compiled data, `__pycache__`, and `kore-exec.tar.gz` were not
used. The semantics copied into scratch came from the trusted reference mount.
The initial scratch precheck confirmed that `runtime-kompiled`,
`proof-base-kompiled`, and `proof-kompiled` did not exist.

The live tools are K v7.1.293. These fresh commands succeeded:

| Purpose | Command summary | Result |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | exit 0 |
| Concrete examples | `krun concrete_tests.regenerated.mpy --definition runtime-kompiled` | exit 0, `.K`, `NoExc` |
| Loop proof definition | `kompile verification.k --backend haskell --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX --output-definition proof-base-kompiled` | exit 0 |
| Loop module | `kprove spec.k --definition proof-base-kompiled --spec-module LOOP-SPEC` | exit 0, `#Top` |
| Entry proof definition | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition proof-kompiled` | exit 0 |
| Entry module | `kprove spec.k --definition proof-kompiled --spec-module SPEC` | exit 0, `#Top` |

Each actual claim was then run alone using its correct bare CLI label (the
source uses trailing `[label(...)]` attributes):

- `--claims loop-correct`: exit 0, `#Top`;
- `--claims entry-small`: exit 0, `#Top`;
- `--claims entry-large-prefix`: exit 0, `#Top`.

The reconstruction log also preserves an initial reviewer diagnostic mistake
using `MODULE.label`, which K rejected as an unused filtering label before proof
execution. The corrected runs above are in
`evidence/stage3_claims_individual.log` and all succeeded. This diagnostic error
is not candidate evidence.

Evidence:

- `evidence/stage3_reconstruct.sh`
- `evidence/stage3_reconstruct.log`
- `evidence/stage3_claims_individual.sh`
- `evidence/stage3_claims_individual.log` (exit 0)

Thus the candidate’s `#Top` claims are reproducible. That fact proves only the
claims actually written.

## 4. Adequacy and real-program pinning

### Constructor identity

`kast --expand-macros --output json` was used to parse the trusted regeneration
and independently expand `#entryBody`, `#primeCond`, and `#primeLoopBody`.
A structural KAST comparison established:

- function name exactly `"is_prime"`;
- parameter list exactly `"n"`;
- `#entryBody` exactly equals the submitted `FuncDef` body;
- `#primeCond` exactly equals the submitted `While` condition;
- `#primeLoopBody` exactly equals the submitted `While` body.

This is constructor-level identity, not a textual approximation. The formal
claims begin inside an already established call frame, which is allowed by the
audit boundary because the exact function body is pinned.

Evidence: `evidence/constructor_compare.py`,
`evidence/stage4_constructor_retry.log` (exit 0).

### Claim meanings and satisfiable witnesses

| Claim | Plain-language precondition and postcondition | Satisfiable witness | Assessment |
|---|---|---|---|
| `loop-correct` | With exact remaining loop code, integer `D >= 2`, local `n=N`, local `divisor=D`, and a well-formed call frame, execution returns `trialPrime(N,D)`, pops the frame, and preserves heap/exception/exit state. | `N=5, D=2, L=1, CALLER=0, SC={}`, empty heap/stack tail, `.K` continuation. `trialPrime(5,2)=true`; both Python implementations return `True`. | Result-constraining loop lemma. |
| `entry-small` | With the exact closure/body and call frame, if `N < 2`, execution returns `false` and pops the frame. | `N=1`; both Python implementations return `False`. | Correct result theorem for the small branch. |
| `entry-large-prefix` | If `N >= 2`, reduce only the initial false branch to the residual `Assign; While; Return(true); #endcall`. Omitted stack, return, heap, and exception cells are merely framed. | `N=4` and `N=5` with `SC={}` both satisfy it. | Prefix theorem only; no Boolean result or final state. |

The decisive contrast is `N=4` versus `N=5`: the required results are
respectively `False` and `True`, but `entry-large-prefix` reaches the same
residual program shape and asserts neither result. It is therefore not a
one-way encoding of a result; it has no result postcondition at all.

`isPrimeSpec` occurs only in `verification.k` definitions and comments. It
occurs in no claim. `trialPrime` occurs in the loop lemma, but no entry claim
has destination `trialPrime(N,2)` or `isPrimeSpec(N)`.

The comment at `spec.k:93-96` describes an intended composition: assignment
would establish `divisor=2`, and then the loop theorem would return
`trialPrime(N,2)`. That composition is not present in K:

- `LOOP-SPEC` is proved against `proof-base-kompiled`;
- `SPEC` imports `VERIFICATION`, not `LOOP-SPEC`;
- the loop claim is not part of either proof definition;
- proving one specification module does not install its claim into the later
  compiled definition;
- there is no full entry claim whose source and destination could exercise the
  loop circularity.

The large-prefix claim also omits the concrete call-frame cells that the loop
claim requires, so even the necessary configuration-level composition is left
informal.

### Body sensitivity

A fresh mutation changed the actual `#entryBody` macro’s final
`Return(Bool(true))` to `Return(Bool(false))`, while leaving the prefix claim’s
explicit destination unchanged. Structural comparison then reported that the
executed macro no longer equaled the submitted body, and the independently
rebuilt `entry-large-prefix` proof failed with a stuck residual
`Return(false)`. This mutation changes the claim’s executed term, rather than
merely editing an external Python file.

Evidence:

- `evidence/verification-body-mutation.k`
- `evidence/spec-body-mutation.k`
- `evidence/stage4_body_sensitivity.log` (expected mutation failures observed)
- `evidence/claim_witnesses.py`
- `evidence/stage4_claim_adequacy_retry.log` (exit 0)

## 5. Rule-by-rule static soundness review

The complete source-level inventory is
`evidence/rule_inventory.tsv` (SHA-256
`22f94fe154f1e67e6e580a3dd2e92f94bac2cb35aada89781e3c1250447842c7`).
It contains every declaration starting with `configuration`, `syntax`, `rule`,
`context`, or `claim` in the assembled semantics, every supplied helper K file,
`verification.k`, and `spec.k`, with complete guards and attributes.

Inventory totals:

- 946 items: 1 configuration, 232 syntax declarations, 705 rules, 5 contexts,
  and 3 claims;
- 467 equational and 238 operational rules;
- 148 function declarations, 107 `total` declarations, 41 priority-bearing
  items, 35 concrete rules, and 26 `owise` rules;
- 22 `symbol`/`no-evaluators` opaque symbols;
- no source `functional` or `simplification` attributes.

The supplied-semantics tree is the fixed trusted baseline for this rendered
mode. The inventory marks all 928 supplied items and distinguishes the 51
declarations/rules used by the formal claims from 877 items not reachable from
the submitted constructor fragment. The unused float, sort, MD5, collection,
string, and other helpers cannot match the integer-only terms or cells reached
by these claims. In particular, none of the 22 opaque symbols can affect a
branch, returned value, state, exception, or postcondition in this proof.

The submitted constructs map to the following checked fixed-semantics fragment:

- `Module`, `FuncDef`, `Params`, statement sequencing, and the exact
  configuration in `syntax.k`, `core.k`, and `functions.k`;
- `Int`, `Bool`, and local `Name` lookup in `core.k`;
- left-to-right `BinOp` strictness and explicit `Compare` contexts in
  `syntax.k` and `operators.k`;
- integer `+`, `*`, positive-divisor `%`, `<`, `<=`, and `==` in `int.k`;
- assignment, augmented assignment, `If`, and `While`/loop-label control in
  `controls.k`;
- `Return`, `#pop`, environment restoration, frame removal, and scope deletion
  in `functions.k`.

On the claim domain, every modulo divisor is at least 2. Thus the supplied
`pyMod` rule is defined and agrees with Python; no division-by-zero or negative
divisor behavior is exposed. All values are unbounded mathematical integers,
matching Python integers for this program. The program allocates no heap
objects, produces no output, and has no modeled exception path, so the loop
claim’s unchanged heap/heap-location/exception/exit cells are accurate.
Return/pop control is fully reflected in the loop and small-entry destinations.

The 15 proof-local inventory items are:

1. Two finite-map deletion identities. If `L` is absent from `M`, deleting it
   returns `M`; if `(M L |-> V)` is formed with `L` absent from `M`, deleting
   `L` returns `M`. Their guards make the cases true and non-overlapping.
2. Three macro declarations and their three equations. Structural KAST
   comparison proves that they are exact syntax abbreviations and do not
   replace execution.
3. `trialPrime` plus three guarded equations. For used `D >= 2`, the guards
   `D*D>N`, divisible, and non-divisible are disjoint and exhaustive; the
   recursive case increments `D`. It is not declared `total`, introduces no
   oracle, and its value is fixed by the equations on every use.
4. `isPrimeSpec` plus two equations. `N<2` and `N>=2` are disjoint and
   exhaustive over integers. This definition is sound but unused by every
   claim.

There are no proof-local priority rules, totality assertions, opaque symbols,
simplification rules, operational bridges, or execution-summary rewrites.
No proof-local rule is unsound, so this review makes no unsound-rule allegation
requiring a false-conclusion witness. The failure is narrower and decisive:
the required large-domain result claim is absent. The `N=4`/`N=5` witness above
demonstrates that adequacy gap without mislabeling a true prefix rule as
unsound.

Evidence:

- `evidence/rule_inventory.py`
- `evidence/rule_inventory.tsv`
- `evidence/rule_inventory_summary.json`
- `evidence/rule_inventory_retry.log` (exit 0)

## 6. Fresh non-vacuity test

The fresh `SPEC-VACUITY` mutation changed the result-bearing `entry-small`
destination from `false` to `true`. `N=1` satisfies the unchanged precondition,
and both trusted canonical and submitted Python implementations return `False`.
The continuation was concretely fixed to `.K` so the probe tested only this
obligation.

`kprove ... --dry-run` exited 0, establishing that the mutation parsed and
built. The actual proof exited 1 with `WarnStuckClaimState`; its residual
configuration has `<k> false ~> .K </k>` while the destination demands `true`.
This is the expected unmet result obligation.

An earlier exploratory version left `CONT` arbitrary and reached an unrelated
unsupported `FLOAT.min` hook. That run is preserved in
`stage6_nonvacuity.log` but is explicitly rejected as non-vacuity evidence.
The narrowed retry in `stage6_nonvacuity_retry.log` is the valid test.

Evidence:

- `evidence/spec-vacuity.k`
- `evidence/stage6_nonvacuity.sh`
- `evidence/stage6_nonvacuity_retry.log` (overall audit script exit 0; expected
  `kprove` exit 1)

The mutation shows that the small-entry theorem is discriminating. It cannot
supply the missing large-entry result theorem.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied K theory and the sound proof-local equations:

1. The exact submitted remaining `while` computation, started with any integer
   `N` and `D >= 2` in the stated call frame, returns the recursively defined
   `trialPrime(N,D)` value if it terminates, restores the caller frame, and
   preserves the stated non-control cells.
2. The exact submitted body returns `false` for every integer `N < 2` from the
   stated call frame.
3. For every integer `N >= 2`, the exact submitted body’s initial `if` reduces
   to the residual assignment/loop/return code.

### Not formally established

The candidate does not establish that executing `is_prime(N)` returns
`trialPrime(N,2)` or `isPrimeSpec(N)` for `N >= 2`. Consequently it does not
establish the requested equivalence between the real program’s returned
Boolean and primality over the full integer domain.

### Trust ledger

| Boundary | Dependents and assessment |
|---|---|
| Supplied MPY semantics | Fixed by the condition and recursively integrity-checked. The actually used integer/control/frame fragment was manually reviewed and concretely exercised. Acceptable. |
| K Int/Bool/Map hooks and Haskell/LLVM backends | Ordinary low-level execution/proof boundary used by all claims. Tool versions and fresh builds are recorded. Acceptable. |
| Trusted translator | Connects `solution.py` to `solution.mpy`; byte identity and constructor identity were independently established. Acceptable. |
| Elementary factor theorem | The informal fact that a composite `N >= 2` has a factor at most `sqrt(N)` connects `trialPrime(N,2)` to mathematical primality. It is true ordinary mathematics but not a K theorem here. This would be a minor intent bridge if a full entry theorem existed; it cannot repair the missing theorem. |
| Partial-correctness termination boundary | `kprove` establishes partial correctness, not termination. This is the requested proof mode and is acceptable. |
| 22 fixed-semantics opaque symbols | All are unreachable from the submitted integer-only claim terms and have no dependents in the result. Acceptable/inert. |
| Differential and concrete tests | 7,046 Python cases plus K boundaries support program fidelity and the intended mathematical bridge only. They are finite evidence and are not treated as the proof. |

Gate accounting:

- Real-program/result gate: **FAIL for the requested theorem**. Existing claims
  are sound and body-sensitive, but the final result for `N >= 2` is not
  constrained by any entry claim.
- Intent adequacy gate: **FAIL**. The source contract covers all integers,
  while the only complete entry result theorem covers `N < 2`.
- Evidence/trust auditability gate: **PASS**. Provenance, builds, proofs,
  witnesses, inventory, and mutations are reproducible.

Under the benchmark decision boundary, a missing or non-result-constraining
target theorem is `FAIL / NOT_LEGIT`, even when supporting lemmas and finite
tests are correct. This is not an infrastructure failure and not merely a
non-fatal trust-boundary concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
