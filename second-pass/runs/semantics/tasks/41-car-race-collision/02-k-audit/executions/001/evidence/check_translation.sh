#!/usr/bin/env bash
set -u

trusted_translator=/tmp/audit-work/reconstruction/trusted/py2mpy.py
source_file=/tmp/audit-work/reconstruction/candidate-src/solution.py
submitted_file=/tmp/audit-work/reconstruction/candidate-src/solution.mpy
regenerated_file=/tmp/audit-work/reconstruction/work/solution.regenerated.mpy

python3 "$trusted_translator" "$source_file" >"$regenerated_file"
translator_status=$?
printf 'translator_exit=%d\n' "$translator_status"
if [[ "$translator_status" -ne 0 ]]; then
  exit "$translator_status"
fi

sha256sum "$source_file" "$submitted_file" "$regenerated_file"
cmp -- "$submitted_file" "$regenerated_file"
cmp_status=$?
printf 'byte_identity_cmp_exit=%d\n' "$cmp_status"
if [[ "$cmp_status" -ne 0 ]]; then
  diff -u -- "$submitted_file" "$regenerated_file"
fi
exit "$cmp_status"
