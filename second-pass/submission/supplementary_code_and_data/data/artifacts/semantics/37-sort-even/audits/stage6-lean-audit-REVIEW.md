# Independent audit: `37-sort-even`, semantics / `SUPPLIED_SEMANTICS`

## Result

I audited the frozen inputs as untrusted evidence and independently checked the
Stage 3 classification, deterministic Stage 4 generation, and Stage 5 Lean
proof. The launcher mode is `CLASSIFICATION_AND_PROOF`. The classification and
generated three-obligation target are legitimate, the candidate proves the
exact fixed target in a clean build, and its four target-parameter definitions
implement the frozen operational meanings rather than merely convenient
functions that make the equations true.

Raw command output, reconstructed data, audit programs, and adversarial Lean
tests are in `evidence/`.

## Producer authentication and frozen inputs

Before judging the generated output, I hashed the two mounted producer files:

| File | SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both hashes match `source-manifest.json` and `generator-manifest.json`. The
generator image ID is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in both manifests, and the same ID is encoded in the immutable producer-source
path recorded by `/audit-input.json`. The producer-source tree hash
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`
also matches the audit input. There is therefore no producer-source
infrastructure error. The raw comparisons are in
`evidence/01-producer-authentication.txt`.

I independently recomputed all 34 per-file Stage 1 hashes and all launcher tree
hashes. They match `/audit-input.json`, including:

- Stage 1 export:
  `6e881a6af2cf04c0597d424de90bfa767609c5067eb3edc0bb392a68db60d041`
- selected Stage 4 generation:
  `b4297f79c551502b59e34473c75131da19c68b2b958384c6c931123c1effff18`
- generated Lean tree:
  `2c166bcce81f51e5b8fe42a08269d6cd6585cfcd0f4122df3ba5c34cb1e333f8`
- Stage 5 workspace:
  `c1c4b28e478a872355570ea9bc2a94fa3371f96aad64bf1ebcf20772b39b2014`

The independent hash results are in
`evidence/19-independent-hash-and-bijection-results.json`.

## Inventory reconstruction

Using the trusted `tools.k_rule_inventory.inventory_verification` code, I
reconstructed the local verification-module closure from the frozen
`verification.k`. The closure resolves to module `VERIFICATION` and contains
exactly 17 rules. Its source file hash is
`6f526893b5fc95aee9abfe4f96101bb5117c1198185434087af23f8537b23f83`;
the reconstructed whole-inventory hash is
`19ccf32385bf6229704aae39b7d666065b9baf106918dff1bb92756e75d53fa1`.

For every rule I recomputed the source span, normalized source, normalized
hash, and `source_rule_id`. The 17 reconstructed identities are unique and
match `/reference/lemma-discovery.json` bijectively and in source order. There
are no missing, extra, duplicated, reordered, or hash-changed entries. The
complete reconstruction is in `evidence/02-reconstructed-inventory.json`.

## Independent rule classification

The following table records my classification from the frozen source and
operational semantics. IDs are shown by distinctive prefix; their complete
values and normalized sources are in the reconstructed inventory.

| # | Lines | Rule ID prefix | Classification | Independent reason |
|---:|---:|---|---|---|
| 1 | 8–14 | `d0c1bbfa8593` | `DEFINITION` | Defines the named loop-body statement macro. |
| 2 | 17–36 | `aead8f7d1128` | `DEFINITION` | Defines the complete named function-body macro corresponding to the frozen source function. |
| 3 | 39 | `cd2992427dd1` | `DEFINITION` | Defines the named `sortEvenClosure` proof term. |
| 4 | 44–47 | `62cf92bfffe0` | `OPERATIONAL_RULE` | Performs ordinary singleton argument binding in the current scope. |
| 5 | 53–58 | `4f57ef5c3049` | `DEFINITION` | Defines the even-index subsequence summary. |
| 6 | 59–64 | `021488743949` | `DEFINITION` | Defines the odd-index subsequence summary. |
| 7 | 68 | `04d9e2459c84` | `DEFINITION` | Base case of the named `pairedVS` recurrence. |
| 8 | 69–72 | `2dfeaad39b94` | `DEFINITION` | Recursive case of `pairedVS`. |
| 9 | 75 | `fb1fcc399b3a` | `DEFINITION` | Base case of the named `advancedIndex` recurrence. |
| 10 | 76–77 | `c7f8558094f3` | `DEFINITION` | Recursive case of `advancedIndex`. |
| 11 | 82–87 | `bfb12556320d` | `DEFINITION` | Defines the remaining-even-elements summary. |
| 12 | 90–91 | `cee852fbf20e` | `DEFINITION` | Defines the final assembled result summary. |
| 13 | 96 | `656b75764c32` | `DOMAIN_LEMMA` | Right identity of the supplied recursive `valSeqConcat`; it is a theorem, not a defining clause. |
| 14 | 97–101 | `654c2f49cd7e` | `DOMAIN_LEMMA` | Associativity of `valSeqConcat`; also a derived algebraic fact rather than a definition. |
| 15 | 106–114 | `e4098f840641` | `DOMAIN_LEMMA` | Distinct-key map-membership fact removing the five explicit local bindings. |
| 16 | 119–121 | `9a011c8bf638` | `OPERATIONAL_RULE` | Observes a returned reference by reading its heap value. |
| 17 | 122–123 | `790b92e52d74` | `OPERATIONAL_RULE` | Observes an already-direct non-reference value. |

This gives 11 definitions, 3 operational rules, 3 domain lemmas, and no
proved-derived lemmas. Stage 1 does not first prove any exact rule in a module
that omits it and then reuse that rule later. In particular, proving the
separate `SPEC.loop-correct` reachability claim and trusting that claim for the
entry theorem does not make any inventory rule a `PROVED_DERIVED_LEMMA`.

All three `[simplification]` rules are classified as `DOMAIN_LEMMA`, satisfying
the simplification restriction. Their mathematical and program relevance is
genuine:

1. The supplied semantics defines `valSeqConcat` by recursion on its first
   sequence. Right identity and associativity follow from those two defining
   cases. They are needed to reassociate the symbolic result accumulator,
   paired prefix, and final even suffix used by the loop summary and
   postcondition.
2. K maps forbid duplicate keys. The literals `evens`, `odds`, `result`, `i`,
   and `odd` are each distinct from `$cells`; adding those local bindings
   cannot affect whether `$cells` occurs in the framed remainder `M`. This is
   directly relevant to the source function's five local variables and to
   pruning the closure-cell operational branch.

Thus the true domain set is nonempty and contains exactly these three rules.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
using exactly `/reference/k-proof`,
`/reference/lemma-discovery.json`, and
`/reference/klean-generation`. It returned `PASS` with three obligations and
zero designated sorries. The returned evidence is
`evidence/18-rerun-preflight-success.json`.

The container's restricted procfs initially made the pinned Lean executable
fail before project processing with “could not detect the configuration of the
Lake installation.” I diagnosed this as a failed `readlink("/proc/<pid>/exe")`
despite `"/proc/self/exe"` being available. I used the narrow, recorded
`LD_PRELOAD` compatibility shim in `evidence/17_lean_proc_fix.c`, which only
redirects such executable-path `readlink` requests to `/proc/self/exe`. It
does not alter project files, Lean source, elaboration, or proof checking.
The original failure is in
`evidence/07-rerun-preflight-without-proc-workaround.txt`; pinned-version and
successful-build evidence is in `evidence/17-lean-proc-fix-validation.txt`.

The independently checked source-rule/obligation correspondence is exactly:

| Source rule | Generated conjunct |
|---|---|
| `rule-656b75764c3203134f266be9408944fcc82d61f11a51b6ca12049b4e0fddc5cb` | `∀ VS, valSeqConcat VS .ValSeq = VS` |
| `rule-654c2f49cd7e7e59ab81408e4712d1a42c74c6bd59416f943395163de8bed937` | `∀ C B A, valSeqConcat (valSeqConcat A B) C = valSeqConcat A (valSeqConcat B C)` |
| `rule-e4098f840641d982cc071ea690be2438850392507ef1b3d1e9de094705d06500` | `$cells` membership is unchanged after adjoining the five distinct local bindings |

The three domain-rule IDs and the source identifiers carried by the generated
obligation records are unique and identical in the same order. Each conjunct
preserves the variables, operation, direction, and equality of its frozen K
rule. None is omitted, duplicated, irrelevant, weakened, or vacuous.

The sole fixed target is
`Klean37SortEven.Lemmas.targetStatement`. Its definition hash is
`3ecf80c107f59fb45ea1a478bd6eb3334c24aedff45cadd558bf28fdae10f11b`
and its applied-statement hash is
`6fe058d7b4dba6759b751ece0e1ae3b69876940a5f967bc992954d066d56924e`.
The parsed target, parameter metadata, KORE symbols, binding hashes, source
rule IDs, generator manifest, and audit input all agree exactly.

## Stage 5 clean proof and target identity

I created a fresh workspace at
`/tmp/audit-work/stage5-proof-audit-2`, copied the candidate into it, and
copied the immutable generated project into its existing `Base` directory. In
that workspace both `lake clean` and `lake build` exited 0. Complete output is
in `evidence/21-stage5-clean-build-success.txt`.

The fresh `Base/Klean37SortEven/Lemmas.lean` has the same file SHA-256 as the
generated source, and reparsing both copies returns the exact target hashes and
parameter metadata above. The candidate has only its four parameter
definitions and `theorem final`; it neither defines nor shadows
`targetStatement`. A scan of all candidate Lean files found no `sorry`,
`admit`, `unsafe`, `axiom`, or `opaque`. These checks and both target parses are
in `evidence/28-candidate-target-and-forbidden-scan.txt`.

`Proof.final` states the exact fixed application:

`Klean37SortEven.Lemmas.targetStatement _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_|->_» «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»`

It is not a duplicate, reformulation, or weakened theorem.

Running Lean with `#print axioms Proof.final` produced exactly:

`'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]`

There is no `sorryAx`. These are the three standard Lean base principles
explicitly admitted by the trusted final gate. None of the 49
generation-recorded trust declarations in `trust-inventory.json` is used by
`Proof.final`, and there is no unrecorded dependency. The exact output and
reconciliation are in `evidence/22-print-axioms.txt` and
`evidence/29-axiom-reconciliation.txt`. The complete trusted mechanical final
gate also returned `PASS`; see `evidence/25-trusted-final-gate.json`.

## Operational bridge

The fixed equations do not uniquely characterize their four function
parameters, so a successful proof alone would not establish operational
honesty. I compared every candidate definition to its target metadata, bound
KORE symbol and source rule IDs, frozen rules, source solution, supplied
semantics, and K's built-in collection semantics:

| Candidate definition | Independent operational judgment |
|---|---|
| `_Map_` | Appends the two underlying key/value collections. On K's defined domain—well-formed maps with disjoint keys—this implements `MAP.concat`/map union. K declares overlapping-key concatenation partial; behavior on duplicate-key Lean representations is an irrelevant total extension forced by the target's total type. |
| `«_in_keys(_)_MAP_Bool_KItem_Map»` | Uses exact `SortKItem` equality and `List.any` over keys, which is precisely key membership for the represented map. It is not constant and observes its key and map arguments. |
| `«_|->_»` | Constructs exactly the one-entry key/value collection required by K's `MAP.element`. It observes both arguments. |
| `«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»` | Recurses on the first `SortValSeq`, returning the right sequence at `.ValSeq` and preserving the head before recursing at `vCons`. These are exactly the two frozen defining rules in `reference-semantics/semantics/list.k`. |

K's own built-in documentation confirms that maps have unique keys,
`MAP.concat` is disjoint union and partial on overlap, `MAP.element` constructs
a binding, `MAP.in_keys` checks membership, and list concatenation is ordered.
The extracted declarations and descriptions are in
`evidence/27-k-builtin-hook-semantics.txt`.

I compiled independent Lean witness tests for:

- empty and nonempty sequence concatenation;
- exact singleton-map contents;
- concatenation of two distinct singleton maps;
- present-key membership returning true; and
- absent-key membership returning false.

All tests passed. I also defined adversarial counterfactuals: an empty map
concatenator, constant-false membership, empty singleton, and left-projection
sequence concatenation. Lean confirms that these deliberately wrong meanings
still satisfy the whole fixed `targetStatement`, while separate witnesses show
that each differs from the candidate's actual implementation. This
demonstrates why the operational-bridge audit is material; it does not expose a
candidate failure, because the actual four definitions match the frozen
semantics and reject the counterexamples. The tests and exact successful
output are in `evidence/24_BridgeTests.lean` and
`evidence/24-operational-bridge-tests-success.txt`.

## Conclusion

The independently reconstructed inventory validates Stage 3's complete
classification. The true domain set has exactly three relevant lemmas, and
Stage 4 emits exactly their three faithful obligations under an authenticated
deterministic producer and fixed target. Stage 5 cleanly proves that exact
target without forbidden declarations or trust escapes. Most importantly,
the candidate's target-parameter definitions pass an independent operational
comparison and adversarial testing despite the generated equations alone
being underdetermining.

VERDICT: PASS
LEGITIMACY: LEGIT
