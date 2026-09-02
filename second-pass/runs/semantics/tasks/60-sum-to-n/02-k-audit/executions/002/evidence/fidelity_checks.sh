#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction || exit 99

printf '$ python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy\n'
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
rc=$?
printf '[exit %d]\n\n' "$rc"

printf '$ cmp -s solution.regenerated.mpy solution.mpy\n'
cmp -s solution.regenerated.mpy solution.mpy
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc == 0 )); then
  printf 'BYTE_IDENTICAL\n\n'
else
  printf 'NOT_BYTE_IDENTICAL\n'
  diff -u solution.mpy solution.regenerated.mpy
  printf '\n'
fi

printf '$ python3 /audit-output/evidence/differential_test.py\n'
python3 /audit-output/evidence/differential_test.py
rc=$?
printf '[exit %d]\n' "$rc"
