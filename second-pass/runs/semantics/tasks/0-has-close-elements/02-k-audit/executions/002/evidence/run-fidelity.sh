#!/usr/bin/env bash
set -uo pipefail

LOG=/audit-output/evidence/02-fidelity.log
exec > >(tee "$LOG") 2>&1

run() {
  echo "\$ $*"
  "$@"
  local status=$?
  echo "[exit $status]"
  return 0
}

echo '$ python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/case/regenerated-solution.mpy'
python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/case/regenerated-solution.mpy
status=$?
echo "[exit $status]"

run cmp -s /candidate/solution.mpy /tmp/audit-work/case/regenerated-solution.mpy
run sha256sum /candidate/solution.py /candidate/solution.mpy /tmp/audit-work/case/regenerated-solution.mpy
run python3 -m py_compile /tmp/audit-work/case/solution.py /tmp/audit-work/case/canonical.py
run python3 /audit-output/evidence/differential.py
run sha256sum /audit-output/evidence/differential.py /audit-output/evidence/differential-inputs.json
