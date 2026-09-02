#!/usr/bin/env bash
set -o pipefail

cd /tmp/audit-work/candidate-src || exit 90

echo 'WITNESS: input 5 satisfies the exact initial configuration; trusted canonical and candidate Python both return [1, 5], not [1, 7].'

echo 'COMMAND: kprove spec-vacuity-audit.k --definition /tmp/audit-work/verification-kompiled-audit --spec-module SPEC-VACUITY-AUDIT --dry-run'
kprove spec-vacuity-audit.k \
  --definition /tmp/audit-work/verification-kompiled-audit \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run
dry_run_rc=$?
echo "EXIT: $dry_run_rc"
if (( dry_run_rc != 0 )); then
  echo 'UNEXPECTED: mutation did not build'
  exit 1
fi

echo 'COMMAND: kprove spec-vacuity-audit.k --definition /tmp/audit-work/verification-kompiled-audit --spec-module SPEC-VACUITY-AUDIT --output pretty'
kprove spec-vacuity-audit.k \
  --definition /tmp/audit-work/verification-kompiled-audit \
  --spec-module SPEC-VACUITY-AUDIT \
  --output pretty \
  2>&1 | tee /tmp/audit-work/nonvacuity-proof-output.txt
proof_rc=${PIPESTATUS[0]}
echo "EXIT: $proof_rc"

grep -q 'WarnStuckClaimState' /tmp/audit-work/nonvacuity-proof-output.txt
stuck_warning_rc=$?
echo "WarnStuckClaimState_grep_exit=$stuck_warning_rc"

if (( proof_rc == 0 || stuck_warning_rc != 0 )); then
  echo 'UNEXPECTED: false reachable result was not rejected by a stuck claim'
  exit 1
fi

echo 'EXPECTED: mutation built, reached the result obligation, and failed with a stuck claim.'
