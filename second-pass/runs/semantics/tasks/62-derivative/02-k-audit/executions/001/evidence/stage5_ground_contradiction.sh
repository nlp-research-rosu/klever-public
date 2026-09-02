#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/62-derivative
cp --no-dereference \
  /audit-output/evidence/spec-bridge-ground-candidate-false.k \
  "$scratch/"
cd "$scratch" || exit 70

timeout 300 kprove spec-bridge-ground-candidate-false.k \
  --definition verification-kompiled \
  --spec-module SPEC-BRIDGE-GROUND-CANDIDATE-FALSE \
  --claims candidate-ground-empty-is-empty
status=$?
printf 'GROUND_EMPTY_FALSE_EXIT_STATUS: %d\n' "$status"
exit "$status"
