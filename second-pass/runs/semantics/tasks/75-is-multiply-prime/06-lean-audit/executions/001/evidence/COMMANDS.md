# Commands used

The command outputs are stored in the numbered evidence files. Material
commands were:

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json
```

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

The first preflight command reached `lake clean` and exposed the audit
container's `/proc/<pid>/exe` namespace mismatch. After compiling the narrow
compatibility shim preserved at
`/tmp/audit-work/proc_self_exe_compat.c`, the same trusted check was rerun:

```sh
LD_PRELOAD=/tmp/audit-work/proc_self_exe_compat.so \
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/independent_integrity_checks.py
```

The successful preflight internally ran these commands in its fresh temporary
copy:

```sh
lake clean
lake build
```
