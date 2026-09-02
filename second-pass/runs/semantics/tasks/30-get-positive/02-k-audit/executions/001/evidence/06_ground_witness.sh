#!/usr/bin/env bash
set -u

work=/tmp/audit-work/30-get-positive
failed=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  if test "$status" -ne 0; then
    failed=1
  fi
}

run python3 /audit-output/evidence/06_ground_compare.py

run kprove "$work/ground-spec.k" \
  --definition "$work/verification-kompiled" \
  --spec-module GROUND-SPEC \
  --claims GROUND-SPEC.filter-loop,GROUND-SPEC.ground-entry \
  --trusted GROUND-SPEC.filter-loop \
  --smt-timeout 10000

exit "$failed"

