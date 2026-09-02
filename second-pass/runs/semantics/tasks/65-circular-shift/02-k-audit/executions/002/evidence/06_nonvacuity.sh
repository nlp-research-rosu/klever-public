#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
cd "$scratch" || exit 2

echo '$ cp scratch mutation to reviewer evidence'
cp spec-vacuity.k "$evidence/06_spec_vacuity.k"
copy_status=$?
echo "EXIT_STATUS=$copy_status"
sha256sum spec-vacuity.k "$evidence/06_spec_vacuity.k"

echo '$ kprove false-result mutation --dry-run'
kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run \
  --warnings none \
  2>&1 | tee "$evidence/06a_mutation_dry_run.log"
dry_status=${PIPESTATUS[0]}
echo "EXIT_STATUS=$dry_status" | tee -a "$evidence/06a_mutation_dry_run.log"

echo '$ kprove false-result mutation (expected unmet result obligation)'
kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  --warnings none \
  2>&1 | tee "$evidence/06b_mutation_proof.log"
proof_status=${PIPESTATUS[0]}
echo "EXIT_STATUS=$proof_status" | tee -a "$evidence/06b_mutation_proof.log"

echo "EXPECTED: copy=0 dry_run=0 proof_nonzero_with_WarnStuckClaimState"
echo "OBSERVED: copy=$copy_status dry_run=$dry_status proof=$proof_status"

if (( copy_status != 0 || dry_status != 0 || proof_status == 0 )); then
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' "$evidence/06b_mutation_proof.log"; then
  echo 'FAIL: mutation did not fail with WarnStuckClaimState'
  exit 1
fi
if ! rg -Fq 'iCons ( 50 , iCons ( 49' "$evidence/06b_mutation_proof.log"; then
  echo 'FAIL: residual did not expose actual "21" code sequence'
  exit 1
fi
exit 0
