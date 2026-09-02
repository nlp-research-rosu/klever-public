# Independent adversarial audit — 58-common

Decision: **FAIL / NOT_LEGIT**.

The candidate does contain a cleanly reconstructible, non-vacuous K proof of a
result-constraining theorem under the supplied K theory. The submitted
`solution.mpy` is pinned exactly and the proof-local definitions are sound
within that theory. It is nevertheless not a legitimate proof of the real
Python program over the contract’s full input domain: the used supplied
membership rules model equality with structural `==K`. Python equates numeric
cross-types such as `True` and `1`; K does not. The candidate entry claim has no
integer-only or homogeneous-type precondition and accepts arbitrary `ValSeq`.
For the valid input `common([True], [1])`, both trusted canonical Python and the
candidate Python return `[True]`, while a fresh execution of the exact
translated program under the supplied K semantics computes the empty list and
fails a `[True]` assertion. This is a concrete false-conclusion witness for the
rules at `reference-semantics/semantics/list.k:63-66`.

All paths below are under `/audit-output/` unless otherwise stated.

## 1. Input and provenance integrity

The rendered mode and trusted mounts agree: this is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` exists as a regular directory. There is no
infrastructure breach.

The recursive, no-dereference comparison found the candidate
`reference-semantics/` tree byte-identical to the trusted tree. It found no
missing, additional, changed, mistyped, or symlinked entry. Candidate
`prompt.py` and `py2mpy.py` are likewise byte-identical to their trusted mounted
versions, and no candidate symlink exists. Evidence:

- `evidence/stage1/check_integrity.sh`
- `evidence/stage1/integrity.log`
- `evidence/stage1/source_hashes.log`

Four requested provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured trace is present. Consequently there were no such untrusted
claims to read. This is a provenance/auditability integrity failure, although it
did not prevent independent reconstruction. `kore-exec.tar.gz` and
`__pycache__/solution.cpython-310.pyc` were treated only as untrusted built
artifacts and removed from the scratch copy. Candidate `prove.sh`,
`concrete-tests.py`, and `concrete-tests.mpy` were inspected only as claims.

The source snapshot and line-numbered candidate proof artifacts are preserved
in `evidence/stage1/core_sources.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt says `common(l1, l2)` returns the sorted, unique elements
common to the two input lists. The trusted canonical implementation performs
nested equality comparisons, inserts equal elements into a set, converts the
set to a list, and sorts it. The natural Python domain is therefore pairs of
lists for which the relevant equality, hashing, and final sorting operations
terminate normally. The prompt and signature impose no element-type,
integer-only, or homogeneous-numeric restriction.

The candidate uses a result list, scans `l1` left-to-right, appends an item
exactly when it occurs in `l2` and is not already in the result, and returns
`sorted(result)`. It is a different but ordinary implementation of the same
Python behavior.

### Translation identity

The trusted translator regenerated `solution.mpy` from the scratch copy of
`solution.py` with exit 0. The regenerated and submitted files are byte
identical, both SHA-256
`031e94b911c1eae40ab6f6bcda882685fd599c7c48bb1d39f2c3a804e517a352`.
See `evidence/stage2/regenerate_solution.sh` and
`evidence/stage2/regeneration.log`.

### Independent differential

`evidence/stage2/differential_test.py` independently imports
`/reference/canonical.py` and the scratch candidate source. It records all
inputs in `evidence/stage2/differential-inputs.json` and covers:

- the two documented examples;
- nine explicit empty, loop, membership, duplicate-suppression, order,
  negative, and large-integer boundaries;
- all 24,336 ordered pairs of lists of length 0 through 3 over
  `[-2,-1,0,1,2]`;
- 1,000 deterministic random integer-list pairs (seed 580058, lengths 0
  through 20, values -1000 through 1000).

Command and result are in `evidence/stage2/differential.log`: 25,347 total
cases, zero mismatches, exit 0.

The later mixed-numeric witness also confirms that candidate Python agrees with
canonical Python on `[True]`/`[1]`, `[1]`/`[True]`, `[1]`/`[1.0]`, and a
`False`/`0` duplicate case. Thus the eventual failure is not a
candidate-versus-canonical algorithm divergence; it is the K-to-Python bridge.
See `evidence/stage5/python_mixed_numeric.log`.

## 3. Clean proof reconstruction

All work was done under `/tmp/audit-work/case58`. The copied archive and Python
cache were removed, the copied semantics directory was replaced with a fresh
copy from `/reference/reference-semantics`, and a recursive comparison confirmed
identity. See `evidence/stage3/scratch_sanitization.log`.

The independently installed live toolchain is K v7.1.337 (build date
2026-06-18); exact paths and versions are in
`evidence/stage3/toolchain.log`.

### Concrete definition

Fresh command:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled
```

It exited 0. The LLVM compiler warned about non-exhaustive total functions in
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and out-of-bounds
`valSeqAt`. None of those terms is reachable from this submitted program on the
audited paths. Full bounded output is in
`evidence/stage3/kompile_llvm.log`.

The trusted translator reproduced the candidate concrete driver byte-for-byte.
Fresh `krun` execution exited 0 with `.K`, `NoExc`, and exit code 0 after all
four assertions. See:

- `evidence/stage3/concrete_regeneration.log`
- `evidence/stage3/krun_candidate_tests.log`

### Proof definition and positive claims

Fresh command:

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition verification-kompiled
```

It exited 0. Its only warnings were unused variables in two supplied string
comparison rules. See `evidence/stage3/kompile_haskell.log`.

Each target was then run in dependency order. A helper was trusted only in a
later command after its own proof had exited 0 with `#Top`:

| Target | Dependency treatment | Result |
|---|---|---|
| `SPEC.member-fold` | none trusted | exit 0, `#Top` |
| `SPEC.common-loop` | previously proved `member-fold` trusted | exit 0, `#Top` |
| `SPEC.common-function` | previously proved `member-fold` and `common-loop` trusted | exit 0, `#Top` |

Exact commands and outputs:

- `evidence/stage3/kprove_member_fold.log`
- `evidence/stage3/kprove_common_loop.log`
- `evidence/stage3/kprove_common_function.log`

Accordingly, clean reconstruction itself passes. The verdict is not based on a
timeout, stale definition, cache, candidate trace, or unverified `#Top`.

## 4. Adequacy and real-program pinning

Plain-language preconditions, postconditions, and concrete satisfying states
for all three claims are recorded in
`evidence/stage4/claim-witnesses.md`.

In summary:

- `member-fold` starts with the real supplied `#memberAcc` fold under an
  arbitrary continuation and concludes with `memberVS` under that same
  continuation.
- `common-loop` starts at the real `#loop` head with the exact target and body,
  a scope containing `l1`, `l2`, `result`, and `item`, and a heap result list.
  It consumes the loop, updates `item` to the last yielded value, and updates
  only the result heap object via `commonAcc`, while framing unrelated state and
  the continuation.
- `common-function` starts from the pristine supplied configuration, loads the
  exact function definition, and calls it on `list(FIRST)` and
  `list(SECOND)`. It returns the fixed reference `ref(1)`, fixes heap object 0
  to `commonSpec`, fixes object 1 to `sortVS(commonSpec)`, fixes the heap
  counter to 2, and constrains scope, stack, return, exception, and exit state.
  There is no free return variable or one-way implication.

### Exact submitted-program identity

The reviewer parsed the submitted `solution.mpy` and the proof term
`Module(commonDefinition)` independently with the fresh proof definition and
serialized both to KORE. They are byte-identical, with the same SHA-256
`2efed36c798d24a4b8579dfad30aafef9f12ce6499006ac3ea2b3e35ae5b6cba`.
Thus the macros do not substitute a different program. Evidence:

- `evidence/stage4/check_program_pinning.sh`
- `evidence/stage4/program_pinning.log`
- `evidence/stage4/submitted-program.kore`
- `evidence/stage4/macro-program.kore`

### Satisfying ground instance

For `FIRST=[2,2,1,1]` and `SECOND=[1,2,2]`, `commonSpec` is `[2,1]` and
the claimed sorted value is `[1,2]`. Both Python implementations return
`[1,2]` (`evidence/stage4/python_ground_witness.log`). A separate, fully ground
K entry claim with the exact concrete heap result closed directly with `#Top`
and exit 0 without trusting either symbolic helper claim
(`evidence/stage4/kprove_ground_witness.log`).

The real-program pinning is therefore syntactically exact and non-vacuous.
Adequacy nevertheless fails on the broader precondition: `FIRST:ValSeq` and
`SECOND:ValSeq` admit the mixed-numeric witness described in Stage 5, and no
claim guard narrows that domain.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/stage5/inventory_k.py` inventories the byte-identical trusted
`semantics.k` tree plus candidate `verification.k` and `spec.k`.
`evidence/stage5/rule-inventory.tsv` has exactly 1,118 records, matching an
independent source-pattern count:

- 707 rules;
- 235 syntax declarations;
- 3 claims;
- 1 configuration;
- 5 contexts;
- all module/import/require records;
- 150 function-bearing declarations;
- 112 `total` declarations;
- no `functional` declarations;
- 45 priority-bearing records;
- 3 simplification rules;
- 35 concrete rules;
- 26 `owise` rules;
- 25 symbol declarations, of which 22 are explicitly `no-evaluators`.

Every record has file/line range, kind, attributes, reachability classification,
and disposition. The final inventory hash, counts, and the two mismatching
rules are in `evidence/stage5/inventory_final_hash.log`. The submitted construct
to rule/control/state map is
`evidence/stage5/used-construct-map.md`.

All unused modules and opaque symbols are construct-disjoint from the submitted
program. Of the 22 no-evaluator symbols, only `sortVS` is reachable.

### Candidate proof-local rules

The candidate adds no ordinary runtime rewrite, priority rule, operational
bridge, arbitrary return, or unconstrained oracle.

| Extension | Static decision |
|---|---|
| `commonLoopBody` macro/rule | Exact body abbreviation; KORE pinning passes. |
| `commonBody` macro/rule | Exact submitted function body; KORE pinning passes. |
| `commonDefinition` macro/rule | Exact submitted `FuncDef`; KORE pinning passes. |
| `memberVS` | Exhaustive empty/cons equations; equality/disequality guards are disjoint; recursion strictly shortens the sequence. It exactly summarizes K membership, including K’s modeling limitation. |
| `shouldAdd` | Exact Boolean conjunction of the two K membership predicates. |
| `commonAcc` | Exhaustive empty/cons equations; each call strictly shortens `FIRST`; true branch appends exactly once. |
| `commonSpec` | Transparent alias to `commonAcc(...,.ValSeq)`. |
| `lastAfter` | Exhaustive empty/cons equations; strict structural descent. |

All five proof-local function declarations are `total`; their equations cover
their algebraic domains, their recursive arguments descend, and no overlaps
give conflicting right-hand sides. The only simplification rules in the
candidate are the three `memberVS` cases. There are no candidate opaque symbols
or priority rules.

`member-fold` is a bridge-free universal connection theorem for the complete
operational membership-fold context and is proved before downstream use.
`common-loop` matches the exact target, body, environment bindings, result heap
object, and arbitrary continuation. The fixed rules preserve evaluation order:
callee and call arguments evaluate left-to-right; `and` short-circuits;
iteration yields left-to-right; `append` updates the same allocated list;
`sorted` reads that list, allocates a new object; and return restores the frame.
Priority rules on the reachable path have appropriate containment:

- ref dereferencing precedes generic comparisons/builtin routing;
- the list `append` rule precedes generic bound-method routing;
- the `sorted` rule precedes the generic `applyBuiltin` fallback;
- closure-cell assignment/binding rules require `$cells` and are pruned in this
  plain frame.

The helper claims frame the remaining configuration; allocation and return
effects are pinned in the entry postcondition.

### Opaque supplied sort boundary

`sortVS` at `semantics/sort.k:18` is `[function,total,symbol(sortVS),
no-evaluators]`. In symbolic proof it is an externally supplied, result-bearing
opaque primitive. The K theorem establishes a result of the form
`sortVS(commonSpec(FIRST,SECOND))`; it does not prove within K that this is an
ascending permutation. Concrete integer/string insertion-sort rules exist for
execution, and the direct ground proof plus the 25,347 integer differentials
support the integer bridge finitely. They do not establish a universal
connection theorem. This would independently warrant a documented trust
concern, not by itself the present failure.

### Material used-semantics mismatch and false witness

The used rules are:

```text
list.k:63-64  #iterYield(E, _) ~> #memberCont(V) => true
              requires E ==K V
list.k:65-66  #iterYield(E, R) ~> #memberCont(V) => #memberAcc(V, R)
              requires notBool (E ==K V)
```

These guards are consistent structural K mathematics, but they are not the
real Python equality used by `item in list` on their complete match domain.
Python specifies numeric cross-type equality such that `True == 1`.

Concrete false-conclusion witness:

```text
FIRST  = [True]
SECOND = [1]
Python canonical.common = [True]
Python solution.common  = [True]
K common result         = []
```

`evidence/stage5/mixed-type-k.py` begins with the exact submitted function and
asserts `common([True],[1]) == [True]`. It was translated with the trusted
translator (`evidence/stage5/translate_mixed_k.log`, exit 0) and executed
against the fresh LLVM definition. The final K configuration has the two input
objects, heap object 2 as the empty accumulator, heap object 3 as the empty
sorted result, `AssertionError`, and `<exit-code> 1`; `krun` exits 1. See
`evidence/stage5/krun_mixed_type.log`. The two Python results and additional
mixed-numeric cases are in `evidence/stage5/python_mixed_numeric.log`.

This input satisfies the prompt-level list contract, both Python programs
terminate normally, and the candidate K entry precondition admits both
constructors. The mismatch therefore makes a wrong result conclusion possible
on the intended domain. It is not merely an unreachable bad rule, a timeout, an
unsupported unused construct, or finite-evidence uncertainty. No other rule is
labeled unsound in this review.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; the reviewer created a fresh one at
`evidence/stage6/spec-vacuity.k`.

The mutation keeps the exact entry execution and complete final heap but changes
the returned reference from the real sorted-list object `ref(1)` to accumulator
object `ref(0)`. It is observably false for the satisfying ground input
`[2,2,1,1]`, `[1,2,2]`: object 0 denotes `[2,1]`, while object 1 denotes
`[1,2]`. See `evidence/stage6/mutation_witness.log`.

The mutation dry-run parsed and compiled successfully with exit 0
(`evidence/stage6/mutation_dry_run.log`). The actual proof then exited 1 with
`WarnStuckClaimState`. Its residual is the complete expected final
configuration with active value `ref(1)` and the prover reports that it cannot
unify with the mutated destination `ref(0)`. This is the expected unmet result
obligation, not a parser/import/backend failure. Exact command and residual:
`evidence/stage6/kprove_false_mutation.log`.

Non-vacuity therefore passes.

## 7. Proven versus assumed accounting

The successful reachability proof establishes the following, and only the
following:

> Under the supplied K theory, from the pristine configuration and for
> arbitrary K `ValSeq` inputs, executing the exact submitted definition and
> call reaches normal return `ref(1)` with heap object 0 equal to
> `commonAcc(FIRST,SECOND,.ValSeq)` and heap object 1 equal to the opaque
> `sortVS` of that sequence, while the specified configuration cells have the
> claimed final values. As a partial-correctness result it does not establish
> termination.

Formally proved:

- exact operational membership equals `memberVS` under K equality;
- the real loop updates the accumulator according to `commonAcc`;
- the exact submitted function body calls the supplied `sorted`, returns the
  fixed new reference, and has the pinned state footprint;
- the false return reference is rejected.

Assumed or informal:

- correctness of K v7.1.337 and its backends/hooks;
- correctness of the trusted Python-to-MPY translator;
- fidelity of the supplied language semantics to Python;
- the universal ascending-sort/permutation interpretation of opaque `sortVS`;
- the elementary mathematical reading of `commonAcc` as encounter-order
  deduplicated intersection;
- the finite differential bridge from the two Python implementations and
  concrete K executions.

The complete dependency, effect, and assessment ledger is
`evidence/stage7/trust-ledger.md`. Differential testing is used only as finite
bridge evidence and never as a substitute for the K proof.

Gate accounting:

- Clean dynamic reconstruction: PASS.
- Result constraint and fresh non-vacuity: PASS.
- Candidate proof-local equation/circularity soundness under the supplied
  theory: PASS.
- Real-program semantics/intent adequacy on the stated list domain: FAIL, with
  the concrete `True`/`1` false-conclusion witness.
- Provenance/evidence completeness: FAIL because the four requested generation
  artifacts and structured trace are absent; independent evidence otherwise
  remains reproducible.

Because the used equality semantics permits a false result conclusion for a
satisfying, terminating input admitted by both the natural contract and the
formal precondition, the decision boundary requires `FAIL / NOT_LEGIT`, rather
than `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
