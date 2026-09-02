#!/usr/bin/env bash
set -uo pipefail

status=0
regenerated=/tmp/audit-work/84-solve/regenerated-solution.mpy

python3 /reference/py2mpy.py /candidate/solution.py > "$regenerated"
translator_exit=$?
printf 'TRANSLATOR_EXIT %d\n' "$translator_exit"
if [[ "$translator_exit" -ne 0 ]]; then
  status=1
fi

cmp -s "$regenerated" /candidate/solution.mpy
identity_exit=$?
printf 'SOLUTION_MPY_BYTE_IDENTITY_EXIT %d\n' "$identity_exit"
if [[ "$identity_exit" -ne 0 ]]; then
  status=1
fi

sha256sum "$regenerated" /candidate/solution.mpy

python3 /audit-output/evidence/differential_test.py
differential_exit=$?
printf 'DIFFERENTIAL_EXIT %d\n' "$differential_exit"
if [[ "$differential_exit" -ne 0 ]]; then
  status=1
fi

printf 'OVERALL_EXIT %d\n' "$status"
exit "$status"
