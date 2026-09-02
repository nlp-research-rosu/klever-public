#!/usr/bin/env bash
set -euxo pipefail
gcc -shared -fPIC -O2 -Wall -Wextra -Werror \
  -o /tmp/audit-work/lean-proc-exe-shim.so \
  /audit-output/evidence/lean-proc-exe-shim.c \
  -ldl
sha256sum \
  /audit-output/evidence/lean-proc-exe-shim.c \
  /tmp/audit-work/lean-proc-exe-shim.so
export PATH="/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH"
export LD_PRELOAD=/tmp/audit-work/lean-proc-exe-shim.so
lean --version
lake --version
PYTHONPATH=/reference python3 - <<'PY'
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
PY
