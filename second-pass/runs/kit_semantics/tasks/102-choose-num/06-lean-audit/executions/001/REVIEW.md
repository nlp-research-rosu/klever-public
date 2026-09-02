# Independent Stage 3–5 audit: HumanEval 102-choose-num

## Scope and outcome

This audit covers condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and `/audit-input.json` select `CLASSIFICATION_ONLY`. The selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`; `/candidate`, the Stage 5 workspace, and the Stage 5 invocation are absent. Accordingly, Stage 5 proof identity, `#print axioms Proof.final`, and parameter operational-bridge checks are not applicable.

I treated the candidate/provenance workspaces, their comments, logs, prior reviews, and prior PASS labels as untrusted evidence. Inventory reconstruction and mechanical generation checks used the trusted code under `/reference/tools`. The mathematical classification below was made independently from the frozen source and supplied operational semantics.

The final judgment is PASS/LEGIT. The four local rules are genuinely definitional branches of a fresh result summary, so the independently determined domain-lemma set is empty. Stage 4 correctly generates no obligations and no theorem target.

## Immutable provenance and producer identity

Before judging Stage 4, I hashed the exact generation-time producer sources:

- `klean_export.py`: `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b`
- `klean.py`: `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`

These equal the `exporter_sha256` and `klean_py_sha256` in `generator-manifest.json` and the `files` entries in `/reference/generation-tools/source-manifest.json`. The producer bundle contains exactly those two files plus the source manifest. Its trusted `pipeline_contract.sha256_tree` is `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`, exactly the launcher-recorded producer-bundle hash.

The immutable generator image ID is `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`. It agrees in generator provenance, the producer source manifest, and the basename of the generation-producer path recorded in `/audit-input.json`.

I independently recomputed every launcher-recorded mounted artifact/tree hash:

| Artifact | Recomputed hash | Result |
|---|---|---|
| Stage 1 workspace, pipeline tree | `8df25ec66e3431da41021a468a988034e71beecd66df60d65f04db03ee3d0d37` | match |
| Stage 1 exported tree | `5af15dab0d5e0a6edfaa9cd7937b6f7391b760ca38e4a5628571f0e8761f31a2` | match |
| Selected Stage 2 audit tree | `586409297f782c65a8a3c275db72ee7d637d8822f66a6f6a77b27575e75d6cdf` | match |
| Protected Stage 3 file | `608d1a5cf80908fa99b1147aa71fc764f7731132eee2a71138c4b722ef483870` | match |
| Selected Stage 4 tree | `d1695c5813e56b72bdf45d4133e1c0d8d65565a59fd21a7eb11bc2cc55d1b53c` | match |
| Generated Lean tree | `251fbcdd494eab5705705629ca85dc8ca9eca6f9eb6c23acccd7865ca0cdd8af` | match |
| Producer source bundle | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` | match |

All 769 individual Stage 1 regular-file hashes recorded in `/audit-input.json` also match, with no missing, extra, or changed entries. The Stage 5 hashes are correctly `null`.

Evidence: `evidence/00-producer-provenance.txt`, `evidence/04-integrity-results.json`, and the complete rerunnable checker `evidence/verify_integrity.py`.

## Rule inventory reconstruction and bijection

Running `tools.k_rule_inventory.inventory_verification` against the frozen `/reference/k-proof` selected module `VERIFICATION`. Its local verification-file closure contains only that module. The frozen `verification.k` SHA-256 is `4c46f42d047210c45238c9a388253b00d3425c908156774797ae053c9092441d`.

The trusted inventory reconstructed exactly four rules:

| Order | Span | Normalized hash / source identity | Attributes |
|---|---:|---|---|
| 1 | 10–11 | `05e369c2e0f0a26d0d7e674102a669feb198db11697b02b0e440dae13cd6c789` | none |
| 2 | 13–15 | `18311e31edf98c4536c300005037838e4651a7b61c9d5624cbb197cfddea4789` | none |
| 3 | 17–20 | `c368375f7e518bf5b5f01ece3f7c41709c726a6ea30af9bebc2373407ae0c2c9` | none |
| 4 | 22–25 | `958329aed53dacc63f3d6c9422ab4eea2c1be9b87f0cbe409620d2734fa18f44` | none |

Each `source_rule_id` is `rule-` followed by the displayed normalized hash. The canonical whole-inventory hash is `360e01670f3b99020548a8895a06b99e29352f5581ab4741bdfafc1dec0ce0da`.

The protected Stage 3 manifest has the same inventory hash and the same four identities in the same order. There are no duplicate identities, omissions, extra rules, changed normalized hashes, reordered rules, or unaccounted classifications. `lemma_discovery_contract.validate_trust_boundary` independently accepted the bijection and enriched each manifest entry with the exact reconstructed text, span, module, attributes, and normalized hash.

Evidence: `evidence/01-inventory-command.txt` and `evidence/01-reconstructed-inventory.json`.

## Independent classification and mathematical judgment

The source declares the fresh symbol:

`syntax Int ::= chooseNumSpec(Int, Int) [function, total]`

The four inventory rules are guarded equations for this symbol. They do not match an MPY source AST constructor, a K-cell item, a call or continuation, or an operational configuration. The frozen program continues to execute through the supplied `Call`, name lookup, argument binding, `If`, integer comparison/arithmetic, return, and frame-pop rules. No inventory rule can replace, accelerate, preempt, or observe one of those execution steps, and none reads or writes any cell.

The independent classifications are:

1. Lines 10–11: `DEFINITION`. It defines the summary as `-1` when `X > Y`.
2. Lines 13–15: `DEFINITION`. It defines the summary as `Y` when the interval is nonempty and `Y` is even.
3. Lines 17–20: `DEFINITION`. It defines the summary as `Y-1` when `Y` is odd and that predecessor remains at least `X`.
4. Lines 22–25: `DEFINITION`. It defines the summary as `-1` in the remaining odd-endpoint case.

These guards are pairwise disjoint and exhaustive over integers: `X > Y` versus `X <= Y`; then zero versus nonzero `pyMod(Y,2)`; then `Y-1 >= X` versus `Y-1 < X`. The supplied semantics defines integer `%` through `pyMod`; with divisor 2, the parity branch agrees with Python for every relevant positive endpoint.

The equations reproduce the exact source branches and the HumanEval postcondition. If `Y` is even, it is the largest even endpoint. If `Y` is odd, `Y-1` is the largest possible even integer and is returned exactly when it lies in the interval. Otherwise no even candidate exists. Boundary cases `(13,12)`, `(12,14)`, `(12,15)`, and `(13,13)` distinguish all four branches. Counterfactual changes to the parity test, predecessor, or range guards change a source outcome.

Therefore none is an `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`. No rule is marked `simplification`, so the simplification-class restriction is satisfied vacuously. The equations name the program's branch-result summary; they do not independently assume an evenness, maximality, or existence theorem. The protected `DEFINITION` labels are correct and the true domain-lemma set is genuinely empty.

Evidence: `evidence/02-independent-classification.md`.

## Stage 4 structural integrity, obligations, and target identity

The generated `input-manifest.json` contains the same four definitions, in inventory order, with exact reconstructed source spans, text, IDs, and normalized hashes. Its `source_rules` domain list is empty. The generated `obligation-map.json` contains:

- `source_rules: []`
- `obligations: []`
- `trust_parameters: []`

The obligation-map hash is `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`, matching the generator manifest. The exporter result and generator manifest both record obligation count zero. Thus the source-rule/obligation bijection is exactly the empty bijection: there can be no omission, duplicate, irrelevant or weakened obligation, or vacuous conjunct.

The generator manifest's fixed target is `null`. Independently calling `tools.klean_export.target_statement` on the generated project also returns `null`; `Klean102ChooseNum/Lemmas.lean` contains an empty namespace and no generated proposition. There is no changed, duplicated, weakened, or vacuous theorem target.

The trust inventory records 41 generated data/function hook declarations and zero designated or other sorries. The preflight's independent proposition-trust gate accepted them; no proposition or proof is assumed. Since there is no target theorem, no proof depends on these declarations in this audit mode.

## Required preflight and clean generated build

I invoked `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the required frozen Stage 1 workspace, protected discovery manifest, selected generation, and pinned toolchain lock.

The first invocation exposed an audit-container infrastructure issue before any project checking: Lean attempted `readlink("/proc/8/exe")`, but the mounted `/proc` did not expose the namespace PID and returned `ENOENT`. A narrow local `LD_PRELOAD` shim redirected only numeric `/proc/<pid>/exe` lookups to `/proc/self/exe`, restoring the kernel's intended self-executable lookup. It did not alter any input, generated file, Lean source, compiler, checker, or proof rule. With the shim, Lean reported version 4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the lock.

The unchanged trusted checker then returned:

- status `KLEAN_NO_OBLIGATIONS`
- `lake clean`: exit 0, empty output
- `lake build`: exit 0; all seven Klean modules built and Lake reported success
- frozen input hash `5af15d…31a2`
- Stage 3 hash `608d1a…3870`
- generated tree hash `251fbc…d8af`
- obligation count 0
- target `null`
- designated sorry count 0

The checker also snapshotted and rechecked the read-only inputs after its fresh copied build, so no mounted input changed.

Evidence: `evidence/03-preflight-command.txt`, `evidence/03-preflight-result.json`, `evidence/03-preflight-build.log`, and `evidence/proc_self_exe_shim.c`.

## Deterministic reproduction

As an additional independent check, I loaded `/reference/generation-tools/klean_export.py`, explicitly bound it to the exact `/reference/generation-tools/klean.py`, and regenerated Stage 4 under `/tmp/audit-work` with the frozen inputs, pinned lock, problem ID, and recorded generator image ID.

The reproduction returned the same Stage 1 hash, Stage 3 hash, `KLEAN_NO_OBLIGATIONS` status, obligation count zero, trust-inventory hash, and generated-tree hash. `diff -qr` found the selected and reproduced generated projects byte-identical. `generator-manifest.json`, `trust-inventory.json`, and `export-result.json` are also byte-identical.

The only non-byte-identical sidecar is `input-manifest.json`, solely because its 25 `required_k_files` strings preserve the absolute input mount prefix: `/frozen-k` in the immutable generator image and `/reference/k-proof` in this audit mount. The relative files and order are identical, and every content hash, rule record, classification, obligation, trust entry, target, and generated Lean byte is unchanged. This is recorded explicitly rather than hidden as an alleged exact full-sidecar match.

Evidence: `evidence/05-stage4-reproduction-command.txt` and `evidence/05-stage4-reproduction-compare.txt`.

## Stage 5 applicability and final legitimacy

`AUDIT_MODE=CLASSIFICATION_ONLY`, the independently established domain set is empty, the selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`, the fixed target is absent, and `/candidate` does not exist. This is exactly the required no-Stage-5 state. Creating a `Base` copy, building a proof candidate, printing `Proof.final` axioms, or checking target parameters would invent a proof stage that the launcher correctly did not select.

The Stage 3 classification is complete and mathematically faithful; Stage 4 preserves its provenance and produces exactly the required empty obligation/target set. No proof verdict relies on a prior audit label, a generated vacuity, an operational bridge, or an unrecorded trust escape.

VERDICT: PASS
LEGITIMACY: LEGIT
