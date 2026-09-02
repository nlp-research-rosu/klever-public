#!/usr/bin/env bash
set -uo pipefail

SCRATCH=/tmp/audit-work/59-lpf
EVIDENCE=/audit-output/evidence
cd "$SCRATCH" || exit 1

echo "satisfying_witness: N=4 F=2 L=1 SC_keys={-1,0} CALLER=0 CONT=.K REST=.List"
echo "expected_false_obligation: lpfSpec(4,2)=2 but mutation demands 3"

echo "$ kprove spec-vacuity-reviewer.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY-REVIEWER --dry-run"
kprove spec-vacuity-reviewer.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-REVIEWER \
  --dry-run \
  > "$EVIDENCE/09_false_mutation_dry_run.log" 2>&1
dry_status=$?
echo "dry_run_exit=$dry_status"
if [ "$dry_status" -ne 0 ]; then
  tail -160 "$EVIDENCE/09_false_mutation_dry_run.log"
  exit "$dry_status"
fi

echo "$ timeout --foreground 45s kprove spec-vacuity-reviewer.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY-REVIEWER"
timeout --foreground 45s \
  kprove spec-vacuity-reviewer.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC-VACUITY-REVIEWER \
  > "$EVIDENCE/09_false_mutation_kprove.log" 2>&1
proof_status=$?
echo "kprove_exit=$proof_status"
tail -200 "$EVIDENCE/09_false_mutation_kprove.log"

if [ "$proof_status" -eq 0 ]; then
  echo "ERROR: false mutation unexpectedly proved"
  exit 1
fi
if [ "$proof_status" -eq 124 ]; then
  echo "ERROR: false mutation timed out"
  exit 1
fi
if ! rg -q 'WarnStuckClaimState|cannot be rewritten further' "$EVIDENCE/09_false_mutation_kprove.log"; then
  echo "ERROR: failure was not a stuck unmet obligation"
  exit 1
fi
echo "meaningful_false_mutation_rejected=true"
