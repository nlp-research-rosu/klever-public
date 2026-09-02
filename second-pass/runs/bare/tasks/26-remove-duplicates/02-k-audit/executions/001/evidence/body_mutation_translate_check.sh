#!/usr/bin/env bash
set -u

python3 /tmp/audit-work/trusted/py2mpy.py \
  /audit-output/evidence/body_sensitivity_solution.py \
  > /tmp/audit-work/build/body-sensitivity.mpy

sha256sum \
  /tmp/audit-work/build/body-sensitivity.mpy \
  /tmp/audit-work/candidate-src/solution.mpy

if cmp -s \
  /tmp/audit-work/build/body-sensitivity.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
then
  printf 'UNEXPECTED: body mutation did not change translated AST\n'
  exit 1
fi

printf 'EXPECTED: body mutation changed translated AST\n'
