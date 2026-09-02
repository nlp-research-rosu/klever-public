#!/usr/bin/env bash
set -eu

out=/tmp/audit-work/159-eat/solution-body-mutated.mpy
python3 /tmp/audit-work/159-eat/trusted/py2mpy.py \
  /audit-output/evidence/solution-body-mutated.py >"$out"

printf 'MUTATED_MPY_SHA256='
sha256sum "$out"
printf 'SUBMITTED_MPY_SHA256='
sha256sum /tmp/audit-work/159-eat/candidate-src/solution.mpy
if cmp -s "$out" /tmp/audit-work/159-eat/candidate-src/solution.mpy; then
  printf 'IDENTITY_CHECK=UNEXPECTED_MATCH\n'
  exit 1
fi
printf 'IDENTITY_CHECK=EXPECTED_MISMATCH\n'
