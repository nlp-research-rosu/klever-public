#!/usr/bin/env bash
set -uo pipefail

cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/lean-app-path-shim.so \
  /audit-output/evidence/lean-app-path-shim.c
export LD_PRELOAD=/tmp/audit-work/lean-app-path-shim.so
export PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH

PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path

from tools.klean_final_gate import check_proof_candidate

result = check_proof_candidate(
    Path("/reference/klean-generation"),
    Path("/candidate"),
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
