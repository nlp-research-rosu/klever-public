#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

SCRATCH=/tmp/audit-work/candidate
DEF="$SCRATCH/verification-kompiled"

printf '%s\n' 'Stage 6: fresh false-result mutation'
printf '%s\n' 'Witness: numbers=[1,2,3], delimeter=4'
printf '%s\n' 'True result:  [1,4,2,4,3]'
printf '%s\n' 'False target: [1,4,2,4,4]'

run cp /audit-output/evidence/06_spec_vacuity.k "$SCRATCH/audit-spec-vacuity.k"
run kprove "$SCRATCH/audit-spec-vacuity.k" \
  --definition "$DEF" \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run
run kprove "$SCRATCH/audit-spec-vacuity.k" \
  --definition "$DEF" \
  --spec-module AUDIT-SPEC-VACUITY
