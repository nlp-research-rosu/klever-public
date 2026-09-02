#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/102-choose-num
printf 'Stage 2 translator regeneration and independent differential testing\n'

printf '\n$ cd %q && python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy\n' "$scratch"
(
  cd "$scratch" || exit 125
  python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy
)
status=$?
printf '[exit %d]\n' "$status"

run cmp -s "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
run sha256sum "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
run diff -u "$scratch/solution.mpy" "$scratch/regenerated-solution.mpy"
run python3 /audit-output/evidence/differential_test.py
