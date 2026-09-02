#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT=%s\n" "$status"' EXIT
set -x

audit_work=/tmp/audit-work/audit149
cd "$audit_work"
cp /audit-output/evidence/spec-vacuity-audit.k spec-vacuity-audit.k

kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --claims audit-false-result \
  --dry-run \
  -w none \
  > audit-vacuity-dry-run.out 2>&1
dry_status=$?
printf 'VACUITY_DRY_RUN_EXIT=%s\n' "$dry_status"
sed -n '1,120p' audit-vacuity-dry-run.out
if (( dry_status != 0 )); then
  exit 1
fi

set +e
kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --claims audit-false-result \
  --output pretty \
  -w none \
  > audit-vacuity-proof.out 2>&1
proof_status=$?
set -e
printf 'VACUITY_PROOF_EXIT=%s\n' "$proof_status"
sed -n '1,240p' audit-vacuity-proof.out

if (( proof_status == 0 )); then
  printf 'UNEXPECTED_VACUITY_SUCCESS\n'
  exit 1
fi
if ! grep -Fq 'WarnStuckClaimState' audit-vacuity-proof.out; then
  printf 'MISSING_EXPECTED_STUCK_CLAIM\n'
  exit 1
fi
if ! grep -Fq 'AUDIT_SENTINEL' audit-vacuity-proof.out; then
  printf 'MISSING_MUTATED_RESULT_IN_RESIDUAL\n'
  exit 1
fi
printf 'EXPECTED_FALSE_RESULT_REJECTED witness=INPUT:.Words\n'
