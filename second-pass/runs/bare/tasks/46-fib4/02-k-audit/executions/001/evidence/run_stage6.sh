#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/46-fib4
cd "$scratch" || exit 2

printf 'AUDIT STAGE 6: fresh false result mutation\n'
printf '\nCOMMAND: cp %q %q\n' \
  /audit-output/evidence/spec-vacuity.k "$scratch/spec-vacuity.k"
cp /audit-output/evidence/spec-vacuity.k "$scratch/spec-vacuity.k"
copy_status=$?
printf 'EXIT: %d\n' "$copy_status"
if (( copy_status != 0 )); then
  exit 1
fi

printf '\nCOMMAND: kprove spec-vacuity.k --definition semantic-haskell-kompiled --spec-module SPEC-VACUITY --dry-run\n'
kprove spec-vacuity.k \
  --definition semantic-haskell-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run
dry_status=$?
printf 'EXIT: %d\n' "$dry_status"
if (( dry_status != 0 )); then
  printf 'UNEXPECTED: mutation did not parse/build successfully\n'
  exit 1
fi

mutation_output=/tmp/audit-work/46-fib4/spec-vacuity-proof-output.log
printf '\nCOMMAND: kprove spec-vacuity.k --definition semantic-haskell-kompiled --spec-module SPEC-VACUITY\n'
kprove spec-vacuity.k \
  --definition semantic-haskell-kompiled \
  --spec-module SPEC-VACUITY \
  2>&1 | tee "$mutation_output"
prove_status=${PIPESTATUS[0]}
printf 'EXIT: %d\n' "$prove_status"

printf '\nCOMMAND: grep -F WarnStuckClaimState %q\n' "$mutation_output"
grep -F WarnStuckClaimState "$mutation_output"
warn_status=$?
printf 'EXIT: %d\n' "$warn_status"

printf '\nCOMMAND: grep -F result ( 2 ) %q\n' "$mutation_output"
grep -F 'result ( 2 )' "$mutation_output"
residual_status=$?
printf 'EXIT: %d\n' "$residual_status"

if (( prove_status == 0 )); then
  printf 'UNEXPECTED: false result mutation proved\n'
  exit 1
fi
if (( warn_status != 0 || residual_status != 0 )); then
  printf 'UNEXPECTED: failure did not expose the expected stuck result obligation\n'
  exit 1
fi
printf 'EXPECTED FAILURE CONFIRMED: reachable n=2 execution produced result(2), not result(3)\n'
exit 0
