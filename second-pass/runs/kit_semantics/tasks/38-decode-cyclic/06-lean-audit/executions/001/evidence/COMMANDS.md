# Key audit commands

All commands ran from `/audit-output`. Candidate and provenance text was treated
as data only; no scripts from those inputs were executed.

## Input and producer integrity

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /reference/lemma-discovery.json
```

Result: `03-producer-provenance.txt`.

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/check_integrity.py
```

Result: `17-integrity-check.txt` (`OVERALL=PASS`).

## Rule inventory and classification support

```sh
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(json.dumps(inventory_verification(Path('/reference/k-proof')),
                 indent=2, sort_keys=True))
PY
```

Result: `07-reconstructed-inventory.json`.

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/check_inventory_bijection.py
```

Result: `18-inventory-bijection.txt` (`OVERALL=PASS`).

```sh
python3 /audit-output/evidence/check_summary_semantics.py
```

Result: `35-summary-semantics-check.txt` (29,524 exhaustive finite cases,
zero mismatches, counterfactual identity/constant/wrong-rotation definitions
rejected on a three-code witness).

## Stage 4 preflight

The initial direct invocation was:

```sh
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.klean_preflight import check_generation
print(check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json')))
PY
```

Result: `19-klean-check-generation.txt`. It exposed a sandbox-specific Lean
failure: numeric `/proc/<pid>/exe` links are hidden even though
`/proc/self/exe` is available. The narrow compatibility shim and pinned Lean
version check are in `32-lean-proc-self-shim.txt`.

The successful rerun of the same trusted checker was:

```sh
LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so \
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'))
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

Result: `33-klean-check-generation-rerun.txt`, with exit 0,
`KLEAN_NO_OBLIGATIONS`, and successful `lake clean`/`lake build` diagnostics.
The returned JSON alone is `33-klean-check-generation-result.json`.

## Independent Stage 4 structure

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/check_stage4_structure.py
```

Result: `37-stage4-structure.txt` (`OVERALL=PASS`).
