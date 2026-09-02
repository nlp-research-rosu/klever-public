#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate-src || exit 90

echo 'COMMAND: python3 /tmp/audit-work/reference/py2mpy.py solution.py > regenerated.mpy'
python3 /tmp/audit-work/reference/py2mpy.py solution.py > regenerated.mpy
regen_status=$?
echo "EXIT: ${regen_status}"

echo 'COMMAND: cmp -s regenerated.mpy solution.mpy'
cmp -s regenerated.mpy solution.mpy
cmp_status=$?
echo "EXIT: ${cmp_status}"

echo 'COMMAND: sha256sum regenerated.mpy solution.mpy'
sha256sum regenerated.mpy solution.mpy
hash_status=$?
echo "EXIT: ${hash_status}"

echo 'COMMAND: python3 /audit-output/evidence/differential.py'
python3 /audit-output/evidence/differential.py
differential_status=$?
echo "EXIT: ${differential_status}"

if [ "${regen_status}" -ne 0 ] || [ "${cmp_status}" -ne 0 ] \
   || [ "${hash_status}" -ne 0 ] || [ "${differential_status}" -ne 0 ]; then
  exit 1
fi
