# Principal audit commands

Raw results are in the numbered evidence files alongside this record.

```sh
printenv AUDIT_MODE
sha256sum /audit-input.json
rg --files /reference/k-proof /reference/k-audit /reference/klean-generation /reference/generation-tools /reference/tools /candidate
```

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json
```

```sh
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(json.dumps(inventory_verification(Path('/reference/k-proof')),
                 indent=2, sort_keys=True))
PY
```

```sh
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools import klean_export, pipeline_contract
# Recomputed pipeline tree hashes, export tree hashes, the protected manifest
# hash, and every one of the 774 Stage 1 per-file hashes.
PY
```

The direct preflight command was first run without compatibility variables and
failed before reading Lean source because this sandbox does not expose
`/proc/<getpid()>/exe`. The exact failure is preserved in
`06_klean_preflight_command_and_result.txt`.

The compatibility shim in `/tmp/audit-work/readlink-self-shim.c` changes only a
numeric `/proc/<pid>/exe` `readlink` request to `/proc/self/exe`. It was compiled
and tested with:

```sh
gcc -shared -fPIC -O2 -Wall -Wextra -Werror \
  -o /tmp/audit-work/readlink-self-shim.so \
  /tmp/audit-work/readlink-self-shim.c -ldl
LD_PRELOAD=/tmp/audit-work/readlink-self-shim.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
```

The unchanged trusted preflight was then rerun successfully:

```sh
LD_PRELOAD=/tmp/audit-work/readlink-self-shim.so \
LAKE_HOME=/tmp/audit-work/lake-install \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
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

```sh
rg -n -C 3 'syntax ValSeq|vCons|valSeqConcat|isRefV|applyBin|#loop|append|BinOp|For\(' \
  /reference/k-proof/reference-semantics/semantics \
  /reference/k-proof/reference-semantics/semantics.k
rg -n 'derivAcc|noRefsVS' /reference/k-proof \
  --glob '*.k' --glob '*.mpy' --glob '*.py'
```

```sh
PYTHONPATH=/reference python3 - <<'PY'
from tools.lemma_discovery_contract import validate_trust_boundary
from tools import klean_export
# Independently compared validated classes, source_rules, obligation IDs,
# obligation-map hashes, counts, trust parameters, and target_statement.
PY
```

```sh
nl -ba /reference/klean-generation/generated/Klean62Derivative.lean
nl -ba /reference/klean-generation/generated/Klean62Derivative/Lemmas.lean
rg -n 'KleanTarget|target|def .*Prop|theorem|lemma' \
  /reference/klean-generation/generated --glob '*.lean'
```
