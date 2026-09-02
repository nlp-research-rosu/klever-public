#!/usr/bin/env bash
set -euo pipefail
set -x

export PATH="$HOME/.nix-profile/bin:$PATH"
cd /tmp/audit-work/35-max-element

set +e
kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run \
  > /audit-output/evidence/stage6-vacuity-dry-run.raw.log 2>&1
mutation_build_status=$?
set -e
echo "MUTATION_DRY_RUN_EXIT=$mutation_build_status"
sed -n '1,180p' /audit-output/evidence/stage6-vacuity-dry-run.raw.log
test "$mutation_build_status" -eq 0

set +e
kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  > /audit-output/evidence/stage6-vacuity-kprove.raw.log 2>&1
mutation_proof_status=$?
set -e
echo "MUTATION_KPROVE_EXIT=$mutation_proof_status"
sed -n '1,260p' /audit-output/evidence/stage6-vacuity-kprove.raw.log
test "$mutation_proof_status" -ne 0
rg -n 'WarnStuckClaimState|result \\( 3 \\)|cannot be rewritten further' \
  /audit-output/evidence/stage6-vacuity-kprove.raw.log
