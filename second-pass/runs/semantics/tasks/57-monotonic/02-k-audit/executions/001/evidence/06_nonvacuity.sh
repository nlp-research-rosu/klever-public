#!/usr/bin/env bash
set +e

WORK=/tmp/audit-work/57-monotonic

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run cp /audit-output/evidence/06_false_mutation.k "$WORK/spec-false-mutation.k"

run kprove "$WORK/spec-false-mutation.k" \
  --definition "$WORK/verification-kompiled" \
  --spec-module MONOTONIC-SPEC-FALSE-MUTATION \
  --dry-run

run kprove "$WORK/spec-false-mutation.k" \
  --definition "$WORK/verification-kompiled" \
  --spec-module MONOTONIC-SPEC-FALSE-MUTATION

run python3 -c \
  'import sys; sys.path.insert(0, "/tmp/audit-work/57-monotonic"); import canonical, solution; print("witness=[] canonical=", canonical.monotonic([]), "generated=", solution.monotonic([]))'
