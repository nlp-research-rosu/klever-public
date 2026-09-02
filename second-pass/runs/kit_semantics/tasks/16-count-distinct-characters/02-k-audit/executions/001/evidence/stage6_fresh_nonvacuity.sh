#!/usr/bin/env bash
set -u
set -o pipefail

exec > >(tee /audit-output/evidence/stage6-fresh-nonvacuity.log) 2>&1
set -x

cd /tmp/audit-work/reconstruction || exit 90

kprove spec-fresh-false.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-FRESH-FALSE \
  --dry-run > /audit-output/evidence/stage6-fresh-mutation-build.log 2>&1
build_status=$?
printf 'fresh_false_mutation_dry_run_exit=%d\n' "$build_status"

kprove spec-fresh-false.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-FRESH-FALSE \
  > /audit-output/evidence/stage6-fresh-mutation-proof.log 2>&1
proof_status=$?
printf 'fresh_false_mutation_kprove_exit=%d\n' "$proof_status"

rg -n 'WarnStuckClaimState|implication check|#Equals|terminated because' \
  /audit-output/evidence/stage6-fresh-mutation-proof.log
residual_status=$?
printf 'expected_unmet_obligation_residual_check_exit=%d\n' "$residual_status"

sed -n '1,240p' /audit-output/evidence/stage6-fresh-mutation-proof.log

if [[ "$build_status" -ne 0 ]] ||
   [[ "$proof_status" -eq 0 ]] ||
   [[ "$residual_status" -ne 0 ]]; then
  exit 1
fi
