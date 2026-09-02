#!/usr/bin/env bash
set -u
set -o pipefail
cd /tmp/audit-work/audit147 || exit 99

echo '$ cmp -s spec-vacuity.k /audit-output/evidence/spec-vacuity.k'
cmp -s spec-vacuity.k /audit-output/evidence/spec-vacuity.k
status=$?
echo "exit_status=$status"
if [ "$status" -ne 0 ]; then exit 1; fi

echo '$ kprove spec-vacuity.k --definition fresh-verification-kompiled --spec-module SPEC-VACUITY --dry-run > vacuity-dry-run.kore'
kprove spec-vacuity.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run > vacuity-dry-run.kore
build_status=$?
echo "dry_run_exit_status=$build_status"
if [ "$build_status" -ne 0 ]; then
  echo "RESULT=FAIL mutation did not build"
  exit 1
fi

echo '$ kprove spec-vacuity.k --definition fresh-verification-kompiled --spec-module SPEC-VACUITY'
kprove spec-vacuity.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-VACUITY 2>&1 | tee vacuity-proof.raw.log
proof_status=${PIPESTATUS[0]}
echo "proof_exit_status=$proof_status"

grep -q 'WarnStuckClaimState' vacuity-proof.raw.log
stuck_status=$?
echo "WarnStuckClaimState_present=$([ "$stuck_status" -eq 0 ] && echo yes || echo no)"

echo 'satisfying_witness=N=5; actual_result=1; false_mutated_result=2'
if [ "$proof_status" -ne 0 ] && [ "$stuck_status" -eq 0 ]; then
  echo "RESULT=EXPECTED_MEANINGFUL_FAILURE"
  exit 0
fi

echo "RESULT=FAIL mutation did not fail with the expected unmet obligation"
exit 1
