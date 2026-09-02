#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruction
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
translate_status=$?
printf 'trusted_translation_exit=%s\n' "$translate_status"
sha256sum solution.py solution.mpy regenerated-solution.mpy
cmp -s solution.mpy regenerated-solution.mpy
cmp_status=$?
printf 'submitted_vs_regenerated_mpy_cmp_exit=%s\n' "$cmp_status"
if [ "$cmp_status" -ne 0 ]; then
  diff -u solution.mpy regenerated-solution.mpy
fi

python3 /audit-output/evidence/02_differential.py
differential_status=$?
printf 'differential_exit=%s\n' "$differential_status"

if [ "$translate_status" -ne 0 ] || [ "$cmp_status" -ne 0 ] || [ "$differential_status" -ne 0 ]; then
  exit 1
fi
