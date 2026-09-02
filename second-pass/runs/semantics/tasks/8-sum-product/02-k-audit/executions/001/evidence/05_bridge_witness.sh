#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/reconstruction
cd "$WORK" || exit 99

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS: %d\n' "$rc"
  return 0
}

run cp /audit-output/evidence/bridge-fixed-spec.k "$WORK/bridge-fixed-spec.k"
run cp /audit-output/evidence/bridge-enabled-spec.k "$WORK/bridge-enabled-spec.k"

printf '\nFIXED_SEMANTICS_EXPECTED_SCOPE_ZERO_UPDATES\n'
run kprove bridge-fixed-spec.k \
  --definition verification-kompiled \
  --spec-module LOOP-BRIDGE-FIXED-WITNESS \
  --output pretty

printf '\nBRIDGE_CONTEXT_REJECTION_EXPECTED_FAILURE\n'
run kprove bridge-enabled-spec.k \
  --definition verification-lemma-kompiled \
  --spec-module LOOP-BRIDGE-ENABLED-WITNESS \
  --output pretty
