#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate || exit 90

printf '%s\n' '$ python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy'
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
translate_status=$?
printf 'EXIT: %s\n' "$translate_status"

printf '%s\n' '$ sha256sum solution.mpy solution.regenerated.mpy'
sha256sum solution.mpy solution.regenerated.mpy
hash_status=$?
printf 'EXIT: %s\n' "$hash_status"

printf '%s\n' '$ cmp solution.mpy solution.regenerated.mpy'
cmp solution.mpy solution.regenerated.mpy
cmp_status=$?
printf 'EXIT: %s\n' "$cmp_status"

printf '%s\n' '$ python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
diff_status=$?
printf 'EXIT: %s\n' "$diff_status"

if (( translate_status != 0 || hash_status != 0 || cmp_status != 0 || diff_status != 0 )); then
  exit 1
fi
