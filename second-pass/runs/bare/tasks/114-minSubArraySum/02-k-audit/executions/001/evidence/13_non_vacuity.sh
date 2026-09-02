#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run kprove spec-vacuity-audit.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run

run kprove spec-vacuity-audit.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY-AUDIT

run python3 -c \
  'from solution import minSubArraySum; assert minSubArraySum([7]) == 7; assert minSubArraySum([7]) != 8; print("witness [7]: actual=7 mutated=8, false obligation confirmed")'
