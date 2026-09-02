#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

fresh=/tmp/audit-work/fresh
run mkdir -p "$fresh/reference-semantics"
run cp /candidate/solution.py "$fresh/solution.py"
run cp /candidate/solution.mpy "$fresh/submitted-solution.mpy"
run cp /candidate/verification.k "$fresh/verification.k"
run cp /candidate/spec.k "$fresh/spec.k"
run cp /reference/py2mpy.py "$fresh/py2mpy.py"
run cp -a /reference/reference-semantics/. "$fresh/reference-semantics/"

printf '$ python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/fresh/regenerated-solution.mpy\n'
python3 /reference/py2mpy.py /candidate/solution.py > "$fresh/regenerated-solution.mpy"
status=$?
printf '[exit %d]\n' "$status"

run cmp -s "$fresh/regenerated-solution.mpy" /candidate/solution.mpy
run sha256sum "$fresh/regenerated-solution.mpy" /candidate/solution.mpy
run python3 /audit-output/evidence/02_differential.py
