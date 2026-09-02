#!/usr/bin/env bash
set -u

printf 'COMMAND: %q\n' "$0"
printf 'PWD_BEFORE: %s\n' "$PWD"
cd /tmp/audit-work/review/candidate-src
printf 'PWD_BUILD: %s\n' "$PWD"

printf 'COMMAND: python3 /tmp/audit-work/review/trusted/py2mpy.py solution.py > regenerated-solution.mpy\n'
python3 /tmp/audit-work/review/trusted/py2mpy.py solution.py > regenerated-solution.mpy
translate_exit=$?
printf 'TRANSLATE_EXIT=%s\n' "$translate_exit"
sha256sum solution.py solution.mpy regenerated-solution.mpy

printf 'COMMAND: cmp solution.mpy regenerated-solution.mpy\n'
cmp solution.mpy regenerated-solution.mpy
cmp_exit=$?
printf 'MPY_BYTE_IDENTITY_CMP_EXIT=%s\n' "$cmp_exit"

printf 'COMMAND: python3 /audit-output/evidence/02_differential.py\n'
python3 /audit-output/evidence/02_differential.py
differential_exit=$?
printf 'DIFFERENTIAL_EXIT=%s\n' "$differential_exit"

if [ "$translate_exit" -ne 0 ] || [ "$cmp_exit" -ne 0 ] || [ "$differential_exit" -ne 0 ]; then
  printf 'SCRIPT_EXIT=1\n'
  exit 1
fi
printf 'SCRIPT_EXIT=0\n'
