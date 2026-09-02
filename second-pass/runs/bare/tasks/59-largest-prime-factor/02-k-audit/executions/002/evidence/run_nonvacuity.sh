#!/usr/bin/env bash
set -u

work=/tmp/audit-work/59-largest-prime-factor
spec="$work/source/spec-vacuity.k"
definition="$work/build-stage3-fresh/verification-kompiled"
all_status=0

run_and_record() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local command_status=$?
  printf 'EXIT: %d\n' "$command_status"
  return "$command_status"
}

run_and_record kprove "$spec" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY \
  --dry-run \
  --output pretty \
  || all_status=1

printf '%s\n' 'EXPECTED FAILURE COMMAND FOLLOWS'
run_and_record kprove "$spec" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY \
  --output pretty
proof_status=$?
if (( proof_status == 0 )); then
  printf '%s\n' 'UNEXPECTED: false result mutation proved'
  all_status=1
else
  printf 'EXPECTED_NONZERO_CONFIRMED: %d\n' "$proof_status"
fi

exit "$all_status"
