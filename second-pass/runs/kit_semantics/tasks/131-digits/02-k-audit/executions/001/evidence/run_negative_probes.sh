#!/usr/bin/env bash
set -o pipefail

cd /tmp/audit-work/source || exit 90
definition=/tmp/audit-work/rebuilt-verification-kompiled

{
  echo '$ kprove audit-spec-vacuity.k --definition /tmp/audit-work/rebuilt-verification-kompiled --spec-module AUDIT-SPEC-VACUITY --dry-run'
  kprove audit-spec-vacuity.k \
    --definition "$definition" \
    --spec-module AUDIT-SPEC-VACUITY \
    --dry-run
  status=$?
  echo "EXIT_STATUS=$status"
  exit "$status"
} 2>&1 | tee /audit-output/evidence/audit_vacuity_dry_run.log
vacuity_build_status=${PIPESTATUS[0]}

{
  echo '$ kprove audit-spec-vacuity.k --definition /tmp/audit-work/rebuilt-verification-kompiled --spec-module AUDIT-SPEC-VACUITY'
  kprove audit-spec-vacuity.k \
    --definition "$definition" \
    --spec-module AUDIT-SPEC-VACUITY
  status=$?
  echo "EXIT_STATUS=$status"
  exit "$status"
} 2>&1 | tee /audit-output/evidence/audit_vacuity_failure.log
vacuity_proof_status=${PIPESTATUS[0]}

{
  echo '$ kprove audit-spec-body-sensitivity.k --definition /tmp/audit-work/rebuilt-verification-kompiled --spec-module AUDIT-SPEC-BODY-SENSITIVITY --dry-run'
  kprove audit-spec-body-sensitivity.k \
    --definition "$definition" \
    --spec-module AUDIT-SPEC-BODY-SENSITIVITY \
    --dry-run
  status=$?
  echo "EXIT_STATUS=$status"
  exit "$status"
} 2>&1 | tee /audit-output/evidence/audit_body_dry_run.log
body_build_status=${PIPESTATUS[0]}

{
  echo '$ kprove audit-spec-body-sensitivity.k --definition /tmp/audit-work/rebuilt-verification-kompiled --spec-module AUDIT-SPEC-BODY-SENSITIVITY'
  kprove audit-spec-body-sensitivity.k \
    --definition "$definition" \
    --spec-module AUDIT-SPEC-BODY-SENSITIVITY
  status=$?
  echo "EXIT_STATUS=$status"
  exit "$status"
} 2>&1 | tee /audit-output/evidence/audit_body_failure.log
body_proof_status=${PIPESTATUS[0]}

vacuity_warning_status=1
body_warning_status=1
rg -q 'WarnStuckClaimState' \
  /audit-output/evidence/audit_vacuity_failure.log
vacuity_warning_status=$?
rg -q 'WarnStuckClaimState' \
  /audit-output/evidence/audit_body_failure.log
body_warning_status=$?

echo \
  "SUMMARY vacuity_build=$vacuity_build_status" \
  "vacuity_proof=$vacuity_proof_status" \
  "vacuity_stuck_warning=$vacuity_warning_status" \
  "body_build=$body_build_status" \
  "body_proof=$body_proof_status" \
  "body_stuck_warning=$body_warning_status"

test "$vacuity_build_status" -eq 0 \
  && test "$vacuity_proof_status" -ne 0 \
  && test "$vacuity_warning_status" -eq 0 \
  && test "$body_build_status" -eq 0 \
  && test "$body_proof_status" -ne 0 \
  && test "$body_warning_status" -eq 0
