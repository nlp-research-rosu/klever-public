#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction

echo 'COMMAND: python3 /reference/py2mpy.py /tmp/audit-work/reconstruction/solution.py > /tmp/audit-work/reconstruction/solution.regenerated.mpy'
python3 /reference/py2mpy.py "$work/solution.py" > "$work/solution.regenerated.mpy"
translate_status=$?
echo "EXIT_STATUS: $translate_status"

echo 'COMMAND: cmp -s /tmp/audit-work/reconstruction/solution.regenerated.mpy /tmp/audit-work/reconstruction/solution.mpy'
cmp -s "$work/solution.regenerated.mpy" "$work/solution.mpy"
identity_status=$?
echo "EXIT_STATUS: $identity_status"

echo 'COMMAND: sha256sum /tmp/audit-work/reconstruction/solution.regenerated.mpy /tmp/audit-work/reconstruction/solution.mpy'
sha256sum "$work/solution.regenerated.mpy" "$work/solution.mpy"
hash_status=$?
echo "EXIT_STATUS: $hash_status"

echo 'COMMAND: python3 /audit-output/evidence/02_differential.py'
python3 /audit-output/evidence/02_differential.py
differential_status=$?
echo "EXIT_STATUS: $differential_status"

if (( translate_status != 0 || identity_status != 0 || hash_status != 0 || differential_status != 0 )); then
  exit 1
fi
exit 0
