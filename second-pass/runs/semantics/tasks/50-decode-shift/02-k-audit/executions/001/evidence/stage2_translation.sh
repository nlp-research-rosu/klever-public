#!/usr/bin/env bash
set -u

trusted_translator=/tmp/audit-work/50-decode-shift/trusted-src/py2mpy.py
candidate_python=/tmp/audit-work/50-decode-shift/candidate-src/solution.py
regenerated_mpy=/tmp/audit-work/50-decode-shift/regenerated-solution.mpy
submitted_mpy=/tmp/audit-work/50-decode-shift/candidate-src/solution.mpy

printf 'COMMAND: python3 %q %q > %q\n' \
  "$trusted_translator" "$candidate_python" "$regenerated_mpy"
python3 "$trusted_translator" "$candidate_python" >"$regenerated_mpy"
translate_status=$?
printf 'EXIT_STATUS: %d\n\n' "$translate_status"

printf 'COMMAND: cmp --silent %q %q\n' "$regenerated_mpy" "$submitted_mpy"
cmp --silent "$regenerated_mpy" "$submitted_mpy"
compare_status=$?
printf 'EXIT_STATUS: %d\n\n' "$compare_status"

printf 'COMMAND: sha256sum %q %q\n' "$regenerated_mpy" "$submitted_mpy"
sha256sum "$regenerated_mpy" "$submitted_mpy"
hash_status=$?
printf 'EXIT_STATUS: %d\n' "$hash_status"

if [[ "$translate_status" -ne 0 || "$compare_status" -ne 0 || "$hash_status" -ne 0 ]]; then
  exit 1
fi
