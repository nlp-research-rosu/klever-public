#!/usr/bin/env bash
set -u

run_shell() {
  local command_text="$1"
  printf 'COMMAND: %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf 'EXIT_STATUS: %s\n\n' "$status"
  return 0
}

run_shell "python3 /reference/py2mpy.py /tmp/audit-work/source/solution.py > /tmp/audit-work/regenerated-solution.mpy"
run_shell "cmp --silent /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/source/solution.mpy"
run_shell "sha256sum /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/source/solution.mpy"
run_shell "python3 /audit-output/evidence/stage2/differential.py"

