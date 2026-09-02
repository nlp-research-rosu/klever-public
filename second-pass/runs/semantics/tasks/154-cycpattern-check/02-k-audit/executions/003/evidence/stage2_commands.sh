#!/usr/bin/env bash
set -u

run() {
  echo "\$ $*"
  "$@"
  status=$?
  echo "EXIT: $status"
  return "$status"
}

run mkdir -p /tmp/audit-work/fresh
run cp /candidate/solution.py /tmp/audit-work/fresh/solution.py
run cp /candidate/solution.mpy /tmp/audit-work/fresh/solution.mpy
run cp /candidate/spec.k /tmp/audit-work/fresh/spec.k
run cp /candidate/verification.k /tmp/audit-work/fresh/verification.k
run cp /candidate/concrete_tests.py /tmp/audit-work/fresh/concrete_tests.py
run cp /candidate/concrete_tests.mpy /tmp/audit-work/fresh/concrete_tests.mpy
run cp /reference/py2mpy.py /tmp/audit-work/fresh/py2mpy.py
run cp /reference/prompt.py /tmp/audit-work/fresh/prompt.py
run cp /reference/canonical.py /tmp/audit-work/fresh/canonical.py
run cp -a /reference/reference-semantics /tmp/audit-work/fresh/reference-semantics
run python3 /tmp/audit-work/fresh/py2mpy.py /tmp/audit-work/fresh/solution.py
echo "\$ python3 /tmp/audit-work/fresh/py2mpy.py /tmp/audit-work/fresh/solution.py > /tmp/audit-work/fresh/solution.regenerated.mpy"
python3 /tmp/audit-work/fresh/py2mpy.py /tmp/audit-work/fresh/solution.py > /tmp/audit-work/fresh/solution.regenerated.mpy
status=$?
echo "EXIT: $status"
run cmp /tmp/audit-work/fresh/solution.mpy /tmp/audit-work/fresh/solution.regenerated.mpy
run sha256sum /tmp/audit-work/fresh/solution.mpy /tmp/audit-work/fresh/solution.regenerated.mpy
run python3 /audit-output/evidence/differential_test.py
