#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run_shell() {
  printf '\n$ %s\n' "$1"
  bash -o pipefail -c "$1"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run_shell "python3 /reference/py2mpy.py /tmp/audit-work/69-search/solution.py > /tmp/audit-work/69-search/regenerated-solution.mpy"
run cmp -s /tmp/audit-work/69-search/regenerated-solution.mpy /candidate/solution.mpy
run sha256sum /tmp/audit-work/69-search/regenerated-solution.mpy /candidate/solution.mpy
run diff -u /candidate/solution.mpy /tmp/audit-work/69-search/regenerated-solution.mpy
run python3 /audit-output/evidence/differential_test.py
