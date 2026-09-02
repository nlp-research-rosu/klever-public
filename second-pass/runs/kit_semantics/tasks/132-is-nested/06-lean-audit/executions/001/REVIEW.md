# Independent Stage 3–5 audit: HumanEval 132-is-nested

## Scope and result

The launcher and `/audit-input.json` both record `AUDIT_MODE=CLASSIFICATION_ONLY` for problem `132-is-nested`, condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. The selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`. `/candidate` is absent, the Stage 5 workspace and invocation hashes are null, and no Stage 5 result is present. Accordingly, this audit covers the independent Stage 3 classification and deterministic Stage 4 generation. The proof-mode-only Base copy, candidate build, `#print axioms Proof.final`, and operational-bridge parameter checks do not apply.

I treated every mounted candidate/provenance narrative, prior review, log, and comment as untrusted evidence. The reconstruction used `/reference/tools/k_rule_inventory.py`; structural Stage 4 validation used the trusted `/reference/tools/klean_preflight.py`. Mathematical classification and program/semantics correspondence were reassessed from the frozen sources rather than inherited from an earlier result.

## Producer-source and immutable-image authentication

Authentication was completed before judging Stage 4. The producer bundle has exactly three regular files: `klean_export.py`, `klean.py`, and `source-manifest.json`; it has no extra file or link.

- `klean_export.py`: `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`: `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`
- Producer bundle tree: `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`
- Generator image: `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`

Both file hashes match the source manifest and the `exporter_sha256`/`klean_py_sha256` fields in `generator-manifest.json`. The image ID matches the source manifest, the generator manifest provenance, and the final component of the producer-source path recorded in `/audit-input.json`. The bundle tree matches `generation_producer_sources_sha256` in `/audit-input.json`. There is no producer-source infrastructure error.

## Frozen-input and inventory reconstruction

All 771 regular Stage 1 files and their individual SHA-256 values match the exact `stage1_source_hashes` key/value set in `/audit-input.json`; there are no missing or extra files. The recorded Stage 1 pipeline-tree hash is `281d183fbcdf52c692024a54c713dd3a3a48adb25b901bf661739ae95140483d`, and the Klean canonical frozen-input digest is `c5a16677d96b6c783daced6fc0ac18857eda9c93f994bcb36999bd62e5364f78`. Both independently recompute to their recorded values.

The trusted inventory code resolved `VERIFICATION` as the Stage 1 main verification module. Its local closure inside `verification.k` contains only `VERIFICATION`; imported `MPY`, `INT`, and `BOOL` are supplied modules outside that local file. The frozen `verification.k` SHA-256 is `c2c1ac308f8bc7b382807be812a05075c3df7b13fb3e54cee20e9bff11c46237`.

The reconstruction found exactly ten rules, in source order. For each it independently recovered the source span, complete text, attributes, whitespace-normalized source SHA-256, and `source_rule_id = "rule-" + normalized_sha256`. The canonical ordered inventory hash is:

`cfcda43d802cd76ff5b47b744bbe3c51d030a222ce2c55bad170611d9840faa4`

That hash equals the protected Stage 3 inventory hash and the Stage 4 input-manifest inventory hash. The protected Stage 3 schema stores ordered IDs/classifications/rationales rather than repeating spans and text. Its ordered ID list is identical to the reconstruction; every ID embeds the independently recomputed normalized hash. IDs and normalized hashes are each unique. Enriching the reconstructed records with the protected classifications and rationales yields the Stage 4 `definitions` array exactly, including order and spans. Thus the comparison is bijective: no omitted, duplicated, extra, reordered, or changed rule exists.

## Independent classification judgment

All ten rules are correctly classified as `DEFINITION`:

| Lines | Normalized SHA-256 | Judgment and role |
|---:|---|---|
| 10–11 | `d3f0b3b96e611b41d2e8c331de464a83b4e68e55a3a9ef80c85072283e3a52e6` | `nestedStep` case for an early state and code 91 (`[`) |
| 12–13 | `5235cdc16e73a4af8cde1dbf5b49f86ee7f418aed9aca6ae1e221671c623b08b` | Complementary early-state `nestedStep` case |
| 14–15 | `2632b098e390f757cdbc95d8a688555d956e3ba1ea0c29d982f03ab021c4c38a` | `nestedStep` case for a middle state and code 93 (`]`) |
| 16–17 | `20a7c7c6a34063a9caf1231ef507ed100c405cf13773a8407bb758e23da8a956` | Complementary middle-state `nestedStep` case |
| 18–19 | `97fd5a94cf85ea0ea85838319221cb4b69e04384d7611ccab77c11e40b315cdd` | Absorbing completed-state `nestedStep` case |
| 23 | `93dce5c554493a3aaf098de0b0f849282a9eeabdbd187be97413f28507e3f9f9` | Empty-sequence base equation for `nestedScan` |
| 24–25 | `51cb2a9f32f1e0f28c99c7bb9ba96fa06a420bfc0ff59247b5dfae9db1d39768` | Constructor-decreasing recurrence for `nestedScan` |
| 29 | `86c81c4e83f334a250f0f7cd6a3d696ef3dd176482dc7252a0d002fb835aa66c` | Empty-sequence base equation for `bracketInput` |
| 30–31 | `ae46ad4c111fd8416f3da10532e15c6d50824884fc7bba26f2ddee8a60b4c781` | Constructor-decreasing recurrence for `bracketInput` |
| 35 | `b4ad6b97ec2791a39b26f63843ed3879c0a6a47ab5790df412ba95eca8a70c12` | Definition of `nestedResult` as the initial scan reaching state 4 |

The five `nestedStep` guards are disjoint and cover all integer states: `S < 2`; `2 <= S < 4`; or `S >= 4`, with equality/disequality subcases on the relevant character. `nestedScan` and `bracketInput` recurse on the tail of `IntSeq`; their base/constructor equations cover the data constructors. `nestedResult` is an unconditional named result definition. These are definitions of fresh summary, recurrence, precondition, and result symbols—not asserted properties of pre-existing functions.

The operational comparison also supports that classification. The frozen source initializes `state = 0`, iterates characters, increments below state 2 only on `[`, increments states 2 or 3 only on `]`, and tests `state == 4`. Under the supplied K semantics:

- string iteration yields one-character strings from successive integer codes (`str.k`, rules at lines 8–10);
- the loop binds the yielded character and executes the body before recursing on the remainder (`controls.k`, lines 69–74, and `tuple.k`, lines 32–34);
- integer `<` and `+` have their expected operational dispatch (`int.k`, lines 9 and 22–27);
- string equality compares code sequences (`str.k`, line 25);
- `If`, `AugAssign`, name lookup, and `Return` operate through the frozen execution cells rather than any verification rule (`controls.k`, `core.k`, and `functions.k`).

Consequently `nestedStep` is the exact mathematical state transition, and `nestedScan(CS,S)` is the loop recurrence over the remaining codes. `bracketInput` defines the prompt's bracket-only precondition. `nestedResult` merely names the scan result; the loop and program claims in `spec.k` establish the connection from operational execution to that name.

No inventory rule rewrites a `<k>` configuration, Python AST operation, observation cell, binding, return, or other operational term, so the `OPERATIONAL_RULE` set is empty. No inventory rule was first proved as the same K claim in a module omitting it and then installed for a later proof; all ten equations are present from the start, so the `PROVED_DERIVED_LEMMA` set is empty. The claims found in `spec.k` are the loop and final program reachability claims, not copies of any inventory rule. Every reconstructed rule has an empty attribute list, so there is no `simplification` rule requiring a definition/domain-lemma classification.

Most importantly, none of the rules is a disguised `DOMAIN_LEMMA`. A domain lemma would assert a material mathematical consequence about already defined terms. Here the rules introduce the meaning of the four new named functions themselves. Even `nestedResult(CS) => nestedScan(CS,0) ==Int 4` is expansion of a new name, not an axiom that the source program computes that value; the operational loop claim remains responsible for that connection.

As supplemental finite sensitivity evidence—not as a substitute for the source-level argument—I compared two independently written audit models on every bracket string of length 0 through 10 (2,047 cases), with zero mismatches. Witnesses include `[]` and `[][]` as false, and `[[]]`, `[[][]]`, and `[[]][[` as true. Counterfactual changes from code 91 to 93 in the early phase or 93 to 91 in the later phase make `[[]]` disagree; changing the result test from state 4 to state 3 makes `[][]` incorrectly true. This demonstrates that the classifications' defining equations are operationally load-bearing rather than convenient constants.

The independently correct domain-lemma set is therefore genuinely empty.

## Deterministic Stage 4 generation

All mounted and recorded Stage 4 hashes independently match:

- protected discovery manifest: `23f158542af29ec14aacbc7ed808557dbd41b7917fb8963a4b00633a369d4529`
- generated project tree: `4a6c10be7554a12f9ae4d270c3c88cb86e9951f4c2dd0f1a22859609340efe37`
- complete selected Stage 4 generation tree: `d95654b5cddc38005cd1af716fe88ed1c7ba64af747d2863f60051149fcd8f19`
- obligation map file: `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
- trust inventory file: `68569c00541c7a9b2edffb36fa35916b86f16d4f8e68b0abcb561819ced0f91e`

The Stage 4 input manifest has all ten records in `definitions` and an empty `source_rules` list. The obligation map has exactly empty `source_rules`, `obligations`, and `trust_parameters` lists. The generator and export manifests both record obligation count zero and `KLEAN_NO_OBLIGATIONS`. Thus the source-rule/obligation relation is the unique empty-to-empty bijection: no omission, duplicate, extra rule, irrelevant obligation, weakened obligation, or vacuous conjunct exists.

The producer's expected target definition is `None`; the trusted target parser independently observes `None`; `generator-manifest.json` and `/audit-input.json` record target `null`; `Klean132IsNested/Target.lean` does not exist; and the generated root imports only `Rewrite` and `Lemmas`. This is the required fixed generated target for a genuinely empty domain set: no target theorem at all. There is therefore no altered or weakened theorem hidden behind the no-obligations status.

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the required Stage 1, Stage 3, Stage 4, and lock paths. The first attempt exposed a launcher-specific infrastructure condition: Lake could not discover its installation because processes see namespace PIDs such as `2` while `/proc/2/exe` is absent, although `/proc/self/exe` works. Lean itself reported `failed to locate application`. A local `LD_PRELOAD` compatibility shim redirected only `/proc/<numeric-pid>/exe` lookups to `/proc/self/exe`; it did not change the producer sources, generated project, manifests, toolchain files, imports, or theorem environment.

With that compatibility shim, the unchanged trusted `check_generation` returned successfully. Its fresh temporary project ran both `lake clean` (exit 0, empty output) and `lake build` (exit 0). The build output hash was `9fe3595651320ee96629964f2542a3d2ac0ffe48ad9a15f8c35f72c78b44deed`, matching the recorded preflight, and ended with `Build completed successfully.` The returned evidence recorded zero sorries, 41 generated executable trust declarations, obligation count zero, status `KLEAN_NO_OBLIGATIONS`, and target `null`, with all frozen/generated hashes equal to the independently observed values. The preflight also re-snapshotted its immutable inputs after the build.

The 41 generated `axiom`/`opaque` declarations exactly match `trust-inventory.json`; the preflight's independent policy rejects proposition trust, and a separate scan found no `sorry`, `admit`, or `unsafe`. Because there is no generated proposition or proof target, these executable Klean boundary declarations do not discharge an omitted theorem.

## Stage 5 applicability

Stage 5 must be absent for a legitimate `KLEAN_NO_OBLIGATIONS` result. It is absent: `/candidate` does not exist, both Lean artifact hashes in `/audit-input.json` are null, the obligation map has no trust parameters, and there is no generated target for `Proof.final` to prove. Running proof-mode candidate checks or inventing a target in this mode would itself violate the fixed pipeline state.

## Evidence

- `evidence/00_environment_and_initial_hashes.txt`: launcher mode, candidate absence, and initial producer hashes.
- `evidence/audit_integrity.py`, `evidence/inventory-reconstruction.json`, and `evidence/01_integrity_reconstruction.log`: full tree/file hash verification, producer/image authentication, complete trusted rule reconstruction, ordered bijection, and empty target/obligation checks.
- `evidence/classification_checks.py` and `evidence/02_classification_checks.log`: claim/rule inventory scan, finite correspondence checks, and counterfactual witnesses.
- `evidence/03_preflight_environment_diagnosis.log` and `evidence/proc_self_shim.c`: initial Lake failure, proc/PID diagnosis, and the narrowly scoped compatibility shim.
- `evidence/04_check_generation_rerun.log`: exact returned `check_generation` evidence from the successful clean build.
- `evidence/05_target_and_candidate_absence.log`: independent expected/observed null target and Stage 5 absence.

VERDICT: PASS
LEGITIMACY: LEGIT
