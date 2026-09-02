#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/candidate-src
output=/tmp/audit-work/body-sensitivity-proof.out

echo 'satisfying_witness: N=3'
echo 'mutated_executed_body: return n - n'
echo 'mutated_actual_result: 0'
echo 'unchanged_claimed_result: 9'
echo
echo '$ kprove audit-body-mutation.k --definition audit-verification-kompiled --spec-module AUDIT-BODY-MUTATION --dry-run'
kprove audit-body-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-BODY-MUTATION \
  --dry-run >/tmp/audit-work/body-sensitivity-dry.out 2>&1
dry_status=$?
echo "exit_status=$dry_status"
test "$dry_status" -eq 0 || exit 97

echo
echo '$ kprove audit-body-mutation.k --definition audit-verification-kompiled --spec-module AUDIT-BODY-MUTATION'
kprove audit-body-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-BODY-MUTATION >"$output" 2>&1
proof_status=$?
echo "exit_status=$proof_status"
rg -n -C 4 \
  'WarnStuckClaimState|implication check|#Equals|cannot be rewritten further' \
  "$output" || true
tail -n 30 "$output"
test "$proof_status" -ne 0 || exit 98
rg -q 'WarnStuckClaimState' "$output" || exit 99
rg -q 'implication check between the conditions has failed' "$output" || exit 100
echo 'BODY_SENSITIVITY: PASS (material body mutation rejected)'
