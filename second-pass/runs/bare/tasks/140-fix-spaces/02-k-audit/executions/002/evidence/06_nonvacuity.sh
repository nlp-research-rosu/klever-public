#!/usr/bin/env bash
set -uo pipefail
set -x

kprove /tmp/audit-work/vacuity/spec-vacuity-ground.k \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC-VACUITY-GROUND \
  --dry-run
dry_run_status=$?

kprove /tmp/audit-work/vacuity/spec-vacuity-ground.k \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC-VACUITY-GROUND \
  2>&1 | tee /tmp/audit-work/vacuity/nonvacuity-proof-output.log
proof_status=${PIPESTATUS[0]}

rg -q 'WarnStuckClaimState|implication check.*failed' \
  /tmp/audit-work/vacuity/nonvacuity-proof-output.log
expected_residual_status=$?

set +x
printf '%s\n' \
  'SATISFYING_WITNESS: S=.PString, K=.K, INPUT="", ENV=.Env, RESULT=.K'
printf '%s\n' \
  'FALSE_OBLIGATION_AT_WITNESS: execution returns pyStr(.PString), mutation demands pyStr(ch("X") .PString)'
printf 'vacuity_dry_run_exit=%s\n' "$dry_run_status"
printf 'vacuity_proof_exit=%s\n' "$proof_status"
printf 'expected_stuck_residual_search_exit=%s\n' "$expected_residual_status"

if (( dry_run_status != 0 ||
      proof_status == 0 ||
      expected_residual_status != 0 )); then
  exit 1
fi
