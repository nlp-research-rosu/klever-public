#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/stage5_body_sensitivity.log
scratch=/tmp/audit-work/review-34-unique
exec >"$log" 2>&1

echo "STAGE 5 FRESH BODY-SENSITIVITY MUTATION"
echo "COMMAND: copy reviewer body mutation into scratch"
cp /audit-output/evidence/stage5_body_sensitivity.k "$scratch/stage5_body_sensitivity.k"
status=$?
echo "EXIT: $status"
if [[ "$status" -ne 0 ]]; then
  exit "$status"
fi

echo "COMMAND: kprove body mutation --dry-run"
set +e
kprove "$scratch/stage5_body_sensitivity.k" \
  --definition "$scratch/audit-verification-kompiled" \
  --spec-module AUDIT-BODY-SENSITIVITY \
  --dry-run 2>&1 | sed -n '1,140p'
dry_status=${PIPESTATUS[0]}
set -e
echo "EXIT: $dry_status"
if [[ "$dry_status" -ne 0 ]]; then
  echo "ERROR: body mutation did not parse/build"
  exit 93
fi

echo "COMMAND: kprove reviewer always-append body against original unique result"
set +e
kprove "$scratch/stage5_body_sensitivity.k" \
  --definition "$scratch/audit-verification-kompiled" \
  --spec-module AUDIT-BODY-SENSITIVITY 2>&1 | sed -n '1,320p'
proof_status=${PIPESTATUS[0]}
set -e
echo "EXIT: $proof_status"
if [[ "$proof_status" -eq 0 ]]; then
  echo "ERROR: changed body unexpectedly used the original theorem"
  exit 94
fi
echo "EXPECTED_BODY_SENSITIVITY_FAILURE: $proof_status"
