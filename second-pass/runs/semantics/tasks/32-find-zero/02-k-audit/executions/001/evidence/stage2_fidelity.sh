#!/usr/bin/env bash
set +e

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return "$status"
}

printf 'COMMAND: python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/32-find-zero/regenerated-solution.mpy\n'
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/32-find-zero/regenerated-solution.mpy
printf 'EXIT_STATUS: %d\n' "$?"

run cmp /tmp/audit-work/32-find-zero/regenerated-solution.mpy /candidate/solution.mpy
run sha256sum /tmp/audit-work/32-find-zero/regenerated-solution.mpy /candidate/solution.mpy
run python3 /audit-output/evidence/differential_test.py
