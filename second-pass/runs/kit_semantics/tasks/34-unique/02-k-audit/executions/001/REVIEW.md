# Independent adversarial audit: HumanEval 34 `unique`

The candidate contains a sound, result-constraining partial-correctness proof
of the submitted program under the immutable supplied MPY semantics. The proof
is reconstructed from source, pins the trusted regeneration of `solution.mpy`,
covers arbitrary finite model lists rather than a bounded family, and rejects
both a changed program body and a false returned value.

The result is not an unconditional pass because the supplied symbolic model has
a documented representation/identification gap: it distinguishes `True` from
`1` during list membership, whereas CPython and the supplied concrete semantics
identify them. Symbolic sorting is also delegated to the supplied opaque
`sortVS` primitive. These limitations originate in the read-only reference
semantics, not in candidate rules; the theorem has no additional length or
element guard; the candidate records the gap and a concrete witness; and the
Python program follows CPython. Campaign amendment v2 exception 1 therefore
maps the completed audit to concerns but legitimate, not failure.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `34-unique`, and condition
`kit-semantics`. `/reference/reference-semantics` is present as required.

All required pipeline-v3 records are readable and have the expected types:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the structured trace. The trace contains 745 valid JSON
events and no malformed line. Generation prose and claimed results were treated
only as untrusted history.

The campaign lock is JSON-equal to the campaign block in `audit-input.json` and
has the recorded SHA-256
`053ed73cba6d14969a1268433f910c65d5a2c1f365fd324fb469fa1e51dadd01`.
The independently computed launcher pipeline digests are:

- candidate workspace:
  `c934348a7c09128729896d485dd2aec4cf38fedd8dd26389d3bc57a7436ab264`,
  equal to the workspace digest in both `generation-result.json` and
  `invocation.json`;
- trusted and candidate supplied-semantics trees:
  `4495a50f2231cf6231a75f82531d6d4f9b2397fbede6509e4a6dc42c2dd29ad1`,
  equal to the recorded reference-semantics manifest digest;
- structured trace tree:
  `1b0578fdce028561369596e7cf9efb7859fc1664dca1d841873962fecd88f85f`,
  equal to `usage.json`'s source-trace digest.

The candidate prompt and translator are byte-identical to their trusted mounts
with hashes `c48cad...c1111a6` and `406485...64db16`. The trusted canonical hash
is `5dfd82...f7074`. A recursive, no-dereference comparison of the complete
candidate and trusted semantics trees exits 0. Their file manifests are
identical; neither tree contains a symlink, missing entry, additional entry, or
mistyped entry. No infrastructure breach was found.

Evidence: `evidence/stage1_integrity.sh` and
`evidence/stage1_integrity.log`.

## 2. Program fidelity and candidate-versus-canonical checks

The docstring contract is: return each element of the input list once, in
ascending sorted order. The sole documented example requires
`[5,3,5,2,3,3,9,0,123]` to return `[0,2,3,5,9,123]`. The canonical
`sorted(list(set(l)))` is a helper witness, not the contract.

The submitted Python program accumulates the first occurrence of each value
using ordinary Python membership, then calls `sorted`. This satisfies the
docstring for lists whose elements admit the required equality and ordering.
Trusted translation of the scratch copy produced SHA-256
`553d179a5221cb286bbae3727cbbd69424e00388f70f3340b0398d0d98f19276`,
byte-identical to the submitted `solution.mpy`.

The independent differential exercised:

- the documented example and 15 empty/branch/boundary cases;
- all 3,906 lists of length 0 through 5 over `{-2,-1,0,1,2}`;
- all 121 lists of length 0 through 4 over `{"a","b","c"}`;
- 1,000 deterministic random integer lists of length 0 through 30.

There was one canonical mismatch among 5,043 comparisons:
`[[2],[1],[2]]`. Canonical raises `TypeError` because its elements are
unhashable; the candidate defensibly returns `[[1],[2]]`. The docstring does
not specify hashing, unhashable elements, or error behavior, so campaign
amendment v3 makes this an observation, not a defect. Independently of
canonical, all 5,041 applicable property cases returned a sorted result
covering the input with no duplicate result element. The documented result was
exact.

Evidence: `evidence/independent_differential.py`,
`evidence/stage2_program_fidelity.sh`, and
`evidence/stage2_program_fidelity.log`.

## 3. Clean proof reconstruction

Only candidate source artifacts and the trusted semantics/translator were
copied to `/tmp/audit-work/review-34-unique`. No candidate-built definition or
cache was copied. K, `kprove`, and `krun` independently reported version
7.1.293.

Fresh source builds succeeded for:

1. LLVM `MPY-KRUN`;
2. Haskell `VERIFICATION-BASE`, which contains no membership bridge;
3. Haskell `VERIFICATION-MEMBER`, which contains the already connected
   membership bridge but no loop bridge;
4. Haskell `VERIFICATION`, containing both staged bridges.

The three target commands independently printed exact `#Top` and exited 0:

```text
kprove spec.k --definition audit-verification-base-kompiled \
  --spec-module MEMBER-SPEC
kprove spec.k --definition audit-verification-member-kompiled \
  --spec-module LOOP-SPEC
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC
```

Four fixed-versus-bridged probe modules and the model-boundary module also
printed `#Top` and exited 0, for eight positive proof runs in total. The fresh
LLVM definition executed the documented program to an empty `<k>` cell,
`NoExc`, exit code 0, and output heap sequence `[0,2,3,5,9,123]`.

Evidence: `evidence/stage3_clean_reconstruction.sh` and the bounded complete
command/status record `evidence/stage3_clean_reconstruction.log`.

## 4. Adequacy and real-program pinning

The claims mean the following.

- `MEMBER-SPEC.member-summary`: from fixed-semantics
  `#memberAcc(V,list(VS))`, for every finite `VS`, value `V`, and K
  continuation, execution yields the structurally defined Boolean
  `memberVS(V,VS)`.
- `LOOP-SPEC.unique-loop`: from the exact translated `for` loop, environment
  1, exact local bindings, arbitrary finite remaining `VS`, arbitrary
  accumulator `ACC`, and arbitrary continuation, execution updates heap 1 to
  `dedupFromVS(VS,ACC)` and leaves `x` equal to the last consumed value (or its
  original value for an empty sequence).
- `SPEC.unique-full-domain`: from the exact `unique` closure, builtins scope,
  empty stack, `NoExc`, `noRet`, fresh locations beginning at 1, and an
  arbitrary `INPUT:ValSeq` at heap 0, the call returns `ref(2)`, preserves the
  input, stores the first-seen structural deduplication at heap 1, stores
  `sortVS` of that sequence at heap 2, advances the heap location to 3, restores
  the caller environment, and leaves no exception or return state.

The entry postcondition therefore fixes the returned reference and complete
result sequence; it is neither a free variable, tautology, nor one-way
implication.

A mechanical comparison extracted the trusted-regenerated `FuncDef` and the
claim's `closureVal`. After normalizing only K list-syntax spellings
(`ListExpr()` versus `ListExpr(.Exprs)` and implicit versus explicit empty
`Stmts`), the function name, parameter, complete constructor body, and
definition environment 0 are identical. The entry call resolves that exact
binding. Fixed `FuncDef` semantics is the direct constructor-level step from
the translated module to this closure.

Every precondition is satisfiable. Fresh ground claims instantiated membership,
the loop, and the full entry configuration and all printed `#Top`. At the
common witness `INPUT=[2,1,2]`, the formal result, submitted Python, and
canonical witness all produce `[1,2]`.

Evidence: `evidence/stage4_pinning.py`, `evidence/stage4_witness.k`,
`evidence/stage4_adequacy_pinning.sh`, and
`evidence/stage4_adequacy_pinning.log`.

## 5. Rule-by-rule static soundness review

The exhaustive machine-generated inventory has 1,029 records: 248 syntax
declarations, 775 rules, five contexts, and one configuration. It includes
every supplied `.k` file and all 15 candidate-local entries, with source line,
full normalized text, attributes, and an explicit disposition for every row
(zero undispositioned records). It records 164 function declarations,
117 total declarations, 24 opaque/no-evaluator declarations, 50 priority
rules, two simplification rules, and no `[functional]` declaration. There is
no generated semantic helper file.

The used-construct map covers `Module`, function binding and lookup, left-to-
right call/argument evaluation, frame push/pop, docstring evaluation, list
allocation, assignments, list iteration, target binding, membership,
conditional control, the mutating `append` method, `sorted`, allocation,
return, exceptions, and every affected configuration cell. The detailed map
and all proof-local dispositions are in
`evidence/stage5_proof_local_review.md`; the exhaustive inventory is
`evidence/stage5_rule_inventory.tsv`.

Proof-local findings:

- `memberVS` has an empty equation and complementary equal/unequal cons
  equations. Its two simplification rules agree with fixed structural `==K`,
  and recursion descends on the tail.
- `appendUnique` has complementary membership guards and either preserves the
  accumulator or appends exactly one value through supplied
  `valSeqConcat`.
- `dedupFromVS` and `lastFromVS` have disjoint empty/cons cases and strict
  structural descent.
- The priority-40 membership bridge has exactly the arbitrary-continuation
  domain proved by `MEMBER-SPEC` under `VERIFICATION-BASE`; it reads or writes
  no other cell.
- The priority-40 loop bridge fixes the translated body, environment, local
  map, result heap entry, and parent; frames every other cell and accepts the
  same arbitrary continuation as `LOOP-SPEC`. That connection proof imports
  `VERIFICATION-MEMBER`, not the loop bridge. It updates only `x` and heap 1;
  lookup, sorting, return, allocation, frame pop, and exceptions still execute
  in fixed semantics.

No proof-local symbol is opaque or fresh, no task answer is encoded as an
unconnected oracle, and no bridge has a match domain broader than its
bridge-free connection claim. Guards are disjoint/exhaustive, recursion
descends, and totality is justified.

A fresh body-sensitivity mutation changed the executed loop body to append on
every iteration. It parsed successfully; the exact loop bridge no longer
matched; and proof of the original unique result failed with a completed
residual containing work list `[2,1,2]` and returned list `[1,2,2]`. This
confirms that the theorem depends on the actual body rather than only its name
or an external source file.

No rule was classified unsound, so there is no unsupported unsoundness
allegation requiring a false-conclusion witness.

Evidence: `evidence/stage5_inventory.py`,
`evidence/stage5_static_review.sh`, `evidence/stage5_static_review.log`,
`evidence/stage5_rule_inventory.tsv`,
`evidence/stage5_proof_local_review.md`,
`evidence/stage5_body_sensitivity.k`, and
`evidence/stage5_body_sensitivity.log`.

## 6. Fresh non-vacuity test

The reviewer-authored mutation used the satisfying input `[2,1,2]`, retained
the exact submitted closure body and all entry state, but changed only the
returned heap obligation from the true `[1,2]` to the false `[1,3]`.

`kprove --dry-run` exited 0, establishing that the mutation parsed and built.
The actual proof exited 1 with `WarnStuckClaimState` and the expected
cannot-rewrite-further prover error. Its completed residual contained
`ref(2)`, work list `[2,1]`, and the actual returned list `[1,2]`; the mismatch
with `[1,3]` is the direct cause of failure. This is a reachable unmet result
obligation, not a parse error, timeout, unrelated crash, or unreachable
mutation.

Evidence: `evidence/stage6_false_mutation.k`,
`evidence/stage6_nonvacuity.sh`, and
`evidence/stage6_nonvacuity.log`.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied Haskell MPY theory, the exact regenerated function closure
on every finite `INPUT:ValSeq` executes to
`list(sortVS(dedupFromVS(INPUT,.ValSeq)))`, with the input preserved and the
specified control/heap state. `dedupFromVS` is universally connected to the
real loop, and its membership predicate is universally connected to fixed
`#memberAcc`. The proof is unbounded in list length and has no candidate-added
element-type precondition.

### Trusted or informal boundaries

- **K toolchain and immutable MPY semantics.** These are foundational trusted
  inputs. Candidate rules do not alter them.
- **Trusted translator and closure reconstruction.** Byte regeneration and the
  mechanical constructor comparison establish the source-to-term bridge.
  The theorem begins at the exact closure call rather than replaying module
  loading, whose fixed `FuncDef` rule performs precisely that binding.
- **`sortVS(ValSeq)`.** This is an externally supplied, result-bearing opaque
  primitive in `semantics/sort.k`. The K theorem proves that actual source
  execution invokes it on the deduplicated sequence, but ascending ordering is
  conditional on its supplied contract. Fresh concrete execution plus 5,041
  property cases support common integer/string/numeric behavior; finite tests
  are not a universal proof of the primitive.
- **Symbolic numeric equality.** Supplied proof semantics uses structural
  `==K` for membership. A fresh bridge-free claim proved that `1` is absent
  from model list `[True]`, and the opposite CPython result was rejected.
  Conversely, submitted Python, canonical Python, and freshly compiled LLVM
  all return `[True]` for `unique([True,1])`. This is a concrete
  model-versus-CPython identification witness. It affects the symbolic
  deduplicated value but comes from the supplied split between `MPY` and
  concrete-only `numOrKEq`; it is not a candidate rule or program defect.
- **Other model edges.** ASCII literal encoding, unsupported user-defined
  comparison behavior, and Python exception details are supplied-model limits.
  The docstring does not determine these exotic input/error policies, and the
  submitted Python continues to use ordinary CPython membership and sorting.
- **Partial correctness.** The reported theorem is interpreted under Kit's
  partial-correctness contract. Finite model sequences make the reviewed
  summaries structurally descending, but the verdict does not claim a separate
  total-correctness theorem for CPython.

The numeric-identification witness satisfies every campaign amendment v2
exception-1 condition: the gap is supplied and read-only; the theorem covers
arbitrary finite values in that fixed model with no candidate narrowing; the
trust ledger explicitly identifies the affected rule/value/result and concrete
divergence; and the submitted Python follows CPython on the witness. The opaque
sort primitive is likewise supplied and explicitly conditional. These are
non-fatal trust/model limitations. The candidate's `VALIDATED` headline is
therefore stronger than this benchmark's required concern mapping, but the
underlying proof remains legitimate.

Evidence: `evidence/stage7_model_gap.k`,
`evidence/stage7_model_gap_concrete.py`,
`evidence/stage7_trust_ledger.sh`, and
`evidence/stage7_trust_ledger.log`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
