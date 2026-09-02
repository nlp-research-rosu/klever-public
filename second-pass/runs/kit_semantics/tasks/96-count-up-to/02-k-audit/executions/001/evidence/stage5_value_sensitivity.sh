#!/usr/bin/env bash
set -euo pipefail
export PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

cd /tmp/audit-work/reconstruction

set +e
timeout 600 kprove spec-value-mutation.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC-VALUE-MUTATION-PRIME
prime_opposite_rc=$?
set -e
echo "PRIME_3_FORCED_FALSE_EXPECTED_NONZERO_EXIT=$prime_opposite_rc"
test "$prime_opposite_rc" -ne 0

set +e
timeout 600 kprove spec-value-mutation.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC-VALUE-MUTATION-COMPOSITE
composite_opposite_rc=$?
set -e
echo "COMPOSITE_4_FORCED_TRUE_EXPECTED_NONZERO_EXIT=$composite_opposite_rc"
test "$composite_opposite_rc" -ne 0
