#!/usr/bin/env bash
set -euo pipefail

export ELAN_HOME=/opt/elan
export LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so

echo '$ PYTHONPATH=/reference python3 - <<PY  # tools.klean_final_gate.check_final'
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.klean_final_gate import check_final

result = check_final(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    Path("/candidate"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    audit_input=Path("/audit-input.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
assert result["status"] == "PASS"
assert result["used_axioms"] == []
print("FRESH_MECHANICAL_FINAL_GATE = PASS")
PY
