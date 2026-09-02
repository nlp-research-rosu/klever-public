# Independent audit: HumanEval 135-can-arrange

## Scope and result

This audit independently reviewed Stage 3 lemma classification, deterministic Stage 4 generation, and the Stage 5 Lean proof for condition `kit-semantics` with `SUPPLIED_SEMANTICS`. Both `/audit-input.json` and `AUDIT_MODE` select `CLASSIFICATION_AND_PROOF`. The signed resolution envelope recomputes to `f483fd380447f561f57e8cda98c9f6901e4d7cde7d5247db9362efb6675aa01d`.

Candidate and provenance prose, logs, prior verdicts, and comments were not trusted. Reconstruction used the trusted code under `/reference/tools`; candidate content was inspected as evidence and only built in the expressly required fresh Stage 5 project.

## Producer and immutable-input identity

The required producer-source gate passes:

- `/reference/generation-tools/klean_export.py`: `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`.
- `/reference/generation-tools/klean.py`: `ba1148c5df311b510d03f95887839e72b878bbe302c54fd0d981cf568ea8eaa1`.
- Producer tree: `e2997e276bc28e190348cbf865548aaeda9c5a355767876bf0a1e21fec2aada8`.
- Generator image: `sha256:a12daa6dccbac0cead0f384a86899561d3ceb2d478ef3f182ec36ec52ba2cb77`.

The two file hashes agree with `generator-manifest.json` and `source-manifest.json`. The image ID agrees between both manifests and the immutable producer directory recorded by `/audit-input.json`. The trusted and generation-time copies of both producer files are byte-identical. There is therefore no producer-source `AUDIT_ERROR`.

All mounted proof-input hashes recomputed exactly, including the discovery manifest, generated tree, producer tree, selected K audit, complete K workspace, selected Klean generation, mounted Lean workspace, and Stage 1 export tree. All 835 per-file Stage 1 hashes in `/audit-input.json` also recomputed with zero mismatches. The launcher records a Stage 5 invocation-tree ledger hash for a path that is not among the mounted inputs; it was not used as proof evidence. The mounted `/candidate` project hash did recompute exactly.

Raw producer and hash evidence is in `evidence/01_producer_identity.txt`, `evidence/22_independent_structural_checks.txt`, `evidence/23_trusted_vs_generation_tools_hashes.txt`, and `evidence/25_audit_input_envelope.txt`.

## Stage 3 inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` on the frozen `/reference/k-proof`. It selected `VERIFICATION` from `prove.sh` and reconstructed the local closure in source order as `VERIFICATION-BASE`, `VERIFICATION`.

The result contains 23 rules. For each rule, its source span, whitespace-normalized source, SHA-256, and `source_rule_id = "rule-" + normalized_sha256` independently recomputed. The whole ordered inventory hash is:

`f5b69f74b12f0505988375faf85089ef4d83ccca0e2946d2e4e09f482da52564`

The protected manifest has exactly the same 23 identities in exactly the same order. There are no omissions, extras, duplicates, reordered identities, or hash differences. The trusted Stage 3 boundary validator also accepts the bijection.

### Independent classification

| Frozen lines | Rules | Classification | Independent reason |
|---|---:|---|---|
| 7-8 | 1 | `DEFINITION` | Defines the fresh `isNumericVal` predicate. |
| 11-13 | 1 | `DEFINITION` | Defines the fresh `orderablePair` proof-domain predicate. |
| 20-32 | 4 | `DEFINITION` | Exhaustive base/recursive/totalization equations for the named `scanDefined` recurrence. |
| 38-68 | 11 | `DEFINITION` | Exhaustive equations for the fresh `orderGe` summary: Int, Bool, Float, mixed numeric, string, and guarded non-orderable totalization. |
| 76-98 | 5 | `DEFINITION` | Base and structurally descending equations for the named `arrangeSeq` recurrence, including its negative-index totalization. |
| 106-108 | 1 | `DOMAIN_LEMMA` | A guarded equality for pre-existing operational observation `applyCmp`, not a definition of a fresh summary. |

Thus the independent result is 22 definitions, no ordinary operational rules, no proved-derived lemmas, and one domain lemma. Every `[simplification]` rule is either a definition or that domain lemma.

The last rule is not a `PROVED_DERIVED_LEMMA` under the required strict criterion. Stage 1 first compiles `VERIFICATION-BASE` and proves ten sort-specific connection claims. It does not first prove the exact dynamic guarded rule

`applyCmp(">=", V, W) => orderGe(V, W) requires orderablePair(V, W)`

against a module that omits it. Only afterward does Stage 1 compile `VERIFICATION`, where the dynamic simplification is installed and used. Because the rule relates an existing operational symbol to the new summary, is not itself a definition, and was not proved in the required exact form, `DOMAIN_LEMMA` is the correct classification.

The lemma is materially relevant. The frozen source solution compares each element with its predecessor using `>=`; the loop summary branches on `orderGe`; this equality is the bridge between those two expressions. It is not an unrelated mathematical fact.

The complete reconstructed inventory is in `evidence/02_reconstructed_inventory.json`; frozen sources and proof order are in `evidence/04_frozen_semantics_and_proof_order.txt`.

## Stage 4 deterministic generation

The first literal preflight invocation reached `lake clean` but failed because Lean 4.22 looked up `/proc/<namespace-pid>/exe`, while this audit container exposes only `/proc/self/exe`. The failed command is preserved in `evidence/05_klean_preflight_check_generation.txt`. I diagnosed this as an audit-container PID-namespace incompatibility and used an audit-local `LD_PRELOAD` shim that redirects only numeric `/proc/<pid>/exe` `readlink` calls to `/proc/self/exe`. Its source and binary hashes and a successful pinned Lean version check are in `evidence/07_lean_pid_namespace_shim.txt`. It does not modify or reinterpret any proof input.

With the pinned Lean 4.22 toolchain and that compatibility shim, the required call to `tools.klean_preflight.check_generation` returned `PASS`. Both `lake clean` and `lake build` returned zero, and the reproduced build-output hash is the recorded `6b5eba1d391cb91fac23484cd9946693572e1883d5246c22e494086fa17bce1a`. The full returned JSON is in `evidence/08_klean_preflight_check_generation_rerun.txt`.

The independently reconstructed domain set is nonempty and contains exactly `rule-2fd1883e1dbbdfd9717b1321447ac996a4962a56a877371e6e1bee92b5b19050`. Stage 4 correspondingly contains exactly one source rule and one obligation, in the same order, with no duplicate. The recorded span is frozen lines 106-108 and all inventory/discovery/normalized hashes match.

The generated obligation is exactly:

`forall W V, orderablePair V W = true -> applyCmp ">=" V W = orderGe V W`

It retains both universal values, the operational operator, the source guard, and the result equality. It is neither weakened nor padded with a vacuous conjunct. Its Lean-conjunct hash is `02b175511f3c0b83ae64f5b7c84c0e610236789cc28c505e2f4e6b574b34eb1d`.

The generated target is the exact conjunction of that one obligation:

- Declaration: `Klean135CanArrange.Lemmas.targetStatement`.
- File: `Klean135CanArrange/Lemmas.lean`.
- Definition hash: `29c9d56b6c41f072e1ffbf7a268135fe25c7df1e7221ad70d5f8d0796d516fc3`.
- Fixed statement hash: `f6546a0c884ecb415a7b6dffde624a2418ff099073c317144ff6bc9b0d5340d0`.
- Generated tree hash: `10a92cc1a2a1dbeff9645f8a5e37479ea1537358c4941eb018b3f04351acc1e7`.

The parsed target is identical in the obligation map, generator manifest, Stage 4 preflight record, and `/audit-input.json`. Each of the three parameter binding hashes also recomputes through the trusted target parser. This is not a `KLEAN_NO_OBLIGATIONS` case.

The manifest and target evidence is in `evidence/09_stage4_manifests_and_target.txt` and `evidence/22_independent_structural_checks.txt`.

## Stage 5 clean build and proof identity

I created `/tmp/audit-work/stage5-project`, copied only the candidate source/project files into it, and copied the immutable generated project as `Base`. The copied Base tree remained exactly `10a92cc1a2a1dbeff9645f8a5e37479ea1537358c4941eb018b3f04351acc1e7`; copied candidate files are byte-identical to `/candidate`.

In that fresh project:

- `lake clean` exited 0 (`evidence/12_stage5_lake_clean.txt`).
- `lake build` rebuilt Base and `Proof` and exited 0 (`evidence/13_stage5_lake_build.txt`).
- The immutable `Lemmas.lean` target is byte-identical to Stage 4.
- The candidate does not define or shadow `targetStatement`.
- The candidate contains no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`, and the trusted declaration scanner finds no candidate axiom/opaque declarations.

`#print Proof.final` shows that its type is exactly the fixed generated declaration applied to the three candidate bindings. It is not a copied proposition, a weaker theorem, or a separately defined lookalike. The exact print is in `evidence/21_target_and_proof_identity_print.txt`.

`#print axioms Proof.final` produced exactly:

`'Proof.final' does not depend on any axioms`

Therefore the dependency set is empty. It contains neither `sorryAx` nor any unrecorded escape. The immutable Base trust inventory records 44 generated executable/collection axioms, but none is a dependency of `Proof.final`; the candidate adds no new trust declaration. The exact output and exit code are in `evidence/14_print_axioms_Proof_final.txt`.

## Operational-bridge audit

The theorem alone is not enough: coordinated constant functions can satisfy it. I confirmed this with a clean counterfactual in which constant-false `applyCmp` and `orderGe` plus constant-true `orderablePair` prove the generated target without axioms, yet disagree with the frozen result for `2 >= 1`. A negated `>=` mutation also disagrees. This evidence is in `evidence/20_counterfactual_mutations.txt`.

The submitted definitions do not use that shortcut:

1. `orderablePair` recognizes exactly the frozen rule's orderable domain: all Int/Bool/Float pairings and Str/Str, and no other `SortVal` pair.
2. `orderGe` implements every frozen defining case: integer order, Bool-to-Int promotion, the six Float/mixed cases through `floatLt`, `ltIF`, and `ltFI`, lexicographic strings, and false outside `orderablePair`.
3. `applyCmp` implements the supplied dispatch table. On the complete match domain of the obligation (`operator = ">="` and `orderablePair = true`), it returns exactly the independently implemented `orderGe`. Other defined comparisons are also implemented by the corresponding integer, Boolean, Float, string, iterable, set, dictionary, and `None` cases. Returning false on non-orderable `>=` pairs is only a totalization of K states where supplied `applyCmp` has no result; those states cannot satisfy the source rule's guard and are not claimed by `Proof.final`.

The mixed Int/Float implementation preserves the supplied semantics rather than silently substituting host-language intuition. It uses exact binary64 decomposition for finite floor/ceil behavior and preserves the supplied `intToF` rounding behavior for infinities. Likewise, Float `>=` is the supplied `not floatLt`, so NaN/NaN evaluates true in this supplied model even though that differs from Python. These model behaviors are evidence of fidelity to `SUPPLIED_SEMANTICS`, not convenient host semantics.

Independent K witnesses passed for ascending/descending Ints, Bool/Int promotion, mixed Float/Int comparisons, and strings (`evidence/18_k_adversarial_comparisons.txt`). A separately written exact source-body program also returned the expected last descending index for integer, Bool/Int/Float, string, and Float/Int lists (`evidence/24_k_source_program_adversarial.txt`). Lean witnesses show `applyCmp` and `orderGe` agree on all of those cases, on NaN and infinity/huge-integer edge cases, and that Int/String is correctly outside the guard (`evidence/19_lean_bridge_adversarial_tests.txt`).

These comparisons, the full frozen operational rule table in `evidence/15_operational_comparison_rules.txt` and `evidence/17_all_supplied_applyCmp_rules.txt`, and direct inspection of the exact candidate definitions establish the operational bridge over the complete guarded domain. The clean build and empty axiom list are therefore accompanied by the required semantic check.

## Conclusion

Stage 3 is bijective and correctly classifies exactly one relevant domain lemma. Stage 4 deterministically generates exactly that nonvacuous obligation and fixes the recorded target without omissions, duplicates, weakening, or target drift. Stage 5 cleanly proves that exact target with no axioms, proof holes, shadowing, or trust escape, and its three bound definitions implement the frozen guarded operational meaning rather than merely coordinating convenient functions.

The full command list is in `evidence/COMMANDS.txt`; individual command outputs and exit codes are preserved throughout `evidence/`.

VERDICT: PASS
LEGITIMACY: LEGIT
