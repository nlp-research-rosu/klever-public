#!/usr/bin/env bash
set -uo pipefail

overall=0
run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
  return 0
}

scratch=/tmp/audit-work/46-fib4

printf 'AUDIT STAGE 4: alias pinning, body sensitivity, claim witnesses\n'
run cp /audit-output/evidence/solution-alias.mpy "$scratch/solution-alias.mpy"
run cp /audit-output/evidence/solution-mutated.mpy "$scratch/solution-mutated.mpy"
run python3 /audit-output/evidence/pinning_crosscheck.py
run python3 /audit-output/evidence/adequacy_witnesses.py
exit "$overall"
