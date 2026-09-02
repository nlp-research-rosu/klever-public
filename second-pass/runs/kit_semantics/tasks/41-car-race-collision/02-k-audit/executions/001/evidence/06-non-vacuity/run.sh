#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/candidate-src
definition=audit-verification-kompiled
mutation=audit-false-result.k
dry_output=/tmp/audit-work/non-vacuity-dry-run.out
proof_output=/tmp/audit-work/non-vacuity-proof.out

echo 'satisfying_witness: N=3'
echo 'real_result: 3 * 3 = 9'
echo 'mutated_result: (3 * 3) + 2 = 11'

echo
echo '$ kprove audit-false-result.k --definition audit-verification-kompiled --spec-module AUDIT-FALSE-RESULT --dry-run'
kprove "$mutation" \
  --definition "$definition" \
  --spec-module AUDIT-FALSE-RESULT \
  --dry-run >"$dry_output" 2>&1
dry_status=$?
echo "exit_status=$dry_status"
echo "captured_bytes=$(wc -c < "$dry_output")"
sed -n '1,60p' "$dry_output"
test "$dry_status" -eq 0 || exit 93

echo
echo '$ kprove audit-false-result.k --definition audit-verification-kompiled --spec-module AUDIT-FALSE-RESULT'
kprove "$mutation" \
  --definition "$definition" \
  --spec-module AUDIT-FALSE-RESULT >"$proof_output" 2>&1
proof_status=$?
echo "exit_status=$proof_status"
echo "captured_bytes=$(wc -c < "$proof_output")"
echo '--- expected-obligation diagnostics ---'
rg -n -C 3 \
  'WarnStuckClaimState|implication check|#Equals|cannot be rewritten further|backend terminated' \
  "$proof_output" || true
echo '--- bounded tail ---'
tail -n 80 "$proof_output"

test "$proof_status" -ne 0 || {
  echo 'ERROR: false result mutation unexpectedly proved'
  exit 94
}
rg -q 'WarnStuckClaimState' "$proof_output" || {
  echo 'ERROR: mutation failed without expected stuck-claim diagnostic'
  exit 95
}
rg -q 'implication check between the conditions has failed' "$proof_output" || {
  echo 'ERROR: mutation failed for an unrelated reason'
  exit 96
}
echo 'NON_VACUITY: PASS (expected proof failure)'
