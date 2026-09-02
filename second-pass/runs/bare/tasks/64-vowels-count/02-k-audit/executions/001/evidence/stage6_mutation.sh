#!/usr/bin/env bash
set -u
set -x

cp /audit-output/evidence/spec-vacuity-audit.k \
  /tmp/audit-work/candidate-src/spec-vacuity-audit.k

timeout 300s kprove \
  /tmp/audit-work/candidate-src/spec-vacuity-audit.k \
  --definition /tmp/audit-work/verification-fresh-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run \
  --output pretty \
  > /tmp/audit-work/stage6-dry-run.out 2>&1
dry_run_exit=$?
sed -n '1,160p' /tmp/audit-work/stage6-dry-run.out

timeout 300s kprove \
  /tmp/audit-work/candidate-src/spec-vacuity-audit.k \
  --definition /tmp/audit-work/verification-fresh-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --output pretty \
  > /tmp/audit-work/stage6-proof.out 2>&1
proof_exit=$?
sed -n '1,260p' /tmp/audit-work/stage6-proof.out

printf 'dry_run_exit=%s\n' "$dry_run_exit"
printf 'proof_exit=%s (expected nonzero)\n' "$proof_exit"
test "$dry_run_exit" -eq 0
test "$proof_exit" -ne 0
grep -q 'WarnStuckClaimState' /tmp/audit-work/stage6-proof.out
grep -q 'backend terminated because the configuration cannot be' \
  /tmp/audit-work/stage6-proof.out
