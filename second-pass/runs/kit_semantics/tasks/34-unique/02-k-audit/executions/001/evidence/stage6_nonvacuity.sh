#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/stage6_nonvacuity.log
scratch=/tmp/audit-work/review-34-unique
exec >"$log" 2>&1

echo "STAGE 6 FRESH NON-VACUITY TEST"
echo "SATISFYING INPUT: [2,1,2]"
echo "TRUE RESULT: [1,2]"
echo "MUTATED REQUIRED RESULT: [1,3]"

echo "COMMAND: copy reviewer mutation into scratch for relative K requires"
cp /audit-output/evidence/stage6_false_mutation.k "$scratch/stage6_false_mutation.k"
copy_status=$?
echo "EXIT: $copy_status"
if [[ "$copy_status" -ne 0 ]]; then
  exit "$copy_status"
fi

echo "COMMAND: kprove $scratch/stage6_false_mutation.k --definition $scratch/audit-verification-kompiled --spec-module AUDIT-FRESH-FALSE-MUTATION --dry-run"
set +e
kprove "$scratch/stage6_false_mutation.k" \
  --definition "$scratch/audit-verification-kompiled" \
  --spec-module AUDIT-FRESH-FALSE-MUTATION \
  --dry-run 2>&1 | sed -n '1,160p'
dry_status=${PIPESTATUS[0]}
set -e
echo "EXIT: $dry_status"
if [[ "$dry_status" -ne 0 ]]; then
  echo "ERROR: mutation did not parse/build"
  exit 90
fi

echo "COMMAND: kprove $scratch/stage6_false_mutation.k --definition $scratch/audit-verification-kompiled --spec-module AUDIT-FRESH-FALSE-MUTATION"
set +e
kprove "$scratch/stage6_false_mutation.k" \
  --definition "$scratch/audit-verification-kompiled" \
  --spec-module AUDIT-FRESH-FALSE-MUTATION 2>&1 | sed -n '1,360p'
proof_status=${PIPESTATUS[0]}
set -e
echo "EXIT: $proof_status"

if [[ "$proof_status" -eq 0 ]]; then
  echo "ERROR: false result unexpectedly proved"
  exit 91
fi
echo "EXPECTED_NONVACUITY_FAILURE: $proof_status"
