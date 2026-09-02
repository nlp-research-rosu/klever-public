#!/usr/bin/env bash
set -u

cd /tmp/audit-work/fresh

printf '%s\n' \
  'COMMAND: python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy'
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
translation_status=$?
printf 'EXIT: %s\n' "$translation_status"
if [[ "$translation_status" -ne 0 ]]; then
  exit "$translation_status"
fi

printf '%s\n' \
  'COMMAND: cmp -s solution.regenerated.mpy /candidate/solution.mpy'
cmp -s solution.regenerated.mpy /candidate/solution.mpy
comparison_status=$?
printf 'EXIT: %s\n' "$comparison_status"
if [[ "$comparison_status" -ne 0 ]]; then
  diff -u /candidate/solution.mpy solution.regenerated.mpy
  exit "$comparison_status"
fi

sha256sum solution.regenerated.mpy /candidate/solution.mpy
printf '%s\n' \
  'TRANSLATION_BYTE_IDENTITY=PASS'

printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/stage2_differential.py'
python3 /audit-output/evidence/stage2_differential.py
differential_status=$?
printf 'EXIT: %s\n' "$differential_status"
exit "$differential_status"
