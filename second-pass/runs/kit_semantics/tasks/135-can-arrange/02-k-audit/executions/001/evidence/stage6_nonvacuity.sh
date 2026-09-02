#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/135-can-arrange
definition="$scratch/verification-audit-kompiled"

echo 'COMMAND: kprove fresh mutation --dry-run (must build)'
set +e
kprove /audit-output/evidence/stage6-false-result.k \
  --definition "$definition" \
  --spec-module REVIEWER-FRESH-NONVACUITY \
  -I "$scratch" \
  --dry-run \
  2>&1 | tee /audit-output/evidence/stage6_mutation_dry_run.log
dry_status=${PIPESTATUS[0]}
set -e
echo "EXIT [mutation dry run]: $dry_status"
if test "$dry_status" -ne 0; then exit 1; fi

echo 'COMMAND: kprove fresh false result mutation (must fail meaningfully)'
set +e
kprove /audit-output/evidence/stage6-false-result.k \
  --definition "$definition" \
  --spec-module REVIEWER-FRESH-NONVACUITY \
  -I "$scratch" \
  2>&1 | tee /audit-output/evidence/stage6_mutation_kprove.log
prove_status=${PIPESTATUS[0]}
set -e
echo "EXIT [mutation proof, expected nonzero]: $prove_status"

if test "$prove_status" -eq 0; then exit 1; fi
grep -q 'WarnStuckClaimState' \
  /audit-output/evidence/stage6_mutation_kprove.log || exit 1
grep -q -- '-1 ~> .K' \
  /audit-output/evidence/stage6_mutation_kprove.log || exit 1
exit 0
