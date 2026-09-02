#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction

run() {
  local description="$1"
  shift
  printf '\nCOMMAND (%s):' "$description"
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT STATUS: %d\n' "$status"
  return "$status"
}

printf 'AUDIT STAGE 5: concrete false-conclusion witness for absNum\n'

run "independent exact-rational oracle" \
  python3 /audit-output/evidence/05_negative_denominator_oracle.py
oracle_status=$?

run "execute submitted program on the same formally admitted rational terms" \
  krun "$scratch/solution.mpy" \
    --definition "$scratch/semantic-kompiled" \
    -cARGS='nums(rat(3,-1),rat(1,-1))'
semantic_status=$?

printf '\nINTERPRETATION\n'
printf 'The oracle result is +1. The K result above is rat(-8,8), i.e. -1.\n'
printf 'Both input denominators are nonzero, so these are valid rational representations.\n'

if (( oracle_status || semantic_status )); then
  exit 1
fi
