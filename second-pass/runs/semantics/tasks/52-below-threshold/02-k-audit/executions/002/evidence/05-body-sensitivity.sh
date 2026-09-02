#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/52-below-threshold
evidence=/audit-output/evidence
failures=0

printf '%s\n' \
  'MUTATION: in the macro-expanded function body, replace the >= branch' \
  'Return(Bool(false)) with Return(Bool(true)). Witness: l=[5], t=5;' \
  'the mutated body returns true while the claimed belowThresholdSpec is false.'
diff -u "$scratch/verification.k" "$scratch/verification-body-mutant.k" || true

build_command='kompile verification-body-mutant.k --backend haskell --main-module VERIFICATION-BASE --syntax-module VERIFICATION-BASE --output-definition reviewer-body-mutant-kompiled'
printf 'COMMAND[body-mutant-build]: cd %s && %s\n' "$scratch" "$build_command"
script -q -e -c "cd '$scratch' && $build_command" "$evidence/05-body-mutant-build.log"
build_status=$?
printf 'EXIT[body-mutant-build]=%s\n' "$build_status"
if [[ "$build_status" -ne 0 ]]; then
  failures=$((failures + 1))
fi

proof_command='kprove spec-body-mutant.k --definition reviewer-body-mutant-kompiled --spec-module LOOP-SPEC --output pretty'
printf 'COMMAND[body-mutant-proof]: cd %s && %s\n' "$scratch" "$proof_command"
script -q -e -c "cd '$scratch' && $proof_command" "$evidence/05-body-mutant-proof.log"
proof_status=$?
printf 'EXIT[body-mutant-proof]=%s\n' "$proof_status"
if [[ "$proof_status" -eq 0 ]]; then
  printf 'FAIL body-mutant proof unexpectedly closed\n'
  failures=$((failures + 1))
else
  printf 'OK body-mutant proof was rejected\n'
fi

if tr -d '\r' < "$evidence/05-body-mutant-proof.log" | rg \
    'WarnStuckClaimState|implication check between the conditions has failed' >/dev/null; then
  printf 'OK failure is a stuck result obligation\n'
else
  printf 'FAIL body-mutant failure lacked the expected stuck-obligation diagnostic\n'
  failures=$((failures + 1))
fi

printf 'BODY_SENSITIVITY_FAILURE_COUNT=%s\n' "$failures"
exit "$failures"
