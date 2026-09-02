#!/usr/bin/env bash
set -u

SOURCE=/tmp/audit-work/99-closest-integer/source
DEFINITION=/tmp/audit-work/99-closest-integer/build/verification-fresh-kompiled

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %d\n\n' "$status"
  return 0
}

run cp /audit-output/evidence/pinning-spec.k "$SOURCE/pinning-spec.k"
run kprove "$SOURCE/pinning-spec.k" \
  --definition "$DEFINITION" \
  --spec-module PINNING-SPEC
run python3 /audit-output/evidence/claim_witnesses.py
