#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/102-choose-num
mutation="$scratch/spec-vacuity.k"
definition="$scratch/verification-kompiled"

printf 'Stage 6 fresh false-result mutation\n'
run cp /audit-output/evidence/spec-vacuity.k "$mutation"
run kprove "$mutation" \
  --definition "$definition" \
  --spec-module CHOOSE-NUM-SPEC-VACUITY \
  --dry-run
run kprove "$mutation" \
  --definition "$definition" \
  --spec-module CHOOSE-NUM-SPEC-VACUITY \
  --claims CHOOSE-NUM-SPEC-VACUITY.false-off-by-two
