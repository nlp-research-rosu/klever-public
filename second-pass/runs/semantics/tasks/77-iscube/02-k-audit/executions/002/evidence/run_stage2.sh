#!/usr/bin/env bash
set -uo pipefail

overall=0

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
}

printf '%s\n' 'COMMAND: python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/candidate/solution.regenerated.mpy'
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/candidate/solution.regenerated.mpy
status=$?
printf 'EXIT_STATUS: %s\n' "$status"
if (( status != 0 )); then
  overall=1
fi

run sha256sum \
  /tmp/audit-work/candidate/solution.mpy \
  /tmp/audit-work/candidate/solution.regenerated.mpy
run cmp -s \
  /tmp/audit-work/candidate/solution.mpy \
  /tmp/audit-work/candidate/solution.regenerated.mpy
run python3 /audit-output/evidence/differential_test.py

exit "$overall"
