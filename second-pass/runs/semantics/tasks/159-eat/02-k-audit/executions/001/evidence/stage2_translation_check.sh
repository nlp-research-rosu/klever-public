#!/usr/bin/env bash
set -u

trusted_translator=/tmp/audit-work/trusted/py2mpy.py
candidate_python=/tmp/audit-work/candidate-src/solution.py
submitted_mpy=/tmp/audit-work/candidate-src/solution.mpy
regenerated_mpy=/tmp/audit-work/regenerated-solution.mpy

printf 'TRANSLATE_COMMAND: python3 %q %q > %q\n' \
  "$trusted_translator" "$candidate_python" "$regenerated_mpy"
python3 "$trusted_translator" "$candidate_python" > "$regenerated_mpy"
translate_status=$?
echo "TRANSLATE_STATUS=$translate_status"

cmp -s "$regenerated_mpy" "$submitted_mpy"
cmp_status=$?
echo "BYTE_IDENTITY_CMP_STATUS=$cmp_status"
sha256sum "$regenerated_mpy" "$submitted_mpy"

if (( translate_status != 0 || cmp_status != 0 )); then
  diff -u "$submitted_mpy" "$regenerated_mpy"
  exit 1
fi
