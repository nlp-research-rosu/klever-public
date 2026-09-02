#!/usr/bin/env bash
set -u

maker=/audit-output/evidence/stage3_make_concrete_harness.py
translator=/tmp/audit-work/50-decode-shift/trusted-src/py2mpy.py
harness_py=/tmp/audit-work/50-decode-shift/concrete_harness.py
harness_mpy=/tmp/audit-work/50-decode-shift/concrete_harness.mpy

printf 'COMMAND: python3 %q\n' "$maker"
python3 "$maker"
make_status=$?
printf 'EXIT_STATUS: %d\n\n' "$make_status"

printf 'COMMAND: python3 %q %q > %q\n' "$translator" "$harness_py" "$harness_mpy"
python3 "$translator" "$harness_py" >"$harness_mpy"
translate_status=$?
printf 'EXIT_STATUS: %d\n' "$translate_status"

if [[ "$make_status" -ne 0 || "$translate_status" -ne 0 ]]; then
  exit 1
fi
