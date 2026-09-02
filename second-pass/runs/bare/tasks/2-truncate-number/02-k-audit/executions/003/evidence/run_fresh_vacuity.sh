#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/source
set +e
kprove fresh-vacuity-spec.k \
  --definition /tmp/audit-work/build/proof-kompiled \
  --spec-module FRESH-VACUITY-SPEC 2>&1 \
  | tee /tmp/audit-work/fresh-vacuity-kprove.out
status=${PIPESTATUS[0]}
set -e
echo "FRESH_VACUITY_KPROVE_EXIT=$status"
test "$status" -ne 0
rg -q 'WarnStuckClaimState' /tmp/audit-work/fresh-vacuity-kprove.out
rg -q 'implication check between the conditions has failed' \
  /tmp/audit-work/fresh-vacuity-kprove.out
rg -q '#Equals' /tmp/audit-work/fresh-vacuity-kprove.out
echo "FRESH_VACUITY_EXPECTED_OBLIGATION_STUCK_OK"
