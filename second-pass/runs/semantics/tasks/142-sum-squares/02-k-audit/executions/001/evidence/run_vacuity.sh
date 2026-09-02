#!/usr/bin/env bash
set -u

printf '%s\n' 'WITNESS: IS = .Ints; the entry state is the exact main state, actual/summary result 0, mutated destination 1.'

printf '%s\n' 'COMMAND: kprove /audit-output/evidence/spec-vacuity.k --definition audit-verification-kompiled --spec-module SUM-SQUARES-SPEC-VACUITY --claims SUM-SQUARES-SPEC-VACUITY.false-main --dry-run --output pretty'
kprove /audit-output/evidence/spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module SUM-SQUARES-SPEC-VACUITY \
  --claims SUM-SQUARES-SPEC-VACUITY.false-main \
  --dry-run \
  --output pretty
dry_status=$?
printf 'DRY_RUN_EXIT_STATUS: %s\n' "$dry_status"

printf '%s\n' 'COMMAND: kprove /audit-output/evidence/spec-vacuity.k --definition audit-verification-kompiled --spec-module SUM-SQUARES-SPEC-VACUITY --claims SUM-SQUARES-SPEC-VACUITY.false-main,SUM-SQUARES-SPEC.body --trusted SUM-SQUARES-SPEC.body --output pretty'
set +e
kprove /audit-output/evidence/spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module SUM-SQUARES-SPEC-VACUITY \
  --claims SUM-SQUARES-SPEC-VACUITY.false-main,SUM-SQUARES-SPEC.body \
  --trusted SUM-SQUARES-SPEC.body \
  --output pretty 2>&1 | tee vacuity-backend-output.tmp
proof_status=${PIPESTATUS[0]}
set -e
printf 'PROOF_EXIT_STATUS: %s\n' "$proof_status"

grep -q 'WarnStuckClaimState' vacuity-backend-output.tmp
stuck_status=$?
printf 'WARN_STUCK_PRESENT: %s\n' "$((stuck_status == 0))"

grep -Eq '#Equals|implication check.*failed|cannot be rewritten further' vacuity-backend-output.tmp
residual_status=$?
printf 'UNMET_OBLIGATION_RESIDUAL_PRESENT: %s\n' "$((residual_status == 0))"

if (( dry_status == 0 && proof_status != 0 && stuck_status == 0 && residual_status == 0 )); then
  printf '%s\n' 'EXPECTED_MUTATION_REJECTION: PASS'
  exit 0
fi
printf '%s\n' 'EXPECTED_MUTATION_REJECTION: FAIL'
exit 1
