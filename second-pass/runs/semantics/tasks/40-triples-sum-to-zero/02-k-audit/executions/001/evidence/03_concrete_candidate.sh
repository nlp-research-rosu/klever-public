#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/forty-triples-audit
cd "$scratch/candidate-src" || exit 1

python3 "$scratch/trusted/py2mpy.py" concrete_tests.py \
  > "$scratch/regenerated-concrete-tests.mpy"
translate_status=$?
echo "CONCRETE_TRANSLATOR_EXIT_STATUS $translate_status"
if [[ "$translate_status" -ne 0 ]]; then
  exit "$translate_status"
fi
if cmp -s concrete_tests.mpy "$scratch/regenerated-concrete-tests.mpy"; then
  echo "CONCRETE_HARNESS_MPY_BYTE_IDENTITY OK"
else
  echo "CONCRETE_HARNESS_MPY_BYTE_IDENTITY FAIL"
  diff -u concrete_tests.mpy "$scratch/regenerated-concrete-tests.mpy" || true
  exit 1
fi

krun "$scratch/regenerated-concrete-tests.mpy" \
  --definition "$scratch/runtime-kompiled"
