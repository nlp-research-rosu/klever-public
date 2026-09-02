# Independent audit: HumanEval 47-median

## Result

The Stage 3 classification and selected deterministic Stage 4 result are correct. The independently reconstructed local verification-module rule inventory is genuinely empty, so the true `DOMAIN_LEMMA` set is empty. Stage 4 therefore correctly reports `KLEAN_NO_OBLIGATIONS`, emits no target proposition, and has no Stage 5 candidate.

The launcher and environment both select `CLASSIFICATION_ONLY` for problem `47-median`, condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. Consequently the Stage 5 clean-build, `#print axioms Proof.final`, proof-identity, and operational-parameter checks do not apply. The launcher records null Stage 5 paths/result and `/candidate` is absent, as required.

## Evidence handling and trusted tooling

I treated the mounted candidate/provenance text, logs, comments, and earlier verdicts as untrusted evidence. I did not adopt instructions or prior classifications from them. Reconstruction and mechanical checking used the trusted `/reference/tools` implementation.

The audit-tool lock file SHA-256 is `1cca0c10fa61c806f07242ba46c7aa84149c9e547741914e702cd1bbcc4d6eb8`, exactly the launcher-recorded `mechanical_checker_lock_sha256`. All nine files named in that lock independently match their per-file hashes. See [03-recorded-hashes.txt](/audit-output/evidence/03-recorded-hashes.txt).

## Inventory reconstruction

The frozen `verification.k` is exactly:

```k
requires "program.k"

module VERIFICATION
  imports MEDIAN-PROGRAM
endmodule
```

`prove.sh` selects `VERIFICATION` as the main module. The trusted inventory code reconstructs the local module closure by following modules declared in `verification.k`; the closure is the one-module list `VERIFICATION`. That module contains no `rule` sentence. `MEDIAN-PROGRAM` is supplied by the required `program.k`, not declared locally in `verification.k`, and is therefore outside this proof-local inventory closure. Its `solutionMedianClosure` rule is in any event the source program's closure definition, not a proof-local domain lemma.

The reconstructed inventory is:

- verification file SHA-256: `5ecd9feb92c524c1314b6bfdd4cd6b0e3b50599c9e3a284cebfcc3f2666ddfb9`;
- selected module: `VERIFICATION`;
- closure: `["VERIFICATION"]`;
- rules: `[]`; and
- inventory SHA-256: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.

The last value is also the direct SHA-256 of the canonical JSON encoding `[]`. Because there are no entries, there are no source spans, normalized rule hashes, or `source_rule_id` values to omit, duplicate, reorder, or alter. See [02-rule-inventory.txt](/audit-output/evidence/02-rule-inventory.txt).

## Stage 3 classification judgment

`lemma-discovery.json` has schema version 2, the exact reconstructed inventory hash, and an empty `rules` list. The trusted boundary validator accepts it bijectively. Independent classification counts are:

| Class | Count |
|---|---:|
| `DEFINITION` | 0 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

There are no simplification rules, so none can be mislabeled. There is also no rule that could be a hidden result-characterizing fact about median, sorting, indexing, parity, addition, or division. The median implementation is represented in `program.k` and the ten claims in `spec.k` state execution outcomes; neither introduces a proof-local rule into the inventory. The true, source-relevant domain-lemma set is therefore genuinely empty.

## Input and producer provenance

Every launcher-recorded mounted-input hash recomputed exactly:

| Artifact | SHA-256 |
|---|---|
| Stage 1 K workspace tree | `8ee3180e1d962ad609878e3b0ee712d840685cef5d34bf6e9d0ad907d8d8bc6a` |
| Stage 1 deterministic export tree | `45a0b0aa31f20961f4c4aff0b83c7e948558ad48820be964762bcc7510eb5243` |
| Stage 2 audit tree | `fe4d53864d0bdc183875133eb5884b23ed8629b7a6b47a305874ac0b20ccf97e` |
| Stage 3 discovery manifest | `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3` |
| Stage 4 generation tree | `ea1e459ed85401784971d659282076c6189dbd464c75ab34538fba39bca8e7f4` |
| Generated project tree | `972db4636350c886e0e9da31f00f1b5f44ba71a6f4d05cc0f39afe10ce8a2bc7` |
| Producer-source bundle tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |

All 840 entries in `stage1_source_hashes` match the corresponding regular files; there are no missing, mismatched, or unrecorded files. Both selected-artifact hashes equal their launcher resolution hashes. The canonical resolved-input digest recomputes as `1ae500c9b3abeaaa032d0bd0db74f68bb1ce051a8cb3c3ef43d0ea0af08f43e5`. See [03-recorded-hashes.txt](/audit-output/evidence/03-recorded-hashes.txt) and [04-stage1-file-hash-map.txt](/audit-output/evidence/04-stage1-file-hash-map.txt).

The required generation-time producer checks pass before relying on Stage 4:

- `klean_export.py`: `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`;
- `klean.py`: `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`; and
- immutable generator image: `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.

Both file hashes agree among the mounted sources, `generator-manifest.json`, and `source-manifest.json`. The image ID agrees between both manifests and the image-key basename of the producer path recorded in `/audit-input.json`. See [01-producer-provenance.txt](/audit-output/evidence/01-producer-provenance.txt).

## Stage 4 generation and bijection

The input manifest, generator manifest, export result, obligation map, trust inventory, toolchain lock, and audit input consistently bind the same Stage 1 export, Stage 3 manifest, inventory, generated tree, and toolchain. Independently recomputed notable hashes are:

- obligation map: `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`; and
- trust inventory: `ec099d95a70d69fbcc4aa0831e391e1adaff2fb40268582010acd67194738ead`.

The exact source-rule/obligation relationship is the empty bijection:

```text
Stage 3 DOMAIN_LEMMA source rules: []
obligation-map source_rules:       []
obligation-map obligations:        []
obligation-map trust_parameters:   []
```

Thus there are no omissions, duplicates, weakened or irrelevant obligations, vacuous conjuncts, or parameter bridges to audit. The generator records obligation count 0 and status `KLEAN_NO_OBLIGATIONS`. The trusted target parser returns null, the independently computed expected target is null, and a source scan finds no `def targetStatement`. This is the correct fixed generated target: no target declaration at all. See [07-manifest-bijection.txt](/audit-output/evidence/07-manifest-bijection.txt), [manifest_bijection_check.py](/audit-output/evidence/manifest_bijection_check.py), and [08-target-and-stage5.txt](/audit-output/evidence/08-target-and-stage5.txt).

## Preflight rerun

I invoked `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the required Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and pinned toolchain lock.

The first invocation exposed an audit-sandbox infrastructure restriction: Lean 4.22 could not read `/proc/<own-pid>/exe`, so `lake clean` failed before project evaluation with `could not detect the configuration of the Lake installation`. A direct diagnostic reproduced `PermissionError(13)` and `lean --version` failed with `failed to locate application`.

To complete the mandated rerun, I built a narrow local preload compatibility shim that substitutes only the denied self-executable lookup with the process's resolved invocation path. It does not inspect or modify Lean sources, project files, statements, or proof terms. With the shim, the pinned tools identify as Lean 4.22.0 commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and Lake 5.0.0, exactly matching the lock. The diagnosis, shim source/hash, and toolchain output are recorded in [05-preflight-infrastructure-and-workaround.txt](/audit-output/evidence/05-preflight-infrastructure-and-workaround.txt) and [audit_selfexe.c](/audit-output/evidence/audit_selfexe.c).

The unmodified trusted `check_generation` then returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target null;
- `lake clean` exit 0 with empty output;
- `lake build` exit 0 with output SHA-256 `3651ba1f6157e5b38bd600e2baad6de87684081705f5737171776d14e53e90bb` and `Build completed successfully.`;
- the same frozen Stage 1, Stage 3, and generated-project hashes; and
- no designated sorry.

The complete returned evidence is in [06-check-generation.txt](/audit-output/evidence/06-check-generation.txt). A post-run snapshot confirmed that all immutable input hashes remained unchanged.

The trusted model-free final mechanical gate also exited 0 with status `PASS`, mode `CLASSIFICATION_ONLY`, target null, no candidate, no used axioms, and no diagnostics. Its complete JSON result is in [09-final-mechanical-gate.txt](/audit-output/evidence/09-final-mechanical-gate.txt). This structural result supplements, but does not replace, the independent classification judgment above.

## Stage 5 applicability

Stage 5 is correctly absent. `/candidate` does not exist; the launcher records null `lean_workspace`, `lean_invocation`, `stage5_result`, and target. Because there is no proposition to prove, fabricating `Proof.final`, running `#print axioms Proof.final`, or supplying operational parameter definitions would contradict the selected no-obligations status rather than add validation. The 41 generated executable hook declarations recorded by the Stage 4 trust inventory are structurally accounted for by preflight, but no theorem depends on them because no target or proof exists.

## Final judgment

The Stage 3 manifest is a bijective classification of the exact canonical inventory; the independently judged domain set is genuinely empty. The deterministic Stage 4 provenance is intact, every applicable recorded hash and identity binding matches, the empty obligation mapping is exact, the fixed target is correctly absent, and Stage 5 is correctly absent. No proof or operational bridge has been substituted for the frozen program's meaning.

VERDICT: PASS
LEGITIMACY: LEGIT
