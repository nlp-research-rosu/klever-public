# Audit command index

All mounted candidate/provenance artifacts were read as data. Only trusted
modules below `/reference/tools` were imported. The generated Lean project was
built only through the explicitly required trusted preflight.

## Producer provenance

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.pipeline_contract import sha256_tree; print(sha256_tree(Path("/reference/generation-tools")))'
python3 -m json.tool /reference/generation-tools/source-manifest.json
```

Results: `01_context_producer_manifests.log`,
`03_generation_source_manifest.log`, and
`04_generation_tools_tree_hash.log`.

## Canonical Stage 3 inventory and structural validation

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")), indent=2, sort_keys=True))'
```

Results: `05_reconstructed_rule_inventory.log` and
`15_trusted_stage3_structural_validation.log`. Frozen source and relevant
operational rules are in `06_frozen_core_sources.log` and
`07_relevant_operational_semantics.log`.

## Required Stage 4 preflight

Initial command (result in `08_rerun_klean_preflight.log`):

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; print(json.dumps(check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")), indent=2, sort_keys=True))'
```

The initial call exposed a container PID-namespace incompatibility in Lean's
application-path lookup. The narrow compatibility source and before/after Lean
version results are in `11_lean_proc_compat_diagnosis.log`. It was compiled as:

```sh
cc -shared -fPIC -o /tmp/audit-work/lean_proc_compat.so \
  /tmp/audit-work/readlink_probe.c -ldl
```

Successful exact rerun (result in
`10_rerun_klean_preflight_with_proc_compat.log`):

```sh
LD_PRELOAD=/tmp/audit-work/lean_proc_compat.so PYTHONPATH=/reference \
  python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; print(json.dumps(check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")), indent=2, sort_keys=True))'
```

The shim redirects only `/proc/<digits>/exe` reads to `/proc/self/exe`; it does
not modify the generated project, source inputs, theorem data, or Lean logic.

## Independent hashes, bijection, target, and recurrence checks

```sh
PYTHONPATH=/reference python3 \
  /audit-output/evidence/verify_audit_hashes.py
python3 /audit-output/evidence/check_vowels_tail_recurrence.py
```

Results: `13_independent_hash_and_bijection_checks.log` and
`14_recurrence_and_counterfactual_checks.log`. The scripts themselves are
preserved beside this file. Stage 4 obligation, target, export, and trust data
are in `12_stage4_obligation_and_target_artifacts.log`.
