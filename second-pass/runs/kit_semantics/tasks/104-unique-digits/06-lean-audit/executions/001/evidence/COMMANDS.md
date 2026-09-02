# Audit commands

All commands ran from `/audit-output`. Corresponding complete captured output is in the named log.

## Context and mounted inputs

```bash
printf 'AUDIT_MODE=%s\n' "$AUDIT_MODE"
sha256sum /audit-input.json
sed -n '1,260p' /audit-input.json
find /reference -maxdepth 2 -mindepth 1 -printf '%y %p\n' | sort
find /candidate -maxdepth 3 -printf '%y %p\n' 2>&1 | sort
```

Result: `00_context.log`.

## Producer identity (performed before Stage 4 judgment)

```bash
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/lemma-discovery.json
sed -n '1,260p' /reference/generation-tools/source-manifest.json
sed -n '1,360p' /reference/klean-generation/generator-manifest.json
```

Results: `01_producer_and_generator_manifests.log` and `01b_producer_and_generator_manifests.log`.

```bash
sha256sum \
  /reference/tools/klean_export.py \
  /reference/tools/klean.py \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools import klean_export, pipeline_contract; paths=["/reference/generation-tools","/reference/k-proof","/reference/klean-generation","/reference/klean-generation/generated"]; [(print(p, "klean_export.tree_digest", klean_export.tree_digest(Path(p))), print(p, "pipeline_contract.sha256_tree", pipeline_contract.sha256_tree(Path(p)))) for p in paths]'
```

Result: `06_independent_tree_hashes.log`.

## Frozen source and trusted rule inventory

```bash
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/prove.sh
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/prompt.py
sed -n '1,520p' /reference/lemma-discovery.json
```

Result: `04_frozen_source_and_discovery.log`.

```bash
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

Result: `05_reconstructed_inventory.log`.

## Trusted deterministic-generation preflight

The first invocation exposed the audit sandbox's PID-namespace problem and exited 1:

```bash
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; evidence=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(evidence, indent=2, sort_keys=True))'
```

Result: `07_fresh_check_generation.log`.

The environment diagnosis and minimal self-executable lookup shim are recorded in `08_toolchain_diagnosis.log` through `23_shim_build_and_toolchain_test.log`, plus `proc_self_exe_shim.c` and `proc_self_exe_shim.so`. The successful unchanged-checker invocation was:

```bash
LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LAKE_OVERRIDE_LEAN=true \
LD_PRELOAD=/audit-output/evidence/proc_self_exe_shim.so \
PYTHONPATH=/reference \
python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; evidence=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(evidence, indent=2, sort_keys=True))'
```

Result: `24_fresh_check_generation_configured.log`; returned JSON: `preflight-return.json`.

## Independent structural, bijection, and target checks

```bash
PYTHONPATH=/reference python3 /audit-output/evidence/independent_structural_checks.py
```

Result: `26_independent_structural_checks.log` (`ALL_STRUCTURAL_CHECKS_PASS`).

```bash
for AUDIT_FILE in \
  input-manifest.json generator-manifest.json export-result.json \
  trust-inventory.json generated/obligation-map.json
do
  sha256sum "/reference/klean-generation/$AUDIT_FILE"
  sed -n '1,620p' "/reference/klean-generation/$AUDIT_FILE"
done
find /reference/klean-generation/generated -type f -printf '%P\n' | sort
rg -n 'theorem KLeanTarget|def KLeanTarget|KLeanTarget|sorry|admit|unsafe|^\s*(axiom|opaque)\s+' \
  /reference/klean-generation/generated || true
```

Result: `25_stage4_sidecars_and_target_scan.log`.

## Operational-semantics and finite summary checks

```bash
rg -n 'collect\(|appendCandidate\(|integerVals\(|scanBad\(|scanNumber\(|afterNumber\(|afterBad\(|afterValue\(' \
  /reference/k-proof/verification.k /reference/k-proof/spec.k \
  /reference/k-proof/reference-semantics /reference/k-proof/solution.py
```

Result: `27_summary_usage_and_semantics_index.log`. Relevant operational rules are captured with line numbers in `28_relevant_operational_semantics.log`.

```bash
python3 /audit-output/evidence/summary_semantic_checks.py
```

Result: `29_summary_semantic_checks.log` (`ALL_SUMMARY_SEMANTIC_CHECKS_PASS`).
