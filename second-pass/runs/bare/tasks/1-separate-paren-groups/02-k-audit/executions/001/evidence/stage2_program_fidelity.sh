#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

printf '%s\n' '$ python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/candidate/solution.regenerated.mpy'
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/candidate/solution.regenerated.mpy
printf '[exit %d]\n' "$?"

run cmp -s \
  /tmp/audit-work/candidate/solution.regenerated.mpy \
  /tmp/audit-work/candidate/solution.mpy
run sha256sum \
  /tmp/audit-work/candidate/solution.regenerated.mpy \
  /tmp/audit-work/candidate/solution.mpy
run python3 /audit-output/evidence/differential_test.py
