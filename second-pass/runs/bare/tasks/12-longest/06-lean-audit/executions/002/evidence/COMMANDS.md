# Commands actually run

The corresponding complete outputs are in the numbered transcript files in
this directory.

```bash
PYTHONPATH=/reference python -c '
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(json.dumps(inventory_verification(Path("/reference/k-proof")),
                 indent=2, sort_keys=True))
'
```

```bash
PYTHONPATH=/reference python -c '
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

The first preflight attempt produced the failure saved in
`06_check_generation.txt`. Diagnosis established that the sandbox exposes
`/proc/self/exe` but not Lean 4.22's `/proc/<getpid>/exe` lookup. The local-only
shim was built and validated with:

```bash
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/proc-exe-shim.so \
  /tmp/audit-work/proc-exe-shim.c -ldl

LD_PRELOAD=/tmp/audit-work/proc-exe-shim.so lean --version
LD_PRELOAD=/tmp/audit-work/proc-exe-shim.so lean --print-prefix

cd /tmp/audit-work/lake-debug/project
LD_PRELOAD=/tmp/audit-work/proc-exe-shim.so lake clean
LD_PRELOAD=/tmp/audit-work/proc-exe-shim.so lake build
```

The trusted preflight was then rerun without changing its arguments or
callback:

```bash
LD_PRELOAD=/tmp/audit-work/proc-exe-shim.so \
PYTHONPATH=/reference \
python -c '
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

Hash reconstruction used the trusted hash functions appropriate to each
record:

```bash
PYTHONPATH=/reference python -c '
from pathlib import Path
from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree
print(tree_digest(Path("/reference/k-proof")))
print(sha256_tree(Path("/reference/k-proof")))
print(tree_digest(Path("/reference/klean-generation/generated")))
print(sha256_tree(Path("/reference/k-audit")))
print(sha256_tree(Path("/reference/klean-generation")))
'
```

Source inspection used:

```bash
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/semantic.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
```
