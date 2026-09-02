#!/usr/bin/env bash
set -uo pipefail

cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/lean-app-path-shim.so \
  /audit-output/evidence/lean-app-path-shim.c
export LD_PRELOAD=/tmp/audit-work/lean-app-path-shim.so
export PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH

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
