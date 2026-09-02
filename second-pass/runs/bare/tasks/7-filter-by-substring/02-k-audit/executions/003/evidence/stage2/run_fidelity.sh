#!/usr/bin/env bash
set -u

status=0
scratch=/tmp/audit-work/source

printf '%s\n' '$ python3 /reference/py2mpy.py /tmp/audit-work/source/solution.py > /tmp/audit-work/source/regenerated-solution.mpy'
python3 /reference/py2mpy.py "$scratch/solution.py" > "$scratch/regenerated-solution.mpy"
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

printf '%s\n' '$ cmp -s /candidate/solution.mpy /tmp/audit-work/source/regenerated-solution.mpy'
cmp -s /candidate/solution.mpy "$scratch/regenerated-solution.mpy"
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

printf '%s\n' '$ sha256sum /candidate/solution.mpy /tmp/audit-work/source/regenerated-solution.mpy'
sha256sum /candidate/solution.mpy "$scratch/regenerated-solution.mpy"
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

printf '%s\n' '$ python3 /audit-output/evidence/stage2/differential_test.py'
python3 /audit-output/evidence/stage2/differential_test.py
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

exit "$status"
