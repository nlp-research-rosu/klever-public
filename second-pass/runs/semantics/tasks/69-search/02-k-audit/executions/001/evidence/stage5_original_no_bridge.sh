#!/usr/bin/env bash
set -u

printf '$ /usr/bin/kprove original-spec-no-bridge.k --definition verification-no-bridge-kompiled --spec-module SEARCH-SPEC-NO-BRIDGE\n'
/usr/bin/kprove \
  original-spec-no-bridge.k \
  --definition verification-no-bridge-kompiled \
  --spec-module SEARCH-SPEC-NO-BRIDGE \
  2>&1 | tee /audit-output/evidence/stage5_original_no_bridge_failure.log
status=${PIPESTATUS[0]}
printf '[exit %d; nonzero expected]\n' "$status"
if (( status == 0 )); then
  printf 'ERROR: original target unexpectedly closed without bridge\n'
  exit 1
fi
if ! rg -q '#iterNext.*list|WarnStuckClaimState|cannot be rewritten further' \
     /audit-output/evidence/stage5_original_no_bridge_failure.log; then
  printf 'ERROR: expected fixed-semantics residual absent\n'
  exit 1
fi
