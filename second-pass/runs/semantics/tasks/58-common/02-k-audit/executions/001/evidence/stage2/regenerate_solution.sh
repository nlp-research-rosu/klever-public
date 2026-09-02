#!/usr/bin/env bash
set -uo pipefail

python3 /reference/py2mpy.py /tmp/audit-work/case58/solution.py \
  > /tmp/audit-work/case58/solution.regenerated.mpy
translate_status=$?
printf 'translator-exit=%d\n' "$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

if cmp -s /tmp/audit-work/case58/solution.regenerated.mpy \
          /tmp/audit-work/case58/solution.mpy; then
  printf 'BYTE_IDENTICAL solution.mpy\n'
  sha256sum /tmp/audit-work/case58/solution.regenerated.mpy \
            /tmp/audit-work/case58/solution.mpy
  exit 0
fi

printf 'BYTE_DIFFERENT solution.mpy\n'
diff -u /tmp/audit-work/case58/solution.mpy \
        /tmp/audit-work/case58/solution.regenerated.mpy || true
exit 1
