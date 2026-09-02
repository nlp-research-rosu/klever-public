#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction

echo 'COMMAND: python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/reconstruction/regenerated-solution.mpy'
python3 /reference/py2mpy.py /candidate/solution.py > "$scratch/regenerated-solution.mpy"
translate_status=$?
echo "EXIT_STATUS: $translate_status"

echo 'COMMAND: cmp -s /candidate/solution.mpy /tmp/audit-work/reconstruction/regenerated-solution.mpy'
cmp -s /candidate/solution.mpy "$scratch/regenerated-solution.mpy"
identity_status=$?
echo "EXIT_STATUS: $identity_status"
if [[ $identity_status -eq 0 ]]; then
  echo 'BYTE_IDENTITY: YES'
else
  echo 'BYTE_IDENTITY: NO'
  cmp -l /candidate/solution.mpy "$scratch/regenerated-solution.mpy" | head -n 40
fi

echo 'COMMAND: sha256sum /candidate/solution.mpy /tmp/audit-work/reconstruction/regenerated-solution.mpy'
sha256sum /candidate/solution.mpy "$scratch/regenerated-solution.mpy"
hash_status=$?
echo "EXIT_STATUS: $hash_status"

echo 'COMMAND: python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
differential_status=$?
echo "EXIT_STATUS: $differential_status"

if [[ $translate_status -ne 0 || $identity_status -ne 0 || $hash_status -ne 0 || $differential_status -ne 0 ]]; then
  exit 1
fi
