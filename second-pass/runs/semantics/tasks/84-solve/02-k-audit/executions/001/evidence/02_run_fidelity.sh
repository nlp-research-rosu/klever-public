#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

printf '\n$ python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/regenerated-solution.mpy\n'
python3 /reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
rc=$?
printf '[exit %d]\n' "$rc"
run cmp \
  /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
run sha256sum \
  /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
run python3 /audit-output/evidence/02_differential.py
