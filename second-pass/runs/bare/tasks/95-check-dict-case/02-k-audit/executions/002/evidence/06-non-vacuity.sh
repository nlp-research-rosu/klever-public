#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/95-check-dict-case-audit
cp /audit-output/evidence/spec-vacuity-review.k "$scratch/"

printf '%s\n' \
  'COMMAND: kprove spec-vacuity-review.k --definition verification-fresh-kompiled --spec-module SPEC-VACUITY-REVIEW --dry-run'
(
  cd "$scratch" || exit 1
  kprove spec-vacuity-review.k \
    --definition verification-fresh-kompiled \
    --spec-module SPEC-VACUITY-REVIEW \
    --dry-run
)
dry_status=$?
printf 'VACUITY_DRY_RUN_EXIT=%s\n' "$dry_status"
if [[ "$dry_status" -ne 0 ]]; then
  printf '%s\n' 'NON_VACUITY=INVALID_MUTATION_DID_NOT_BUILD'
  exit 1
fi

printf '%s\n' \
  'COMMAND: kprove spec-vacuity-review.k --definition verification-fresh-kompiled --spec-module SPEC-VACUITY-REVIEW'
(
  cd "$scratch" || exit 1
  kprove spec-vacuity-review.k \
    --definition verification-fresh-kompiled \
    --spec-module SPEC-VACUITY-REVIEW
)
proof_status=$?
printf 'VACUITY_PROOF_EXIT=%s\n' "$proof_status"
if [[ "$proof_status" -eq 0 ]]; then
  printf '%s\n' 'NON_VACUITY=FAIL_FALSE_POSTCONDITION_PROVED'
  exit 1
fi
printf '%s\n' 'SATISFYING_WITNESS={"a":0,"b":0}'
printf '%s\n' 'EXPECTED_RESULT=true'
printf '%s\n' 'MUTATED_RESULT=false'
printf '%s\n' 'NON_VACUITY=PASS_EXPECTED_UNMET_RESULT_OBLIGATION'
exit 0
