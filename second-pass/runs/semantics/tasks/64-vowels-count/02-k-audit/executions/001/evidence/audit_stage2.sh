#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

printf '$ python3 /reference/py2mpy.py /tmp/audit-work/fresh/solution.py > /tmp/audit-work/fresh/solution.regenerated.mpy\n'
python3 /reference/py2mpy.py /tmp/audit-work/fresh/solution.py \
  > /tmp/audit-work/fresh/solution.regenerated.mpy
status=$?
printf '[exit %d]\n' "$status"
run cmp -s /tmp/audit-work/fresh/solution.regenerated.mpy /candidate/solution.mpy
run sha256sum /tmp/audit-work/fresh/solution.regenerated.mpy /candidate/solution.mpy
run diff -u /candidate/solution.mpy /tmp/audit-work/fresh/solution.regenerated.mpy
run python3 /audit-output/evidence/differential_test.py
