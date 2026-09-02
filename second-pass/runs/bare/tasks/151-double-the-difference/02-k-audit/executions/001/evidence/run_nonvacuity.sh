#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/candidate-src
DEFINITION=/tmp/audit-work/build-verified/verification-kompiled

cp /audit-output/evidence/spec-vacuity-audit.k \
  "$WORK/spec-vacuity-audit.k"

printf '%s\n' \
  'COMMAND: kprove spec-vacuity-audit.k --definition /tmp/audit-work/build-verified/verification-kompiled --spec-module SPEC-VACUITY-AUDIT --dry-run'
timeout 300 kprove spec-vacuity-audit.k \
  --definition "$DEFINITION" \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run
dry_status=$?
printf 'VACUITY_DRY_RUN_EXIT_STATUS=%s\n' "$dry_status"
if [[ "$dry_status" -ne 0 ]]; then
  printf '%s\n' 'NONVACUITY_RESULT=FAIL_MUTATION_DID_NOT_BUILD'
  exit "$dry_status"
fi

printf '%s\n' \
  'COMMAND: kprove spec-vacuity-audit.k --definition /tmp/audit-work/build-verified/verification-kompiled --spec-module SPEC-VACUITY-AUDIT'
proof_output="$(
  timeout 300 kprove spec-vacuity-audit.k \
    --definition "$DEFINITION" \
    --spec-module SPEC-VACUITY-AUDIT \
    2>&1
)"
proof_status=$?
printf '%s\n' "$proof_output"
printf 'VACUITY_KPROVE_EXIT_STATUS=%s\n' "$proof_status"

if [[ "$proof_status" -eq 0 ]]; then
  printf '%s\n' 'NONVACUITY_RESULT=FAIL_FALSE_MUTATION_PROVED'
  exit 1
fi
if [[ "$proof_status" -eq 124 ]]; then
  printf '%s\n' 'NONVACUITY_RESULT=FAIL_TIMEOUT'
  exit 1
fi
if ! grep -Fq 'WarnStuckClaimState' <<<"$proof_output"; then
  printf '%s\n' 'NONVACUITY_RESULT=FAIL_NO_STUCK_OBLIGATION'
  exit 1
fi
if ! grep -Fq 'implication check' <<<"$proof_output"; then
  printf '%s\n' 'NONVACUITY_RESULT=FAIL_WRONG_FAILURE_REASON'
  exit 1
fi
printf '%s\n' 'SATISFYING_WITNESS: VS=nil; candidate=0; canonical=0; mutated required result=1'
printf '%s\n' 'NONVACUITY_RESULT=PASS_EXPECTED_UNMET_RESULT_OBLIGATION'
exit 0
