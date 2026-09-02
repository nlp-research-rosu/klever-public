#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/105-by-length/recon
overall=0

printf 'COMMAND: cd %s && python3 py2mpy.py solution.py > regenerated-solution.mpy\n' "$scratch"
(
  cd "$scratch" || exit 90
  python3 py2mpy.py solution.py > regenerated-solution.mpy
)
translate_rc=$?
printf 'TRANSLATOR_EXIT_STATUS: %s\n' "$translate_rc"
if (( translate_rc != 0 )); then
  overall=1
fi

printf 'COMMAND: cmp -s %s/regenerated-solution.mpy %s/solution.mpy\n' "$scratch" "$scratch"
cmp -s "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
cmp_rc=$?
printf 'BYTE_IDENTITY_EXIT_STATUS: %s\n' "$cmp_rc"
if (( cmp_rc != 0 )); then
  overall=1
  diff -u "$scratch/solution.mpy" "$scratch/regenerated-solution.mpy" || true
fi

sha256sum "$scratch/solution.py" \
  "$scratch/solution.mpy" \
  "$scratch/regenerated-solution.mpy"

printf 'COMMAND: python3 /audit-output/evidence/differential_check.py\n'
python3 /audit-output/evidence/differential_check.py
differential_rc=$?
printf 'DIFFERENTIAL_EXIT_STATUS: %s\n' "$differential_rc"
if (( differential_rc != 0 )); then
  overall=1
fi

printf 'EXIT_STATUS: %s\n' "$overall"
exit "$overall"
