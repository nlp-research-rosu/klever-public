#!/usr/bin/env bash
set -euo pipefail
trap 'status=$?; printf "[audit] exit_status=%s\n" "$status"' EXIT
set -x

krun /audit-output/evidence/off-domain-floor-division.mpy -cN=0 \
  --definition /tmp/audit-work/130-tri/build/concrete-kompiled

python3 - <<'PY'
print("python_floor_division_-1_by_2=", -1 // 2)
PY
