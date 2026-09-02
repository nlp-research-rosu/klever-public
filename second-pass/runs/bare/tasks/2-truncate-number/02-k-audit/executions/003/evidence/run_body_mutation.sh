#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/source
set +e
kprove body-mutation-spec.k \
  --definition /tmp/audit-work/build/proof-kompiled \
  --spec-module BODY-MUTATION-SPEC 2>&1 \
  | tee /tmp/audit-work/body-mutation-kprove.out
status=${PIPESTATUS[0]}
set -e
echo "BODY_MUTATION_KPROVE_EXIT=$status"
test "$status" -ne 0
rg -q 'WarnStuckClaimState' /tmp/audit-work/body-mutation-kprove.out
echo "BODY_MUTATION_EXPECTED_STUCK_OK"
