#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/review/candidate-src
cp audit-spec-body-slice-mutation.k \
  /audit-output/evidence/05_audit_spec_body_slice_mutation.k

printf '%s\n' \
  'COMMAND: kprove audit-spec-body-slice-mutation.k --definition audit-verification-kompiled --spec-module AUDIT-SPEC-BODY-SLICE-MUTATION --dry-run'
kprove audit-spec-body-slice-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-BODY-SLICE-MUTATION \
  --dry-run
dry_status=$?
printf 'BODY_MUTATION_DRY_RUN_EXIT=%s\n' "$dry_status"
if [ "$dry_status" -ne 0 ]; then
  exit 1
fi

printf '%s\n' \
  'COMMAND: kprove audit-spec-body-slice-mutation.k --definition audit-verification-kompiled --spec-module AUDIT-SPEC-BODY-SLICE-MUTATION'
kprove audit-spec-body-slice-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-BODY-SLICE-MUTATION \
  2>&1 | tee audit-body-sensitivity-raw.log
proof_status=$?
printf 'BODY_MUTATION_PROOF_EXIT=%s\n' "$proof_status"
if [ "$proof_status" -eq 0 ]; then
  printf 'ERROR: changed executed body unexpectedly proved original result\n'
  exit 1
fi
rg -q 'WarnStuckClaimState' audit-body-sensitivity-raw.log
warning_status=$?
rg -U -q '<k>[[:space:]]*2 ~> \.K' audit-body-sensitivity-raw.log
residual_status=$?
printf 'EXPECTED_STUCK_WARNING_FOUND=%s\n' "$((warning_status == 0))"
printf 'CHANGED_BODY_RESULT_2_RESIDUAL_FOUND=%s\n' "$((residual_status == 0))"
if [ "$warning_status" -ne 0 ] || [ "$residual_status" -ne 0 ]; then
  exit 1
fi
printf 'BODY_SENSITIVITY_CONFIRMED=1\n'
