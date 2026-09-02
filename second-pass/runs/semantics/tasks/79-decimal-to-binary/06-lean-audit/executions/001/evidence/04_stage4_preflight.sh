#!/usr/bin/env bash
set -euo pipefail

export ELAN_HOME=/opt/elan
export LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so

echo '$ export ELAN_HOME=/opt/elan'
echo '$ export LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so'
echo '$ PYTHONPATH=/reference python3 - <<PY  # tools.klean_preflight.check_generation'
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
assert result["status"] == "PASS"
assert result["obligation_count"] == 1
print("FRESH_STAGE4_PREFLIGHT = PASS")
PY
