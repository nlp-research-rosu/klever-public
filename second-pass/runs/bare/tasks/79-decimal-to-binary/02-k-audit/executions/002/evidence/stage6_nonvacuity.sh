#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/audit79
evidence=/audit-output/evidence
status=0
export PATH="$HOME/.nix-profile/bin:$PATH"

echo 'WITNESS: I=0 satisfies I >=Int 0; Python result db0db differs from mutated db0dbx'
echo 'COMMAND: cp spec-vacuity.k scratch/spec-vacuity.k'
cp "$evidence/spec-vacuity.k" "$audit_work/spec-vacuity.k"
command_status=$?
echo "EXIT_STATUS $command_status"
if (( command_status != 0 )); then status=1; fi

echo 'COMMAND: kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY --dry-run'
kprove "$audit_work/spec-vacuity.k" \
  --definition "$audit_work/verification-kompiled" \
  --spec-module SPEC-VACUITY \
  --dry-run
command_status=$?
echo "EXIT_STATUS $command_status"
if (( command_status != 0 )); then status=1; fi

echo 'COMMAND: kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY'
kprove "$audit_work/spec-vacuity.k" \
  --definition "$audit_work/verification-kompiled" \
  --spec-module SPEC-VACUITY
command_status=$?
echo "EXIT_STATUS $command_status (expected nonzero)"
if (( command_status == 0 )); then
  status=1
else
  echo 'EXPECTED_FAILURE_CONFIRMED'
fi

echo "SCRIPT_EXIT_STATUS $status"
exit "$status"
