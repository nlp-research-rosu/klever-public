#!/usr/bin/env bash
set -uo pipefail

echo 'COMMAND: python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/regenerated-solution.mpy'
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
translate_status=$?
echo "EXIT_STATUS: $translate_status"

echo 'COMMAND: cmp /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate/solution.mpy'
cmp /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate/solution.mpy
compare_status=$?
echo "EXIT_STATUS: $compare_status"

echo 'COMMAND: sha256sum /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate/solution.mpy'
sha256sum /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate/solution.mpy
hash_status=$?
echo "EXIT_STATUS: $hash_status"

if (( translate_status != 0 || compare_status != 0 || hash_status != 0 )); then
  exit 1
fi
