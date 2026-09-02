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

run mkdir -p /tmp/audit-work/129-minpath
run cp /candidate/solution.py /tmp/audit-work/129-minpath/solution.py
run cp /candidate/solution.mpy /tmp/audit-work/129-minpath/solution.submitted.mpy
run cp /candidate/spec.k /tmp/audit-work/129-minpath/spec.k
run cp /candidate/verification.k /tmp/audit-work/129-minpath/verification.k
run cp /reference/py2mpy.py /tmp/audit-work/129-minpath/py2mpy.py
run cp -a /reference/reference-semantics /tmp/audit-work/129-minpath/reference-semantics

printf '\n$ python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/129-minpath/solution.regenerated.mpy\n'
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/129-minpath/solution.regenerated.mpy
status=$?
printf '[exit %d]\n' "$status"

run cmp /candidate/solution.mpy /tmp/audit-work/129-minpath/solution.regenerated.mpy
run sha256sum /candidate/solution.py /candidate/solution.mpy /tmp/audit-work/129-minpath/solution.regenerated.mpy
run python3 /audit-output/evidence/commands/differential_minpath.py
