#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruction
cp /audit-output/evidence/06_false_result.k audit-false-result.k

printf '%s\n' 'SATISFYING WITNESS: N=4; true result=288; mutated obligation=292'
python3 -c 'import canonical, solution; n=4; print("canonical=", canonical.special_factorial(n)); print("candidate=", solution.special_factorial(n)); print("false_destination=", solution.special_factorial(n)+n)'
witness_status=$?
printf 'WITNESS_EXIT: %s\n' "$witness_status"

printf '%s\n' 'COMMAND: kprove audit-false-result.k --definition audit-verification-kompiled --spec-module AUDIT-FALSE-RESULT --dry-run'
kprove audit-false-result.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT \
  --dry-run > audit-false-result.dry-run 2>&1
dry_status=$?
printf 'DRY_RUN_EXIT: %s\n' "$dry_status"
wc -l -c audit-false-result.dry-run
sed -n '1,60p' audit-false-result.dry-run

printf '%s\n' 'COMMAND: kprove audit-false-result.k --definition audit-verification-kompiled --spec-module AUDIT-FALSE-RESULT'
kprove audit-false-result.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT > audit-false-result.residual 2>&1
proof_status=$?
printf 'FALSE_PROOF_EXIT: %s\n' "$proof_status"
rg -n 'WarnStuckClaimState|productAfter|\\+Int N|#Equals|backend terminated' \
  audit-false-result.residual
residual_match_status=$?
printf 'EXPECTED_RESIDUAL_MATCH_EXIT: %s\n' "$residual_match_status"
sed -n '1,220p' audit-false-result.residual

if [ "$witness_status" -ne 0 ] || [ "$dry_status" -ne 0 ] || [ "$proof_status" -eq 0 ] || [ "$residual_match_status" -ne 0 ]; then
  exit 1
fi
exit 0
