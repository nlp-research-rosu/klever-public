# Independent audit: HumanEval 118 `get-closest-vowel`

## Scope and result

I audited condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`, in launcher mode `CLASSIFICATION_AND_PROOF`. I treated the mounted Stage 1–5 artifacts, their comments, logs, and prior verdicts as untrusted evidence. Trusted code was limited to the inventory, preflight, hashing, and mechanical-gate tooling under `/reference/tools` and the pinned lock `/reference/klean-toolchain.lock.json`.

The protected Stage 3 classification is correct, Stage 4 deterministically generated the exact two necessary domain obligations, and the Stage 5 candidate honestly instantiates all eight operational parameters and proves the fixed target without an unrecorded trust escape.

## Producer authentication

Before judging generation I independently hashed the two mounted generation-time producer sources:

| Source | Observed SHA-256 |
|---|---|
| `klean_export.py` | `f1a7004c0ec7b8be2646f9fdedbc9a9975903f9797e34cdf8b3e4ecb1df3ed59` |
| `klean.py` | `659c1d1c627ff2ca101ab8f9b5a1f1d73968e019e2a305f4ec1d1afa2d8c5a91` |

Both equal the hashes in `generator-manifest.json` and `/reference/generation-tools/source-manifest.json`. The immutable generator image ID is consistently `sha256:853cc3153c8c3a393e12a3bbc09f51f7f1384695616f4490f55b252c156a3d0e` in the generator provenance, source manifest, and the producer-source path bound by `/audit-input.json`. The producer tree's launcher hash is `3141041ba4f4427b633483489102d026b053f5f382041e7ae1d1041689619478`, also matching the signed audit input. There is therefore no producer-provenance `AUDIT_ERROR`.

Evidence: `evidence/producer_auth.log` and `evidence/producer_auth.py`.

## Rule-inventory reconstruction

I invoked the trusted local verification-closure inventory implementation on the frozen `/reference/k-proof/verification.k` closure, then separately recomputed each recorded source slice, normalized source hash, and `source_rule_id` from the frozen files.

The result contains exactly 21 rules in this order: one from `verification.k`, two from `helper-verification.k`, and eighteen from `foundation.k`. All 21 identities are unique. The protected manifest also has 21 unique entries in the same order. There are no omissions, extras, duplicates, reordered identities, changed spans, or changed source texts/hashes. The independently recomputed whole-inventory hash is:

`fbc118c61ac46ccc2058ad89ed82f5555f2d49875c3ba47ba8a25b1bc24792e6`

It equals both the trusted inventory result and `/reference/lemma-discovery.json`. The frozen `verification.k` hash is `bc26ac4427fd81a74fa4fd18cb5de457bbf799415ec09b2f63c56d6d09d20cb5`; required local source hashes include `foundation.k` = `58775ede2e508431e9a77ae9a91998fc80ead83f7afd070c342601b49e758a6e` and `helper-verification.k` = `c97aa0d7a576c4a85fe1206cb4910b38e51a5a3a3a98056b6082d43219994c66`.

Evidence: `evidence/inventory_reconstruction.log` contains every reconstructed rule, span, text, normalized hash, and identity.

## Independent Stage 3 classification

My classification is:

| Classification | Count | Judgment |
|---|---:|---|
| `DEFINITION` | 16 | The four program/body macros and twelve fresh summary/predicate/recurrence equations define named proof terms or fresh functions. |
| `OPERATIONAL_RULE` | 0 | No remaining inventory entry is an ordinary unclassified execution/observation rule. |
| `PROVED_DERIVED_LEMMA` | 3 | The two helper execution summaries and the loop/return/frame-pop summary were genuinely proved before installation. |
| `DOMAIN_LEMMA` | 2 | The guarded `#Ceil(intSeqAt(...))` and `#Ceil(closestScan(...))` facts are relevant, true, and not previously proved exact claims. |

This exactly matches the protected classifications. Every `[simplification]` entry is either a defining equation of `closestScan` or one of the two domain lemmas.

The domain judgments are mathematical, not merely manifest-based:

- For `intSeqAt`, `0 <= I < isLen(CS)` means constructor descent reaches an existing head after exactly `I` positive-index steps. The supplied semantics has only the zero and positive constructor cases, so this guard establishes definedness.
- For `closestScan`, `I >= 0` and `I + 1 < isLen(CS)` put the current code and both neighbors in bounds whenever `I > 0`. The recurrence decreases `I`; `found = true` is covered directly, while `found = false` partitions exhaustively into current non-vowel, current/left vowels, and current vowel/left non-vowel with either right-neighbor truth value. It therefore reaches the `I <= 0` base without an undefined access. This lemma is directly used by the installed loop summary and is relevant to the source program/postcondition.

Because this independently established domain set has two entries, a `KLEAN_NO_OBLIGATIONS` result would have been illegitimate. The selected generation correctly has two obligations.

### Derived-lemma ordering and generated counter

I rebuilt fresh proof definitions under `/tmp/audit-work/stage1-recheck` using only frozen sources:

1. Compiled `FOUNDATION`, then proved both claims in `connection-spec.k` to `#Top` before `HELPER-VERIFICATION` existed in the proof module.
2. Compiled `HELPER-VERIFICATION`, then proved `loop-connection-spec.k` to `#Top` before the final `VERIFICATION` rule existed.
3. Compiled `VERIFICATION` with JSON output and compared the compiled claims with the installed rules.

The three accepted derived-rule identities are:

- `rule-284c4c4d20e7564f3b85f9ae093aa32298e088fc96aae41906f05d8ef3f0ef15`
- `rule-08d6a79c00e8974a6bd055b18bc2d39ca1d25c682c2008be19c209f460d89d5d`
- `rule-c20cac6fc636336fce2d7dbc24f7aa987c09ce9dd8b4b8e10851db71031a2574`

For each, alpha-canonical digests of every ordinary cell, guard, LHS, and RHS are identical between claim and installed rule. The sole compiled delta is exactly the registered provision: the claim has `<generatedCounter> _Gen0 => ?_Gen1`, while the installed rule has one preserved `_DotVar:GeneratedCounterCell`. Every protected rationale explicitly records that the claim leaves the final counter existential and therefore does not earn credit for preservation. No fixed supplied-semantics rule reads or writes `generatedCounter`; the summarized helper/loop code contains none of the source constructs identified as fresh heap-object allocation. Thus the structural no-fresh-allocation condition is independently satisfied, while the residual preservation caveat remains explicit.

Evidence: `evidence/fresh_compile_foundation.log`, `evidence/fresh_prove_helper_claims.log`, `evidence/fresh_compile_helper.log`, `evidence/fresh_prove_loop_claim.log`, `evidence/fresh_compile_verification_json.log`, `evidence/derived_lemma_compare.log`, and `evidence/generated_counter_source_search.log`.

As a further source-identity check, fresh `kast` output for the `getClosestProgram` macro and frozen `solution.mpy` is byte-identical, with KORE SHA-256 `f916e37174032934441788348b892cb560622e8ae51a398482b46f3042f67372`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` over exactly `/reference/k-proof`, `/reference/lemma-discovery.json`, and `/reference/klean-generation`, using the pinned toolchain lock. It returned `PASS`, ran fresh `lake clean` and `lake build` with exit 0, found two obligations, zero designated sorries, and 41 generated trust declarations.

All mounted artifact hashes match the signed `/audit-input.json`, including:

- Stage 1 export tree: `05e494ad91d9277918a82d4e1f7f30f62538d68efa1ba61eb00bf5c96d371ec5`
- protected discovery file: `8db4374ebbe94bd3d5bc038109d472a0e61a2f0dd52e69e7df1e2b15a717f71f`
- generated project tree: `0c1418689a939c3fb1782d0d0a67ff303f75ddd60b87035fee4d65550384d957`
- complete selected generation tree: `4927a8a0c94f5470cc2b087025a71ef2721fd81a7c3c99d74e2e29a354fe0cb5`
- candidate tree: `582444222e79c82e3186b8656b85db7f27b8cbb4e4626d16571b845320c76e8a`

The signed audit envelope also verifies under the trusted resolution contract, with digest `799c3624ca9e47ae21514c901b80d541df2dcb69f7fec178db13faf6fd11c310`. All 808 frozen Stage 1 files form an exact path/hash bijection with `stage1_source_hashes`.

The obligation map is an exact ordered bijection from the two domain-rule IDs to two Lean conjuncts. Each source span and normalized hash matches the reconstructed inventory, each conjunct hash recomputes, and neither rule is duplicated or omitted. The generated target has exactly one conjunction:

1. under `0 <= I < isLen(CS)`, `intSeqAt CS I` is `some`;
2. under `I >= 0` and `I + 1 < isLen(CS)`, `closestScan CS I R F` is `some`.

The rendered `(...isSome = true) ↔ True` form is not a vacuous fact: it requires `isSome = true`; `h` is the guard premise even though Lean's linter calls its proof variable unused. The guards are satisfiable on ordinary nonempty sequences. These are exactly the K `#Ceil` obligations and neither weakens nor changes their domains.

There is exactly one generated target declaration, `Klean118GetClosestVowel.Lemmas.targetStatement`. Its definition hash is `351a75ae6625af7e3bcf7175f439460f6e7ce0b0caaeca3a063b09023445813f`, and its instantiated-statement hash is `0a68683a16da9c6acd1b3fb8cfbbb73110758840134a6768ce2f61622eaecedf`. The extracted target object is identical in the obligation map, generator manifest, fresh preflight, and signed audit input.

Evidence: `evidence/fresh_stage4_preflight.log` and `evidence/stage4_integrity.log`.

## Stage 5 Lean proof

I created `/tmp/audit-work/lean-proof-audit-2`, copied the generated project into it exactly as `Base`, copied only the candidate source/configuration files into the parent, and ran both `lake clean` and `lake build`. Both exited 0; the latter rebuilt `Base` and `Proof` from source. The trusted `tools.klean_final_gate.check_proof_candidate` independently repeated its own clean copy/build/axiom audit and returned `PASS`; the complete signed-input final gate also returned `PASS`.

The copied `Base/Klean118GetClosestVowel/Lemmas.lean` hash is identical to the immutable generated target file. Outside `Base`, the candidate neither declares nor shadows `targetStatement`; it defines exactly one `Proof.final`, whose normalized declared type is the exact fixed target statement. No candidate Lean source contains `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`.

Running Lean on exactly `#print axioms Proof.final` produced:

`'Proof.final' depends on axioms: [propext, Quot.sound]`

There is no `sorryAx`. `propext` and `Quot.sound` are the two permitted pinned Lean core foundations recognized by the trusted mechanical gate, not candidate declarations. None of the 41 generated collection-hook axioms recorded in `trust-inventory.json` occurs in the dependency result, and there is no unrecorded candidate or generated proof escape.

Evidence: `evidence/stage5_lake_clean.log`, `evidence/stage5_lake_build.log`, `evidence/fresh_stage5_mechanical_gate.log`, `evidence/fresh_full_mechanical_gate.log`, `evidence/stage5_print_axioms.log`, `evidence/stage5_proof_identity.log`, and `evidence/stage5_static_integrity.log`.

## Operational bridge

I located all eight exact public definitions named by `target.parameters` and checked their KORE symbols, source-rule bindings, frozen K rules, and operational meanings:

| Lean binding | Independent operational comparison |
|---|---|
| `_andBool_` | Boolean conjunction, matching hooked K `BOOL.and`. |
| `«_>=Int_»`, `«_<Int_»`, `«_<=Int_»` | `decide` over the corresponding mathematical integer comparisons. |
| `«_+Int_»` | Mathematical integer addition. |
| `«isLen(_)_MPY-CORE_Int_IntSeq»` | Structural fold: empty is 0 and `iCons` adds 1, exactly `core.k:227-229`. |
| `«intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int?»` | `Option`-valued structural descent: head at zero, recurse at a positive index, and `none` outside the K function's defined constructor domain, exactly `subscript.k:16-19`. |
| `«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»` | Base at `I <= 0`; found-state descent; exact ten-code, case-sensitive vowel predicate; current/left/right qualification; singleton result; and decrementing recursion, matching all six equations at `foundation.k:140-175`. |

The Lean adversarial file proves concrete reduction examples for negative, zero, in-range, and out-of-range indices; length boundaries; both left- and right-adjacent-vowel rejection branches; the qualifying branch; preservation after `found = true`; and right-to-left choice when more than one position qualifies.

I also defined counterfactual constant functions returning `some 0` and `some .IntSeq`. Lean confirms those dishonest functions can prove the generated definedness target, while separate examples confirm they disagree with the candidate on both `intSeqAt` and `closestScan`. This demonstrates why the clean target proof alone is insufficient. The actual candidate is structural and input-dependent, agrees on all adversarial cases, and implements the frozen operational meaning; it is not constant, identity, hard-coded, or vacuous.

Evidence: `evidence/stage5_operational_adversarial.log` (exit 0) and `evidence/stage5_operational_adversarial.lean`.

## Audit-environment note

The sandbox initially prevented Lean's generic launcher from resolving numeric `/proc/<pid>/exe`, although the pinned toolchain files were readable. I compiled the narrow shim recorded in `evidence/proc_exe_compat.c`; it changes only numeric `/proc/<pid>/exe` reads to `/proc/self/exe`. With that compatibility fix, the actual pinned Lean executable reported version 4.22.0 and all trusted preflight, clean-build, direct Lean, and mechanical-gate invocations succeeded. The shim does not modify source, generated target, proof terms, or compiler output.

Two explicitly named false-start evidence files are retained for transparency: `producer_auth_wrong_digest_algorithm.log` used the exporter tree algorithm where the launcher contract requires its length-tagged tree algorithm, and `derived_lemma_compare_false_substring_match.log` used a substring source-name check that confused `verification.k` with `helper-verification.k`. Both were corrected using the trusted launcher hash implementation and exact compiled source markers respectively; the successful evidence cited above supersedes them.

VERDICT: PASS
LEGITIMACY: LEGIT
