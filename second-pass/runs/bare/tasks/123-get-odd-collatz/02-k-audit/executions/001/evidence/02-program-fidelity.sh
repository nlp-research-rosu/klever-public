#!/usr/bin/env bash
set -o pipefail

echo 'COMMAND: python3 trusted py2mpy.py candidate solution.py > regenerated.mpy'
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated.mpy
translate_rc=$?
echo "EXIT: $translate_rc"

echo 'COMMAND: cmp regenerated.mpy candidate solution.mpy'
cmp /tmp/audit-work/regenerated.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
cmp_rc=$?
echo "EXIT: $cmp_rc"

echo 'COMMAND: sha256sum regenerated.mpy candidate solution.mpy'
sha256sum \
  /tmp/audit-work/regenerated.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
hash_rc=$?
echo "EXIT: $hash_rc"

echo 'COMMAND: python3 /audit-output/evidence/02-differential.py'
python3 /audit-output/evidence/02-differential.py
differential_rc=$?
echo "EXIT: $differential_rc"

if (( translate_rc != 0 || cmp_rc != 0 || hash_rc != 0 || differential_rc != 0 )); then
  exit 1
fi
