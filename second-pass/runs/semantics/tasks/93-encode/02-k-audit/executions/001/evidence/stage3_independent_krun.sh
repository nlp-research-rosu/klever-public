#!/usr/bin/env bash
set -uo pipefail
set -x

python3 /tmp/audit-work/trusted/py2mpy.py \
  /audit-output/evidence/audit_concrete_tests.py \
  > /tmp/audit-work/audit_concrete_tests.mpy
translate_status=$?

krun /tmp/audit-work/audit_concrete_tests.mpy \
  --definition /tmp/audit-work/candidate-src/runtime-kompiled \
  --output pretty
krun_status=$?

set +x
echo "TRANSLATE_EXIT_STATUS: $translate_status"
echo "KRUN_EXIT_STATUS: $krun_status"

if (( translate_status != 0 || krun_status != 0 )); then
  exit 1
fi
