#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/62-derivative
cp --no-dereference /audit-output/evidence/spec-ground.k "$scratch/spec-ground.k"
cd "$scratch" || exit 70

for label in ground-empty ground-example
do
  printf 'GROUND_CLAIM: %s\n' "$label"
  timeout 300 kprove spec-ground.k \
    --definition verification-kompiled \
    --spec-module SPEC-GROUND \
    --claims "$label"
  status=$?
  printf 'GROUND_CLAIM_EXIT_STATUS: %d\n' "$status"
  if (( status != 0 )); then
    exit "$status"
  fi
done
