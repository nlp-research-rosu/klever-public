#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/prime31
source=/audit-output/evidence/04_body_sensitivity_mutation.k
target="$scratch/audit-body-sensitivity.k"
definition="$scratch/reviewer-verification-kompiled"

echo '$ cp -a /audit-output/evidence/04_body_sensitivity_mutation.k /tmp/audit-work/prime31/audit-body-sensitivity.k'
cp -a "$source" "$target"
copy_status=$?
echo "EXIT: $copy_status"

cd "$scratch" || exit 2

echo '$ kprove audit-body-sensitivity.k --definition reviewer-verification-kompiled --spec-module AUDIT-BODY-SENSITIVITY --dry-run'
kprove "$target" \
  --definition "$definition" \
  --spec-module AUDIT-BODY-SENSITIVITY \
  --dry-run \
  > /audit-output/evidence/04_body_sensitivity_dry_run.log 2>&1
dry_status=$?
echo "EXIT: $dry_status"

echo '$ kprove audit-body-sensitivity.k --definition reviewer-verification-kompiled --spec-module AUDIT-BODY-SENSITIVITY'
kprove "$target" \
  --definition "$definition" \
  --spec-module AUDIT-BODY-SENSITIVITY \
  > /audit-output/evidence/04_body_sensitivity_kprove.log 2>&1
proof_status=$?
echo "EXIT: $proof_status"

if [[ $copy_status -ne 0 || $dry_status -ne 0 ]]; then
  echo 'RESULT=INVALID_TEST_SETUP'
  exit 2
fi
if [[ $proof_status -eq 0 ]]; then
  echo 'RESULT=UNEXPECTED_PROOF_SUCCESS'
  exit 1
fi
if ! grep -q 'WarnStuckClaimState' /audit-output/evidence/04_body_sensitivity_kprove.log; then
  echo 'RESULT=WRONG_FAILURE_MODE'
  exit 3
fi
echo 'RESULT=EXPECTED_BODY_SENSITIVITY'
exit 0
