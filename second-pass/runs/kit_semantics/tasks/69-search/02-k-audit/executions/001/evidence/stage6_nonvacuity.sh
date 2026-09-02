#!/usr/bin/env bash
set -uo pipefail
set -x

cd /tmp/audit-work/reconstruction
status=0
python3 /audit-output/evidence/make_audit_mutations.py
mutation_generation_exit=$?
printf 'mutation_generation_exit=%s\n' "$mutation_generation_exit"
if [[ "$mutation_generation_exit" != 0 ]]; then
  status=1
fi

cp /audit-output/evidence/audit_false_result.k audit_false_result.k
kprove audit_false_result.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT \
  2>&1 |
  tail -n 240 |
  tee /audit-output/evidence/stage6_false_result_bounded.log
mutation_exit="${PIPESTATUS[0]}"
printf 'false_result_kprove_exit=%s\n' "$mutation_exit"

if [[ "$mutation_exit" == 0 ]] ||
   grep -qx '#Top' /audit-output/evidence/stage6_false_result_bounded.log ||
   ! grep -q 'WarnStuckClaimState' /audit-output/evidence/stage6_false_result_bounded.log; then
  status=1
fi

printf 'stage6_nonvacuity_exit=%s\n' "$status"
exit "$status"
