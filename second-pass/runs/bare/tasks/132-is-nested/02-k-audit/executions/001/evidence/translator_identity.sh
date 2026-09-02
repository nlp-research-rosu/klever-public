#!/usr/bin/env bash
set -uo pipefail

python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/source/solution.py \
  > /tmp/audit-work/source/solution.regenerated.mpy
translator_status=$?
printf 'TRANSLATOR_EXIT %d\n' "$translator_status"
if ((translator_status != 0)); then
  exit "$translator_status"
fi

sha256sum \
  /tmp/audit-work/source/solution.mpy \
  /tmp/audit-work/source/solution.regenerated.mpy

if cmp -s \
    /tmp/audit-work/source/solution.mpy \
    /tmp/audit-work/source/solution.regenerated.mpy; then
  printf 'BYTE_IDENTITY PASS\n'
  exit 0
fi

printf 'BYTE_IDENTITY FAIL\n'
diff -u \
  /tmp/audit-work/source/solution.mpy \
  /tmp/audit-work/source/solution.regenerated.mpy
exit 1
