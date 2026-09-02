#!/usr/bin/env bash
set -u

run() {
  echo "\$ $*"
  "$@"
  status=$?
  echo "[exit $status]"
  return "$status"
}

echo "== Trusted translator regeneration =="
echo "$ python3 /reference/py2mpy.py /tmp/audit-work/59-lpf/solution.py > /tmp/audit-work/59-lpf/reviewer-regenerated-solution.mpy"
python3 /reference/py2mpy.py /tmp/audit-work/59-lpf/solution.py \
  > /tmp/audit-work/59-lpf/reviewer-regenerated-solution.mpy
status=$?
echo "[exit $status]"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi
run cmp /tmp/audit-work/59-lpf/reviewer-regenerated-solution.mpy /candidate/solution.mpy
run sha256sum \
  /tmp/audit-work/59-lpf/reviewer-regenerated-solution.mpy \
  /candidate/solution.mpy

echo "== Python syntax and independent differential test =="
run env PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile /tmp/audit-work/59-lpf/solution.py
run env PYTHONDONTWRITEBYTECODE=1 python3 /audit-output/evidence/03_differential.py
