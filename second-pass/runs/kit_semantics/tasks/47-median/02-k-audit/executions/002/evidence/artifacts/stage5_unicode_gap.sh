#!/usr/bin/env bash
set -u

python3 unicode-gap.py
python_status=$?
printf 'cpython_script_exit=%s\n' "$python_status"
python3 -c 'import solution; print("cpython_result=" + repr(solution.median(["é", "a", "b"])))'

python3 py2mpy.py unicode-gap.py > unicode-gap.mpy
translate_status=$?
printf 'translate_exit=%s\n' "$translate_status"

krun unicode-gap.mpy --definition audit-runtime-kompiled
krun_status=$?
printf 'krun_exit=%s\n' "$krun_status"

if [[ "$python_status" -ne 0 || "$translate_status" -ne 0 ]]; then
  exit 1
fi
