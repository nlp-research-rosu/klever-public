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

printf '[trusted translator regeneration]\n'
run bash -c 'python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/proof-audit/solution.regenerated.mpy'
run cmp -s /candidate/solution.mpy /tmp/audit-work/proof-audit/solution.regenerated.mpy
run sha256sum /candidate/solution.mpy /tmp/audit-work/proof-audit/solution.regenerated.mpy
run diff -u /candidate/solution.mpy /tmp/audit-work/proof-audit/solution.regenerated.mpy

printf '[independent canonical-versus-generated differential]\n'
run python3 /audit-output/evidence/differential_test.py
