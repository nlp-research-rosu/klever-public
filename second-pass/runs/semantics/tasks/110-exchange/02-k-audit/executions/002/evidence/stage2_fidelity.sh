#!/usr/bin/env bash
set -u

cd /tmp/audit-work/review || exit 90
status=0

printf 'COMMAND: python3 py2mpy.py solution.py > solution.regenerated.mpy\n'
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmd_status=$?
printf 'TRANSLATOR_EXIT_STATUS: %d\n' "$cmd_status"
if (( cmd_status != 0 )); then
  status=$cmd_status
fi

printf 'COMMAND: cmp -s solution.regenerated.mpy solution.mpy\n'
cmp -s solution.regenerated.mpy solution.mpy
cmp_status=$?
printf 'BYTE_IDENTITY_EXIT_STATUS: %d\n' "$cmp_status"
if (( cmp_status != 0 )); then
  status=$cmp_status
  diff -u solution.mpy solution.regenerated.mpy
fi

sha256sum solution.py solution.mpy solution.regenerated.mpy canonical.py prompt.py py2mpy.py
printf 'EXIT_STATUS: %d\n' "$status"
exit "$status"
