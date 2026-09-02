# Independent Stage 3/4 audit: `80-is-happy`, `kit-semantics`

## Outcome and scope

The launcher records `AUDIT_MODE=CLASSIFICATION_ONLY` and `semantics_mode=SUPPLIED_SEMANTICS`. I independently reconstructed and classified the frozen Stage 1 verification-module closure, checked the deterministic Stage 4 provenance and all hash bindings, reran the trusted Stage 4 preflight, and checked the empty source-rule/obligation bijection and absence of a target. The independently classified domain-lemma set is genuinely empty, so `KLEAN_NO_OBLIGATIONS` is the correct Stage 4 result. No Stage 5 proof is required or permitted in this mode, and `/candidate` is absent.

I treated the mounted Stage 1/2/3/4 files, logs, comments, and prior verdicts as untrusted evidence. No prior PASS or classification was adopted as authority, and no producer or candidate source from a provenance mount was executed. The only executable audit logic used for reconstruction and structural checks came from the trusted `/reference/tools` inventory and preflight modules or from the small audit scripts recorded in `evidence/`.

## Audit mode, hashes, and generator provenance

The environment and `/audit-input.json` both say `CLASSIFICATION_ONLY`; the audit input records no Lean workspace or invocation hashes/paths. The candidate mount is absent. The complete input listing and mode check are in [00_environment_and_input_files.log](evidence/00_environment_and_input_files.log).

Before judging Stage 4, I hashed the exact mounted generation-time producer sources:

- `klean_export.py`: `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b`
- `klean.py`: `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`

Both equal the file hashes in `source-manifest.json` and the `exporter_sha256`/`klean_py_sha256` fields in `generator-manifest.json`. The producer bundle contains exactly those two files plus `source-manifest.json`; its launcher-compatible tree hash is `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`, exactly the audit-input hash. The immutable generator image ID is consistently `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc` in the generator manifest, source manifest, and the basename bound by the audit-input producer-source path. Evidence is in [01_producer_and_manifests.log](evidence/01_producer_and_manifests.log), [02_manifest_contents.log](evidence/02_manifest_contents.log), and [10_recorded_hash_verification.log](evidence/10_recorded_hash_verification.log).

All launcher-recorded tree/file hashes were recomputed with their corresponding trusted hash algorithms and matched:

- Stage 1 pipeline tree: `faf18aa5172dbb6027240d41b4fdbdcfd0ab5f16d8da2c7e6c4ac2946a14bb99`
- Stage 1 deterministic-export tree: `5f39aa25765bf4dd07cbebd9dadaaf9c1a924398cafa99cf14cb9d6e4802410b`
- selected Stage 2 audit tree: `facd3d1287c0101065ecb738cd8ea7f3be48b6eccb720015d906c678e6c90c3c`
- discovery manifest: `ddfd4680f61d186dc24e26388a975936e9bc3a55bf0900eca56c49d9ca776edb`
- selected Stage 4 generation tree: `864d8372e471fd14b16cdd234bf25f4dd40654ef9a0e7a6c8047349bf5271949`
- generated-project deterministic tree: `6edf52c0039720c5c6a63218c3f4aa096d24799814990a2c3b8d4ba684767260`

The audit-input `stage1_source_hashes` map was also checked bijectively: 769 observed regular files, 769 recorded paths, with no missing, extra, or changed entry. The selected artifact hashes equal their recomputed tree hashes. Lean workspace/invocation hashes are correctly null. See [07_tree_and_file_digests.log](evidence/07_tree_and_file_digests.log), [08_pipeline_tree_digests.log](evidence/08_pipeline_tree_digests.log), and [10_recorded_hash_verification.log](evidence/10_recorded_hash_verification.log).

## Canonical inventory reconstruction

Using `tools.k_rule_inventory.inventory_verification` with `PYTHONPATH=/reference`, I reconstructed the local verification-module closure of the frozen `/reference/k-proof/verification.k`. The closure contains only local module `VERIFICATION`; imported `MPY` is supplied by the required semantics and is not a local module in `verification.k`.

The frozen `verification.k` SHA-256 is `f1b0f2b550d53e6867df41c4fd2a56752ef0558cb38a709c34a6b93339020738`. The canonical inventory has three rules, in source order:

| Span | Normalized SHA-256 / `source_rule_id` | Rule attributes | Independent class |
|---|---|---|---|
| line 9 | `c81ca83083d7457acd8bc03869be055c6f82860af5fcb6ab0df7413577ec1931` / `rule-c81ca83083d7457acd8bc03869be055c6f82860af5fcb6ab0df7413577ec1931` | none | `DEFINITION` |
| lines 10–12 | `424ad9bede59bccdcf23851333637603f57a311d80fcb5fef99140e39aae7991` / `rule-424ad9bede59bccdcf23851333637603f57a311d80fcb5fef99140e39aae7991` | none | `DEFINITION` |
| lines 13–18 | `738ed76d501e1fe77a5aa4c3808cc7f2254b9f6b94e6b2a6378b84afed317e55` / `rule-738ed76d501e1fe77a5aa4c3808cc7f2254b9f6b94e6b2a6378b84afed317e55` | none | `DEFINITION` |

The whole canonical rule-document inventory hash is `2ba24efa71b132a7ac64fee85b3a68a5cdfa4cf4871a1b444364b99fc18a7951`. For every rule I separately re-extracted the physical span, normalized whitespace, recomputed SHA-256, reconstructed `rule-<hash>`, and compared the protected manifest identity at the same index. The protected manifest has exactly the same three IDs in the same order, all IDs are unique, and there are no omissions or extras. The protected whole-inventory hash matches. Full reconstructed rule text and comparisons are in [04_inventory_reconstruction.log](evidence/04_inventory_reconstruction.log); the script is [reconstruct_inventory.py](evidence/reconstruct_inventory.py).

## Independent classification judgment

The source symbol is declared as `scanHappy(IntSeq, Int, Int, Int) [function, total]`. Its rules do not match a `<k>` cell or any other execution configuration and cannot preempt the source program. They only reduce terms headed by this fresh named proof-summary symbol.

The supplied operational semantics makes the connection transparent:

1. `For` becomes `#loop`; string iteration yields the head code `C` as the one-character string `str(iCons(C, .IntSeq))` and retains `str(REST)`.
2. `ord` of that one-character string evaluates to exactly `C`.
3. On an iteration with `i >= 2`, the program sets `happy` false exactly when `C == previous1`, `C == previous2`, or `previous1 == previous2`.
4. It then shifts `previous2 := previous1`, `previous1 := C`, increments `i`, and continues over `REST`.

The relevant frozen semantics rules and source/spec links are indexed in [05_operational_semantics_links.log](evidence/05_operational_semantics_links.log) and [06_semantics_rule_index.log](evidence/06_semantics_rule_index.log).

Against that operational behavior, the three inventory rules are definitions:

- Line 9 is the base equation: no remaining characters contribute `true` to the accumulated all-windows property.
- Lines 10–12 are the warm-up equation for `I < 2`: consume one character and shift history without checking a complete three-character window.
- Lines 13–18 are the steady-state recurrence for `I >= 2`: conjoin the negations of the same three equality tests used by the program, then recurse on the strictly shorter `REST` with the same history shift and increment.

For `iCons`, the guards `I < 2` and `I >= 2` are disjoint and exhaustive over K integers. Every recursive call consumes one constructor, so the equations descend structurally. With the empty-sequence equation, they cover every use of the declared total summary. They therefore define a named recurrence; they do not assert an independent theorem about an existing symbol. Their use in the loop invariant and postcondition does not turn a truthful recurrence definition into a `DOMAIN_LEMMA`.

None is an `OPERATIONAL_RULE`: no program term or configuration is rewritten. None is a `PROVED_DERIVED_LEMMA`: Stage 1 does not first prove one of these exact equations in a module excluding it and later import it. None is a `DOMAIN_LEMMA`: each equation defines the head symbol on its left rather than adding a separately stated mathematical fact. No inventory rule has a `simplification` attribute, so the simplification-class restriction is satisfied directly as well.

As adversarial finite support for this semantic reading, I separately transcribed the visible operational loop, the visible recurrence, and the prompt contract. Over all 21,845 sequences of lengths 0 through 7 on alphabet `{-1,0,1,2}`, both the operational loop and recurrence had zero mismatches against “length at least three and every consecutive triple pairwise distinct.” The `-1` cases test the initialization sentinel. Counterfactual versions omitting each of the three inequality conjuncts or delaying the `i >= 2` guard all produced concrete false-positive witnesses. This is supporting evidence, not a substitute for the structural reasoning above. See [09_classification_semantics_check.log](evidence/09_classification_semantics_check.log) and [classification_semantics_check.py](evidence/classification_semantics_check.py).

The resulting independent classification is therefore: three `DEFINITION` rules, zero `OPERATIONAL_RULE`, zero `PROVED_DERIVED_LEMMA`, and zero `DOMAIN_LEMMA`. It exactly agrees with the protected Stage 3 entries, but that agreement was checked only after the independent judgment.

## Deterministic Stage 4 generation

I reran the required `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, using exactly `/reference/k-proof`, `/reference/lemma-discovery.json`, `/reference/klean-generation`, and `/reference/klean-toolchain.lock.json`.

The audit sandbox exposes `/proc` from a PID namespace different from Lean's `getpid()`. The first otherwise-unmodified run failed at `lake clean` because Lean/Lake could not resolve `/proc/<namespace-pid>/exe`; the raw failure is [11_stage4_check_generation.log](evidence/11_stage4_check_generation.log). A syscall-level diagnostic recorded `readlink("/proc/3/exe") = ENOENT` while `/proc/self/exe` was valid; see [18_lean_pathtrace.log](evidence/18_lean_pathtrace.log). I used the narrow audit-only shim [proc_exe_compat.c](evidence/proc_exe_compat.c), which retries only a missing `/proc/<pid>/exe` read as `/proc/self/exe`. It does not alter any mounted input, generated source, target, Lean declaration, or proof behavior. With that compatibility fix, Lean identified the pinned `4.22.0`/`ba2cbbf...` toolchain and the generated project clean-built successfully; see [19_proc_exe_compat_test.log](evidence/19_proc_exe_compat_test.log).

The unchanged trusted `check_generation` then returned exit 0 and:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- designated sorry count `0`;
- trust declaration count `41`;
- `lake clean` exit `0`; and
- `lake build` exit `0`, ending in `Build completed successfully.`

The complete returned JSON and command trace are in [20_stage4_check_generation_compat.log](evidence/20_stage4_check_generation_compat.log). The function's pre/post snapshots also confirmed that the Stage 1 tree, discovery manifest, generated tree, and sidecars did not change during the check.

I independently recomputed every Stage 4 sidecar binding: frozen Stage 1 tree, discovery manifest, `verification.k`, inventory, generated tree, obligation map, trust inventory, generator provenance, and pinned toolchain. All match. The selected preflight's recorded clean/build output hashes also equal the hashes of their complete recorded outputs; see [22_selected_preflight_diagnostic_hashes.log](evidence/22_selected_preflight_diagnostic_hashes.log).

The obligation relationship is the exact empty bijection:

- independent `DOMAIN_LEMMA` IDs: `[]`;
- Stage 4 `input-manifest.json.source_rules`: `[]`;
- `obligation-map.json.source_rules`: `[]`;
- `obligation-map.json.obligations`: `[]`; and
- `obligation-map.json.trust_parameters`: `[]`.

The generator manifest, export result, selected preflight, and selected Stage 4 status all record count zero and `KLEAN_NO_OBLIGATIONS`. There is no irrelevant, weakened, duplicated, omitted, or vacuous conjunct because no domain obligation exists and no target conjunction was generated. Trusted `expected_target_definition` and `target_statement` both return `None`; the generator manifest and audit input both bind target `null`. `Klean80IsHappy/Lemmas.lean` contains only imports, comments, an empty namespace, and no target declaration. The full independent check is [21_independent_stage4_check.log](evidence/21_independent_stage4_check.log), with source in [independent_stage4_check.py](evidence/independent_stage4_check.py).

The generated scaffolding contains 41 allowlisted executable collection-hook axioms, all recorded in `trust-inventory.json`. They are not propositions or proofs, and in this zero-obligation result there is no generated theorem depending on them. Their presence does not manufacture a target. The trusted preflight independently reconciled the declarations with the allowlist and rejected proposition trust.

## Stage 5 applicability and final judgment

Stage 5 proof checks are not applicable. `AUDIT_MODE` is not `CLASSIFICATION_AND_PROOF`; the independently established domain set is empty; all fixed target representations are absent/null; the audit input records no Lean workspace or invocation; and `/candidate` does not exist. Running `Proof.final`, axiom accounting for it, or operational-bridge parameter checks would incorrectly invent a proof stage forbidden by the selected `KLEAN_NO_OBLIGATIONS` path.

The Stage 3 classification is mathematically and structurally sound, the deterministic Stage 4 artifacts are provenance-bound and hash-consistent, the empty obligation set is genuine, and the required no-target/no-candidate conditions hold.

VERDICT: PASS
LEGITIMACY: LEGIT
