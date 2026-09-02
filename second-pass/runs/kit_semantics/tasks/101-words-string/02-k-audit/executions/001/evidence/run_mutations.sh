#!/usr/bin/env bash
set -u

definition=/tmp/audit-work/reconstruction/verification-fresh-kompiled

echo 'COMMAND: kprove /audit-output/evidence/audit-spec-vacuity.k --definition /tmp/audit-work/reconstruction/verification-fresh-kompiled --spec-module AUDIT-SPEC-VACUITY --dry-run'
kprove /audit-output/evidence/audit-spec-vacuity.k \
  --definition "$definition" \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run
vacuity_build_status=$?
echo "EXIT_STATUS: $vacuity_build_status"

echo 'COMMAND: kprove /audit-output/evidence/audit-spec-vacuity.k --definition /tmp/audit-work/reconstruction/verification-fresh-kompiled --spec-module AUDIT-SPEC-VACUITY'
kprove /audit-output/evidence/audit-spec-vacuity.k \
  --definition "$definition" \
  --spec-module AUDIT-SPEC-VACUITY
vacuity_proof_status=$?
echo "EXIT_STATUS: $vacuity_proof_status"

echo 'COMMAND: kprove /audit-output/evidence/audit-spec-body-sensitivity.k --definition /tmp/audit-work/reconstruction/verification-fresh-kompiled --spec-module AUDIT-SPEC-BODY-SENSITIVITY --dry-run'
kprove /audit-output/evidence/audit-spec-body-sensitivity.k \
  --definition "$definition" \
  --spec-module AUDIT-SPEC-BODY-SENSITIVITY \
  --dry-run
body_build_status=$?
echo "EXIT_STATUS: $body_build_status"

echo 'COMMAND: kprove /audit-output/evidence/audit-spec-body-sensitivity.k --definition /tmp/audit-work/reconstruction/verification-fresh-kompiled --spec-module AUDIT-SPEC-BODY-SENSITIVITY'
kprove /audit-output/evidence/audit-spec-body-sensitivity.k \
  --definition "$definition" \
  --spec-module AUDIT-SPEC-BODY-SENSITIVITY
body_proof_status=$?
echo "EXIT_STATUS: $body_proof_status"

if [[ $vacuity_build_status -ne 0 || $body_build_status -ne 0 ]]; then
  echo 'MUTATION_BUILD_RESULT: FAIL'
  exit 1
fi
if [[ $vacuity_proof_status -eq 0 || $body_proof_status -eq 0 ]]; then
  echo 'MUTATION_REJECTION_RESULT: FAIL'
  exit 1
fi
echo 'MUTATION_BUILD_RESULT: PASS'
echo 'MUTATION_REJECTION_RESULT: PASS'
