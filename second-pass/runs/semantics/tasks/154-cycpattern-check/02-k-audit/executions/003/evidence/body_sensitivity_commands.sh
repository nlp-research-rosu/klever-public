#!/usr/bin/env bash
set -u

cd /tmp/audit-work/fresh || exit 125
echo '$ cp /audit-output/evidence/spec-body-mutation.k /tmp/audit-work/fresh/spec-body-mutation.k'
cp /audit-output/evidence/spec-body-mutation.k /tmp/audit-work/fresh/spec-body-mutation.k
copy_status=$?
echo "EXIT: $copy_status"
echo '$ kprove spec-body-mutation.k --definition audit-verification-kompiled --spec-module SPEC-BODY-MUTATION --output pretty'
kprove spec-body-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --output pretty
proof_status=$?
echo "EXIT: $proof_status"
if [ "$copy_status" -eq 0 ] && [ "$proof_status" -ne 0 ]; then
  echo "EXPECTED_BODY_SENSITIVITY_FAILURE: PASS"
  exit 0
fi
echo "EXPECTED_BODY_SENSITIVITY_FAILURE: FAIL"
exit 1
