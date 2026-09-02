#!/usr/bin/env bash
set +e

python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/candidate-src/solution.regenerated.mpy
translator_status=$?
printf 'TRANSLATOR_EXIT=%s\n' "$translator_status"
sha256sum \
  /tmp/audit-work/candidate-src/solution.mpy \
  /tmp/audit-work/candidate-src/solution.regenerated.mpy
cmp -s \
  /tmp/audit-work/candidate-src/solution.mpy \
  /tmp/audit-work/candidate-src/solution.regenerated.mpy
compare_status=$?
printf 'BYTE_COMPARE_EXIT=%s\n' "$compare_status"

if [ "$translator_status" -eq 0 ] && [ "$compare_status" -eq 0 ]; then
  exit 0
fi
diff -u \
  /tmp/audit-work/candidate-src/solution.mpy \
  /tmp/audit-work/candidate-src/solution.regenerated.mpy
exit 1
