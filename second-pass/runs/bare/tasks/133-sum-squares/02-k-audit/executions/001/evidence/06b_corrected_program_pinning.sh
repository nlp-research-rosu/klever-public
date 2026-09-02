#!/usr/bin/env bash
set -u

log=/audit-output/evidence/06b_corrected_program_pinning.log
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

printf '\nCOMMAND: kast spec-program.mpy --definition audit-semantic-kompiled > spec-program.kast\n'
kast spec-program.mpy --definition audit-semantic-kompiled > spec-program.kast
printf 'EXIT_STATUS: %d\n' "$?"
run cmp -s solution.kast spec-program.kast
run sha256sum solution.kast spec-program.kast
