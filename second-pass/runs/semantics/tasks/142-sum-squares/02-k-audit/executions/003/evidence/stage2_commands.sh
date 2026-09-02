#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence

cd "$scratch" || exit 90

echo 'COMMAND: python3 py2mpy.py solution.py > regenerated-solution.mpy'
python3 py2mpy.py solution.py > regenerated-solution.mpy
translate_status=$?
echo "TRANSLATE_EXIT_STATUS=$translate_status"

echo 'COMMAND: cmp -s regenerated-solution.mpy solution.mpy'
cmp -s regenerated-solution.mpy solution.mpy
cmp_status=$?
echo "TRANSLATION_BYTE_IDENTITY_EXIT_STATUS=$cmp_status"

echo 'COMMAND: sha256sum solution.mpy regenerated-solution.mpy'
sha256sum solution.mpy regenerated-solution.mpy
sha_status=$?
echo "SHA256_EXIT_STATUS=$sha_status"

echo 'COMMAND: python3 /audit-output/evidence/differential_test.py'
python3 "$evidence/differential_test.py"
differential_status=$?
echo "DIFFERENTIAL_EXIT_STATUS=$differential_status"

if (( translate_status != 0 || cmp_status != 0 || sha_status != 0 || differential_status != 0 )); then
  exit 1
fi
exit 0
