# Independent adversarial review — HumanEval 58 `common`

The candidate contains a legitimate, result-constraining K partial-correctness
proof of the submitted program under the supplied MPY semantics. Fresh
reconstruction closes all three claims, the theorem term is mechanically
identical to the trustedly regenerated program, and independent false-result
and changed-body probes are rejected for the expected semantic reasons.

I assign `CONCERNS / LEGIT`, rather than `PASS`, because final ordering is a
result-bearing supplied primitive, `sortVS`, whose universal ascending-sort
contract is not machine-checked in the mounted artifacts. The K theorem is
honestly conditional on that fixed primitive and finite concrete/differential
evidence supports it. The supplied MPY-to-CPython value/equality boundary is
similarly finite and partial. These are explicit, non-fatal trust limitations;
they do not create an oracle or false rule in candidate-controlled theory.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3` and
`semantics_mode: SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the rendered mode and
mounts agree. There is no infrastructure breach.

I independently checked the following:

- The `audit_campaign` object is exactly equal to
  `/audit-campaign-lock.json`; the lock SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the hash recorded in `/audit-input.json`.
- All required pipeline-v3 records are regular, readable files:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured
  trace. Every recorded per-file SHA-256 matches.
- The mounted candidate's independently recomputed pipeline tree digest is
  `017d00ed7d9e6bf64014550a6acb496d3318f95fa43cf33eb50f6d0778a4cb9e`,
  matching both the invocation and generation-result output digest.
- The one trace file's recorded hash matches. Its independently recomputed
  tree digest is
  `46c2e260ac6e5fc3d1a040ed17c9587c86b4b856943b70eccb637619bcb46ba9`,
  matching `usage.json`. All 473 JSONL records parse; all 108 tool calls have
  corresponding outputs.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts.
- The candidate and trusted `reference-semantics/` trees have identical
  paths, entry types, and file hashes. Neither tree contains a symlink. Their
  pipeline tree digest is
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the task manifest.
- Required candidate proof artifacts (`solution.py`, `solution.mpy`,
  `verification.k`, `spec.k`, and `prove.sh`) are regular files. Candidate
  compiled definitions and caches were not trusted or reused.

The generation prose, claimed `#Top`, and recorded commands were inspected only
as untrusted historical claims. Reproducible details are in
[01-integrity.log](/audit-output/evidence/01-integrity.log),
[integrity_check.py](/audit-output/evidence/integrity_check.py),
[01-trace-inventory.log](/audit-output/evidence/01-trace-inventory.log), and
[trace_inventory.py](/audit-output/evidence/trace_inventory.py).

## 2. Program fidelity and candidate-versus-canonical checks

The prompt contract is: given two lists, return the ascending sorted list of
distinct elements occurring in both. The trusted canonical implementation
performs a nested comparison, inserts matches into a Python set, then returns
`sorted(list(ret))`. Its normal-return domain therefore presupposes hashable
input elements and mutually orderable result elements.

The submitted `solution.py` scans the first list in order. It appends an item
exactly when the item occurs in the second list and is not already in the
result, then applies `sorted`. This is a different but extensionally equivalent
algorithm on the intended normal-return domain.

Using only the trusted translator in scratch,
`python3 py2mpy.py solution.py > regenerated-solution.mpy` exited 0.
Submitted and regenerated files are byte-identical, both with SHA-256
`031e94b911c1eae40ab6f6bcda882685fd599c7c48bb1d39f2c3a804e517a352`.

The independent differential imports both trusted `canonical.common` and
generated `solution.common`. It covers:

- both documented examples;
- empty-left, empty-right, both-empty, singleton hit/miss;
- all source-branch boundaries, including a first-condition miss, first hit
  with duplicate suppression, and append;
- duplicates, reverse ordering, negative and large integers, strings, tuples,
  Boolean/integer equality, finite floats, infinities, `None`, and a shared
  heterogeneous-sort exception;
- all 24,336 ordered pairs of length-0-through-3 lists over five small
  integers;
- all 1,600 corresponding string-list pairs;
- 5,000 seeded random integer pairs and 1,000 seeded random tuple pairs.

All 31,956 cases agree, including the one shared `TypeError`; mismatch count is
zero. This is finite fidelity evidence, not a proof. See
[02-fidelity.log](/audit-output/evidence/02-fidelity.log),
[02_fidelity.sh](/audit-output/evidence/02_fidelity.sh), and
[differential_test.py](/audit-output/evidence/differential_test.py).

## 3. Clean proof reconstruction

I copied only candidate source artifacts, the trusted translator, and the
trusted supplied semantics into `/tmp/audit-work/58-common`. Candidate
`runtime-kompiled/`, `verification-kompiled/`, caches, logs, and reports were
not copied.

The live tools are K `v7.1.293`. Fresh source reconstruction produced:

- an LLVM `MPY-KRUN` definition, exit 0;
- a translated reviewer-authored concrete program, exit 0;
- `krun` normal completion with `<k> .K </k>`, `<exc> NoExc </exc>`, and
  `<exit-code> 0 </exit-code>` after 11 assertions spanning examples, empty
  lists, membership branches, duplicates, negative integers, and strings;
- a fresh Haskell `VERIFICATION` definition, exit 0.

The claims have an explicit dependency order. `common-loop` uses the proved
`member-fold` helper, and `common-program` uses both helpers. I reconstructed
each target with its dependency closure:

```text
kprove ... --claims SPEC.member-fold
#Top
exit 0

kprove ... --exclude SPEC.common-program
#Top
exit 0

kprove ... --spec-module SPEC
#Top
exit 0
```

Diagnostic runs that deliberately filtered out a helper leave the dependent
loop/entry claim stuck; this confirms the dependencies rather than showing a
target failure. The staged positive commands above each print `#Top` and exit
0. Commands, warnings, exits, and bounded residuals are preserved in
[03-reconstruct.log](/audit-output/evidence/03-reconstruct.log),
[03_reconstruct.sh](/audit-output/evidence/03_reconstruct.sh),
[03b-dependency-proofs.log](/audit-output/evidence/03b-dependency-proofs.log),
and
[03b_dependency_proofs.sh](/audit-output/evidence/03b_dependency_proofs.sh).

## 4. Adequacy and real-program pinning

### Plain-language claims

`member-fold` has no explicit precondition. For arbitrary modeled value `V`,
finite sequence `S`, arbitrary continuation, and framed configuration cells,
fixed execution of `#memberAcc(V, list(S))` returns
`commonMember(V,S)`.

`common-loop` also has no explicit `requires`. Its pre-state fixes:

- unprocessed suffix `A`, second list `B`, and current accumulator `ACC`;
- local bindings for both inputs, `result -> ref(0)`, and `item`;
- the exact post-loop `return sorted(result); #endcall` continuation;
- environment, global/local scopes, allocation counters, caller frame,
  return/exception state, and exit code.

It consumes the loop and leaves the same continuation with heap location 0
changed from `ACC` to `commonAcc(A,B,ACC)`. The final `item` binding is
existential because it is unobservable.

`common-program` starts from the exact initial supplied configuration, loads a
module binding `common` to the submitted body, and calls it on arbitrary finite
model sequences `A` and `B`. It returns `ref(1)`, restores the module scope and
empty stack, and leaves:

```text
heap[0] = list(commonAcc(A,B,.ValSeq))
heap[1] = list(sortVS(commonAcc(A,B,.ValSeq)))
heapLoc = 2
ret = noRet, exc = NoExc, exit-code = 0
```

The result is not free, tautological, or merely implication-constrained: its
reference, sequence argument to `sortVS`, both heap objects, allocation count,
and normal control state are fixed.

### Mechanical program identity

I independently parsed and macro-expanded:

1. trustedly regenerated `solution.mpy`; and
2. the claim's `Module(FuncDef(..., commonBody()))` term.

Their normalized KAST JSON files are byte-identical with SHA-256
`6becf1c682e399738f59c7cc2e50d7970a03c86c2f0c5bfe329b6fe18d269895`.
Thus the theorem loads the same function name, parameters, binding, and body;
the macros are semantically inert constructor abbreviations.

A concrete state satisfies every claim: choose `V=1`, `S=[1]` for
`member-fold`; choose `A=[1]`, `B=[1]`, `ACC=[]`, `ORIG=[1]`, `item=0`, and an
empty global map for `common-loop`; and choose `A=B=[1]` for the entry. A fresh
ground K theorem for the entry reaches `ref(1)` with both heaps containing
`[1]` and prints `#Top`/0. Both trusted canonical Python and generated Python
also return `[1]`.

The claims pass bare `list(A)`/`list(B)` model values as read-only external
inputs, an explicit convention in the supplied semantics. A source-level list
literal would first allocate a reference. This program never mutates or tests
identity of either input, and all its consumers dereference list objects, so
the representation difference has no observable effect here; it remains an
informal harness-to-semantics bridge.

A reviewer-authored body mutation removes the loop body in the *executed claim
term*. Its normalized KAST hash changes to
`ae00cbe07407d8efa6e1e66ed30b27bc023f92051f0552d77dceca2855ae6e47`.
On `[1],[1]` it executes to empty heaps and cannot prove the original `[1]`
obligation (`WarnStuckClaimState`, exit 1). See
[04-pinning.log](/audit-output/evidence/04-pinning.log),
[04_pinning.sh](/audit-output/evidence/04_pinning.sh),
[spec-ground.k](/audit-output/evidence/spec-ground.k),
[04b-body-sensitivity.log](/audit-output/evidence/04b-body-sensitivity.log),
and
[spec-body-sensitivity-audit.k](/audit-output/evidence/spec-body-sensitivity-audit.k).

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers all 26 assembled K files plus `verification.k`
and `spec.k`: 1,109 declaration records, including all 702 rules, 231 syntax
declarations, 148 function declarations, 109 total declarations, 45 priority
rules, 36 concrete rules, 22 `no-evaluators` declarations, six macros, five
contexts, the configuration, all opaque symbols, and the sole simplification
rule. Every record has a path, line, attributes, full declaration, and review
classification in
[05-rule-inventory.log](/audit-output/evidence/05-rule-inventory.log); the
review method and actual firing slice are in
[05-static-review.md](/audit-output/evidence/05-static-review.md).

### Fixed supplied semantics

The proof-relevant execution path is:

```text
#loadAll / FuncDef
  -> closure lookup and call frame
  -> empty result allocation and local assignments
  -> list iteration and item binding
  -> short-circuited list membership
  -> optional append heap update
  -> loop circularity
  -> builtin sorted lookup and result allocation
  -> return and frame pop
```

I checked declaration/rule coverage, evaluation order, guards, priority
overlaps, state footprints, and control for this path in `syntax.k`, `core.k`,
`functions.k`, `call.k`, `controls.k`, `tuple.k`, `bool.k`, `operators.k`,
`list.k`, and `sort.k`. Equal/unequal membership guards and true/false branch
guards are complementary. Cell-variable priority rules cannot match the plain
frame. Builtin argument dereference exposes the accumulator to `sorted`;
mutating-method dispatch preserves the `result` reference for `append`.
Allocation and frame-pop rules account for both persistent heap objects,
restored scope, returned reference, stack, return state, and counters.

All other fixed declarations were inspected and are outside the dependency
slice. Their left-hand-side symbols are absent from the program, claims, and
reachable helpers, so their equations cannot rewrite this proof. In
particular, Haskell verification imports `MPY`, not the concrete-only
`MPY-CONCRETE` module. No unused opaque symbol reaches a result or branch.

### Candidate-controlled extensions

There are no operational bridges or proof-local priority rules.

- `commonMember` is a total definitional fold. Empty/cons cases are disjoint
  and exhaustive; recursion strictly descends. The independently closed
  `member-fold` claim universally connects it to fixed membership execution.
- The sole simplifier is valid on its full guard:
  `notBool(E ==K V)` implies the first disjunct is false, hence
  `(E ==K V) orBool B = B`. It has no state/control footprint and no
  conflicting overlap.
- `commonAcc` is a total definitional fold with disjoint/exhaustive cases and
  strict-tail descent. Its condition exactly mirrors source membership and
  duplicate suppression.
- `commonLoopBody` and `commonBody` are constructor macros whose exact expansion
  was mechanically compared above. They are not runtime rewrites.
- `member-fold`, `common-loop`, and `common-program` are proved reachability
  claims, not unproved semantic rules. The loop invariant matches real control
  flow and accounts for every modeled write.

### Opaque and total symbols

Of 22 supplied `no-evaluators` declarations, only `sortVS` is reachable.
`sorted` performs all real lookup, argument evaluation, allocation, and return
effects, but symbolically stores `sortVS(VS)`. This is a result-bearing,
externally supplied language primitive, not candidate-defined program code.
No proof conclusion identifies it with a different candidate oracle; the
source-facing ascending-order conclusion is explicitly conditional on its
named contract. Ground integer/string equations are disjoint, descending
insertion-sort equations and were exercised by fresh LLVM assertions.

No candidate-local rule is false on its guard, silently fabricates state,
smuggles the task answer, or bypasses source execution. Therefore there is no
claimed unsound rule for which a false-conclusion witness is applicable.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh
`SPEC-AUDIT-VACUITY` claim uses the satisfying ground input `[1],[1]`, keeps the
correct returned reference, but falsely requires both result-bearing heaps to
be empty.

The mutation parses/builds and executes under the fresh Haskell definition.
`kprove` exits 1 with `WarnStuckClaimState`. Its terminal residual has
`ref(1)`, normal control state, and both heap locations containing
`vCons(1,.ValSeq)`, directly exhibiting the unmet result obligation. The
reviewer wrapper exits 0 only after checking the nonzero prover exit, stuck
marker, and concrete `[1]` residual. See
[spec-audit-vacuity.k](/audit-output/evidence/spec-audit-vacuity.k),
[06-nonvacuity.log](/audit-output/evidence/06-nonvacuity.log), and
[06_nonvacuity.sh](/audit-output/evidence/06_nonvacuity.sh).

This is independent of the changed-body test in stage 4: the former changes
the post-state obligation while executing the real body; the latter changes
the executed body while retaining the original result obligation.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY definition, for every finite modeled `ValSeq` pair
`A,B`, normal execution of the exact submitted function body returns a fresh
reference to `sortVS(commonAcc(A,B,.ValSeq))`, where `commonAcc` is the exact
encounter-order, duplicate-suppressing intersection fold defined using fixed
MPY equality. The proof also establishes the universal membership connection
and loop invariant, allocation/state effects, function binding, evaluation
order, normal return, and frame restoration. This is a partial-correctness
reachability proof; termination as a separate source-level theorem is not
claimed.

### Trusted or informal boundaries

- **K toolchain and reachability logic.** K `v7.1.293`, the Haskell backend,
  builtin SMT/K equality and collection hooks are trusted. This is the normal
  low-level proof-checker boundary.
- **Supplied MPY semantics.** The byte-identical trusted definition fixes the
  Python subset, calls, lists, membership, heap, and control. It is accepted by
  the `SUPPLIED_SEMANTICS` condition, while full CPython objects, user-defined
  equality/order effects, and unmodeled exceptions remain outside it.
- **Trusted translator.** `py2mpy.py` is a trusted frontend boundary. Byte
  regeneration and normalized constructor identity eliminate candidate
  substitution risk but do not prove the translator correct for all Python.
- **`sortVS`.** This supplied opaque primitive materially determines final
  ordering. The K theorem is interpretation-parametric/conditional at that
  boundary. Fresh LLVM integer/string cases and the 31,956-case Python
  differential support it finitely; no mounted universal ordering theorem
  discharges the contract. This is the principal reason for `CONCERNS`.
- **External input representation.** Bare semantic list values stand for
  read-only caller-provided lists. Non-mutation and non-identity-use make that
  bridge sound for this body, but the connection is an informal model
  argument.
- **MPY-to-CPython equality/domain adequacy.** Integer/string behavior and a
  broader finite sample agree with canonical Python. Exotic objects, custom
  equality/hash/order behavior, alias-sensitive nested mutables, and full
  exception behavior are not universally bridged. The formal theorem itself
  imposes no fixed size or bounded-unrolling restriction.

Candidate `PROOF.md`, generation traces, concrete tests, and Python
differentials were not treated as substitutes for the K proof. The independent
tests support only program/canonical fidelity and the explicit semantic
boundaries.

Gate A passes: the theory is sound, result-constraining, non-vacuous, and
body-sensitive. Gate B passes for the material HumanEval domain represented by
the supplied semantics; there is no finite-size or example-only restriction.
Gate C has a documented non-fatal limitation because the universal
`sortVS`/CPython intent bridge is trusted rather than mounted and
machine-checked. This warrants `CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
