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

run python3 /audit-output/evidence/decimal_context_witness.py
run cp /audit-output/evidence/unsound-witness-spec.k \
  "$SOURCE/unsound-witness-spec.k"
run kprove "$SOURCE/unsound-witness-spec.k" \
  --definition "$DEFINITION" \
  --spec-module UNSOUND-WITNESS-SPEC \
  --claims UNSOUND-WITNESS-SPEC.positive-context-witness
run kprove "$SOURCE/unsound-witness-spec.k" \
  --definition "$DEFINITION" \
  --spec-module UNSOUND-WITNESS-SPEC \
  --claims UNSOUND-WITNESS-SPEC.negative-context-witness
