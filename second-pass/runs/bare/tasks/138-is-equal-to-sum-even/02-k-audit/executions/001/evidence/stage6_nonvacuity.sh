#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  set +e
  "$@"
  status=$?
  set -e
  printf '[exit %d]\n' "$status"
  return "$status"
}

set -e
source_dir=/tmp/audit-work/review-138/candidate-src
definition=/tmp/audit-work/review-138/build/verification-kompiled

run cmp -s \
  "$source_dir/spec-vacuity.k" \
  /audit-output/evidence/spec-vacuity.k

run kprove "$source_dir/spec-vacuity.k" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY \
  --dry-run

printf '\n$ kprove %q --definition %q --spec-module SPEC-VACUITY\n' \
  "$source_dir/spec-vacuity.k" "$definition"
set +e
proof_output=$(
  kprove "$source_dir/spec-vacuity.k" \
    --definition "$definition" \
    --spec-module SPEC-VACUITY 2>&1
)
proof_status=$?
set -e
printf '%s\n' "$proof_output"
printf '[exit %d; expected nonzero]\n' "$proof_status"

test "$proof_status" -ne 0
test "${proof_output#*WarnStuckClaimState}" != "$proof_output"
test "${proof_output#*BoolValue}" != "$proof_output"
printf 'EXPECTED_FAILURE_CONFIRMED=true\n'
