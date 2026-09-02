#!/usr/bin/env bash
set -u

python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate-src/solution-body-mutated.py \
  > /tmp/audit-work/candidate-src/solution-body-mutated.mpy
mutation_translate_status=$?
printf 'translator exit=%d\n' "$mutation_translate_status"
if [[ "$mutation_translate_status" -ne 0 ]]; then
  exit "$mutation_translate_status"
fi

sha256sum \
  /tmp/audit-work/candidate-src/solution.mpy \
  /tmp/audit-work/candidate-src/solution-body-mutated.mpy
exit 0
