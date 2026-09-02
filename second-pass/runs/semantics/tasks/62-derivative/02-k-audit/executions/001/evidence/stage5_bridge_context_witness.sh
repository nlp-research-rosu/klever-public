#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/62-derivative
cp --no-dereference \
  /audit-output/evidence/spec-bridge-context-candidate.k \
  /audit-output/evidence/spec-bridge-context-fixed.k \
  "$scratch/"
cd "$scratch" || exit 70

printf '%s\n' 'CANDIDATE_EXTENDED_CONTEXT_EXPECTS: true'
timeout 300 kprove spec-bridge-context-candidate.k \
  --definition verification-kompiled \
  --spec-module SPEC-BRIDGE-CONTEXT-CANDIDATE \
  --claims candidate-empty-enum-truthiness
candidate_status=$?
printf 'CANDIDATE_CONTEXT_EXIT_STATUS: %d\n' "$candidate_status"

printf '%s\n' 'FIXED_SEMANTICS_CONTEXT_EXPECTS: false'
timeout 300 kprove spec-bridge-context-fixed.k \
  --definition no-bridge-kompiled \
  --spec-module SPEC-BRIDGE-CONTEXT-FIXED \
  --claims fixed-empty-enum-truthiness
fixed_status=$?
printf 'FIXED_CONTEXT_EXIT_STATUS: %d\n' "$fixed_status"

if (( candidate_status != 0 || fixed_status != 0 )); then
  exit 1
fi
