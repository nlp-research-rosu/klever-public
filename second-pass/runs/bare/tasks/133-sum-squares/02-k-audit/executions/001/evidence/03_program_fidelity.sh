#!/usr/bin/env bash
set -u

log=/audit-output/evidence/03_program_fidelity.log
exec > >(tee "$log") 2>&1
scratch=/tmp/audit-work/133-sum-squares

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

printf 'COMMAND: cd %q\n' "$scratch"
cd "$scratch"
printf 'EXIT_STATUS: %d\n' "$?"

printf '\nCOMMAND: python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy\n'
python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy
printf 'EXIT_STATUS: %d\n' "$?"
run cmp -s solution.mpy regenerated-solution.mpy
run sha256sum solution.mpy regenerated-solution.mpy
run diff -u solution.mpy regenerated-solution.mpy
run python3 /audit-output/evidence/03_differential_test.py
