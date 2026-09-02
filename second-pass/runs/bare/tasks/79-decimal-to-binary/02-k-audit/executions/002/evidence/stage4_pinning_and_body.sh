#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/audit79
evidence=/audit-output/evidence
status=0
export PATH="$HOME/.nix-profile/bin:$PATH"

echo 'COMMAND: program_pinning.py solution.mpy spec.k'
python3 "$evidence/program_pinning.py" \
  "$audit_work/solution.mpy" "$audit_work/spec.k"
command_status=$?
echo "EXIT_STATUS $command_status"
if (( command_status != 0 )); then status=1; fi

echo 'COMMAND: cp spec-body-mutation.k scratch/spec-body-mutation.k'
cp "$evidence/spec-body-mutation.k" "$audit_work/spec-body-mutation.k"
command_status=$?
echo "EXIT_STATUS $command_status"
if (( command_status != 0 )); then status=1; fi

echo 'COMMAND: kprove spec-body-mutation.k --definition verification-kompiled --spec-module SPEC-BODY-MUTATION --dry-run'
kprove "$audit_work/spec-body-mutation.k" \
  --definition "$audit_work/verification-kompiled" \
  --spec-module SPEC-BODY-MUTATION \
  --dry-run
command_status=$?
echo "EXIT_STATUS $command_status"
if (( command_status != 0 )); then status=1; fi

echo 'COMMAND: kprove spec-body-mutation.k --definition verification-kompiled --spec-module SPEC-BODY-MUTATION'
kprove "$audit_work/spec-body-mutation.k" \
  --definition "$audit_work/verification-kompiled" \
  --spec-module SPEC-BODY-MUTATION
command_status=$?
echo "EXIT_STATUS $command_status (expected nonzero)"
if (( command_status == 0 )); then
  status=1
else
  echo 'EXPECTED_FAILURE_CONFIRMED'
fi

echo "SCRIPT_EXIT_STATUS $status"
exit "$status"
