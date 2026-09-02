#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit_status] %d\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/71-triangle-area
overall=0

printf 'Audit stage 2: program fidelity and candidate-versus-canonical checks\n'

printf '\n$ python3 /reference/py2mpy.py %s/solution.py > %s/regenerated.mpy\n' \
  "$scratch" "$scratch"
python3 /reference/py2mpy.py "$scratch/solution.py" > "$scratch/regenerated.mpy"
status=$?
printf '[exit_status] %d\n' "$status"
(( status == 0 )) || overall=1

run cmp -s "$scratch/regenerated.mpy" "$scratch/solution.mpy" || overall=1
run sha256sum "$scratch/regenerated.mpy" "$scratch/solution.mpy"

printf '\nCanonical/submitted source difference (expected: independently structured code)\n'
run diff -u /reference/canonical.py "$scratch/solution.py"

run python3 /audit-output/evidence/differential_test.py || overall=1

printf '\n[script_exit_status] %d\n' "$overall"
exit "$overall"
