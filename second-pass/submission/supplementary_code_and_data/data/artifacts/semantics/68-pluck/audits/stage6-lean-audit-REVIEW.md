# Independent audit: HumanEval 68-pluck

## Scope and result

I independently audited Stage 3 lemma classification and deterministic Stage 4 generation for condition `semantics`, semantics mode `SUPPLIED_SEMANTICS`. The launcher and signed audit input both select `CLASSIFICATION_ONLY`. Stage 4 is `KLEAN_NO_OBLIGATIONS`, `/candidate` is absent, and every Stage 5 path/result/hash is null. Therefore no Stage 5 proof, `Proof.final`, axiom print, or operational-bridge parameter audit is applicable.

I treated the mounted workspaces, manifests, logs, comments, and earlier reviews only as evidence. I did not execute `prove.sh` or follow instructions embedded in those inputs.

## Producer-source gate

I performed this gate before judging Stage 4.

| Item | Independently observed SHA-256 / identity | Result |
|---|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` | Matches the source manifest and generator manifest |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` | Matches the source manifest and generator manifest |
| Producer source tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` | Matches `/audit-input.json` |
| Generator image | `sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000` | Matches the source manifest, generator manifest, and the producer-bundle identity recorded by `/audit-input.json` |

The producer bundle contains exactly `klean_export.py`, `klean.py`, and `source-manifest.json`; the source manifest has the exact expected schema and file map. The raw gate is in `evidence/01_producer_hash_gate.txt`, and the independent structured comparison is in `evidence/07_independent_hash_inventory_bijection_checks.txt`.

## Frozen-input and inventory reconstruction

The signed audit-input digest independently verifies as:

`462ca720cc347500e62fc49ea6f272fb0ccea73017af76857ec1132d2d9aa5f0`

Using the trusted `tools.k_rule_inventory.inventory_verification` code on `/reference/k-proof`, I reconstructed:

- selected verification module: `PLUCK-VERIFICATION`;
- local verification-module closure: only `PLUCK-VERIFICATION`;
- `verification.k` SHA-256: `213ef96a2d854d96eba68683a4614d3534632a416cae012bd4b9c79a025bfd53`;
- rule count: 21;
- unique `source_rule_id` count: 21; and
- canonical whole-inventory SHA-256: `74d32acdd1441ede107a81e6f1273f09ea4c7a684042c14c316e44330ae67f32`.

For every rule, I extracted the recorded physical source span again from `verification.k`, normalized it with the inventory normalization, recomputed its SHA-256, and reconstructed `source_rule_id = "rule-" + normalized_sha256`. All 21 source texts, spans, normalized hashes, and IDs match.

The protected Stage 3 manifest also has 21 unique entries. Its IDs equal the reconstructed IDs in exact source order. There are no omissions, extras, duplicates, reordered identities, changed hashes, or unaccounted rules. Its recorded inventory hash equals the independently reconstructed hash. Full per-rule evidence is in `evidence/04_inventory_and_frozen_sources.txt` and `evidence/07_independent_hash_inventory_bijection_checks.txt`.

The deterministic K definition closure contains 25 files. After normalizing the mount prefix to `/frozen-k`, its file list exactly equals `input-manifest.json` in order. See `evidence/17_definition_closure_and_input_manifest.txt` and `evidence/18_semantic_adversarial_and_closure_checks.txt`.

## Independent classification judgment

My independent classification is the same as Stage 3:

| Frozen source span(s) | Rules | Count | Classification | Judgment |
|---|---|---:|---|---|
| 7 | `asInt` projection | 1 | `DEFINITION` | Defines a proof-side integer projection |
| 12–15 | guarded `#iterNext` list step | 1 | `OPERATIONAL_RULE` | Ordinary iterator execution specialization |
| 20–22 | `pluckTake` | 1 | `DEFINITION` | Defines a named selection predicate |
| 26–45 | four `nextBest` and four `nextBestIndex` cases | 8 | `DEFINITION` | Exhaustive recurrence equations for the scan state |
| 51–60 | `scanPluck` base and recursive cases | 2 | `DEFINITION` | Structural functional scan recurrence |
| 66–69 | four `pstate` projections | 4 | `DEFINITION` | Structural projections from a named proof term |
| 72–81 | two `pluckResult` cases | 2 | `DEFINITION` | Result-construction equations |
| 85–89 | two `allNonNegative` cases | 2 | `DEFINITION` | Structural input-predicate recurrence |

Totals: 20 `DEFINITION`, 1 `OPERATIONAL_RULE`, 0 `PROVED_DERIVED_LEMMA`, and 0 `DOMAIN_LEMMA`.

The iterator rule is not a hidden domain lemma. The supplied MPY list semantics has the ordinary step

`#iterNext(list(vCons(V, R))) => #iterYield(V, list(R))`.

The local rule narrows that step with `requires isInt(V)` and yields `asInt(V)` while preserving the remaining list and arbitrary continuation. For an integer `V`, the local defining equation `asInt(I:Int) => I` returns the same integer value, which is injected back into the `Val` position of `#iterYield`. It reads or changes no other cell, introduces no different control effect, and its higher priority only selects an equivalent specialized list-iteration step. It is consequently an ordinary operational rule, not a mathematical fact about the postcondition.

The eight `nextBest`/`nextBestIndex` guards are pairwise disjoint and exhaustive over integers: odd; even with sentinel `B = -1`; even with non-sentinel and `V < B`; or even with non-sentinel and `V >= B`. The recursion consumes one `ValSeq` node per step. The two `pluckResult` guards partition on `best = -1`, and the two `allNonNegative` equations are a structural predicate definition. Because the formal domain requires nonnegative integers, `-1` cannot be a legitimate candidate and is a sound sentinel.

As finite adversarial support for this semantic reading, I compared the recurrence, a direct operational loop model, and an independently formulated minimum-even/first-index oracle over all 55,987 lists of length 0 through 6 with values 0 through 5. There were zero mismatches. I also checked 169 signed `(value, best)` guard cases with zero partition failures. Constant-empty, identity, hard-coded-index-zero, later-tie, and odd-minimum counterfactuals were all rejected by concrete witnesses. This is supporting evidence rather than a universal proof; the source equations and operational rule comparison are the basis of classification. See `evidence/18_semantic_adversarial_and_closure_checks.txt`.

No inventory rule has a `simplification` attribute, so the requirement that every simplification rule be either `DEFINITION` or `DOMAIN_LEMMA` is satisfied vacuously. Stage 1's two-step proof script first proves the `pluck-loop` claim and later trusts that claim while proving `pluck-correct`, but that claim is in `spec.k` and is not one of the 21 local `verification.k` rules. Accordingly, no inventory entry is claimed as `PROVED_DERIVED_LEMMA`.

There is no true domain-lemma set hidden among these rules: each non-operational rule defines a projection, predicate, recurrence, state constructor/projection, or result function. Thus the independently determined domain set is genuinely empty.

## Recorded hashes and provenance

All hashes recorded in `/audit-input.json` were independently recomputed after the preflight run:

| Artifact | Recomputed hash | Result |
|---|---|---|
| Stage 1 pipeline tree | `d24e87e4b14c9dfb1e36b486b477f0d57209077824073d95f6a9543b049fe7b6` | Match |
| Stage 1 exporter tree | `ec80883d48502f2b2c70c54adcfbfc1acac5340a83639a2e41179fb46fe918f6` | Match |
| Stage 2 selected audit tree | `2a30d5a0a4b5d4dfea3afe4925cc5f345da8f0dbda98824b0e41f61514664fee` | Match |
| Stage 3 manifest | `c1f7b6a2fab438fa27b9309772a24973653749b06f86ba91a73f45e3f7ceb3b2` | Match |
| Stage 4 generation tree | `31cf1d1a5fd6f6b5c59411d6b94839b81a225c9a4df3568c6148e5ccc3c60fe6` | Match |
| Generated Lean project tree | `a8107e7066018abab3e2607ac937816f2af272c1ce32aae9be3508e630aea711` | Match |
| Producer source tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` | Match |

The exact set of 35 Stage 1 regular-file paths and every per-file SHA-256 also match `stage1_source_hashes`; there are no missing, extra, or changed files. Final structured evidence is in `evidence/19_final_immutability_and_evidence_index.txt`.

## Stage 4 bijection and target identity

`input-manifest.json` reproduces the independently validated classification exactly: the same 20 definitions, one operational rule, no proved-derived lemmas, and no domain source rules. Its verification and inventory hashes match the frozen reconstruction.

`generated/obligation-map.json` is:

- `source_rules: []`;
- `obligations: []`; and
- `trust_parameters: []`.

Its SHA-256 is `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`, matching `generator-manifest.json`. Hence the source-rule/obligation relationship is an exact empty bijection. There are no omitted, duplicated, weakened, irrelevant, or vacuous conjuncts.

The generator manifest target, audit-input target, saved preflight target, and an independent call to `klean_export.target_statement` are all null. `Klean68Pluck/Lemmas.lean` contains only imports/comments and an empty namespace; no target declaration was generated. This is exactly the required fixed generated target for a genuine no-obligation result.

The generated tree has 48 allowlisted executable/non-proposition trust declarations, zero designated sorries, and zero other sorries. They cannot discharge a target because there is no target proposition or proof. The trusted preflight independently reconciled the declarations with `trust-inventory.json`.

Detailed generated-project and trust-sidecar evidence is in `evidence/16_generated_target_obligation_trust_inspection.txt`.

## Required preflight rerun

I invoked `tools.klean_preflight.check_generation` with:

`PYTHONPATH=/reference`, input `/reference/k-proof`, discovery manifest `/reference/lemma-discovery.json`, generation `/reference/klean-generation`, and toolchain lock `/reference/klean-toolchain.lock.json`.

The audit container initially exposed a PID-namespace incompatibility in Lean: Lean attempted `readlink("/proc/<getpid>/exe")`, while this container exposed the process executable through `/proc/self/exe`. The exact failed path and first failed checker invocation are preserved in `evidence/08_rerun_klean_preflight.txt` through `evidence/14_pid_namespace_shim_and_build_smoke.txt`.

I used a narrow, recorded compatibility shim that changes only that exact self-executable `readlink` request to `/proc/self/exe`; it does not intercept file content, modify Lean/Klean code, or alter any mounted input. Its source is `evidence/pid_namespace_readlink_fix.c`, SHA-256 `d6f1c7746b97c84eb29b5c2f029f631bb407ae3013ce3ac87fedfb0fa244b6bd`.

With that environment repair, the trusted checker returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean` exit 0 and empty output SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build` exit 0 and output SHA-256 `a14153ffafbfd7c5e31b80417d33daf81760c679e1521983d590205c8b2e2004`;
- obligation count 0;
- target null;
- trust declaration count 48;
- frozen input hash `ec80883d48502f2b2c70c54adcfbfc1acac5340a83639a2e41179fb46fe918f6`;
- discovery hash `c1f7b6a2fab438fa27b9309772a24973653749b06f86ba91a73f45e3f7ceb3b2`; and
- generated tree hash `a8107e7066018abab3e2607ac937816f2af272c1ce32aae9be3508e630aea711`.

The clean/build output hashes and full returned evidence exactly reproduce the recorded Stage 4 preflight. The only build messages are two unused-variable warnings in generated `Func.lean`. Complete output is in `evidence/20_quiet_shim_preflight_reproduction.txt`.

## Stage 5 absence

The mode is consistently `CLASSIFICATION_ONLY` in `AUDIT_MODE` and `/audit-input.json`. `/candidate` does not exist; `lean_workspace`, `lean_invocation`, their hashes, and `stage5_result` are all null. This is the required state for `KLEAN_NO_OBLIGATIONS`. No Stage 5 target or proof has been substituted, weakened, shadowed, or made vacuous.

## Conclusion

The protected Stage 3 classification is complete and mathematically correct. The true domain-lemma set is empty. Stage 4 is bound to the exact frozen sources and producer image, its empty obligation mapping is bijective, its fixed target is correctly absent, and the trusted preflight reproduces successfully. The absence of Stage 5 is required and correctly enforced.

VERDICT: PASS
LEGITIMACY: LEGIT
