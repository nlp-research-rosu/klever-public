#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/reconstruction
mutation=/audit-output/evidence/spec-vacuity-audit.k
dry_output="$scratch/reviewer-vacuity-dry-run.out"
proof_output="$scratch/reviewer-vacuity-kprove.out"

kprove "$mutation" \
  --definition "$scratch/proof-kompiled" \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run \
  -I "$scratch" \
  -w none > "$dry_output" 2>&1
dry_status=$?
sed -n '1,60p' "$dry_output"
printf 'MUTATION_DRY_RUN_EXIT=%d\n' "$dry_status"

set +e
kprove "$mutation" \
  --definition "$scratch/proof-kompiled" \
  --spec-module SPEC-VACUITY-AUDIT \
  --output pretty \
  -I "$scratch" \
  -w none > "$proof_output" 2>&1
proof_status=$?
set -e
sed -n '1,180p' "$proof_output"
printf 'FALSE_MUTATION_PROOF_EXIT=%d\n' "$proof_status"
if [ "$proof_status" -eq 0 ]; then
  printf 'UNEXPECTED_FALSE_MUTATION_TOP=true\n'
  exit 1
fi
grep -Fq 'WarnStuckClaimState' "$proof_output"
grep -Fq 'Result ( VList ( "aa" , .Words ) )' "$proof_output"
printf 'EXPECTED_UNMET_RESULT_OBLIGATION_CONFIRMED=true\n'
