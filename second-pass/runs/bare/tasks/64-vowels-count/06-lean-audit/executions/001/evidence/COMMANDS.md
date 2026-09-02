# Audit command log

All paths below are the immutable mounted inputs or audit-local outputs. The
candidate/provenance scripts were read as evidence and were not executed.

## Launcher and manifests

```sh
printf "AUDIT_MODE=%s\n" "$AUDIT_MODE"
python3 -m json.tool /audit-input.json
python3 -m json.tool /reference/lemma-discovery.json
python3 -m json.tool /reference/klean-generation/generator-manifest.json
python3 -m json.tool /reference/generation-tools/source-manifest.json
```

Results: `00_launcher_and_mounts.txt` and `01_primary_manifests.txt`. The first
attempt also records that `jq` was unavailable; Python's standard JSON formatter
was then used.

## Frozen-source inspection

```sh
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/semantic.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/prompt.py
nl -ba /reference/k-proof/prove.sh
```

Result: `02_frozen_sources.txt`.

## Canonical inventory reconstruction

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/check_inventory.py
```

Exit: 0. Result: `03_inventory_reconstruction.txt`.

## Producer and all recorded hashes

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
PYTHONPATH=/reference python3 /audit-output/evidence/check_hashes.py
```

Exit: 0. Result: `04_hashes_and_producer_authentication.txt`.

## Trusted Stage 4 preflight

Initial exact rerun:

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result = check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Exit: 1. Result: `05_rerun_check_generation.txt`. Lake could not detect its
installation because Lean's `/proc/<namespace-pid>/exe` read failed in this
sandbox. Diagnostics are in `06_toolchain_diagnosis.txt`,
`07_lake_debug.txt`, and `08_rerun_check_generation_with_pinned_elan_home.txt`.

The narrow audit-local compatibility shim was compiled and tested:

```sh
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/readlink_self_shim.so \
  /audit-output/evidence/readlink_self_shim.c -ldl
sha256sum /audit-output/evidence/readlink_self_shim.c \
  /tmp/audit-work/readlink_self_shim.so
LD_PRELOAD=/tmp/audit-work/readlink_self_shim.so lean --version
LD_PRELOAD=/tmp/audit-work/readlink_self_shim.so lake clean
LD_PRELOAD=/tmp/audit-work/readlink_self_shim.so lake build
```

Exit: 0. Result: `09_toolchain_shim_and_test.txt`.

Successful exact preflight rerun:

```sh
LD_PRELOAD=/tmp/audit-work/readlink_self_shim.so \
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result = check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Exit: 0. Result: `10_successful_rerun_check_generation.txt`.

## Independent classification and Stage 4 checks

```sh
python3 /audit-output/evidence/check_semantic_relevance.py
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")), indent=2, sort_keys=True))'
PYTHONPATH=/reference \
  python3 /audit-output/evidence/check_stage4_zero_obligations.py
python3 -m json.tool \
  /reference/klean-generation/generated/obligation-map.json
rg -n -i "target|obligation|domain.?lemma|final" \
  /reference/klean-generation/generated --glob "*.lean" || true
```

Exits: 0 (the final `rg` had no matches, as expected). Results:
`11_obligation_map_and_target_absence.txt`,
`12_semantic_relevance_and_mutations.txt`,
`13_trusted_stage3_boundary_validation.txt`, and
`14_independent_stage4_zero_obligation_check.txt`.
