#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  set +e
  "$@"
  status=$?
  set -e
  printf '[exit %d]\n' "$status"
  return "$status"
}

set -e

run python3 /tmp/audit-work/review-138/reference-src/py2mpy.py \
  /tmp/audit-work/review-138/candidate-src/solution.py

printf '\n$ python3 /tmp/audit-work/review-138/reference-src/py2mpy.py /tmp/audit-work/review-138/candidate-src/solution.py > /tmp/audit-work/review-138/regenerated-solution.mpy\n'
set +e
python3 /tmp/audit-work/review-138/reference-src/py2mpy.py \
  /tmp/audit-work/review-138/candidate-src/solution.py \
  > /tmp/audit-work/review-138/regenerated-solution.mpy
status=$?
set -e
printf '[exit %d]\n' "$status"
test "$status" -eq 0

run cmp -s \
  /tmp/audit-work/review-138/regenerated-solution.mpy \
  /tmp/audit-work/review-138/candidate-src/solution.mpy
run sha256sum \
  /tmp/audit-work/review-138/regenerated-solution.mpy \
  /tmp/audit-work/review-138/candidate-src/solution.mpy
run python3 /audit-output/evidence/differential_test.py
