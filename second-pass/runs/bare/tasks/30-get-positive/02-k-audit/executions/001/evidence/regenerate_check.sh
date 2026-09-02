#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/30-get-positive
generated="$scratch/regenerated-solution.mpy"

python3 /reference/py2mpy.py "$scratch/solution.py" > "$generated"
translator_status=$?
printf 'TRANSLATOR_EXIT_STATUS: %d\n' "$translator_status"
if [[ "$translator_status" -ne 0 ]]; then
  exit "$translator_status"
fi

cmp "$scratch/solution.mpy" "$generated"
cmp_status=$?
printf 'BYTE_IDENTITY_CMP_EXIT_STATUS: %d\n' "$cmp_status"
printf 'SUBMITTED_SHA256: %s\n' "$(sha256sum "$scratch/solution.mpy" | cut -d' ' -f1)"
printf 'REGENERATED_SHA256: %s\n' "$(sha256sum "$generated" | cut -d' ' -f1)"
if [[ "$cmp_status" -ne 0 ]]; then
  diff -u "$scratch/solution.mpy" "$generated" || true
fi
exit "$cmp_status"
