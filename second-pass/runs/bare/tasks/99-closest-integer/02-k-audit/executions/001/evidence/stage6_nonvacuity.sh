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

run cp /audit-output/evidence/spec-vacuity-audit.k \
  "$SOURCE/spec-vacuity-audit.k"
run kprove "$SOURCE/spec-vacuity-audit.k" \
  --definition "$DEFINITION" \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run
run kprove "$SOURCE/spec-vacuity-audit.k" \
  --definition "$DEFINITION" \
  --spec-module SPEC-VACUITY-AUDIT
