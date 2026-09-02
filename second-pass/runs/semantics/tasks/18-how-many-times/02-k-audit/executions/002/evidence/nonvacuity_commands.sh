#!/usr/bin/env bash
set -u

cd /tmp/audit-work/fresh || exit 90

echo '$ kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module HOW-MANY-TIMES-SPEC-VACUITY-AUDIT --dry-run'
kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module HOW-MANY-TIMES-SPEC-VACUITY-AUDIT \
  --dry-run
dry_status=$?
echo "exit_status=$dry_status"

echo '$ kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module HOW-MANY-TIMES-SPEC-VACUITY-AUDIT'
set +e
kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module HOW-MANY-TIMES-SPEC-VACUITY-AUDIT \
  2>&1 | tee /audit-output/evidence/nonvacuity-kprove.raw.log
proof_status=${PIPESTATUS[0]}
set -e
echo "exit_status=$proof_status (expected nonzero)"

echo '$ rg -n "WarnStuckClaimState|implication check|cannot be rewritten further" /audit-output/evidence/nonvacuity-kprove.raw.log'
rg -n \
  'WarnStuckClaimState|implication check|cannot be rewritten further' \
  /audit-output/evidence/nonvacuity-kprove.raw.log
residual_status=$?
echo "exit_status=$residual_status"

if (( dry_status != 0 || proof_status == 0 || residual_status != 0 )); then
  exit 1
fi
exit 0
