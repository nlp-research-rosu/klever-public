#!/usr/bin/env bash
set -uo pipefail

python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
translate_status=$?

if (( translate_status != 0 )); then
  echo "Trusted translator failed with status $translate_status"
  exit "$translate_status"
fi

if cmp -s \
  /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/src/solution.mpy
then
  echo "BYTE_IDENTITY: PASS"
  sha256sum \
    /tmp/audit-work/regenerated-solution.mpy \
    /tmp/audit-work/src/solution.mpy
  cp /tmp/audit-work/regenerated-solution.mpy \
    /audit-output/evidence/regenerated-solution.mpy
  exit 0
fi

echo "BYTE_IDENTITY: FAIL"
diff -u \
  /tmp/audit-work/src/solution.mpy \
  /tmp/audit-work/regenerated-solution.mpy
exit 1
