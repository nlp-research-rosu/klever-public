#!/usr/bin/env bash
set -uo pipefail

trusted_translator=/tmp/audit-work/reference/py2mpy.py
submitted_python=/tmp/audit-work/candidate/solution.py
submitted_mpy=/tmp/audit-work/candidate/solution.mpy
regenerated_mpy=/tmp/audit-work/candidate/regenerated-solution.mpy

python3 "$trusted_translator" "$submitted_python" >"$regenerated_mpy"
translation_status=$?
echo "COMMAND: python3 $trusted_translator $submitted_python >$regenerated_mpy"
echo "EXIT: $translation_status"
sha256sum "$submitted_mpy" "$regenerated_mpy"
cmp --silent "$submitted_mpy" "$regenerated_mpy"
identity_status=$?
echo "COMMAND: cmp --silent $submitted_mpy $regenerated_mpy"
echo "EXIT: $identity_status"
if [[ "$translation_status" -ne 0 || "$identity_status" -ne 0 ]]; then
  echo "TRANSLATION_IDENTITY=FAIL"
  exit 1
fi
echo "TRANSLATION_IDENTITY=PASS"
