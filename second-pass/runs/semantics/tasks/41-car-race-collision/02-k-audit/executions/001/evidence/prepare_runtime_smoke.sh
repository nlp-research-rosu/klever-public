#!/usr/bin/env bash
set -u

translator=/tmp/audit-work/reconstruction/trusted/py2mpy.py
source_file=/audit-output/evidence/runtime_smoke.py
solution_file=/tmp/audit-work/reconstruction/candidate-src/solution.py
translated_file=/audit-output/evidence/runtime_smoke.mpy
work_file=/tmp/audit-work/reconstruction/work/runtime_smoke.mpy

sed -n '1,2p' "$source_file" | cmp -- "$solution_file" -
source_prefix_status=$?
printf 'solution_source_prefix_cmp_exit=%d\n' "$source_prefix_status"
if [[ "$source_prefix_status" -ne 0 ]]; then
  exit "$source_prefix_status"
fi
python3 "$translator" "$source_file" >"$translated_file"
translator_status=$?
printf 'translator_exit=%d\n' "$translator_status"
if [[ "$translator_status" -ne 0 ]]; then
  exit "$translator_status"
fi
cp -a -- "$translated_file" "$work_file"
sha256sum "$translated_file" "$work_file"
