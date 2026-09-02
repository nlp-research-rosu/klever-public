# Independent adversarial audit: 117-select-words

The candidate reconstructs to `#Top`, and its Python implementation is correct,
but the K theorem is not a proof over the HumanEval input domain. It replaces
real strings and real whitespace splitting with an artificial tagged-word
algebra, then assigns each tagged word the consonant count needed by the
postcondition. There is no bridge-free theorem connecting that algebra to any
concrete input string. Worse, the formal precondition permits incorrect tags,
for which the extended rules prove results opposite to both Python
implementations. This is a result-bearing oracle and a substituted-domain
proof, so the benchmark decision is `FAIL / NOT_LEGIT`.

The complete reviewer command record is
`/audit-output/evidence/COMMANDS.md`. All builds and mutations were made below
`/tmp/audit-work`; candidate caches were never used.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem `117-select-words`, and condition
`semantics`. The trusted `/reference/reference-semantics` mount is present, so
the mounts agree with the rendered mode; this is not an infrastructure-error
case.

All required pipeline-v3 records are real, readable regular files:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the structured JSONL trace below
  `/generation-evidence/codex-trace/`;
- `/audit-input.json`, `/audit-campaign-lock.json`, and all launcher-declared
  provenance mounts.

The campaign object in `/audit-campaign-lock.json` exactly equals the
`audit_campaign` block in `/audit-input.json`. Its independently computed
SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
equal to the recorded lock hash.

Every recorded per-file hash checked by the reviewer matches, including the
canonical program, trusted and candidate prompt/translator, run/task/result
manifests, invocation and metrics records, usage, generation prompt, final
message, and 2.1 MB output log. The independently reimplemented pipeline tree
hash of `/candidate` is
`34a1cef65071b1fde03e7d015f0e8c11efaabae148917ebced32ffa8b79553c7`,
matching both the invocation and generation-result workspace hashes. The trace
tree hash is
`bd96163751ef1f01e07a247e3b56aec8a8dae7aeced40156f7b65f24f2e42dcb`,
matching `usage.json`, and its sole JSONL file matches the hash in
`generation-result.json`.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. A recursive lstat-and-content
inventory of candidate and trusted `reference-semantics/` has 25 entries and
is exactly equal: no missing, added, changed, mistyped, unsupported, or
symlinked entry. Both trees independently have pipeline hash
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.

The generation records were inspected only as untrusted claims. All 755
structured trace lines parse. They contain 55 shell commands, 22 patches, and
113 process polls; the generation output contains earlier failures as well as
the final `#Top` claim. No generation result was accepted without fresh
reconstruction. Evidence:

- `/audit-output/evidence/stage1_integrity.py`
- `/audit-output/evidence/stage1-integrity.log` (exit 0)
- `/audit-output/evidence/stage1_generation_records.py`
- `/audit-output/evidence/stage1-generation-records.log` (exit 0)

Stage 1 result: integrity passes; no infrastructure breach.

## 2. Program fidelity and canonical comparison

The trusted contract is: for a string containing only letters and spaces and a
natural number `n`, split the string on whitespace and return, in original
order, exactly those words having `n` consonants, case-insensitively. A
consonant is a letter other than `a/e/i/o/u`. The empty string returns `[]`.

`/candidate/solution.py` implements a different but equivalent algorithm on
that domain: it lowercases each word and computes

`len(word) - count(a) - count(e) - count(i) - count(o) - count(u)`.

Because the documented words contain letters only, that is exactly the
canonical consonant count. The trusted translator regenerated
`solution.regenerated.mpy` with exit 0; it is byte-identical to the submitted
`solution.mpy` (both SHA-256
`2f34321a2cc080f79f455422cc15544733cf808d9a2d11b645da4584b96570b4`).

The reviewer differential imported the trusted canonical entry point and the
generated entry point. It checked:

- all five documented examples;
- 18 explicit empty, space-only, n=0, below/equal/above count, repeated-space,
  and case boundaries;
- every length-0-through-6 string over `aEbZ `, for every `n` from 0 through
  7 (156,248 cases);
- 10,000 deterministic generated ASCII-letter/space strings of length 0
  through 80.

All 166,271 comparisons matched. The script fixes the seed and complete input
construction, and records a case-manifest hash. Evidence:

- `/audit-output/evidence/stage2_differential.py`
- `/audit-output/evidence/stage2_fidelity.sh`
- `/audit-output/evidence/stage2-fidelity.log` (exit 0, mismatch count 0)

Stage 2 result: implementation and translation fidelity pass. These finite
tests do not establish the later proof abstraction.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/proof`; neither
`/candidate/runtime-kompiled` nor
`/candidate/verification-kompiled` was copied or used. The observed K tools
are version 7.1.293.

Fresh commands and results:

1. `kompile reference-semantics/semantics.k --backend llvm
   --main-module MPY-KRUN --syntax-module MPY-SYNTAX
   --output-definition runtime-audit-kompiled` — exit 0.
2. `krun stage3_concrete.mpy --definition runtime-audit-kompiled` — exit 0,
   final `<k> .K </k>`, `<exc> NoExc </exc>`, and exit-code 0. The reviewer
   program covers empty/space-only strings, zero consonants, exact/below/above
   branches, repeated spaces, and mixed case.
3. `kompile verification.k --backend haskell
   --main-module SELECT-WORDS-VERIFICATION
   --syntax-module SELECT-WORDS-VERIFICATION
   --output-definition verification-audit-kompiled` — exit 0.
4. The isolated `SELECT-WORDS-SPEC.select-loop` target — `#Top`, exit 0.
5. The candidate's required positive command,
   `kprove spec.k --definition verification-audit-kompiled
   --spec-module SELECT-WORDS-SPEC` — `#Top`, exit 0. This unfiltered command
   proves all three claims in the spec.

An additional isolated `select-loop-entry` filter remained active near 94% CPU
and stable memory for approximately 20 minutes and was reviewer-interrupted
with status 130. The required unfiltered command then closed in about 25
seconds. This filter-path timing anomaly is documented, but it is not used as a
candidate failure because the declared positive command closed every claim.

Evidence:

- `/audit-output/evidence/stage3_concrete.py`
- `/audit-output/evidence/stage3-kompile-llvm.log`
- `/audit-output/evidence/stage3-krun.log`
- `/audit-output/evidence/stage3-kompile-haskell.log`
- `/audit-output/evidence/stage3-kprove-select-loop.log`
- `/audit-output/evidence/stage3-kprove-select-loop-entry.status`
- `/audit-output/evidence/stage3-kprove-all.log`

Stage 3 result: clean positive reconstruction passes. `#Top` establishes
closure under the candidate-extended theory, not the soundness of that theory.

## 4. Adequacy and real-program pinning

### Plain-language claims

`select-loop` has no explicit `requires`. Given a `wordIter(N,WS)`, a frame
containing all loop locals, and a result list with prefix `ACC`, it claims that
the actual translated loop body terminates with `.K` and appends
`selectedWords(WS,N)` to the list. The final per-word locals are existential.
A satisfying state exists, for example `N=0`, `WS=.WordSeq`,
`ACC=.ValSeq`, a valid displayed frame, and a heap list at `H`.

`select-loop-entry` starts from the same artificial iterator before
`word/lower/consonants` locals exist. It claims termination and the same list
summary, depending on `select-loop`. `N=0`, `WS=.WordSeq`, and an empty result
list again give a satisfying state.

`select-words-correct` starts from the exact initial MPY configuration, requires
`N >=Int 0`, loads the function, calls it on
`str(inputWords(N,WS))`, and then applies `#expectList(selectedWords(WS,N))`.
It constrains the returned reference, exact heap list, heapLoc, scopes, stack,
return state, exception state, and exit code. Thus it is not a tautology or a
free-result claim. `N=0, WS=.WordSeq` is a satisfiable formal state; its
intended empty-string projection and both Python implementations return `[]`.

### Program body identity

The claim does not read `solution.mpy`, but this immutable candidate pins its
function body mechanically. Fresh `kast --expand-macros --output json` parsing
of submitted `solution.mpy` and of `selectWordsModule` produced byte-identical
14,241-byte constructor terms, both SHA-256
`6853c81dcec0b5abde491df2f2469ec3f05cb5bc635fdab5d9fb71881437153a`.
See `/audit-output/evidence/stage4-constructor-pinning.log`.

A body-sensitivity mutation changed the macro-expanded executed statement
`Return(Name("result"))` to `Return(Name("n"))`. The separate definition built
successfully, and its proof failed with exit 1 and a reachable residual
`N ~> #expectList(...)`. This confirms that changing the loaded body changes
the theorem. Evidence:

- `/audit-output/evidence/stage4_body_mutation.diff`
- `/audit-output/evidence/stage4-body-kompile.log` (exit 0)
- `/audit-output/evidence/stage4-body-kprove.log` (exit 1,
  `WarnStuckClaimState`)

### Pinning failure

Exact body syntax is insufficient because the call is not made on any concrete
translated source string. Concrete MPY strings have `.IntSeq/iCons(...)`
code sequences. The only end-claim arguments have the new constructor
`inputWords(N,WS)`. No real source input satisfies that term pattern, and no
claim maps arbitrary concrete code sequences to a `WS`.

Nor does the formal precondition validate its tags. It permits, for example:

- `N=0, WS=keepWord(codes("b"),.WordSeq)`. The formal postcondition selects a
  wrapped `"b"`, while both Python implementations return `[]` for `"b",0`.
- `N=0, WS=skipWord(codes("a"),.WordSeq)`. The formal postcondition omits the
  word, while both Python implementations return `["a"]` for `"a",0`.

These are satisfying substitutions because `keepWord/skipWord` impose no
guards. The exact Python and formal witness accounting is preserved in
`/audit-output/evidence/stage4-witness.log`.

Stage 4 result: the syntax of the submitted body is pinned and the formal
result is constrained, but execution is redirected onto a substituted input
model that contains no concrete source strings. Real-program pinning fails.

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers all 24 supplied-semantics source files plus
candidate `verification.k` and `spec.k`:

- 236 syntax declarations;
- 713 rules;
- 5 evaluation contexts;
- 1 configuration;
- 3 reachability claims;
- 958 records total.

The fixed supplied tree contributes 928 records and is the
integrity-checked selected-semantics baseline. The materially used path was
checked through module loading/sequencing, closure creation and frame
push/pop, left-to-right call evaluation, lookup/assignment, list allocation
and append, `For/#loop`, whitespace split, `lower`, `count`, `len`, integer
subtraction/equality, `If`, and return. Those fixed rules model every source
construct in `solution.mpy`. The complete inventory and construct map are:

- `/audit-output/evidence/stage5-rule-inventory.log`
- `/audit-output/evidence/stage5_candidate_assessment.md`

Candidate-local code contributes nine syntax declarations, 18 rules, and
three claims. Every item is assessed below.

### Declarations

1. `WordSeq` introduces `.WordSeq/keepWord/skipWord`. These are unguarded tags,
   not facts about a concrete word.
2. `inputWords` and `countedWord` extend trusted `IntSeq` with artificial,
   non-source constructors and no projection theorem.
3. `wordIter` introduces an artificial iterable with no connection to trusted
   `splitWS`.
4. `consonantCount` is
   `[function,total,symbol,no-evaluators]`, is result-bearing, and has no
   defining coverage for `.IntSeq`, `iCons`, or `inputWords`. Its totality
   declaration is unjustified.
5. `selectedWords` is structurally total over the tag algebra, but its
   source-contract meaning depends on the unproved tags.
6. `#expectList` is an exact proof-harness result observer and is acceptable.
7–9. The three body/module macros are constructor-faithful, as independently
   checked.

There are no candidate-local `[functional]` declarations. The sole opaque
result-bearing symbol is `consonantCount`; the sole local priority bridge is
the split rule.

### Rules 1–6: decisive bridges and oracles

1. The split bridge at `/candidate/verification.k:22` rewrites
   `#applyK(...str(inputWords(N,WS))..."split"...)` directly to
   `wordIter(N,WS)` at priority 30. It preempts the trusted priority-40 split
   rule at `semantics/methods.k:72`. There is no bridge-free universal
   connection theorem.

   Its complete match frames every continuation and omits every state cell.
   The mismatch is observable on the satisfiable symbolic state
   `N=0, WS=.WordSeq, heap=.Map, heapLoc=0`: the local bridge leaves heap and
   heapLoc unchanged and supplies `wordIter`; the fixed rule supplies
   `#alloc(list(splitWS(...)))`, then a reference, a heap entry, and heapLoc 1.
   Thus result, allocation/state footprint, and the value delivered to the
   continuation differ. This is a concrete symbolic false transition witness,
   not merely a missing test.

2. The empty-iterator rule is internally faithful to the artificial algebra,
   conditional on the failed bridge.
3. The `keepWord` iterator rule yields `countedWord(N,W)` for every `W`. It
   therefore assigns rather than proves the branch-controlling count. The
   concrete false-result witness is `N=0,W=codes("b")`.
4. The `skipWord` iterator rule yields `countedWord(N+1,W)` for every `W`.
   The concrete false-result witness is `N=0,W=codes("a")`.
5. The simplification from the real five-subtraction computation to opaque
   `consonantCount(W)` replaces a program-derived calculation without a
   fixed-semantics connection theorem.
6. `consonantCount(countedWord(C,W)) => C` fixes that opaque result
   unconditionally. With `C=0,W=codes("b")`, it concludes 0 although the real
   consonant count is 1. The same opaque symbol controls the program branch and
   appears in the tag-defined postcondition, so this is circular
   result-bearing abstraction.

The `keep/skip` comments cannot serve as preconditions. A K constructor does
not assert that its payload has the described property.

### Rules 7–18

7–9. The three `selectedWords` equations are disjoint, descending, and
complete over `WordSeq`. They truthfully define a filter over the tags, but do
not prove that the tags describe real words. The keep equation also returns
`str(countedWord(N,W))`, not original `str(W)`; no unwrap/equivalence theorem
exists.

10–11. `valSeqConcat` associativity and right identity are valid by induction
over the trusted `ValSeq` constructors.

12–14. The three map membership/update/lookup simplifications are valid for
well-formed finite K Maps with unique keys; their guards/overlaps do not admit
conflicting results.

15. `#expectList` exactly checks the heap list at the returned reference and
does not bypass the function body.

16–18. The loop, function, and module macro equations are exact expansions of
the submitted constructor term.

The local iterator equations are constructor-disjoint; `selectedWords` is
total and terminating. Those internal facts do not cure the uncovered/opaque
`consonantCount` domain or the overlap in which the priority-30 split bridge
preempts fixed execution.

### Claim review

The loop and entry claims execute the real loop-body constructors, but only
over `wordIter` and tag-selected wrapper values. The end claim executes the
real module constructors, but only after the unsound split bridge and count
oracle have replaced the material value computation. `selectedWords` is used
on both the execution abstraction and postcondition side, so it is not
independent evidence of source meaning.

Stage 5 result: Gate A fails. The bridge changes fixed execution and state, and
the unconnected result-bearing abstraction admits opposite ground outcomes.
Independently, Gate B fails because no concrete HumanEval string is in the
entry domain.

## 6. Fresh non-vacuity test

The reviewer created a new spec module
`SELECT-WORDS-SPEC-VACUITY` and changed the result observer from
`#expectList(selectedWords(WS,N))` to `#expectList(.ValSeq)`. This demands an
empty result for every input and is false for the satisfying substitution
`N=1, WS=keepWord(codes("b"),.WordSeq)`; both Python implementations return
`["b"]` for source input `"b",1`.

`kprove ... --dry-run` built the mutation successfully with exit 0. The real
proof exited 1 with `WarnStuckClaimState`; its residual explicitly contains
`#Not { .ValSeq #Equals selectedWords(WS,N) }` and the reachable
`ref(0) ~> #expectList(.ValSeq)`. This is the expected unmet result obligation,
not a parser error, missing import, crash, or unreachable mutation.

Evidence:

- `/audit-output/evidence/spec-vacuity.k`
- `/audit-output/evidence/stage6_false_mutation.diff`
- `/audit-output/evidence/stage6-vacuity-dry-run.log` (exit 0)
- `/audit-output/evidence/stage6-vacuity-kprove.log` (exit 1)

Stage 6 result: the theorem discriminates results inside its artificial model.
Non-vacuity does not establish that the model denotes real strings.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the supplied MPY semantics plus all rules in candidate
`verification.k`, if the artificial call on
`str(inputWords(N,WS))` terminates, the exact submitted function body returns a
heap list equal to `selectedWords(WS,N)`. Operationally, `inputWords` is
intercepted into `wordIter`; `keepWord` elements are wrapped with count `N`;
`skipWord` elements are wrapped with count `N+1`; and the real arithmetic is
simplified to the wrapper-selected count. The proof also establishes the
displayed scope, heapLoc, stack, exception, and exit-code poststate under that
extended theory.

It does not establish that the function returns the right words for any
concrete HumanEval string.

### Trust and assumption ledger

- **Supplied MPY semantics:** trusted selected-semantics boundary after exact
  recursive integrity comparison. Material program constructs are covered.
- **K 7.1.293 compiler/prover/backend:** ordinary machine-checking trust
  boundary. Fresh build and proof logs make it auditable.
- **Trusted translator:** the source-to-`solution.mpy` bridge is accepted after
  byte-identical regeneration.
- **Macro-to-submitted-program identity:** machine-checked by equal expanded
  constructor JSON. Acceptable.
- **Python implementation equivalence:** supported on 166,271 finite cases by
  the independent canonical oracle. This supports implementation fidelity but
  is not a universal K theorem.
- **`valSeqConcat` and K Map lemmas:** ordinary, valid mathematics over the
  supplied constructors. Acceptable.
- **`#expectList`:** exact proof-harness observer. Acceptable.
- **`inputWords` to real whitespace split:** assumed, result/control/state
  affecting, and unsupported by any connection theorem. Illegitimate.
- **`keepWord/skipWord` classification:** assumed by constructor choice,
  branch/result affecting, and contradicted by satisfying ground tag
  substitutions. Illegitimate.
- **`countedWord(C,W)` has count `C`:** unguarded opaque value oracle,
  branch/result affecting, and false for the exhibited projections.
  Illegitimate.
- **`consonantCount` totality/value:** not covered or independently derived;
  it depends circularly on `countedWord`. Illegitimate.
- **Termination:** as usual for reachability, the result is partial
  correctness; termination itself is not the requested theorem.

Kit Gate A fails on real-program soundness, Gate B fails on source-domain
adequacy, and the otherwise strong finite evidence cannot replace the missing
universal connection theorem. The benchmark specifically maps materially
narrowed/substituted HumanEval domains and materially unsound proof rules to
`FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
