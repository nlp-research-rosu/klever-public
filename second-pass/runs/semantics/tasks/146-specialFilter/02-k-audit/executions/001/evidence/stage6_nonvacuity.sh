#!/usr/bin/env bash
set -u
set -o pipefail
set -x

PATH="/home/agent/.nix-profile/bin:$PATH"
work=/tmp/audit-work/candidate-clean
evidence=/audit-output/evidence
overall=0

cp "$evidence/spec-vacuity.k" "$work/spec-vacuity.k"

kprove "$work/spec-vacuity.k" \
  --definition "$work/verification-kompiled" \
  --spec-module SPECIALFILTER-SPEC-VACUITY \
  --dry-run \
  2>&1 | tee "$evidence/stage6_vacuity_dry_run.log"
dry_status=${PIPESTATUS[0]}
printf 'VACUITY_DRY_RUN_EXIT=%s\n' "$dry_status"
(( dry_status == 0 )) || overall=1

kprove "$work/spec-vacuity.k" \
  --definition "$work/verification-kompiled" \
  --spec-module SPECIALFILTER-SPEC-VACUITY \
  2>&1 | tee "$evidence/stage6_vacuity_proof.log"
proof_status=${PIPESTATUS[0]}
printf 'VACUITY_PROOF_EXIT=%s\n' "$proof_status"
if (( proof_status == 0 )); then
  printf 'UNEXPECTED_FALSE_MUTATION_SUCCESS\n'
  overall=1
fi

grep -q 'WarnStuckClaimState' "$evidence/stage6_vacuity_proof.log"
stuck_status=$?
printf 'VACUITY_STUCK_WARNING_CHECK_EXIT=%s\n' "$stuck_status"
(( stuck_status == 0 )) || overall=1

grep -Eq 'implication check.*failed|cannot be rewritten further' \
  "$evidence/stage6_vacuity_proof.log"
obligation_status=$?
printf 'VACUITY_UNMET_OBLIGATION_CHECK_EXIT=%s\n' "$obligation_status"
(( obligation_status == 0 )) || overall=1

printf 'EXPECTED_FALSE_PROOF_NONZERO=%s\n' "$proof_status"
printf 'STAGE6_OVERALL_EXIT=%s\n' "$overall"
exit "$overall"
