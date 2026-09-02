#!/usr/bin/env bash
set -u

work=/tmp/audit-work/30-get-positive/candidate-src
cd "$work" || exit 90

printf 'WITNESS input=[1] original_precondition_satisfied=True python_expected=[1] mutated_expected=[]\n'
kprove spec-vacuity.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.wrong-result \
  --dry-run
dry_status=$?
printf 'STATUS mutation_dry_run=%s\n' "$dry_status"

kprove spec-vacuity.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.wrong-result
proof_status=$?
printf 'STATUS mutation_proof_expected_nonzero=%s\n' "$proof_status"

if [ "$dry_status" -eq 0 ] && [ "$proof_status" -ne 0 ]; then
  exit 0
fi
exit 1
