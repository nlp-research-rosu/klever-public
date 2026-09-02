#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/52-below-threshold
echo 'COMMAND: python3 py2mpy.py solution.py > regenerated-solution.mpy'
(
  cd "$scratch" || exit 72
  python3 py2mpy.py solution.py > regenerated-solution.mpy
)
translate_status=$?
echo "TRANSLATE_EXIT=$translate_status"

echo 'COMMAND: cmp -s regenerated-solution.mpy submitted-solution.mpy'
cmp -s "$scratch/regenerated-solution.mpy" "$scratch/submitted-solution.mpy"
cmp_status=$?
echo "BYTE_IDENTITY_CMP_EXIT=$cmp_status"

echo 'HASHES: regenerated then submitted'
sha256sum "$scratch/regenerated-solution.mpy" "$scratch/submitted-solution.mpy"

if (( translate_status != 0 || cmp_status != 0 )); then
  echo 'EXIT_STATUS=1'
  exit 1
fi
echo 'EXIT_STATUS=0'
