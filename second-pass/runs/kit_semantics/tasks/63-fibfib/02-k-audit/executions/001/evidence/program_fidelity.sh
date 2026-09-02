#!/usr/bin/env bash
set -u

cd /tmp/audit-work || exit 1
status=0

printf 'COMMAND: python3 py2mpy.py solution.py > solution.regenerated.mpy\n'
python3 py2mpy.py solution.py > solution.regenerated.mpy
translate_status=$?
printf 'TRANSLATOR_EXIT_STATUS: %d\n' "$translate_status"
if [[ $translate_status -ne 0 ]]; then status=1; fi

printf 'COMMAND: cmp solution.regenerated.mpy solution.mpy\n'
cmp solution.regenerated.mpy solution.mpy
cmp_status=$?
printf 'BYTE_IDENTITY_EXIT_STATUS: %d\n' "$cmp_status"
if [[ $cmp_status -ne 0 ]]; then status=1; fi

printf 'SHA256\n'
sha256sum solution.py solution.mpy solution.regenerated.mpy

printf 'COMMAND: python3 differential_test.py\n'
python3 differential_test.py
differential_status=$?
printf 'DIFFERENTIAL_EXIT_STATUS: %d\n' "$differential_status"
if [[ $differential_status -ne 0 ]]; then status=1; fi

printf 'FINAL_STATUS: %d\n' "$status"
exit "$status"
