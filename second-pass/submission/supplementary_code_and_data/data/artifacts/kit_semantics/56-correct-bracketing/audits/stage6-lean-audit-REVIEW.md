# Independent Stage 3–5 Audit: `56-correct-bracketing`

## Outcome

The protected Stage 3 classification is complete and mathematically correct. The frozen verification-module closure contains seven rules, all of which are genuine definitional equations for named summaries or predicates. My independent classification finds no `DOMAIN_LEMMA`, so Stage 4's `KLEAN_NO_OBLIGATIONS` status, empty obligation map, absent generated target, and absence of a Stage 5 candidate are all legitimate.

The launcher records `AUDIT_MODE=CLASSIFICATION_ONLY`, condition `kit-semantics`, and semantics mode `SUPPLIED_SEMANTICS`. `/candidate` is absent, and the launcher records null Stage 5 paths, hashes, target, and result. The proof-mode-only clean-copy, `Proof.final`, axiom, and operational-bridge checks therefore do not apply.

## Trust handling and audit method

I treated the mounted candidate and provenance artifacts as untrusted evidence. I did not execute prior audit scripts, prior reviews, Stage 1 solution code, or instructions found in those artifacts. I used the trusted code in `/reference/tools` to reconstruct the K rule inventory and rerun `tools.klean_preflight.check_generation`. The generated Lean project was executed only through that mandated trusted preflight path.

## Producer-source authentication

This gate passed before any Stage 4 judgment:

- `/reference/generation-tools/klean_export.py` hashes to `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`.
- `/reference/generation-tools/klean.py` hashes to `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.
- Both hashes agree exactly with `source-manifest.json` and `generator-manifest.json`.
- Both manifests record generator image `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`; the same image digest is the final path component of the launcher-recorded producer-source path.
- The bundle contains exactly `source-manifest.json`, `klean_export.py`, and `klean.py`.
- Its trusted pipeline tree hash is `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, exactly the value in `/audit-input.json`.

There is no producer-source mismatch and thus no infrastructure `AUDIT_ERROR`.

## Inventory reconstruction and Stage 3 bijection

Using `tools.k_rule_inventory.inventory_verification` on the frozen `/reference/k-proof`, I reconstructed:

- selected verification module: `VERIFICATION`;
- local verification-module closure: only `VERIFICATION` (the imported `MPY` is external to `verification.k`);
- frozen `verification.k` SHA-256: `46feea0ab0dab68706635fd10883a7f4e1005fdf2509669a8ac76eed014ab850`;
- rule count: 7; and
- canonical inventory SHA-256: `58de3e4264854ce375024959a6666e49997e6893c6bcfe16411f27c5f9579b3d`.

For every rule I separately sliced the recorded physical source span, normalized whitespace, recomputed SHA-256, reconstructed `source_rule_id = "rule-" + normalized_sha256`, and recomputed the canonical whole-inventory hash. Every check matched. The Stage 3 manifest has exactly seven unique entries in canonical source order; its ordered identity list, identity set, and inventory hash equal the reconstruction. There are no omitted, duplicated, extra, reordered, or hash-changed rules.

| Span | `source_rule_id` | Independent class | Judgment |
|---|---|---|---|
| 10 | `rule-d41a7c26910af38bb78f1217c17a05fb4908c3fed5fa4ee9cf52a907efe9076e` | `DEFINITION` | Base equation `bracketDelta(.IntSeq) = 0`. |
| 11–13 | `rule-6e139480c6d3c873164275a75006bf2c7de6128ebe1831dff691b7356d458245` | `DEFINITION` | Structural tail recurrence for the net balance change. |
| 18 | `rule-72a7f3bf2662beedba9a1783574ce1abf92a90c271d4654d1e77593de0e3a595` | `DEFINITION` | Base equation for prefix safety. |
| 19–25 | `rule-629a5508eaace33c393adaba948a78672ca9cab6968f8af11b634b57692c1d5d` | `DEFINITION` | Structural tail recurrence for prefix safety from a supplied balance. |
| 29 | `rule-cf490f8754fe92929eaab0735f4ff5a17b4e27ba2daa08db685d19b50b42f655` | `DEFINITION` | Base equation for the bracket-character input predicate. |
| 30–31 | `rule-c8a4addc9644eed5b1facf23847f2fc64e34e209298c664aa662eba0aed1237b` | `DEFINITION` | Structural tail recurrence accepting exactly codes 60 (`<`) and 62 (`>`). |
| 34–36 | `rule-2a2831baeb8891ff1e832a3bbe0d70c052055c870fd80fa066e571f5296ae2af` | `DEFINITION` | Compositional definition of `bracketCorrect` from prefix safety and final zero balance. |

All seven left-hand sides define fresh named functions declared `[function, total]`. The base/constructor cases cover `IntSeq`, recursive calls strictly descend to `REST`, and the final rule merely names the conjunction used by the postcondition. In particular, `bracketCorrect` does not assert that program execution returns the desired property; that connection remains the separate K reachability claim in `spec.k`. It is therefore a definition, not a disguised domain lemma.

No inventory rule has a `simplification` attribute. There are no claimed operational rules, proved-derived lemmas, or domain lemmas. Consequently there is no mislabeled `DOMAIN_LEMMA`, no unproved derived-lemma claim to validate against an earlier bridge-free proof, and no irrelevant domain proposition.

## Operational and mathematical classification judgment

The supplied semantics confirms that these rules summarize rather than replace execution:

- string iteration emits one-character strings from the `IntSeq` head;
- `For` lowers to `#loop`, obtains `#iterNext`, binds the yielded character, executes the body, and recurs on the remainder;
- string equality with `"<"` compares its code sequence, so code 60 takes the increment branch and every other code takes the decrement branch;
- integer `AugAssign`, comparisons, `If`, and sticky assignment of `valid = false` implement exactly the state transition summarized by `bracketDelta` and `bracketPrefixOK`; and
- the return expression is short-circuiting `valid and balance == 0`, exactly the conjunction named by `bracketCorrect` after the loop invariant accounts for the consumed suffix.

The source contract states that inputs contain only `"<"` and `">"`, matching `bracketChars`. On that domain the two recurrence branches are exhaustive. The broader `bracketDelta`/`bracketPrefixOK` else branch also agrees with the source's own `else` for non-`"<"` characters, although those characters are excluded by the formal precondition.

As finite adversarial support, I independently implemented the source loop and the four recurrences without importing or executing `solution.py`. Exhaustive comparison over all 511 bracket strings of length at most 8, plus adversarial non-domain cases, found zero mismatches. Counterfactual constant, identity-like, prefix-only, and vacuous variants were refuted by witnesses such as `"<"`, `">"`, and `"x"`. This testing supports, but is not substituted for, the direct equation-and-semantics analysis above.

## Launcher and manifest integrity

The signed resolution digest `33d6c77d960015b65768551d4de2304d09de0aeefc47e84931fe4920487ecaff` recomputes exactly. Relevant independent hashes all match their launcher and sidecar records:

- Stage 1 pipeline tree: `079a0ec5512f3ace1c02db3e543ad600f1dce9df84a50f5deb7f97283d80cd66`;
- Stage 1 deterministic-export tree: `5e34129a88e22ca6172c54e76906c40df67b07ccf7c89959972092e48c6382cd`;
- Stage 2 selected audit tree: `51cd5ffefb694cab72e9a9353b7264ad5f61844aaf3688fb9ad6c220e97d67c7`;
- Stage 3 manifest: `2bdd46fcd0dbf080a0c77ec7ba8f70bcb2cac48148e1209c4838d10838b65abf`;
- Stage 4 generation tree: `d2cebadf4fff814082de638442ef6011e103f5f5c37c913fe55e4635c4524d66`; and
- generated project deterministic-export tree: `55486f3fd00b4c40b0fba50d26d3720fb6de4482025090706cc8bd6363dea629`.

The launcher records 769 individual Stage 1 source-file paths and hashes. I independently walked the regular-file tree and obtained the same 769 paths with no missing, extra, or mismatched hash. The Stage 1, Stage 3, generated-project, obligation-map, producer, and trust-inventory hashes in `input-manifest.json`, `generator-manifest.json`, `export-result.json`, and `/audit-input.json` all reconcile.

## Deterministic Stage 4, obligation bijection, and fixed target

The input manifest's seven definition records equal the reconstructed inventory plus the protected classifications and rationales, in exact order. My true domain-lemma set is empty, and the following are all exactly the same empty ordered set:

- protected Stage 3 `DOMAIN_LEMMA` IDs;
- Stage 4 `input-manifest.json.source_rules` IDs;
- `obligation-map.json.source_rules` IDs; and
- `obligation-map.json.obligations` IDs.

There are no duplicates, omissions, irrelevant obligations, weakened conjuncts, or vacuous conjuncts. `trust_parameters` is empty and both recorded obligation counts are zero.

The trusted `expected_target_definition` and `target_statement` functions both return `None`. An independent scan finds no `def targetStatement` in any generated Lean source. `Klean56CorrectBracketing/Lemmas.lean` contains only its namespace, while the generator manifest and launcher both record `target: null`. Thus the fixed generated target is genuinely absent, as required for a legitimate `KLEAN_NO_OBLIGATIONS` result.

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the required Stage 1, Stage 3, Stage 4, and toolchain-lock inputs. Its temporary-copy `lake clean` and `lake build` both exited 0, and the generated library build completed successfully. The returned evidence is `KLEAN_NO_OBLIGATIONS`, with zero designated sorries, zero obligations, null target, the expected frozen/generated hashes, and 41 trust declarations exactly accounted for by the generated trust inventory. The complete returned JSON exactly equals the launcher-recorded `stage4_preflight` object.

The first local attempt exposed a launcher infrastructure peculiarity: `getpid()` reports a nested namespace PID, while the mounted `/proc` exposes host PIDs. Lean 4.22 uses `/proc/<getpid>/exe`, so it initially reported `failed to locate application`; `/proc/self/exe` remained valid. I recorded the failure and used a narrow `LD_PRELOAD` shim for only the preflight subprocesses, making `getpid()` return the host PID named by `/proc/self`. With that compatibility shim, pinned Lean reported version 4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the trusted preflight produced byte-for-byte the same returned evidence as the launcher record. No frozen input or generated source was changed; Lake's configured build directory is under `/tmp`.

## Stage 5 applicability

This is not `CLASSIFICATION_AND_PROOF`. `/candidate` does not exist, and the signed resolution has null `lean_workspace`, `lean_invocation`, Lean hashes, `stage5_result`, and target. A Stage 5 proof candidate would violate the selected no-obligation classification. Therefore no `Proof.final`, `#print axioms`, candidate trust-escape scan, target-shadowing check, or candidate parameter operational-bridge analysis exists or is required.

## Evidence index

- [Producer, launcher mode, and tree hashes](/audit-output/evidence/00_launcher_producer_and_hashes.log)
- [Canonical inventory reconstruction and bijection](/audit-output/evidence/01_inventory_reconstruction.log)
- [Trusted Stage 3 structural contract](/audit-output/evidence/02_stage3_contract_and_classification.log)
- [Frozen source, claims, and supplied operational semantics](/audit-output/evidence/03_operational_semantics_context.log)
- [Independent recurrence/source-loop adversarial checks](/audit-output/evidence/04_summary_counterexamples.log)
- [Lean PID-environment diagnosis and compatibility validation](/audit-output/evidence/05a_lean_environment_workaround.log)
- [Required `check_generation` rerun, full build output, and returned evidence](/audit-output/evidence/05_preflight_check_generation.log)
- [Independent Stage 4 bijection and null-target gate](/audit-output/evidence/06_stage4_bijection_and_target.log)
- [Signed launcher and all manifest/file hash checks](/audit-output/evidence/07_launcher_and_manifest_integrity.log)

VERDICT: PASS
LEGITIMACY: LEGIT
