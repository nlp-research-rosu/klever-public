#!/usr/bin/env bash
set -uo pipefail

failures=0
scratch=/tmp/audit-work/161-solve/scratch

printf 'COMMAND: python3 /reference/py2mpy.py %s/solution.py > %s/regenerated-solution.mpy\n' \
  "$scratch" "$scratch"
python3 /reference/py2mpy.py "$scratch/solution.py" > "$scratch/regenerated-solution.mpy"
translator_status=$?
printf 'TRANSLATOR_EXIT_STATUS: %d\n' "$translator_status"
if [[ "$translator_status" -ne 0 ]]; then
  failures=$((failures + 1))
fi

sha256sum "$scratch/solution.mpy" "$scratch/regenerated-solution.mpy"
printf 'COMMAND: cmp %s/solution.mpy %s/regenerated-solution.mpy\n' "$scratch" "$scratch"
if cmp "$scratch/solution.mpy" "$scratch/regenerated-solution.mpy"; then
  printf 'SOLUTION_MPY_BYTE_IDENTITY PASS\n'
else
  cmp_status=$?
  printf 'SOLUTION_MPY_BYTE_IDENTITY FAIL exit=%d\n' "$cmp_status"
  failures=$((failures + 1))
fi
cp "$scratch/regenerated-solution.mpy" /audit-output/evidence/regenerated-solution.mpy

printf 'COMMAND: python3 /audit-output/evidence/differential_audit.py\n'
python3 /audit-output/evidence/differential_audit.py
differential_status=$?
printf 'DIFFERENTIAL_EXIT_STATUS: %d\n' "$differential_status"
if [[ "$differential_status" -ne 0 ]]; then
  failures=$((failures + 1))
fi

printf 'OVERALL_FAILURES: %d\n' "$failures"
if [[ "$failures" -eq 0 ]]; then
  printf 'STAGE2_PROGRAM_FIDELITY PASS\n'
  printf 'EXIT_STATUS: 0\n'
  exit 0
fi
printf 'STAGE2_PROGRAM_FIDELITY FAIL\n'
printf 'EXIT_STATUS: 1\n'
exit 1
