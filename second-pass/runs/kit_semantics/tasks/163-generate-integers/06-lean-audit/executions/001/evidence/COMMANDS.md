# Decisive audit commands

The scripts named below are stored beside their corresponding raw logs. All
mounted candidate/provenance inputs were read-only. No mounted script was run.

## Producer and mounted-input hashes

```bash
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
PYTHONPATH=/reference python3 \
  /audit-output/evidence/31-verify-recorded-hashes.py
```

Results: `09-producer-sha256.txt` and `31-verify-recorded-hashes.log`.

## Canonical inventory and Stage 3 structural contract

```bash
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(json.dumps(inventory_verification(Path('/reference/k-proof')),
                 indent=2, sort_keys=True))
PY
```

The analogous Stage 3 command called
`tools.lemma_discovery_contract.validate_trust_boundary`, then independently
compared the canonical and manifest ID lists for exact order and uniqueness.
Results: `21-reconstructed-inventory.json` and
`22-stage3-contract-and-order-check.txt`.

## Required Stage 4 preflight

The exact checker call was:

```bash
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.klean_preflight import check_generation
print(check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
))
PY
```

The first run failed before elaboration because Lake could not use the
sandbox-hidden `/proc/<own-pid>/exe`; see `32-check-generation.log`. Explicit
Lean/Lake installation roots advanced to the same child-Lean failure; see
`68-check-generation-rerun.log`. The recorded shim in
`79-lean-app-path-shim-source.txt` redirects only the hidden self-PID path to
the equivalent available `/proc/self/exe`. The successful unchanged checker
invocation was:

```bash
lean_root=/opt/elan/toolchains/leanprover--lean4---v4.22.0
LEAN_SYSROOT="$lean_root" \
LAKE_HOME="$lean_root/src/lean/lake" \
LD_PRELOAD=/tmp/audit-work/lean-app-path-shim.so \
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

Complete returned evidence and exit status: `81-check-generation-final.log`
and `81-check-generation-final.status`.

## Independent Stage 4 and mathematical sensitivity checks

```bash
PYTHONPATH=/reference python3 \
  /audit-output/evidence/91-independent-stage4-gate.py
python3 /audit-output/evidence/92-classification-witnesses.py
```

Results: `91-independent-stage4-gate.log` (35/35 checks pass) and
`92-classification-witnesses.log` (289 finite comparisons, zero mismatches;
all six counterfactuals rejected).
