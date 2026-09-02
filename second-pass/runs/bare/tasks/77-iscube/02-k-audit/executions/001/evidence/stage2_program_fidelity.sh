#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/77-iscube

printf '$ python3 /reference/py2mpy.py %s > %s\n' \
  "$scratch/candidate-src/solution.py" "$scratch/regenerated-solution.mpy"
python3 /reference/py2mpy.py "$scratch/candidate-src/solution.py" \
  > "$scratch/regenerated-solution.mpy"
regen_status=$?
printf '[exit %d]\n' "$regen_status"

run cmp -s "$scratch/regenerated-solution.mpy" /candidate/solution.mpy
run sha256sum "$scratch/regenerated-solution.mpy" /candidate/solution.mpy
run python3 /audit-output/evidence/differential_test.py
run python3 /audit-output/evidence/canonical_precision_probe.py
