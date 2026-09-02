#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/95-check-dict-case-audit
status=0

printf '%s\n' 'COMMAND: python3 py2mpy.py solution.py > regenerated-solution.mpy'
(
  cd "$scratch" || exit 1
  PYTHONDONTWRITEBYTECODE=1 python3 py2mpy.py solution.py > regenerated-solution.mpy
)
translator_status=$?
printf 'TRANSLATOR_EXIT=%s\n' "$translator_status"
if [[ "$translator_status" -ne 0 ]]; then
  status=1
fi

printf '%s\n' 'COMMAND: cmp -s regenerated-solution.mpy solution.mpy'
cmp -s "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
identity_status=$?
printf 'MPY_BYTE_IDENTITY_EXIT=%s\n' "$identity_status"
if [[ "$identity_status" -ne 0 ]]; then
  status=1
fi

printf '%s\n' 'COMMAND: python3 differential.py canonical.py solution.py'
PYTHONDONTWRITEBYTECODE=1 python3 \
  /audit-output/evidence/differential.py \
  "$scratch/canonical.py" \
  "$scratch/solution.py"
differential_status=$?
printf 'DIFFERENTIAL_EXIT=%s\n' "$differential_status"
if [[ "$differential_status" -ne 0 ]]; then
  status=1
fi

printf 'FIDELITY_STATUS=%s\n' "$status"
exit "$status"
