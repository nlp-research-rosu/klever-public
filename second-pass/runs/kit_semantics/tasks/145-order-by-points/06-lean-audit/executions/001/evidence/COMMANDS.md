# Primary audit commands

All commands ran with working directory `/audit-output`. The numbered evidence
files contain their stdout/stderr. Mounted candidate and provenance scripts were
not executed.

```sh
env | rg '^AUDIT_MODE='
sed -n '1,260p' /audit-input.json
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
python3 -m json.tool /reference/generation-tools/source-manifest.json
python3 -m json.tool /reference/klean-generation/generator-manifest.json
```

```sh
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(inventory_verification(Path('/reference/k-proof')))
PY
```

```sh
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.lemma_discovery_contract import validate_trust_boundary
print(validate_trust_boundary(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
))
PY
```

The first mandated preflight attempt (evidence `09`) used the exact command
below and failed because Lean's numeric `/proc/<pid>/exe` lookup returned
`ENOENT` in the container's mismatched PID/proc namespaces:

```sh
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

Evidence `17` records the failing path and `18` verifies the narrow
`/proc/<digits>/exe` to `/proc/self/exe` compatibility interposer. The successful
unchanged preflight (evidence `19`) was:

```sh
LD_PRELOAD=/tmp/audit-work/lean_proc_self_compat.so \
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

The independent hash, category transport, obligation bijection, and target
cross-check is preserved verbatim in `21_independent_stage4_crosscheck.txt`.
