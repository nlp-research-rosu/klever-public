#!/usr/bin/env bash
set -u

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %d\n\n' "$status"
  return 0
}

printf '%s\n' \
  'COMMAND: python3 /tmp/audit-work/99-closest-integer/trusted/py2mpy.py /tmp/audit-work/99-closest-integer/source/solution.py > /tmp/audit-work/99-closest-integer/build/regenerated.mpy'
python3 /tmp/audit-work/99-closest-integer/trusted/py2mpy.py \
  /tmp/audit-work/99-closest-integer/source/solution.py \
  > /tmp/audit-work/99-closest-integer/build/regenerated.mpy
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
run cmp \
  /tmp/audit-work/99-closest-integer/build/regenerated.mpy \
  /tmp/audit-work/99-closest-integer/source/solution.mpy
run sha256sum \
  /tmp/audit-work/99-closest-integer/build/regenerated.mpy \
  /tmp/audit-work/99-closest-integer/source/solution.mpy
run python3 /audit-output/evidence/differential.py
