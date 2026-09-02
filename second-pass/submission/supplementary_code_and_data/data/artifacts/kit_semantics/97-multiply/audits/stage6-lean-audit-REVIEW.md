# Independent Stage 3–5 audit: `97-multiply`

## Scope and conclusion

I independently audited HumanEval `97-multiply`, condition `kit-semantics`, with supplied MPY semantics. The launcher and `AUDIT_MODE` both record `CLASSIFICATION_ONLY`; `/candidate` is absent. The selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`.

That status is mathematically justified. The local verification-module closure contains no rules at all, so its true `DOMAIN_LEMMA` set is empty. The frozen source function computes exactly the expression in the K postcondition through ordinary supplied operational rules. Stage 4 preserves the empty source-rule/obligation bijection, emits no target, and has no Stage 5 candidate.

All mounted candidate and provenance material was treated as untrusted evidence. I executed only the trusted `/reference/tools` checks, independently authored audit scripts, and the clean generated-project build performed by the required preflight.

## Integrity and producer authentication

The signed resolution envelope recomputes to `af5f69d611a2d9861fd106a4f8f246ed3f313b332181c2f09180f1d56be0242e`. Independent tree/file recomputation matched every resolution hash checked, including:

| Artifact | Recomputed and recorded SHA-256 |
|---|---|
| Stage 1 selected workspace tree | `545c57965af135a2cb4855762f5887a73da6b9dfb931f9e3286d880e23aeeed0` |
| Stage 1 deterministic-export tree | `28b214b60749af21b998246bce7bf4816d641a3f7366ce6534e23124462f8fcf` |
| Stage 2 audit tree | `e71a72b630bd7e9d83e6b9d28406913bca452d0eb17c35e7d07977b0cecd2abe` |
| Protected Stage 3 manifest | `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3` |
| Selected Stage 4 generation tree | `65e7841d4950b23fb88aefd0b31f4666286fc9381058d0001c82c4a6820bd332` |
| Generated Lean project tree | `c3ef93c63914542bad8344259c2532a4dce8324f4ea9ab4969210249be228279` |
| Stage 4 producer-source bundle | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |

The complete 788-entry Stage 1 regular-file hash map also matches `/audit-input.json` exactly.

Before judging Stage 4, I hashed the two mounted producer files:

- `klean_export.py`: `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`: `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

Both hashes match `generator-manifest.json` and `source-manifest.json`. The bundle contains exactly those files plus the source manifest. Generator image ID `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` matches the generator manifest, source manifest, and the producer-bundle path recorded in `/audit-input.json`. The generator toolchain object exactly matches `/reference/klean-toolchain.lock.json`. There is therefore no producer-source infrastructure error.

## Inventory reconstruction and Stage 3 classification

Using the trusted canonical inventory implementation on frozen `/reference/k-proof/verification.k`, I reconstructed:

- verification file SHA-256: `ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`;
- verification main module: `VERIFICATION`;
- local verification-module closure: `["VERIFICATION"]`;
- ordered rule inventory: `[]`; and
- canonical inventory SHA-256: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.

`verification.k` only requires the supplied semantics and imports `MPY`; it declares no local `rule`. Rules belonging to the supplied fixed semantics are not proof-local extensions in the local verification-module closure.

The protected Stage 3 manifest has the same schema version, inventory hash, and empty ordered rule list. The comparison is bijective: zero canonical entries and zero classified entries, with no omitted, duplicated, extra, reordered, or hash-altered identity. With no entries, there are no source spans, normalized rule hashes, or `source_rule_id` values to disagree. The validated classification partitions for `DEFINITION`, `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, and `DOMAIN_LEMMA` are all empty. There are likewise no `simplification` rules to misclassify.

My independent reclassification therefore also yields an empty domain set. This is not hiding a derived fact under another label: there is no proof-local rule of any category, and thus no claimed `PROVED_DERIVED_LEMMA` whose prior derivation would need validation.

## Mathematical and operational judgment

The frozen source is:

```python
def multiply(a, b):
    return (a % 10) * (b % 10)
```

The K claim starts from the exact closure body and requires the result `pyMod(A, 10) *Int pyMod(B, 10)` for arbitrary K integers `A` and `B`. The supplied operational semantics performs the relevant computation directly:

1. `Call` evaluates the named closure and arguments, creates the function frame, and binds `a` and `b`.
2. `Return` and `BinOp` are strict; `BinOp` evaluates operands left-to-right and dispatches to `applyBin`.
3. Integer `%` rewrites to the supplied `pyMod`, and integer `*` rewrites to K's `*Int`.
4. The return rule restores the caller frame with that computed value.

Consequently, the result expression follows from ordinary fixed execution. No summary theorem, recurrence, macro, named proof term, or source-specific domain fact is necessary or relevant. A separately authored arithmetic check compared the frozen source formula against the K `pyMod` postcondition on all 40,401 pairs in `[-100,100]^2`, including negative operands, and found zero mismatches. Large and negative witnesses also agree. Constant, identity, unmodded-product, and additive counterfactuals fail on discriminating examples. This finite test supports, but does not replace, the direct rule-level semantic comparison above.

## Deterministic Stage 4 and target identity

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` on the required frozen workspace, discovery manifest, generation directory, and pinned toolchain lock.

The first invocation exposed an audit-sandbox issue: Lean could not resolve its executable because the namespace PID had no corresponding `/proc/<pid>/exe`. Evidence records the installed pinned versions and the failure. I then used a narrow, recorded `LD_PRELOAD` compatibility shim that only answers `/proc/*/exe` `readlink` requests with the truthful immutable Lean/Lake executable path selected by the process name. It changes neither generated sources nor Lean semantics. With the exact pinned toolchain path and `LEAN_SYSROOT`, the unchanged preflight passed:

- `lake clean`: exit 0;
- `lake build`: exit 0 and reported `Build completed successfully`;
- frozen Stage 1 hash: unchanged;
- protected discovery hash: unchanged;
- generated tree hash: unchanged;
- obligation count: 0;
- target: `null`; and
- status: `KLEAN_NO_OBLIGATIONS`.

I also checked the Stage 4 structure independently of the preflight result:

- `input-manifest.json` records empty definitions, operational rules, proved-derived lemmas, and domain source rules.
- `obligation-map.json` has the exact zero-obligation shape: `source_rules: []`, `obligations: []`, and `trust_parameters: []`.
- Its SHA-256 matches `generator-manifest.json`.
- Generator, export, stored preflight, signed audit preflight, and selected status all agree on zero obligations and `KLEAN_NO_OBLIGATIONS`.
- The trust-inventory hash matches the export result; generated sources have no proof holes under the trusted preflight.
- Every target record in the generator manifest, preflight, and audit input is `null`.
- An independent scan of all seven generated Lean sources finds zero declarations named `targetStatement`; `Klean97Multiply/Lemmas.lean` contains only imports, explanatory comments, and an empty namespace.

Because the independently classified domain set is genuinely empty, there is no omitted, duplicate, weakened, irrelevant, or vacuous conjunct. The exact source-rule/obligation bijection is empty-to-empty, and no fixed target exists to be changed.

## Stage 5 applicability and trust

Stage 5 is correctly absent. The audit input has `lean_workspace: null`, `lean_invocation: null`, `stage5_result: null`, and `target: null`; `/candidate` does not exist. Therefore a `Base` copy, candidate clean build, `#print axioms Proof.final`, candidate shadowing scan, proof identity check, and operational-bridge parameter audit are inapplicable. Performing or accepting a Stage 5 proof here would itself violate the `KLEAN_NO_OBLIGATIONS` contract.

## Evidence

- [Material command ledger](/audit-output/evidence/COMMANDS.md)
- [Environment and mounted-file record](/audit-output/evidence/00_environment_and_files.txt)
- [Core frozen sources and manifests](/audit-output/evidence/02_core_sources_and_manifests.txt)
- [Independent hash recomputation](/audit-output/evidence/03_recomputed_integrity.txt)
- [Canonical inventory reconstruction](/audit-output/evidence/04_reconstructed_inventory.txt)
- [Initial preflight failure](/audit-output/evidence/05_rerun_preflight.txt)
- [Lean environment diagnosis](/audit-output/evidence/06_lean_environment_diagnosis.txt)
- [Elan diagnosis](/audit-output/evidence/07_elan_diagnosis.txt)
- [Compatibility shim source/build/test](/audit-output/evidence/08_lean_proc_shim_build_and_test.txt)
- [Successful required preflight rerun](/audit-output/evidence/09_rerun_preflight_with_proc_shim.txt)
- [Generated Lean sources](/audit-output/evidence/10_generated_lean_sources.txt)
- [Independent Stage 4 structure check](/audit-output/evidence/11_independent_stage4_check.txt)
- [Operational semantic trace sources](/audit-output/evidence/12_operational_semantics_trace_sources.txt)
- [Adversarial arithmetic examples](/audit-output/evidence/13_semantic_counterexamples.txt)
- [Name-lookup semantics](/audit-output/evidence/14_name_lookup_semantics.txt)
- [Raw producer SHA-256 output](/audit-output/evidence/15_raw_sha256s.txt)
- [Final consistency self-check](/audit-output/evidence/16_final_selfcheck.txt)

VERDICT: PASS
LEGITIMACY: LEGIT
