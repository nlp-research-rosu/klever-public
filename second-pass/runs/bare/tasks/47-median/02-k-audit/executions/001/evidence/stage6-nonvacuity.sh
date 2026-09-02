#!/usr/bin/env bash
set +e

record() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  return 0
}

mutation=/tmp/audit-work/47-median/candidate-src/spec-vacuity-audit.k
definition=/tmp/audit-work/47-median/build/proof-kompiled

record kprove "$mutation" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run
record kprove "$mutation" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY-AUDIT
