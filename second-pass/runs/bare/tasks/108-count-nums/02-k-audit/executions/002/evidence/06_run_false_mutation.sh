#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT_STATUS=%s\n" "$status"' EXIT
set -x

SCRATCH=/tmp/audit-work/108-count-nums
cd "$SCRATCH"
cp /audit-output/evidence/spec-vacuity-audit.k "$SCRATCH/spec-vacuity-audit.k"

kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run
dry_run_status=$?
printf "DRY_RUN_EXIT_STATUS=%s\n" "$dry_run_status"

set +e
timeout --signal=TERM --kill-after=10 120 \
  kprove spec-vacuity-audit.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY-AUDIT \
  2>&1 | tee /audit-output/evidence/06_false_mutation_kprove.raw.log
proof_status=${PIPESTATUS[0]}
set -e

printf "EXPECTED_PROOF_FAILURE_STATUS=%s\n" "$proof_status"
test "$dry_run_status" -eq 0
test "$proof_status" -ne 0
test "$proof_status" -ne 124
test "$proof_status" -ne 137
grep -F 'WarnStuckClaimState' /audit-output/evidence/06_false_mutation_kprove.raw.log
grep -F 'IntV ( 0 )' /audit-output/evidence/06_false_mutation_kprove.raw.log
grep -F '=> IntV(1)' /audit-output/evidence/spec-vacuity-audit.k
