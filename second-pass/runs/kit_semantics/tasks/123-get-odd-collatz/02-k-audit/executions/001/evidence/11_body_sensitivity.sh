#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ command: '
set -x

cd /tmp/audit-work/candidate
sha256sum spec-body-mutation.k

set +e
kprove spec-body-mutation.k \
  --definition auditor-verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  > /audit-output/evidence/11_body_mutation_kprove.raw.log 2>&1
proof_status=$?
set -e
printf 'body_mutation_kprove_exit=%s\n' "$proof_status"

rg -n -F 'WarnStuckClaimState' \
  /audit-output/evidence/11_body_mutation_kprove.raw.log
stuck_check=$?
rg -n -F 'vCons ( 1 , vCons ( 2 , vCons ( 2 , .ValSeq ) ) )' \
  /audit-output/evidence/11_body_mutation_kprove.raw.log
result_check=$?
printf 'body_mutation_stuck_check_exit=%s\n' "$stuck_check"
printf 'body_mutation_result_check_exit=%s\n' "$result_check"

wc -lc /audit-output/evidence/11_body_mutation_kprove.raw.log
tail -n 120 /audit-output/evidence/11_body_mutation_kprove.raw.log

if [[ "$proof_status" -eq 0 || "$stuck_check" -ne 0 || "$result_check" -ne 0 ]]; then
  exit 1
fi
