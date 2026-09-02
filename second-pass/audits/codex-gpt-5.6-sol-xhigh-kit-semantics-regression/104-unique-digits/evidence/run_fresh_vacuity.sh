#!/usr/bin/env bash
set -u

work=/tmp/audit-work
evidence=/audit-output/evidence
cd "$work" || exit 90
cp "$evidence/spec-fresh-vacuity.k" spec-fresh-vacuity.k

dry_log="$evidence/06a-fresh-vacuity-dry-run.log"
echo '$ kprove spec-fresh-vacuity.k --definition audit-verification-kompiled --spec-module FRESH-VACUITY-SPEC --claims FRESH-VACUITY-SPEC.empty-returns-one --dry-run' \
  | tee "$dry_log"
kprove spec-fresh-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module FRESH-VACUITY-SPEC \
  --claims FRESH-VACUITY-SPEC.empty-returns-one \
  --dry-run \
  2>&1 | tee -a "$dry_log"
dry_status=${PIPESTATUS[0]}
echo "EXIT_STATUS=$dry_status" | tee -a "$dry_log"

proof_log="$evidence/06b-fresh-vacuity-proof.log"
echo '$ kprove spec-fresh-vacuity.k --definition audit-verification-kompiled --spec-module FRESH-VACUITY-SPEC --claims FRESH-VACUITY-SPEC.empty-returns-one' \
  | tee "$proof_log"
kprove spec-fresh-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module FRESH-VACUITY-SPEC \
  --claims FRESH-VACUITY-SPEC.empty-returns-one \
  2>&1 | tee -a "$proof_log"
proof_status=${PIPESTATUS[0]}
echo "EXIT_STATUS=$proof_status" | tee -a "$proof_log"

echo "EXPECTED dry_run=0 proof_nonzero OBSERVED dry_run=$dry_status proof=$proof_status"
if [[ "$dry_status" -ne 0 || "$proof_status" -eq 0 ]]; then
  exit 1
fi
exit 0
