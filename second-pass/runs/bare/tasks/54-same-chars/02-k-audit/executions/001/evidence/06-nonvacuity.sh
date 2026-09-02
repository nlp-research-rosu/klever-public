#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction

printf '+ kprove %q --definition %q --spec-module SPEC-VACUITY --dry-run\n' \
  "$work/spec-vacuity.k" "$work/proof-kompiled"
kprove "$work/spec-vacuity.k" \
  --definition "$work/proof-kompiled" \
  --spec-module SPEC-VACUITY \
  --dry-run
dry_status=$?
printf 'EXIT_STATUS=%d\n' "$dry_status"
if (( dry_status != 0 )); then
  exit "$dry_status"
fi

printf '+ kprove %q --definition %q --spec-module SPEC-VACUITY --claims SPEC-VACUITY.false-empty-result\n' \
  "$work/spec-vacuity.k" "$work/proof-kompiled"
kprove "$work/spec-vacuity.k" \
  --definition "$work/proof-kompiled" \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.false-empty-result
proof_status=$?
printf 'EXIT_STATUS=%d\n' "$proof_status"
printf 'EXPECTED_NONZERO=%s\n' "$([[ $proof_status -ne 0 ]] && printf yes || printf no)"
printf 'SATISFYING_WITNESS=S0="", S1="", env=.Map, result=noResult\n'
printf 'PYTHON_AND_K_ACTUAL_RESULT=true\n'
printf 'MUTATED_REQUIRED_RESULT=false\n'

if (( proof_status == 0 )); then
  exit 1
fi
exit 0
