#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/75-is-multiply-prime/work
cp /audit-output/evidence/spec-vacuity.k ./spec-vacuity.k

# A successful dry run distinguishes a valid built mutation from a parse error.
kprove spec-vacuity.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run | tee spec-vacuity-dry-run.out

set +e
kprove spec-vacuity.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY 2>&1 | tee spec-vacuity-proof.out
vacuity_kprove_status=${PIPESTATUS[0]}
set -e

echo "kprove_exit=${vacuity_kprove_status}"
test "${vacuity_kprove_status}" -ne 0
rg -n 'WarnStuckClaimState|implication check.*failed|cannot be rewritten further' \
  spec-vacuity-proof.out
