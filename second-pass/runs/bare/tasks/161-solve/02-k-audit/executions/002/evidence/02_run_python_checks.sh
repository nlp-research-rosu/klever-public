#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf 'Trusted translation fidelity:\n'
run bash -c 'python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/k-proof/regenerated-solution.mpy'
run cmp /tmp/audit-work/k-proof/regenerated-solution.mpy /candidate/solution.mpy
run sha256sum /tmp/audit-work/k-proof/regenerated-solution.mpy /candidate/solution.mpy

printf '\nIndependent Python differential:\n'
run python3 /audit-output/evidence/02_differential.py
