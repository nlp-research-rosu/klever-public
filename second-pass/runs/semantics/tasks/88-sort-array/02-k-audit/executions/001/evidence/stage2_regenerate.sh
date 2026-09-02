#!/usr/bin/env bash
set -u

scratch_root=/tmp/audit-work/88-sort-array
cd "$scratch_root" || exit 2

python3 py2mpy.py solution.py > regenerated-solution.mpy
translate_status=$?
printf 'TRANSLATOR_EXIT: %s\n' "$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

cmp regenerated-solution.mpy submitted-solution.mpy
cmp_status=$?
printf 'SUBMITTED_VS_REGENERATED_CMP_EXIT: %s\n' "$cmp_status"
sha256sum regenerated-solution.mpy submitted-solution.mpy
if (( cmp_status != 0 )); then
  diff -u submitted-solution.mpy regenerated-solution.mpy
fi
exit "$cmp_status"
