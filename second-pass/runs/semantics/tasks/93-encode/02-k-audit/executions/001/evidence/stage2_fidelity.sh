#!/usr/bin/env bash
set -uo pipefail
set -x

python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
translate_status=$?

cmp -s \
  /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
cmp_status=$?

set +x
echo "TRANSLATE_EXIT_STATUS: $translate_status"
echo "MPY_BYTE_IDENTITY_STATUS: $cmp_status"
sha256sum \
  /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate-src/solution.mpy

if (( cmp_status != 0 )); then
  diff -u \
    /tmp/audit-work/candidate-src/solution.mpy \
    /tmp/audit-work/regenerated-solution.mpy || true
fi

if (( translate_status != 0 || cmp_status != 0 )); then
  exit 1
fi
