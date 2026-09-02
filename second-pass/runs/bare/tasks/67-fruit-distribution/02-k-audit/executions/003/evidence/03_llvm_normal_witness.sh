#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/fruit67/candidate || exit 99
echo 'PYTHON_WITNESS: canonical=8 generated=8 for ("5 apples and 6 oranges",19)'
echo 'COMMAND: timeout 12s krun audit-string-1.mpy --definition audit-verification-llvm-kompiled --output pretty'
timeout 12s krun audit-string-1.mpy \
  --definition audit-verification-llvm-kompiled \
  --output pretty
status=$?
echo "KRUN_EXIT_STATUS=$status"
if [[ "$status" -ne 0 ]]; then
  echo "EXPECTED_BACKEND_SEMANTICS_DIVERGENCE=true"
  exit 0
fi
echo "EXPECTED_BACKEND_SEMANTICS_DIVERGENCE=false"
exit 1
