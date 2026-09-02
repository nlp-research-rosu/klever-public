#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/111-histogram
overall_status=0

printf 'COMMAND: python3 py2mpy.py solution.py > regenerated-solution.mpy\n'
(
  cd "$audit_work" &&
  python3 py2mpy.py solution.py > regenerated-solution.mpy
)
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

printf 'COMMAND: cmp -s regenerated-solution.mpy solution.mpy\n'
(
  cd "$audit_work" &&
  cmp -s regenerated-solution.mpy solution.mpy
)
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

printf 'COMMAND: sha256sum regenerated-solution.mpy solution.mpy\n'
(
  cd "$audit_work" &&
  sha256sum regenerated-solution.mpy solution.mpy
)
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

printf 'COMMAND: python3 /audit-output/evidence/differential_test.py\n'
python3 /audit-output/evidence/differential_test.py
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

exit "$overall_status"
