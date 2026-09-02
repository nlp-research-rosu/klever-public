#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return "$status"
}

printf '$ python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate-src/solution.py | cmp - /tmp/audit-work/candidate-src/solution.mpy\n'
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  | cmp - /tmp/audit-work/candidate-src/solution.mpy
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
test "$status" -eq 0

run sha256sum \
  /tmp/audit-work/candidate-src/solution.py \
  /tmp/audit-work/candidate-src/solution.mpy \
  /candidate/solution.py \
  /candidate/solution.mpy

run python3 /audit-output/evidence/differential_test.py
