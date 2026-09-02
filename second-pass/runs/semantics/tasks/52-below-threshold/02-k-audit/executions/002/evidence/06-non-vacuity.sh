#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/52-below-threshold
evidence=/audit-output/evidence
failures=0

printf '%s\n' \
  'MUTATION: entry result belowThresholdSpec(IS,T) -> notBool belowThresholdSpec(IS,T).' \
  'SATISFIABLE WITNESS: IS=.IntSeq, T=0, exact initial configuration from SPEC.' \
  'For this witness the generated function, canonical function, and original postcondition are true;' \
  'the mutated destination is false.'
nl -ba "$scratch/reviewer-spec-vacuity.k"

dry_command='kprove reviewer-spec-vacuity.k --definition reviewer-verification-kompiled --spec-module REVIEWER-SPEC-VACUITY --dry-run --output pretty'
printf 'COMMAND[mutation-dry-run]: cd %s && %s\n' "$scratch" "$dry_command"
script -q -e -c "cd '$scratch' && $dry_command" "$evidence/06-mutation-dry-run.log"
dry_status=$?
printf 'EXIT[mutation-dry-run]=%s\n' "$dry_status"
if [[ "$dry_status" -ne 0 ]]; then
  failures=$((failures + 1))
fi

proof_command='kprove reviewer-spec-vacuity.k --definition reviewer-verification-kompiled --spec-module REVIEWER-SPEC-VACUITY --output pretty'
printf 'COMMAND[mutation-proof]: cd %s && %s\n' "$scratch" "$proof_command"
script -q -e -c "cd '$scratch' && $proof_command" "$evidence/06-mutation-proof.log"
proof_status=$?
printf 'EXIT[mutation-proof]=%s\n' "$proof_status"
if [[ "$proof_status" -eq 0 ]]; then
  printf 'FAIL false result mutation unexpectedly closed\n'
  failures=$((failures + 1))
else
  printf 'OK false result mutation was rejected\n'
fi

if tr -d '\r' < "$evidence/06-mutation-proof.log" | rg \
    'WarnStuckClaimState|implication check between the conditions has failed' >/dev/null; then
  printf 'OK rejection exposes the unmet result implication\n'
else
  printf 'FAIL mutation rejection was not the expected result-obligation failure\n'
  failures=$((failures + 1))
fi

printf 'NON_VACUITY_FAILURE_COUNT=%s\n' "$failures"
exit "$failures"
