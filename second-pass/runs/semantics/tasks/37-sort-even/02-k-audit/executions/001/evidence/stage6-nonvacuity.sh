#!/usr/bin/env bash
set -u

work=/tmp/audit-work/37-sort-even-audit/reconstruction-fresh
evidence=/audit-output/evidence
dry_log=$evidence/stage6-mutation-dry-run.log
proof_log=$evidence/stage6-mutation-proof.log

cd "$work" || exit 1

(
  echo '$ kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module SPEC-VACUITY-AUDIT --claims SPEC.loop-correct,SPEC-VACUITY-AUDIT.sort-even-false-empty-is-zero --trusted SPEC.loop-correct --dry-run'
  kprove spec-vacuity-audit.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY-AUDIT \
    --claims SPEC.loop-correct,SPEC-VACUITY-AUDIT.sort-even-false-empty-is-zero \
    --trusted SPEC.loop-correct \
    --dry-run
  dry_status=$?
  echo "exit=$dry_status"
  exit "$dry_status"
) > "$dry_log" 2>&1
dry_status=$?
echo "mutation_dry_run_exit=$dry_status"
if test "$dry_status" -ne 0; then
  exit 1
fi

(
  echo '$ kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module SPEC-VACUITY-AUDIT --claims SPEC.loop-correct,SPEC-VACUITY-AUDIT.sort-even-false-empty-is-zero --trusted SPEC.loop-correct --output pretty'
  kprove spec-vacuity-audit.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY-AUDIT \
    --claims SPEC.loop-correct,SPEC-VACUITY-AUDIT.sort-even-false-empty-is-zero \
    --trusted SPEC.loop-correct \
    --output pretty
  proof_status=$?
  echo "exit=$proof_status"
  exit "$proof_status"
) > "$proof_log" 2>&1
proof_status=$?
echo "mutation_proof_exit=$proof_status"

if test "$proof_status" -eq 0; then
  echo 'ERROR: false mutation unexpectedly proved'
  exit 1
fi

if rg -q 'WarnStuckClaimState|implication check between the conditions has failed' "$proof_log"; then
  echo 'expected_stuck_obligation=yes'
else
  echo 'ERROR: failure did not expose the expected stuck obligation'
  exit 1
fi

echo 'stage6_exit=0'
exit 0
