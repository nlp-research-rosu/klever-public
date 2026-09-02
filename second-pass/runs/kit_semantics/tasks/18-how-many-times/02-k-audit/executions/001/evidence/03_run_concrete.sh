#!/usr/bin/env bash
set -u

cd /tmp/audit-work/review/candidate-src
printf 'PWD=%s\n' "$PWD"
printf '%s\n' \
  'COMMAND: python3 /tmp/audit-work/review/trusted/py2mpy.py /audit-output/evidence/03_concrete_cases.py > audit-concrete-cases.mpy'
python3 /tmp/audit-work/review/trusted/py2mpy.py \
  /audit-output/evidence/03_concrete_cases.py > audit-concrete-cases.mpy
translate_status=$?
printf 'TRANSLATE_CONCRETE_EXIT=%s\n' "$translate_status"
cp audit-concrete-cases.mpy /audit-output/evidence/03_concrete_cases.mpy

printf '%s\n' \
  'COMMAND: krun audit-concrete-cases.mpy --definition audit-runtime-kompiled'
krun audit-concrete-cases.mpy --definition audit-runtime-kompiled
krun_status=$?
printf 'KRUN_CONCRETE_EXIT=%s\n' "$krun_status"
if [ "$translate_status" -ne 0 ] || [ "$krun_status" -ne 0 ]; then
  exit 1
fi
