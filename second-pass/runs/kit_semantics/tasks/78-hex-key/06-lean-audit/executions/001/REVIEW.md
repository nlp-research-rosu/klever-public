# Independent Stage 3/4/5 Audit: `78-hex-key`

## Scope and outcome

This audit covers HumanEval problem `78-hex-key`, condition `kit-semantics`, and semantics mode `SUPPLIED_SEMANTICS`. Both the environment and `/audit-input.json` select `CLASSIFICATION_ONLY`. The selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`; `/candidate` is absent, so no Stage 5 proof audit is applicable.

I independently reconstructed the frozen Stage 1 rule inventory, reclassified every rule from the K source and operational semantics, verified all mounted hash bindings and producer provenance, reran the trusted Stage 4 preflight, and separately checked the source-rule/obligation/target correspondence. The classification is correct, the true domain-lemma set is empty, and the no-obligations generation is legitimate.

## Input and producer integrity

The launcher binding is internally consistent:

- `AUDIT_MODE=CLASSIFICATION_ONLY`, matching `/audit-input.json`.
- Problem, condition, and semantics mode are `78-hex-key`, `kit-semantics`, and `SUPPLIED_SEMANTICS`.
- The canonical resolved-input digest recomputes to `f261872286cb2f2c20deb5a9c5ab94eb6f7eb3a1890283b69d3dd54603d533bd`.
- All 771 regular Stage 1 files are represented exactly once in `stage1_source_hashes`; there are no missing, extra, or mismatched files.
- Every recorded mounted-input hash recomputes exactly: the Stage 1 pipeline tree and export tree, Stage 2 audit tree, Stage 3 manifest, Stage 4 generation tree, generated project tree, and producer-source tree. The recomputed values are in `evidence/06_hash_check_results.txt`.

Before judging Stage 4, I hashed the two immutable generation-time producer files:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both values exactly match `generation-tools/source-manifest.json` and `klean-generation/generator-manifest.json`. The source manifest and generator manifest both bind the immutable generator image to `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`; `/audit-input.json` independently binds the producer-source path to the same digest in its basename and binds the complete producer tree to `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`. There is no producer-source infrastructure mismatch.

## Stage 1 inventory reconstruction

I invoked the trusted local `tools.k_rule_inventory.inventory_verification` implementation against `/reference/k-proof`, without using the Stage 3 classifications as input. It selected main module `VERIFICATION`; its local verification-module closure contains only `VERIFICATION`. The frozen `verification.k` SHA-256 is `685a9bdd74764d4cd0b6d8451827211187bf5febcaf7d58dc6520da2671d9a2a`.

The reconstructed inventory is:

| Order | Span | `source_rule_id` | Normalized SHA-256 | Attributes |
|---:|---:|---|---|---|
| 1 | 9–9 | `rule-1f493419665e264916f30ab5358e05eef39549f5227088474c1ff240d5e27abe` | `1f493419665e264916f30ab5358e05eef39549f5227088474c1ff240d5e27abe` | none |
| 2 | 10–14 | `rule-7d9e21c1ff4818429cf5dfabc65f7730ee1b9f46e3a11cc4a89558f5cd957c74` | `7d9e21c1ff4818429cf5dfabc65f7730ee1b9f46e3a11cc4a89558f5cd957c74` | none |

The canonical whole-inventory hash is `134928cdbb2e86afcf7d1b87d805c043d37ffcf38c6f9991d2d17f482d832a24`.

The comparison with `/reference/lemma-discovery.json` is bijective and order-sensitive. The two ordered identities and the whole-inventory hash match exactly; both sides have unique IDs and the same count; there are no omissions, duplicates, extras, reordered identities, changed normalized hashes, or unaccounted classifications. The full source spans and comparison results are in `evidence/07_inventory_reconstruction.txt`.

## Independent Stage 3 classification

### Rule 1: empty sequence

`hexCount(.IntSeq) => 0` is a `DEFINITION`. The declaration immediately above it introduces the named proof summary `hexCount : IntSeq -> Int` with `[function, total]`. This rule supplies the base equation of that structural definition. It neither rewrites a program configuration nor asserts an independent mathematical property.

### Rule 2: nonempty sequence

The `iCons(C, CS)` rule is also a `DEFINITION`. It is the descending structural recurrence for the same named summary: it adds one exactly when the one-code string for `C` occurs in the fixed code sequence for `"2357BD"`, then recurses on the strict tail `CS`.

This classification follows the frozen operational semantics, not the Stage 3 rationale:

- String iteration yields `str(iCons(C, .IntSeq))` for the head and continues with the tail.
- Source `digit in "2357BD"` dispatches to `applyCmp("in", ...)`, then to `strContains` over the same one-code string and fixed target sequence.
- Integer-plus-Boolean addition maps `true` to one and `false` to zero.
- The `hex-loop` claim accumulates the processed prefix and retains `hexCount(CS)` for the remaining iterator, so the recurrence names exactly the per-iteration summary used by ordinary execution.

The equation does not preempt `Call`, `For`, `#loop`, lookup, binding, comparison, augmentation, return, or any other operational step. It does not state the requested postcondition as an independent fact; it defines the mathematical value to which ordinary source execution is connected by the loop claim. The literal `"2357BD"` exactly matches the source program and the stated prime hexadecimal digits `2, 3, 5, 7, B, D`, so the summary is relevant to both the source program and postcondition.

Neither inventory rule is an `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`. No rule claims the special two-stage derivation required for `PROVED_DERIVED_LEMMA`. Both rule attribute lists are empty, so there are no `[simplification]` rules to classify. The independently determined true domain-lemma set is therefore genuinely empty.

The frozen source, specification, and relevant operational rules are recorded in `evidence/08_frozen_source_and_semantics.txt` and `evidence/09_operational_path_rules.txt`.

## Deterministic Stage 4 generation

### Trusted preflight rerun

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and these exact logical inputs:

```text
frozen_input=/reference/k-proof
discovery_manifest=/reference/lemma-discovery.json
generation=/reference/klean-generation
toolchain_lock=/reference/klean-toolchain.lock.json
```

The sandbox initially exposed `/proc/self/exe` but not `/proc/<namespace-pid>/exe`, which prevented Lean 4.22 from locating its executable and made the first `lake clean` fail before elaboration. I diagnosed and recorded that infrastructure behavior, then compiled the narrow shim in `evidence/procself_shim.c` under `/tmp/audit-work`. It changes only `readlink`/`readlinkat` requests matching `/proc/<digits>/exe` to `/proc/self/exe`; it does not modify any frozen, discovery, generation, or Lean source. With that shim preloaded, the pinned Lean executable reports version 4.22.0 and the unchanged trusted preflight completes. The preflight's before/after snapshots independently confirm that all immutable inputs remained unchanged.

The returned preflight evidence is saved verbatim in `evidence/18_klean_preflight_success.txt`:

- status: `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0;
- `lake build`: exit 0;
- build output SHA-256: `a538eb4a7c3b93c2dd1dc28564af1ad6bfabd422ee3135528ff43d04318b51b6`, exactly matching the recorded generation-time preflight;
- obligation count: 0;
- target: `null`;
- generated tree SHA-256: `7d93362e3e1aaa129ed9a37b2910615b530ae4f78c9e43b11459d1eefb4ab49c`.

The initial infrastructure failure, diagnosis, shim source/hash, Lean version check, and successful direct clean build remain visible in `evidence/10_klean_preflight_rerun.txt` through `evidence/17_procself_shim_validation.txt`.

### Independent obligation and target audit

I separately compared the reconstructed inventory, independent classifications, input manifest, generator manifest, export result, obligation map, toolchain lock, generated Lean sources, and audit input. All checks in `evidence/19_stage4_structural_results.txt` pass:

- `input-manifest.json.definitions` is exactly the two reconstructed ordered rules with their Stage 3 classifications and rationales.
- The independently classified domain IDs are `[]`.
- `input-manifest.json.source_rules`, `obligation-map.json.source_rules`, `obligations`, and `trust_parameters` are all exactly `[]`.
- The obligation IDs therefore form the exact unique ordered bijection with the true domain set. There can be no omission, duplicate, irrelevant obligation, weakened obligation, or vacuous conjunct because both sides are genuinely empty.
- The obligation-map file hash matches the generator manifest.
- `klean_export.target_statement` returns `None`, and `expected_target_definition` returns `None`.
- The generator manifest, recorded preflight, and `/audit-input.json` all record target `null`.
- An independent scan finds no `theorem` or `lemma` declaration anywhere in the generated Lean sources.
- The generated tree, Stage 1 export, Stage 3 manifest, inventory, trust-inventory, and pinned toolchain bindings all recompute and agree.

Thus `KLEAN_NO_OBLIGATIONS` is not a self-consistent concealment of a domain lemma: it follows from the independent mathematical classification. There is no generated target to weaken or change.

## Stage 5

Stage 5 is correctly absent. The launcher selected `CLASSIFICATION_ONLY`, the true domain set is empty, the generated target is absent, and `/candidate` does not exist. The proof-mode clean-copy, `Proof.final`, axiom accounting, and operational-bridge parameter checks therefore do not apply.

## Evidence index

- `evidence/00_launcher_and_files.txt`: launcher mode and mounted file inventory.
- `evidence/01_manifests_and_producer_hashes.txt` through `evidence/04_audit_input_generator_fields.txt`: manifests and producer/image bindings.
- `evidence/05_trusted_tool_interfaces.txt`: trusted inventory/preflight interfaces.
- `evidence/06_hash_check_results.txt` and `evidence/hash_check.py`: complete recomputation of mounted hashes and Stage 1 per-file hashes.
- `evidence/07_inventory_reconstruction.txt` and `evidence/inventory_check.py`: canonical inventory and bijection.
- `evidence/08_frozen_source_and_semantics.txt` and `evidence/09_operational_path_rules.txt`: source and operational-semantic classification evidence.
- `evidence/10_klean_preflight_rerun.txt` through `evidence/18_klean_preflight_success.txt`: preflight attempts, environment diagnosis, narrow shim, clean build, and returned evidence.
- `evidence/19_stage4_structural_results.txt` and `evidence/stage4_structural_check.py`: independent no-obligation and null-target audit.

VERDICT: PASS
LEGITIMACY: LEGIT
