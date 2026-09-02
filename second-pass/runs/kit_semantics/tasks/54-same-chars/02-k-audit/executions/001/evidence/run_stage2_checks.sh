#!/usr/bin/env bash
set -o xtrace
python3 /reference/py2mpy.py /tmp/audit-work/54-same-chars/solution.py > /tmp/audit-work/54-same-chars/solution.regenerated.mpy
translate_status=$?
cmp -s /tmp/audit-work/54-same-chars/solution.regenerated.mpy /tmp/audit-work/54-same-chars/solution.mpy
identity_status=$?
sha256sum /tmp/audit-work/54-same-chars/solution.regenerated.mpy /tmp/audit-work/54-same-chars/solution.mpy
python3 /audit-output/evidence/program_pinning_check.py
pinning_status=$?
python3 /audit-output/evidence/differential_test.py
differential_status=$?
printf 'TRANSLATE_EXIT_STATUS=%s\n' "$translate_status"
printf 'BYTE_IDENTITY_EXIT_STATUS=%s\n' "$identity_status"
printf 'PINNING_EXIT_STATUS=%s\n' "$pinning_status"
printf 'DIFFERENTIAL_EXIT_STATUS=%s\n' "$differential_status"
if (( translate_status || identity_status || pinning_status || differential_status )); then
  exit 1
fi
