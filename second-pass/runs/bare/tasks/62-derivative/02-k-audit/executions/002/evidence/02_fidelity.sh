#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction-62 || exit 70

printf 'COMMAND: python3 /tmp/audit-work/trusted-62/py2mpy.py solution.py > regenerated-trusted.mpy\n'
python3 /tmp/audit-work/trusted-62/py2mpy.py solution.py > regenerated-trusted.mpy
translate_status=$?
printf 'EXIT_STATUS: %d\n' "$translate_status"

printf 'COMMAND: cmp solution.mpy regenerated-trusted.mpy\n'
cmp solution.mpy regenerated-trusted.mpy
cmp_status=$?
printf 'EXIT_STATUS: %d\n' "$cmp_status"

printf 'COMMAND: python3 /audit-output/evidence/02_differential.py\n'
python3 /audit-output/evidence/02_differential.py
differential_status=$?
printf 'EXIT_STATUS: %d\n' "$differential_status"

if (( translate_status != 0 || cmp_status != 0 || differential_status != 0 )); then
  exit 1
fi
