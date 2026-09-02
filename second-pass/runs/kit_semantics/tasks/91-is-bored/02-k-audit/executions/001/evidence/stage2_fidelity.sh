#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/case91
overall=0

printf 'COMMAND: cd %s && python3 py2mpy.py solution.py > regenerated-solution.mpy\n' "$scratch"
(
  cd "$scratch"
  python3 py2mpy.py solution.py > regenerated-solution.mpy
)
translator_ec=$?
printf 'TRANSLATOR_EXIT=%d\n' "$translator_ec"
if [[ $translator_ec -ne 0 ]]; then overall=1; fi

printf 'COMMAND: cmp -s %s/regenerated-solution.mpy %s/solution.mpy\n' "$scratch" "$scratch"
cmp -s "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
cmp_ec=$?
printf 'BYTE_IDENTITY_EXIT=%d\n' "$cmp_ec"
if [[ $cmp_ec -ne 0 ]]; then
  diff -u "$scratch/solution.mpy" "$scratch/regenerated-solution.mpy"
  overall=1
fi

sha256sum "$scratch/solution.py" "$scratch/solution.mpy" "$scratch/regenerated-solution.mpy"

printf 'COMMAND: python3 /audit-output/evidence/stage2_differential.py\n'
python3 /audit-output/evidence/stage2_differential.py
diff_ec=$?
printf 'DIFFERENTIAL_EXIT=%d\n' "$diff_ec"
if [[ $diff_ec -ne 0 ]]; then overall=1; fi

printf 'FINAL_STATUS=%d\n' "$overall"
exit "$overall"
