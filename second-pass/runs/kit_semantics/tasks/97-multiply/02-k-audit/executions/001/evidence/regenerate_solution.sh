#!/usr/bin/env bash
set -uo pipefail

regenerated=/tmp/audit-work/reconstruction/solution.regenerated.mpy

printf 'COMMAND: python3 /reference/py2mpy.py /candidate/solution.py > %s\n' "$regenerated"
python3 /reference/py2mpy.py /candidate/solution.py >"$regenerated"
translator_status=$?
printf 'TRANSLATOR_EXIT_STATUS: %d\n' "$translator_status"
if [[ $translator_status -ne 0 ]]; then
  exit "$translator_status"
fi

printf 'COMMAND: cmp -s %s /candidate/solution.mpy\n' "$regenerated"
cmp -s "$regenerated" /candidate/solution.mpy
comparison_status=$?
printf 'COMPARISON_EXIT_STATUS: %d\n' "$comparison_status"

sha256sum /reference/py2mpy.py /candidate/solution.py \
  "$regenerated" /candidate/solution.mpy
exit "$comparison_status"
