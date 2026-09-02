# Independent audit: `99-closest-integer`

## Scope and result

I independently audited Stage 3 classification and deterministic Stage 4 generation for condition `kit-semantics` under `SUPPLIED_SEMANTICS`. Both the `AUDIT_MODE` environment variable and the signed `/audit-input.json` resolution say `CLASSIFICATION_ONLY`. The resolution has `lean_workspace: null`, `lean_invocation: null`, and `stage5_result: null`; `/candidate` is absent. Stage 5 proof checks therefore do not apply.

I treated all mounted candidate/provenance narratives and earlier verdicts as untrusted evidence. The judgment below comes from the frozen source, trusted inventory/preflight code, recomputed hashes, and fresh mechanical checks.

## Launcher and hash integrity

The signed audit-input envelope validates with resolved-input digest `8ab2b58dbcaddc19602120fc9962b64f696693cac046179cc8ec6210271d784d`. The recorded problem, condition, and semantics mode are respectively `99-closest-integer`, `kit-semantics`, and `SUPPLIED_SEMANTICS`.

Every launcher-recorded resolution hash was independently recomputed with the corresponding trusted hash routine:

| Artifact | Recomputed and recorded SHA-256 |
|---|---|
| Stage 1 workspace tree | `679a45d6e4555c4f3b11050f12191d7ba80257d1304481994a1585590bf1bfda` |
| Stage 1 generation/export tree | `64fd0b579473d97ccfb6e1429d32f137d2812d8d00a7da11d7597bd78f20133e` |
| Stage 2 selected audit tree | `930bba2f999666319837c34d5a5958e3756371c2cc8ea04f9aabffed93bb68b8` |
| Stage 3 discovery file | `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3` |
| Stage 4 selected generation tree | `49be1613e503e52d2ec2fe37df13e8c1b9de661e3597797dbeb94f61716c6bab` |
| Generation producer-source tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |
| Generated Lean project tree | `fb70e5cf0199a828174e17bcd1f653c96593240457485a3497146f276ffe9217` |

The Stage 1 per-file ledger is also bijective: 809 hashes were recorded, 809 regular files exist, and there are no missing paths, extra paths, or content mismatches. See `evidence/04_hash_and_bijection_results.log` and `evidence/07_audit_input_validation.log`.

## Stage 3 inventory reconstruction

The frozen `verification.k` is five lines long. It requires the supplied semantics and defines only:

```k
module VERIFICATION
  imports MPY
endmodule
```

Running the trusted `tools.k_rule_inventory.inventory_verification` against `/reference/k-proof` independently reconstructed:

- verification module: `VERIFICATION`;
- local verification-module closure: `["VERIFICATION"]`;
- verification source hash: `ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`;
- rules: `[]`; and
- inventory hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`, the canonical SHA-256 of `[]`.

`MPY` is provided by the required frozen semantics; it is not a proof-local module declared in `verification.k`. The trusted inventory therefore correctly excludes those fixed-semantics rules from the local proof-extension inventory.

The reconstructed document matches `/reference/lemma-discovery.json` exactly in schema, inventory hash, rule count, identity order, and complete ordered rule list. Since the inventory has zero entries, there are no source spans, normalized rule hashes, `source_rule_id` values, omissions, duplicates, reordered identities, extra rules, or unaccounted classifications. Raw reconstruction is in `evidence/02_inventory_reconstruction.log`.

## Independent classification judgment

Every inventory entry was reclassified; the set is empty. Consequently the counts for `DEFINITION`, `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, and `DOMAIN_LEMMA` are all zero. There are also zero local `simplification` rules, so none can be mislabeled or left outside the required `DEFINITION`/`DOMAIN_LEMMA` classes.

This is a genuinely empty domain-lemma set, not an omission. The frozen source program converts the input string to a float, computes `floor` and `ceil`, and returns one of them according to sign and distance from the adjacent integer. The four K claims use the same branch guards and return expressions. The relevant execution is supplied by fixed `MPY` rules for `float`, `math.floor`, `math.ceil`, subtraction, and comparison (`decStrToF`, `floorFI`, `ceilF`, `subF`, `ltIF`, and `floatLt`). No rule in `verification.k` summarizes that computation, asserts the closest-integer property, preempts execution, or supplies a proof-local named proof term. Relevant frozen source and operational rules are recorded in `evidence/06_classification_source_semantics.log`.

The supplied semantics intentionally leaves symbolic floating operations opaque to `kprove` while providing concrete operational rules. That is part of the frozen `SUPPLIED_SEMANTICS` boundary, not a Stage 1 local rule that Stage 3 could relabel as a definition or derived lemma. The Stage 3 result therefore has no domain lemma to export to Lean.

## Producer authentication

Producer authentication passed before the Stage 4 judgment:

| Source | Actual SHA-256 | Required SHA-256 |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | same in source manifest and generator manifest |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | same in source manifest and generator manifest |

The source manifest and generator manifest both identify generator image `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`. The immutable producer-source directory named in `/audit-input.json` ends in that same image digest, and its recomputed pipeline tree hash is the recorded `388cac39...f11e`. There is no producer-source mismatch or infrastructure `AUDIT_ERROR`. See `evidence/01_launcher_and_producer_auth.log` and `evidence/01b_producer_tree_pipeline_hash.log`.

## Stage 4 manifest and obligation bijection

The independently checked sets are:

| Binding | Value |
|---|---|
| Stage 3 rules | `[]` |
| Stage 4 `source_rules` | `[]` |
| definitions | `[]` |
| operational rules | `[]` |
| proved derived lemmas | `[]` |
| obligation-map source rules | `[]` |
| obligations | `[]` |
| trust parameters | `[]` |

The obligation map file hash is `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`, exactly the generator-manifest value. Both the generator manifest and export result report obligation count zero. Inventory, Stage 1, Stage 3, generated-tree, toolchain-lock, export-result, and selection-status cross-bindings all match.

There are no obligations that could be irrelevant, weakened, duplicated, vacuous, or mapped to the wrong source rule. There is likewise no omitted obligation because the independently classified true domain set is empty. `KLEAN_NO_OBLIGATIONS` is therefore the correct Stage 4 status.

## Fixed target identity

The generator manifest target is `null`, the signed audit-input target is `null`, and the trusted `klean_export.target_statement` independently derives `None` from the generated project. A source scan finds no `final`, theorem, or lemma declaration in the generated Lean files. Thus there is no generated target declaration, statement, parameter, or target hash to change or weaken. The generated project is fixed by its matching tree hash, and no Stage 5 proof candidate exists. See `evidence/04_hash_and_bijection_results.log` and `evidence/05_no_target_no_candidate_scan.log`.

The generated generic prelude contains 41 collection-hook axioms, all structurally reconciled by the trusted preflight with `trust-inventory.json`. With no target theorem, none constitutes a hidden proof of a target. Proof-mode axiom accounting and operational-bridge parameter checks are inapplicable because there is no `Proof.final`, no target parameters, and no candidate.

## Fresh trusted preflight

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the required Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and pinned toolchain lock.

The audit container initially exposed a PID-namespace mismatch: `getpid()` returned namespace PID 2 while `/proc` exposed host PIDs, causing Lean's `readlink("/proc/2/exe")` installation lookup to fail. I recorded the failures, diagnosed the exact syscall path, and used an audit-local preload shim that changes only `/proc/<current-pid>/exe` to `/proc/self/exe`. Its complete 20-line source and hashes are in `evidence/proc_self_readlink_shim.c` and `evidence/03g_lean_namespace_shim.log`; it does not alter generated sources, Lean declarations, or theorem checking.

With that namespace-only correction, the pinned Lean reports version 4.22.0 and commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`. The trusted preflight returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0;
- `lake build`: exit 0, “Build completed successfully”;
- generated tree hash `fb70e5cf0199a828174e17bcd1f653c96593240457485a3497146f276ffe9217`;
- obligation count 0;
- target `null`;
- designated sorry count 0; and
- trust declaration count 41.

The fresh build's output hash differs from the generation-time preflight only because independent modules were printed in a different parallel completion order; the source tree, target, obligations, exit status, and trusted preflight result are unchanged. Complete returned evidence is in `evidence/03h_preflight_rerun_success.log`; the resolved environment failures remain preserved in the preceding `03*` logs.

## Final judgment

Stage 3 is a complete and exact empty classification of the local verification-module rule closure. Stage 4 authenticates to the immutable producer, preserves every recorded hash and provenance binding, maps the empty source-rule set bijectively to an empty obligation set, and correctly emits neither a target nor a Stage 5 task. No mathematical domain lemma about `closest_integer` was hidden under another category or omitted from Lean generation.

VERDICT: PASS
LEGITIMACY: LEGIT
