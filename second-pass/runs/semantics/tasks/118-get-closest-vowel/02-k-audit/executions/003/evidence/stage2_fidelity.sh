#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction || exit 90

printf '%s\n' 'COMMAND: python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy'
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
translate_status=$?
printf 'EXIT: %s\n' "$translate_status"

printf '%s\n' 'COMMAND: cmp solution.regenerated.mpy solution.mpy'
cmp solution.regenerated.mpy solution.mpy
cmp_status=$?
printf 'EXIT: %s\n' "$cmp_status"

printf '%s\n' 'COMMAND: sha256sum solution.regenerated.mpy solution.mpy'
sha256sum solution.regenerated.mpy solution.mpy
hash_status=$?
printf 'EXIT: %s\n' "$hash_status"

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
differential_status=$?
printf 'EXIT: %s\n' "$differential_status"

if (( translate_status != 0 || cmp_status != 0 || hash_status != 0 || differential_status != 0 )); then
  exit 1
fi
exit 0
