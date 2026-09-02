#!/usr/bin/env bash
set -u

export PATH="/home/agent/.nix-profile/bin:$PATH"

echo "Satisfying witness: N=15, D=14."
echo "The real/candidate summary is firstDivisorAtOrBelow(15,14)=5;"
echo "the mutated destination demands 6."
echo

echo '$ cp /audit-output/evidence/stage6_false_result.k /tmp/audit-work/stage6_false_result.k'
cp /audit-output/evidence/stage6_false_result.k /tmp/audit-work/stage6_false_result.k
copy_rc=$?
printf '[exit %d]\n\n' "$copy_rc"

echo '$ kprove stage6_false_result.k --definition verification-kompiled --spec-module AUDIT-FALSE-RESULT --dry-run'
(
  cd /tmp/audit-work || exit 1
  kprove stage6_false_result.k \
    --definition verification-kompiled \
    --spec-module AUDIT-FALSE-RESULT \
    --dry-run
)
dry_rc=$?
printf '[exit %d]\n\n' "$dry_rc"

proof_log=/audit-output/evidence/stage6_false_result_proof.log
echo '$ kprove stage6_false_result.k --definition verification-kompiled --spec-module AUDIT-FALSE-RESULT'
(
  cd /tmp/audit-work || exit 1
  kprove stage6_false_result.k \
    --definition verification-kompiled \
    --spec-module AUDIT-FALSE-RESULT
) 2>&1 | tee "$proof_log"
proof_rc=${PIPESTATUS[0]}
printf '[exit %d]\n\n' "$proof_rc"

echo '$ rg -n "WarnStuckClaimState|implication check|cannot be rewritten|firstDivisorAtOrBelow|\\+Int" /audit-output/evidence/stage6_false_result_proof.log'
rg -n \
  'WarnStuckClaimState|implication check|cannot be rewritten|firstDivisorAtOrBelow|\+Int' \
  "$proof_log"
residual_rc=$?
printf '[exit %d]\n\n' "$residual_rc"

if (( copy_rc != 0 || dry_rc != 0 )); then
  echo "ERROR: the mutation did not build cleanly."
  exit 1
fi
if (( proof_rc == 0 )); then
  echo "ERROR: the false result mutation unexpectedly proved."
  exit 1
fi
if (( residual_rc != 0 )); then
  echo "ERROR: expected unmet-obligation residual was not found."
  exit 1
fi
echo "EXPECTED FAILURE CONFIRMED: build succeeded; proof failed on the false result."
