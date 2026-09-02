#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/130-tri-audit
overall=0

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  if [[ "$status" -ne 0 ]]; then
    overall=1
  fi
}

run python3 "$scratch/py2mpy.trusted.py" "$scratch/solution.py"

printf '\nCOMMAND: python3 trusted translator redirected to %s\n' "$scratch/solution.regenerated.mpy"
python3 "$scratch/py2mpy.trusted.py" "$scratch/solution.py" > "$scratch/solution.regenerated.mpy"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
if [[ "$status" -ne 0 ]]; then overall=1; fi

run cmp -s "$scratch/solution.submitted.mpy" "$scratch/solution.regenerated.mpy"
run sha256sum "$scratch/solution.submitted.mpy" "$scratch/solution.regenerated.mpy"
run python3 /audit-output/evidence/differential_test.py

printf '\nSTAGE2_OVERALL_EXIT_STATUS: %d\n' "$overall"
exit "$overall"
