#!/usr/bin/env bash
set -uo pipefail

scratch_root=/tmp/audit-work/96-count-up-to
evidence_root=/audit-output/evidence

python3 "$scratch_root/py2mpy.py" "$scratch_root/solution.py" \
  > "$evidence_root/regenerated-solution.mpy"
translate_status=$?
printf 'translator_exit=%d\n' "$translate_status"

cmp "$evidence_root/regenerated-solution.mpy" "$scratch_root/solution.mpy"
cmp_status=$?
printf 'byte_identity_cmp_exit=%d\n' "$cmp_status"

sha256sum \
  "$scratch_root/solution.py" \
  "$scratch_root/solution.mpy" \
  "$evidence_root/regenerated-solution.mpy"

if [[ "$translate_status" -ne 0 || "$cmp_status" -ne 0 ]]; then
  exit 1
fi
