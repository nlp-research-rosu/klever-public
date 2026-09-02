#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ command: '
set -x

cd /tmp/audit-work/candidate
cmp -s \
  auditor-false-result.k \
  /audit-output/evidence/10_auditor_false_result.k
printf 'preserved_mutation_cmp_exit=%s\n' "$?"

set +e
kprove auditor-false-result.k \
  --definition auditor-verification-kompiled \
  --spec-module AUDITOR-FALSE-RESULT \
  > /audit-output/evidence/10_mutation_kprove.raw.log 2>&1
proof_status=$?
set -e
printf 'auditor_false_result_kprove_exit=%s\n' "$proof_status"

rg -n -F 'WarnStuckClaimState' \
  /audit-output/evidence/10_mutation_kprove.raw.log
stuck_check=$?
rg -n -F '0 |-> list ( vCons ( 1 , .ValSeq ) )' \
  /audit-output/evidence/10_mutation_kprove.raw.log
actual_result_check=$?
rg -n -F 'backend terminated because the configuration cannot be' \
  /audit-output/evidence/10_mutation_kprove.raw.log
termination_check=$?
residual_check=$((stuck_check || actual_result_check || termination_check))
printf 'expected_residual_check_exit=%s\n' "$residual_check"

wc -lc /audit-output/evidence/10_mutation_kprove.raw.log
tail -n 120 /audit-output/evidence/10_mutation_kprove.raw.log

if [[ "$proof_status" -eq 0 || "$residual_check" -ne 0 ]]; then
  exit 1
fi
