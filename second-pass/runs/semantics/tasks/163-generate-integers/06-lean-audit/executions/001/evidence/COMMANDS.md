# Audit command index

All mounted candidate and provenance inputs were treated as read-only data.
Only the trusted `/reference/tools` Python modules and the pinned Lean
toolchain were executed.

## Inventory reconstruction

```sh
PYTHONPATH=/reference python /audit-output/evidence/inventory_reconstruction.py
```

Result: exit 0. Full output is in
`inventory-reconstruction.log`.

## Signed inputs, producer provenance, and hashes

```sh
PYTHONPATH=/reference python /audit-output/evidence/hash_verification.py
```

Result: exit 0 with `all_checks True`. Full output is in
`hash-verification.log`.

## Stage 3/Stage 4 bijection and target check

```sh
PYTHONPATH=/reference python /audit-output/evidence/stage4_bijection.py
```

Result: exit 0. Full output is in `stage4-bijection.log`.

## Required Stage 4 preflight

The first direct invocation was:

```sh
PYTHONPATH=/reference python - <<'PY'
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

It reached `lake clean` but the sandbox prevented Lean 4.22 from resolving
its numeric `/proc/<pid>/exe` path. The exact failure is preserved in
`preflight-initial-error.log`.

The compatibility source `proc_self_exe_shim.c` redirects only matching
`/proc/<digits>/exe` readlink calls to `/proc/self/exe`. The successful
rerun was:

```sh
gcc -shared -fPIC -O2 -Wall -Wextra -Werror \
  -o /tmp/audit-work/proc_self_exe_shim.so \
  /audit-output/evidence/proc_self_exe_shim.c -ldl
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so lean --version
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so \
  PYTHONPATH=/reference \
  python /audit-output/evidence/run_preflight.py
```

Result: exit 0; pinned Lean commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`; both `lake clean` and
`lake build` exit 0; `KLEAN_NO_OBLIGATIONS`; target null. Full returned
evidence is in `preflight-success.log`.

## Independent semantic cross-check

```sh
python3 /audit-output/evidence/semantic_crosscheck.py
```

Result: exit 0, zero mismatches over 400 positive endpoint pairs, with four
counterfactual mutations rejected. Full output is in
`semantic-crosscheck.log`.

## Audit mode and candidate absence

The commands and exact output establishing `CLASSIFICATION_ONLY`, null Stage
5 fields, and an absent `/candidate` are in `mode-check.log`.
