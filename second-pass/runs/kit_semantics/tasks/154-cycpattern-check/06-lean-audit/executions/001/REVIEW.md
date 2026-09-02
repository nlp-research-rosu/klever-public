# Independent Stage 3–5 audit: `154-cycpattern-check`

## Scope and result

The launcher-recorded mode is `CLASSIFICATION_ONLY`, condition `kit-semantics`, with `SUPPLIED_SEMANTICS`. The selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`; `/candidate` is absent, the audit input has null Lean workspace/invocation and Stage 5 result fields, and there is no generated target. Stage 5 proof, axiom, and operational-bridge checks are therefore inapplicable.

I treated the mounted K proof, prior audit, discovery manifest, generation, comments, and logs as untrusted evidence. Reconstruction used the trusted `/reference/tools` implementations, followed by an independent source/semantics review. Raw commands and results are under [`evidence/`](/audit-output/evidence).

## Provenance and immutable-input integrity

The signed Stage 6 resolution verifies with `resolved_input_sha256` `c284f73aeba87e96bdf7934306bc0a838284367de8a4e61e6a5c4d0c485cea0d`.

All signed-resolution hashes were recomputed and matched:

- Stage 1 pipeline tree: `cc2b37ea2fbbfe325c2cfcf42e2d8b14931c3f0d78b7cc74a03f66f4e904d6a7`.
- Stage 1 Klean export tree: `a5ef93c02cc1abf072d6e599aa3d2c6cdd42f9f5cfeb7013579e7d512088b21c`.
- Stage 3 discovery manifest: `e96e3bd7d34d18ed1ad4eebb61b0f6d45a6ef9fe56ffb67535a361e56ce4b610`.
- Selected Stage 2 audit tree: `e693ef84308b8c9d290c43c7b9278dc8b9f4a068a099623842a381a5a2075347`.
- Selected Stage 4 generation tree: `9c653bd3b51d225ee81dab87851f837ae44d191d27f9a3570b01bd7f00616a5a`.
- Generated Lean project tree: `e336f07528f3cb2b9b28d797c6a1e02ed86e20b3b520073a086222b0bbcb28d4`.
- Generation-time producer bundle tree: `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.

The exact 773-file Stage 1 source-hash map has the same file set and zero hash mismatches. Selection artifact hashes also equal their recomputed trees. Evidence: [`10-audit-input-all-hash-reconciliation.txt`](/audit-output/evidence/10-audit-input-all-hash-reconciliation.txt) and [`20-fresh-preflight-and-signed-resolution.txt`](/audit-output/evidence/20-fresh-preflight-and-signed-resolution.txt).

The launcher metadata field `mechanical_checker_lock_sha256` is the supervisor's checker-bundle lock digest, not the SHA-256 of `/reference/klean-toolchain.lock.json`; it is outside the signed `resolution` object and no checker-lock file is mounted for re-hashing. The mounted Lean toolchain lock itself is structurally equal to `generator-manifest.json.toolchain`, and the trusted preflight consumed it successfully.

### Generation-time producer pinning

This check was completed before judging Stage 4:

| Producer | Observed SHA-256 | Manifest SHA-256 |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | same |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | same |

Those values agree simultaneously with `source-manifest.json` and `generator-manifest.json`. The immutable image ID `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` agrees among the source manifest, generator provenance, and the final component of the producer-source path recorded in `/audit-input.json`. The bundle has exactly the two producers plus its source manifest, and its recomputed pipeline-tree hash matches the audit input. Evidence: [`09-producer-crosscheck-and-stage4-artifacts.txt`](/audit-output/evidence/09-producer-crosscheck-and-stage4-artifacts.txt).

## Rule-inventory reconstruction and bijection

Running `tools.k_rule_inventory.inventory_verification` on the frozen workspace selected `VERIFICATION` from `prove.sh`. Its local module closure is exactly `["VERIFICATION"]`; imported supplied-semantics modules are outside the local `verification.k` module closure. The frozen file hash is `ff11587dbe1bada5c3d825253a9abce30fa0f5c16fcf338d2fc76c9de28a8647`.

The trusted inventory found eight rules and recomputed inventory hash `e8965936389b130da83ca966c8f2d352ba5819829004bcaf84d4d910698449b8`:

| # | Span | Defined symbol/case | Normalized SHA-256 | Independent class |
|---:|---:|---|---|---|
| 1 | 10–17 | `rotateWith` | `559e566db3b1fe403e430522019764b109978ce18accff4e8fc4c00edfab6ed7` | `DEFINITION` |
| 2 | 23–24 | `cycScan`, empty | `b19680acd78644f18d76a448f2b158b2dc9b290ed3ef4e6f1665f0694ff9b45a` | `DEFINITION` |
| 3 | 25–30 | `cycScan`, constructor | `d280dfa12381c84afad63e46d90ef2f2dac21170864a382830122fb86ba15a04` | `DEFINITION` |
| 4 | 33 | `finalRotation`, empty | `acbce82cd11415df09853f747a659e49288044368dc70960b9cda12ac64f5394` | `DEFINITION` |
| 5 | 34–35 | `finalRotation`, constructor | `42982e2255d4f887a541b2534f1f2adb8ad67fdf1ccc543cb223c4851b6924a5` | `DEFINITION` |
| 6 | 38 | `finalChar`, empty | `e209dd690d629457adfb070d37467ab97ac0b807f7ac9e8f4d651cdc65b814e0` | `DEFINITION` |
| 7 | 39–40 | `finalChar`, constructor | `9ced6a3b7bc4bcc4f1a55e7ce3760972548397312ff6474917ec6dbfc9a31542` | `DEFINITION` |
| 8 | 45–50 | `cycPattern` | `dbc206f58341f9a20282d64086026114a906fa04c84592d51fa174533659cd10` | `DEFINITION` |

For every entry, `source_rule_id` is exactly `rule-<normalized_sha256>`. The discovery manifest has eight entries, eight unique IDs, the same ID set, the exact canonical order, and the same inventory hash. There are no omissions, duplicates, extras, reordered identities, or changed hashes. The trusted trust-boundary validator also passed. Evidence: [`04-independent-tree-hashes-and-rule-inventory.txt`](/audit-output/evidence/04-independent-tree-hashes-and-rule-inventory.txt) and [`08-strict-inventory-bijection-and-semantics-locations.txt`](/audit-output/evidence/08-strict-inventory-bijection-and-semantics-locations.txt).

## Independent classification judgment

All eight entries are genuinely `DEFINITION`, not disguised domain lemmas:

- `rotateWith` is an unconditional named summary of `rotation[1:] + c`. Under the supplied slice rules, `clampHi(1, len, 1)` is `min(1, len)`, `buildIS` constructs the suffix, and `seqConcat` appends the one-code sequence.
- The two `cycScan` equations are exhaustive, nonoverlapping structural equations on `IntSeq`. The constructor case consumes exactly one remaining character, applies the rotation update, and accumulates `FOUND orBool strContains(newRotation, A)`. This is the loop fold, not a proposition asserting a property of its result.
- The `finalRotation` and `finalChar` pairs are exhaustive structural recurrences for the two loop-mutated environment bindings tracked by the circularity. Both recurse on the strict tail `REST`.
- `cycPattern` only initializes that fold: supplied slice normalization makes `buildIS(B, 0, clampLo(len(B)-1, 1), 1)` exactly `B[:-1]`; `strContains(B, A)` is exactly the semantics of `b in a`.

The rules match only newly declared helper-function terms. None matches a `<k>` cell, a program AST operation, or any operational configuration, so none replaces fixed-semantics execution. The operational `For/#loop/#iterNext` rules remain responsible for execution; the Stage 1 `cyc-loop` claim connects that execution to the summaries. Base/constructor guards are exhaustive and disjoint, recursive calls descend on `REST`, and the two unconditional definitions are total over their declared sorts.

No rule has a `simplification` attribute, so the simplification-class restriction is satisfied trivially. No rule claims `PROVED_DERIVED_LEMMA` status, so there is no unproved “derived” rule to justify. Most importantly, none states an extra theorem about cyclic patterns, rotations, or substring membership; the top-level helper is an execution summary of the source algorithm, not a material mathematical property assumed to close the postcondition. The independent counts are therefore:

- `DEFINITION`: 8
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

As finite adversarial support for the structural reasoning, an independently written checker compared the source algorithm with `cycPattern`, `finalRotation`, and `finalChar` on 3,969 pairs over `{a,b}` through length five: zero mismatches. An identity-rotation mutation is rejected by witness `a="ab", b="ba"` (true versus false), and iterating full `B` instead of `B[:-1]` changes final loop state for `b="ab"` (`"ba"` versus `"ab"`). Evidence and checker source: [`64-independent-summary-adversarial-check.txt`](/audit-output/evidence/64-independent-summary-adversarial-check.txt), [`independent_summary_check.py`](/audit-output/evidence/independent_summary_check.py), and [`69-operational-semantics-detail.txt`](/audit-output/evidence/69-operational-semantics-detail.txt).

## Deterministic Stage 4 generation

I reran the required call to `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the frozen Stage 1 workspace, protected discovery manifest, selected generation, and mounted toolchain lock.

The first attempt exposed a container-only PID-namespace issue: Lean 4.22's `IO.appPath` reads `/proc/<getpid()>/exe`, whereas this sandbox exposes the executable at `/proc/self/exe`. I used an audit-local `LD_PRELOAD` compatibility shim that changes only a `readlink` request of the form `/proc/*/exe` to `/proc/self/exe`. It does not modify Lean, the generated tree, or theorem data. With the shim, the frozen-toolchain assertion confirmed K `7.1.293`, pyk/Klean `7.1.293`, Lean `4.22.0` commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and Codex `0.144.6`.

The fresh preflight then returned `KLEAN_NO_OBLIGATIONS`:

- `lake clean`: exit 0, empty output hash `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `lake build`: exit 0, output hash `0e2e2d72e7c0440573e3b5c9dbb1b997179c6be5d7e5e3bbff58b63c59177e07`.
- Obligation count: 0.
- Target: null.
- Generated-tree hash: `e336f07528f3cb2b9b28d797c6a1e02ed86e20b3b520073a086222b0bbcb28d4`.

The complete fresh result equals both `/reference/klean-generation/preflight.json` and the preflight object signed into `/audit-input.json`, including diagnostics. Evidence: [`61-proc-exe-compatibility-shim.txt`](/audit-output/evidence/61-proc-exe-compatibility-shim.txt), [`62-fresh-preflight-success.txt`](/audit-output/evidence/62-fresh-preflight-success.txt), and [`68-fresh-preflight-reconciliation.txt`](/audit-output/evidence/68-fresh-preflight-reconciliation.txt).

Independent of preflight, I recomputed the Stage 3 domain source list as empty and checked:

- `input-manifest.source_rules = []`;
- `obligation-map.source_rules = []`;
- `obligation-map.obligations = []`;
- `obligation-map.trust_parameters = []`;
- both obligation-count fields are zero;
- the obligation-map and generated-tree hashes match their manifests;
- `expected_target_definition`, the parsed generated target, generator-manifest target, and audit-input target are all null;
- there are no empty/vacuous conjuncts because there are no conjuncts at all; and
- `/candidate` does not exist, and every Stage 5 field is null.

Thus the source-rule/obligation map is the exact empty bijection, not an omission. `KLEAN_NO_OBLIGATIONS` is legitimate precisely because the independent classification found a genuinely empty domain-lemma set. Evidence: [`67-independent-stage4-bijection-and-target-check.txt`](/audit-output/evidence/67-independent-stage4-bijection-and-target-check.txt).

## Final judgment

The protected Stage 3 classification is bijective and mathematically correct. The selected Stage 4 generation is provenance-pinned, hash-consistent, freshly buildable, and has the uniquely correct empty target/obligation state. Stage 5 is correctly absent in classification-only mode.

VERDICT: PASS
LEGITIMACY: LEGIT
