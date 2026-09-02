# Audit commands

The corresponding complete outputs are in the numbered `.log` files.

## Context and hashes

```sh
echo AUDIT_MODE="$AUDIT_MODE"
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/lemma-discovery.json \
  /reference/k-proof/verification.k
PYTHONPATH=/reference python3 -c '
from pathlib import Path
from tools.pipeline_contract import sha256_tree
print("generation_producer_sources_sha256",
      sha256_tree(Path("/reference/generation-tools")))
print("klean_generation_sha256",
      sha256_tree(Path("/reference/klean-generation")))
print("k_workspace_sha256",
      sha256_tree(Path("/reference/k-proof")))
'
```

Output: `00_context_and_producer_hashes.log`.

## Inventory reconstruction

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/inventory_audit.py
```

Output: `01_inventory_reconstruction.log`.

## Classification sources

```sh
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/reference-semantics/semantics/call.k |
  sed -n '18,32p;69,75p'
nl -ba /reference/k-proof/reference-semantics/semantics/core.k |
  sed -n '129,180p'
nl -ba /reference/k-proof/reference-semantics/semantics/functions.k |
  sed -n '62,91p'
nl -ba /reference/k-proof/reference-semantics/semantics/builtins.k |
  sed -n '12,42p'
nl -ba /reference/k-proof/reference-semantics/semantics/operators.k |
  sed -n '10,18p'
nl -ba /reference/k-proof/reference-semantics/semantics/set.k |
  sed -n '6,40p'
```

Output: `02_classification_sources.log`.

## Producer provenance

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/producer_provenance_audit.py
```

Output: `03_producer_provenance.log`.

## Trusted preflight

The initial command, preserved because it exposed the `/proc` namespace issue:

```sh
PYTHONPATH=/reference python3 -c '
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
'
```

Output: `04_preflight_rerun.log`.

Compile the environment-only `/proc/<pid>/exe` compatibility shim:

```sh
gcc -shared -fPIC \
  -o /tmp/audit-work/proc_exe_compat.so \
  /audit-output/evidence/proc_exe_compat.c \
  -ldl
```

Successful rerun of the same trusted checker:

```sh
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
PYTHONPATH=/reference \
python3 -c '
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
'
```

Output: `05_preflight_rerun_with_proc_compat.log`.

## Independent Stage 4 integrity

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/stage4_integrity_audit.py
```

Output: `06_stage4_integrity.log`.

## Generation-time zero-domain path

```sh
nl -ba /reference/generation-tools/klean_export.py |
  sed -n '770,975p;1038,1058p;1118,1134p;1218,1270p'
nl -ba /reference/generation-tools/klean.py |
  sed -n '322,370p;564,646p;680,739p'
nl -ba \
  /reference/klean-generation/generated/Klean54SameChars/Lemmas.lean
sed -n '1,120p' \
  /reference/klean-generation/generated/obligation-map.json
```

Output: `07_generation_zero_domain_path.log`.
