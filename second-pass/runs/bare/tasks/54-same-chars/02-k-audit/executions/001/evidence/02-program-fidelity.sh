#!/usr/bin/env bash
set -u

run() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS=%d\n' "$status"
  return "$status"
}

printf '+ python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/fresh/solution.py > /tmp/audit-work/fresh/regenerated-solution.mpy\n'
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/fresh/solution.py \
  > /tmp/audit-work/fresh/regenerated-solution.mpy
status=$?
printf 'EXIT_STATUS=%d\n' "$status"

run cmp /tmp/audit-work/fresh/regenerated-solution.mpy \
  /tmp/audit-work/fresh/solution.mpy
run sha256sum /tmp/audit-work/fresh/regenerated-solution.mpy \
  /tmp/audit-work/fresh/solution.mpy
run python3 /audit-output/evidence/02-differential.py
