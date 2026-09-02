# Independent audit: HumanEval 118-get-closest-vowel

Scope: condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`, audit mode `CLASSIFICATION_AND_PROOF`. I treated the candidate, prior audit, manifests, logs, comments, and classifications as untrusted evidence. Trusted code was taken only from `/reference/tools`; Stage 4 producer source was authenticated before it was used as provenance evidence.

## Executive judgment

The artifacts are mechanically intact, deterministic Stage 4 generation is internally exact for the **protected** two-rule domain set, and the Stage 5 candidate cleanly proves that fixed generated target with honest operational definitions. The audit nevertheless fails because the protected Stage 3 classification calls three verification summaries `PROVED_DERIVED_LEMMA` even though Stage 1 proved weaker reachability claims. The compiled claims permit the final generated counter to be arbitrary, whereas each installed rule preserves the initial generated counter. Under the required “exact same rule” test, those three rules are unproved, relevant `DOMAIN_LEMMA`s. The independently classified domain set therefore has five rules, but Stage 4 emits only two obligations and Stage 5 proves only those two.

This is a proof-legitimacy failure, not an infrastructure error and not an operational-bridge failure in the submitted Lean definitions.

## Producer and immutable-input provenance

The two required producer hashes match the source manifest and generator manifest:

- `klean_export.py`: `f1a7004c0ec7b8be2646f9fdedbc9a9975903f9797e34cdf8b3e4ecb1df3ed59`
- `klean.py`: `659c1d1c627ff2ca101ab8f9b5a1f1d73968e019e2a305f4ec1d1afa2d8c5a91`

The immutable generator image identity is `sha256:853cc3153c8c3a393e12a3bbc09f51f7f1384695616f4490f55b252c156a3d0e` in both manifests and in the basename of the producer-source path recorded by `/audit-input.json`. The producer tree hash is `3141041ba4f4427b633483489102d026b053f5f382041e7ae1d1041689619478`, exactly as recorded.

Using each recorded hash's own canonical convention, all selected trees match: Stage 1 full tree `2a6c7c670dbbe6b764235b5fd10f9575d04b9d2f462686e2757df0291a64b617`; Stage 1 exporter tree `05e494ad91d9277918a82d4e1f7f30f62538d68efa1ba61eb00bf5c96d371ec5`; Stage 2 tree `6a5a8e36c377169161d59485f1c2024cb5cd584cb72ee4e82eadf945d7dde13e`; complete Stage 4 tree `4927a8a0c94f5470cc2b087025a71ef2721fd81a7c3c99d74e2e29a354fe0cb5`; generated-project tree `0c1418689a939c3fb1782d0d0a67ff303f75ddd60b87035fee4d65550384d957`; and candidate tree `582444222e79c82e3186b8656b85db7f27b8cbb4e4626d16571b845320c76e8a`. The 808-entry Stage 1 source-file hash map also has no missing, extra, or changed file.

Consolidated raw results are in `evidence/51_consolidated_hash_and_producer_provenance.txt`.

## Frozen rule inventory reconstruction

I reran `tools.k_rule_inventory.inventory_verification` on `/reference/k-proof`. The local verification-module closure is, in order, `VERIFICATION`, `HELPER-VERIFICATION`, `FOUNDATION-SYNTAX`, `FOUNDATION`. Its relevant files hash as follows:

- `verification.k`: `bc26ac4427fd81a74fa4fd18cb5de457bbf799415ec09b2f63c56d6d09d20cb5`
- `helper-verification.k`: `c97aa0d7a576c4a85fe1206cb4910b38e51a5a3a3a98056b6082d43219994c66`
- `foundation.k`: `58775ede2e508431e9a77ae9a91998fc80ead83f7afd070c342601b49e758a6e`

The trusted reconstruction contains 21 rules and has inventory hash `fbc118c61ac46ccc2058ad89ed82f5555f2d49875c3ba47ba8a25b1bc24792e6`. The protected manifest has exactly the same 21 ordered identities. There are no omitted, extra, duplicated, reordered, span-changed, or hash-changed entries. For every row below, `source_rule_id` is `rule-` followed by the displayed normalized SHA-256:

```text
 #  source span                         normalized SHA-256                                                protected                  independent
 1  verification.k:12-87               c20cac6fc636336fce2d7dbc24f7aa987c09ce9dd8b4b8e10851db71031a2574  PROVED_DERIVED_LEMMA       DOMAIN_LEMMA
 2  helper-verification.k:14-53         284c4c4d20e7564f3b85f9ae093aa32298e088fc96aae41906f05d8ef3f0ef15  PROVED_DERIVED_LEMMA       DOMAIN_LEMMA
 3  helper-verification.k:55-94         08d6a79c00e8974a6bd055b18bc2d39ca1d25c682c2008be19c209f460d89d5d  PROVED_DERIVED_LEMMA       DOMAIN_LEMMA
 4  foundation.k:24-66                  9750751be23de63eea428066c5f2315f3bebcc22fe43dddf5e6d79c43915d75b  DEFINITION                  DEFINITION
 5  foundation.k:68-92                  9f040a569fbdef71fcf41191a36aa87b4a12a1408da3cb7e8e4fd521f3142050  DEFINITION                  DEFINITION
 6  foundation.k:94-101                 b469237f699e183d197e8af26b5fe59f2f7ee10feb5e2cae653d35fa6db3b18e  DEFINITION                  DEFINITION
 7  foundation.k:103-112                bda9325d20b98ccb8ea35f87db6a25e30467c4fdc5a3795dff9cc7b0fad1df95  DEFINITION                  DEFINITION
 8  foundation.k:114-115                f92258ede26e827ded78066798d36a19faf667c244668896801918a553460f73  DEFINITION                  DEFINITION
 9  foundation.k:117-127                b53c8b783e2e5811d5637116208c57afb5dff0bec4c0f204437b0d5e025b40bf  DEFINITION                  DEFINITION
10  foundation.k:128-130                4ffa001d0025dfc39e75914c4018aec5fc84882a251347e2f7d3411147df71c2  DEFINITION                  DEFINITION
11  foundation.k:131-133                d4475acafd5ccc48b928bf84e40a47c36c492090891bdaac93fb21beb3dd6a08  DEFINITION                  DEFINITION
12  foundation.k:135-138                3ece48af78d3f7d2f9eaef5f4a84518a114cf9815cb9dbeb7d46bd3102033d68  DEFINITION                  DEFINITION
13  foundation.k:140-142                438d7cc7c496278810f0bb993f58a64eacd19276c70d0f101e30bc6b5084c96f  DEFINITION                  DEFINITION
14  foundation.k:143-146                44428f2a6174cdcf211cfdd4a90819eb05c02a3189ffc69f34a0c1f6958959a7  DEFINITION                  DEFINITION
15  foundation.k:147-157                a7036ead5012afd996265af2ec30eed7ee568c6f0416cf2e867b9ee5977d169c  DEFINITION                  DEFINITION
16  foundation.k:158-162                faba90d09a0cbb9fce0409db469110529b83cdc311057d00d3f26b64c3f6667f  DEFINITION                  DEFINITION
17  foundation.k:163-168                460633535e62fabbd09b552246be723a3c6834d4c684d42e87597492b2b6ab1f  DEFINITION                  DEFINITION
18  foundation.k:169-175                2dd28623449f964e93ee34df5544e991e09c1d1d901864a6c0da8b6e223cb7c7  DEFINITION                  DEFINITION
19  foundation.k:177-178                b246dcd7d7a81de803c8f1e6ffff14aa138826f5bc035c9b59b2b595f75d9202  DEFINITION                  DEFINITION
20  foundation.k:183-186                1cad334b6905baf03866113ddd1797f5714a455f71cedf67b42074759ca10ca7  DOMAIN_LEMMA                DOMAIN_LEMMA
21  foundation.k:188-191                3cb106e69fb9d49b1f6233a47205ceacbe2aee414ced90880b1ceb6cbb0782e5  DOMAIN_LEMMA                DOMAIN_LEMMA
```

The full reconstructed JSON is `evidence/09_inventory_reconstruction.json`; the ordered bijection is in `evidence/10_stage3_bijection_and_classifications.txt`.

## Independent classification judgment

Rules 4–19 genuinely define macros, bodies, predicates, recurrences, or summaries. Rules 13–18 are the six `[simplification]` equations of the fresh recursive `closestScan` summary, so they properly remain definitions. Rules 20 and 21 are guarded definedness facts for partial `intSeqAt` and recursive `closestScan`; they are relevant to the program and postcondition and properly remain domain lemmas. Thus every simplification rule is independently either a definition or a domain lemma.

Rules 1–3 are the failure. Stage 1 did use the correct order: the two helper claims were proved against `FOUNDATION` before installing `HELPER-VERIFICATION`, and the loop claim was proved against `HELPER-VERIFICATION` before installing `VERIFICATION`. Fresh reruns return `#Top`. But rule identity is not exact:

- Both compiled helper claims contain `<generatedCounter> _Gen0 => ?_Gen1`.
- The compiled loop claim contains `<generatedCounter> _Gen0 => ?_Gen1`.
- Each later installed rule contains the same `_DotVar0` generated-counter value on its left and right sides.

An existential final counter proves a weaker reachability relation; it does not prove preservation of the incoming counter. The fact that this cell is bookkeeping or is not read by the source program cannot strengthen the theorem that was actually stated. Because the audit expressly requires the **exact same rule** to be proved first, none of these three entries qualifies as `PROVED_DERIVED_LEMMA`. They are verification-specific summary lemmas, not ordinary language execution/observation rules and not definitions, so the remaining classification is `DOMAIN_LEMMA`. They are directly relevant: two summarize the program's vowel helper and one summarizes the main loop/return execution.

The independent counts are therefore 16 `DEFINITION`, 0 `OPERATIONAL_RULE`, 0 `PROVED_DERIVED_LEMMA`, and 5 `DOMAIN_LEMMA`. Compiled counter fragments and the resulting domain gap are recorded in `evidence/36_compiled_claim_counter_fragments.txt`, `evidence/38_installed_rule_counter_identity.txt`, `evidence/39_positive_claim_reruns.txt`, `evidence/50_independent_reclassification_and_domain_gap.txt`, and `evidence/52_derived_claims_vs_installed_source.txt`.

## Deterministic Stage 4 generation

I reran the required call to `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` over `/reference/k-proof`, `/reference/lemma-discovery.json`, and `/reference/klean-generation`. It returned structural `PASS`, built the generated project after `lake clean`, found zero designated sorries, 41 inventoried generated trust declarations, and two obligations. The exact returned evidence is `evidence/32_preflight_rerun_success.json`.

The pinned Lean binary could not initially discover its application path because the audit sandbox denies `/proc/<pid>/exe`. I used an audit-only preload shim that rewrites only that `readlink` request to `/proc/self/exe`; all other calls pass through. The binary remained the pinned Lean 4.22.0 commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`. The workaround and diagnostics are retained in `evidence/18_direct_toolchain_diagnostics.txt` through `evidence/31_toolchain_workaround_validation.txt`; it did not alter any mounted input or proof source.

For the protected manifest's two domain rules, Stage 4 is byte-for-byte deterministic and mathematically faithful:

1. `rule-1cad…10ca7` becomes guarded totality of `intSeqAt?`: for `0 ≤ I < isLen(CS)`, `isSome (intSeqAt? CS I) = true`. Its conjunct hash is `715bbd613f6c56d70122156ecf298334032defe63100062e22459c69f7b47eb1`.
2. `rule-3cb…782e5` becomes guarded totality of `closestScan?`: for `I ≥ 0` and `I + 1 < isLen(CS)`, `isSome (closestScan? CS I R F) = true`. Its conjunct hash is `4e5db951334cc65167cb2ed2a811c0acab99ddd714d65395a7a88a4527c09cc5`.

The displayed `↔ True` form is the faithful proposition-level encoding of `#Ceil(...) => #Top`; it is not by itself a vacuous conjunct. The guards are premises and are used by the submitted proof. There are no duplicates or target mutations among these two obligations.

The generated declaration is exactly `Klean118GetClosestVowel.Lemmas.targetStatement`. Its extracted definition hash is `351a75ae6625af7e3bcf7175f439460f6e7ce0b0caaeca3a063b09023445813f`; its fully applied statement hash is `0a68683a16da9c6acd1b3fb8cfbbb73110758840134a6768ce2f61622eaecedf`. There is exactly one declaration, all eight parameter binding hashes reproduce, and the target agrees with both the generator manifest and `/audit-input.json`. See `evidence/40_independent_stage4_target_audit.txt`.

However, this protected-source bijection is not a bijection with the independently classified domain set. Stage 4 omits all three relevant rules `rule-c20…2574`, `rule-284…ef15`, and `rule-08d…9d5d`. Consequently its fixed theorem is weakened by omission and Stage 4 is not legitimate even though every recorded hash is self-consistent.

## Stage 5 Lean proof and proof identity

I made a fresh project at `/tmp/audit-work/proof-audit-118.0OsEJ4`, copied the generated project as `Base`, copied the candidate, and ran both commands:

- `lake clean`: exit 0
- `lake build`: exit 0, “Build completed successfully.”

The full outputs are `evidence/43_lake_clean.txt` and `evidence/44_lake_build.txt`. The copied generated `Lemmas.lean` is byte-identical to the selected generated file. Candidate sources contain no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`; no candidate declaration shadows `targetStatement`; and `Proof.final` states the exact fully applied fixed target rather than a duplicate or weakened variant. See `evidence/45_candidate_integrity_and_target_shadow_scan.txt`.

Running Lean on `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext, Quot.sound]
```

There is no `sorryAx`. Neither the candidate nor `Proof.final` uses any of the 41 generated axioms recorded in `trust-inventory.json`. `propext` and `Quot.sound` are pinned Lean core axioms explicitly accepted by the trusted final gate's core allowlist; they are not candidate-added or generated trust escapes. The trusted final gate independently returns `PASS` with the same two dependencies. Exact output and reconciliation are in `evidence/46_print_axioms.txt` and `evidence/47_trusted_final_gate.json`.

Accordingly, `Proof.final` is a valid Lean proof of the fixed **two-obligation** target. It cannot repair the three obligations omitted before generation.

## Operational bridge audit

Let `D_at` denote `rule-1cad334b6905baf03866113ddd1797f5714a455f71cedf67b42074759ca10ca7` and `D_scan` denote `rule-3cb106e69fb9d49b1f6233a47205ceacbe2aee414ced90880b1ceb6cbb0782e5`. Every generated parameter has exactly one candidate `def` and implements its bound K meaning:

| Lean parameter | Bound source rules | Independent operational comparison |
|---|---|---|
| `_andBool_` | `D_at`, `D_scan` | Boolean conjunction, implemented as `left && right`. |
| `«_>=Int_»` | `D_scan` | K integer `≥`, implemented by `decide (left ≥ right)`. |
| `«_<Int_»` | `D_at`, `D_scan` | K integer `<`, implemented by `decide (left < right)`. |
| `«_<=Int_»` | `D_at` | K integer `≤`, implemented by `decide (left ≤ right)`. |
| `«_+Int_»` | `D_scan` | K integer addition, implemented as Lean integer addition. |
| `«isLen…»` | `D_at`, `D_scan` | The supplied K rules map empty to 0 and `iCons` to one plus the tail length; the candidate performs that same recursion. |
| `«intSeqAt…?»` | `D_at` | The supplied K rules return the head at 0 and recurse with `I-1` for positive `I`; the candidate returns the corresponding `some`, and `none` where K has no defining rule. |
| `«closestScan…?»` | `D_scan` | The candidate matches the K base case, found-true recursion, isolated-vowel selection, current-consonant case, left-vowel exclusion, and right-vowel exclusion. Its ten vowel codes exactly match the source helper and `vowelPred`. |

I compiled independent probes for empty, negative, zero, last, and out-of-bounds indexing; an isolated vowel in `bab`; the left-vowel case `aab`; the right-vowel case `baa`; `found=true`; and a negative-index base case. All reduce to the K-expected results. The probes are in `evidence/49_operational_audit_source.txt`, and Lean accepts them with exit 0 in `evidence/48_operational_adversarial_and_mutation_tests.txt`.

As a counterfactual, I also defined a constant `intSeqAt? := some 0` and an identity `closestScan? := some result`. Those dishonest definitions still prove the generated totality-only target. This confirms that a clean proof of the target is not sufficient operational evidence. The submitted definitions are not those mutations: on the empty sequence the candidate returns `none`, and on `bab` at index 1 it returns the singleton vowel code 97 rather than the input result. The source-to-definition comparison and branch probes therefore find no operational-bridge failure in this candidate.

## Final finding

Stage 3 misclassifies three relevant, not-exactly-proved verification summaries. The true domain set has five entries; Stage 4 and Stage 5 cover only two. Mechanical integrity and an honest proof of the truncated target do not establish the frozen verification theorem under the required trust boundary.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
