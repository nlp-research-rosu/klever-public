#!/usr/bin/env bash
set -uo pipefail

trusted_translator=/tmp/audit-work/25-factorize-audit/trusted/py2mpy.py
python_source=/tmp/audit-work/25-factorize-audit/source/solution.py
submitted_mpy=/tmp/audit-work/25-factorize-audit/source/solution.mpy
regenerated_mpy=/tmp/audit-work/25-factorize-audit/generated/solution.trusted.mpy

echo "$ python3 $trusted_translator $python_source > $regenerated_mpy"
python3 "$trusted_translator" "$python_source" > "$regenerated_mpy"
status=$?
printf '[exit_status=%d]\n' "$status"
if (( status != 0 )); then
  exit "$status"
fi

echo "$ cmp $submitted_mpy $regenerated_mpy"
cmp "$submitted_mpy" "$regenerated_mpy"
status=$?
printf '[exit_status=%d]\n' "$status"

sha256sum "$submitted_mpy" "$regenerated_mpy"
exit "$status"
