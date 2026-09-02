#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/fruit67/candidate || exit 99
echo "SATISFYING_WITNESS: A=5 O=6 N=19; actual=8; mutated destination=9"
echo "COMMAND: kprove spec-vacuity-audit.k --definition audit-verification-haskell-kompiled --spec-module SPEC-VACUITY-AUDIT"
kprove spec-vacuity-audit.k \
  --definition audit-verification-haskell-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
status=$?
echo "KPROVE_EXIT_STATUS=$status"
if [[ "$status" -ne 0 ]]; then
  echo "EXPECTED_FALSE_MUTATION_FAILURE=true"
  exit 0
fi
echo "EXPECTED_FALSE_MUTATION_FAILURE=false"
exit 1
