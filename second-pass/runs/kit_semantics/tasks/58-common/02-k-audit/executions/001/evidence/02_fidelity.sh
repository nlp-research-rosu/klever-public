#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/58-common

echo 'COMMAND: python3 py2mpy.py solution.py > regenerated-solution.mpy'
python3 py2mpy.py solution.py > regenerated-solution.mpy
translate_status=$?
echo "EXIT: ${translate_status}"
sha256sum solution.mpy regenerated-solution.mpy

echo 'COMMAND: cmp -s solution.mpy regenerated-solution.mpy'
cmp -s solution.mpy regenerated-solution.mpy
cmp_status=$?
echo "EXIT: ${cmp_status}"
if [[ ${cmp_status} -eq 0 ]]; then
  echo 'BYTE_IDENTITY: yes'
else
  echo 'BYTE_IDENTITY: no'
  diff -u solution.mpy regenerated-solution.mpy
fi

echo 'COMMAND: python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
differential_status=$?
echo "EXIT: ${differential_status}"

if [[ ${translate_status} -ne 0 || ${cmp_status} -ne 0 || ${differential_status} -ne 0 ]]; then
  exit 1
fi
