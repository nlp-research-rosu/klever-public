#!/usr/bin/env bash
set -euo pipefail
export PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

cd /tmp/audit-work/reconstruction

timeout 300 kprove reviewer-false-result.k \
  --definition reviewer-verification-kompiled \
  --spec-module REVIEWER-FALSE-RESULT \
  --dry-run
echo "FRESH_FALSE_MUTATION_BUILD_DRY_RUN_EXIT=$?"

set +e
timeout 600 kprove reviewer-false-result.k \
  --definition reviewer-verification-kompiled \
  --spec-module REVIEWER-FALSE-RESULT
false_proof_rc=$?
set -e
echo "FRESH_FALSE_MUTATION_PROOF_EXPECTED_NONZERO_EXIT=$false_proof_rc"
test "$false_proof_rc" -ne 0
