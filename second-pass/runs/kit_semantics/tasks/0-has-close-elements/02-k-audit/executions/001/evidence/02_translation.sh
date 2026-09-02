#!/usr/bin/env bash
set -u
finish() {
  local rc=$?
  echo "SCRIPT_EXIT=$rc"
}
trap finish EXIT

echo "COMMAND: python3 /tmp/audit-work/reconstruction/py2mpy.py /tmp/audit-work/reconstruction/solution.py > /tmp/audit-work/reconstruction/solution.mpy"
python3 /tmp/audit-work/reconstruction/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/solution.mpy

echo "HASHES"
sha256sum \
  /tmp/audit-work/reconstruction/solution.py \
  /tmp/audit-work/reconstruction/solution.mpy \
  /candidate/solution.py \
  /candidate/solution.mpy

echo "BYTE_COMPARISON"
cmp -l /tmp/audit-work/reconstruction/solution.mpy /candidate/solution.mpy
rc=$?
if [[ "$rc" -eq 0 ]]; then
  echo "REGENERATED_SOLUTION_MPY_BYTE_IDENTICAL"
else
  echo "REGENERATED_SOLUTION_MPY_DIFFERS cmp_exit=$rc"
fi
exit "$rc"
