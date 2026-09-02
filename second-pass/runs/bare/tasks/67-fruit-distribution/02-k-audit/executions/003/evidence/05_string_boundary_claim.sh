#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/fruit67/candidate || exit 99
echo 'PYTHON_WITNESS: canonical=8 generated=8 for ("5  apples and 6 oranges",19)'
echo 'COMMAND: kprove spec-string-boundary.k --definition audit-verification-haskell-kompiled --spec-module SPEC-STRING-BOUNDARY'
kprove spec-string-boundary.k \
  --definition audit-verification-haskell-kompiled \
  --spec-module SPEC-STRING-BOUNDARY
status=$?
echo "KPROVE_EXIT_STATUS=$status"
if [[ "$status" -ne 0 ]]; then
  echo "EXPECTED_SEMANTICS_GAP_FAILURE=true"
  exit 0
fi
echo "EXPECTED_SEMANTICS_GAP_FAILURE=false"
exit 1
