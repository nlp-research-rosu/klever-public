#!/usr/bin/env bash
set +e
cd /tmp/audit-work/build || exit 90

echo '$ kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module SPEC-VACUITY-AUDIT --dry-run'
kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run
build_status=$?
echo "exit=$build_status"

echo '$ kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module SPEC-VACUITY-AUDIT'
proof_output=$(
  kprove spec-vacuity-audit.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY-AUDIT 2>&1
)
proof_status=$?
printf '%s\n' "$proof_output"
echo "exit=$proof_status"

printf '%s\n' "$proof_output" | grep -q 'WarnStuckClaimState'
stuck_marker=$?
echo "stuck_marker_status=$stuck_marker"

printf '%s\n' "$proof_output" | grep -q 'IntVal ( 0 )'
actual_zero_marker=$?
echo "actual_zero_marker_status=$actual_zero_marker"

echo "summary dry_run=$build_status proof=$proof_status stuck_marker=$stuck_marker actual_zero_marker=$actual_zero_marker"
if (( build_status != 0 || proof_status == 0 || stuck_marker != 0 || actual_zero_marker != 0 )); then
  exit 1
fi
exit 0
