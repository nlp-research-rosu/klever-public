#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/159-eat

python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
translation_status=$?
echo "translation_exit=${translation_status}"

cmp -s solution.mpy regenerated-solution.mpy
identity_status=$?
echo "translation_byte_identity_exit=${identity_status}"

sha256sum solution.py solution.mpy regenerated-solution.mpy \
  /reference/prompt.py /reference/canonical.py /reference/py2mpy.py
hash_status=$?
echo "sha256sum_exit=${hash_status}"

python3 /audit-output/evidence/differential_test.py
differential_status=$?
echo "differential_exit=${differential_status}"

if (( translation_status != 0 || identity_status != 0 || hash_status != 0 ||
      differential_status != 0 )); then
  exit 1
fi
