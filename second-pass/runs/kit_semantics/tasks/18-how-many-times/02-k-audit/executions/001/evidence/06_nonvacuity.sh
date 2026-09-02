#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/review/candidate-src
cp audit-spec-vacuity.k /audit-output/evidence/06_audit_spec_vacuity.k
printf 'WITNESS_SOURCE=%s\n' 'ababa'
printf 'WITNESS_PATTERN=%s\n' 'aba'
printf 'CANONICAL_AND_CANDIDATE_RESULT=2\n'
printf 'MUTATED_REQUIRED_RESULT=3\n'

printf '%s\n' \
  'COMMAND: kprove audit-spec-vacuity.k --definition audit-verification-kompiled --spec-module AUDIT-SPEC-VACUITY --dry-run'
kprove audit-spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run
dry_status=$?
printf 'VACUITY_DRY_RUN_EXIT=%s\n' "$dry_status"
if [ "$dry_status" -ne 0 ]; then
  printf 'ERROR: mutation did not parse/build\n'
  exit 1
fi

printf '%s\n' \
  'COMMAND: kprove audit-spec-vacuity.k --definition audit-verification-kompiled --spec-module AUDIT-SPEC-VACUITY'
kprove audit-spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  2>&1 | tee audit-vacuity-raw.log
proof_status=$?
printf 'VACUITY_PROOF_EXIT=%s\n' "$proof_status"

if [ "$proof_status" -eq 0 ]; then
  printf 'ERROR: false mutation unexpectedly proved\n'
  exit 1
fi
rg -q 'WarnStuckClaimState' audit-vacuity-raw.log
warning_status=$?
rg -U -q '<k>[[:space:]]*2 ~> \.K' audit-vacuity-raw.log
residual_status=$?
printf 'EXPECTED_STUCK_WARNING_FOUND=%s\n' "$((warning_status == 0))"
printf 'EXPECTED_ACTUAL_RESULT_2_RESIDUAL_FOUND=%s\n' "$((residual_status == 0))"
if [ "$warning_status" -ne 0 ] || [ "$residual_status" -ne 0 ]; then
  printf 'ERROR: failure was not the expected unmet result obligation\n'
  exit 1
fi
printf 'EXPECTED_FALSE_MUTATION_REJECTION=1\n'
