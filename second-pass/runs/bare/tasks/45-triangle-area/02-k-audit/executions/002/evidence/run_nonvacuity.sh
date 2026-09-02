#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate || exit 1

printf '%s\n' '$ kprove spec-vacuity.k --definition proof-kompiled --spec-module SPEC-VACUITY --dry-run'
dry_output="$(
  kprove spec-vacuity.k \
    --definition proof-kompiled \
    --spec-module SPEC-VACUITY \
    --dry-run 2>&1
)"
dry_status=$?
printf '%s\n' "$dry_output"
printf '[exit %d]\n' "$dry_status"
if (( dry_status != 0 )); then
  printf '%s\n' 'ERROR: false mutation did not compile to KORE'
  exit 1
fi

printf '%s\n' '$ kprove spec-vacuity.k --definition proof-kompiled --spec-module SPEC-VACUITY'
proof_output="$(
  kprove spec-vacuity.k \
    --definition proof-kompiled \
    --spec-module SPEC-VACUITY 2>&1
)"
proof_status=$?
printf '%s\n' "$proof_output"
printf '[exit %d]\n' "$proof_status"
if (( proof_status == 0 )); then
  printf '%s\n' 'ERROR: false postcondition unexpectedly proved'
  exit 1
fi
if [[ "$proof_output" != *WarnStuckClaimState* ]]; then
  printf '%s\n' 'ERROR: false mutation failed for a reason other than the unmet obligation'
  exit 1
fi
if [[ "$proof_output" != *'PyNum ( 15 , 2 )'* ]]; then
  printf '%s\n' 'ERROR: residual did not expose the real result PyNum(15,2)'
  exit 1
fi
printf '%s\n' 'EXPECTED: satisfiable input (5,3) reaches PyNum(15,2), not mutated PyNum(16,2)'
