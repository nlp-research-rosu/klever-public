#!/usr/bin/env bash
set -u

cd /tmp/audit-work/fresh || exit 125
echo '$ cp /audit-output/evidence/spec-vacuity.k /tmp/audit-work/fresh/spec-vacuity.k'
cp /audit-output/evidence/spec-vacuity.k /tmp/audit-work/fresh/spec-vacuity.k
copy_status=$?
echo "EXIT: $copy_status"

echo '$ kprove spec-vacuity.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY --dry-run --output none'
kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run \
  --output none
build_status=$?
echo "EXIT: $build_status"

echo '$ kprove spec-vacuity.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY --output pretty'
kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --output pretty
proof_status=$?
echo "EXIT: $proof_status"

if [ "$copy_status" -eq 0 ] && [ "$build_status" -eq 0 ] && [ "$proof_status" -ne 0 ]; then
  echo "EXPECTED_FALSE_POSTCONDITION_FAILURE: PASS"
  exit 0
fi
echo "EXPECTED_FALSE_POSTCONDITION_FAILURE: FAIL"
exit 1
