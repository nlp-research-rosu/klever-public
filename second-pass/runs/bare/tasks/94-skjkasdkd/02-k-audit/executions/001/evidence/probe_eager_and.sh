#!/usr/bin/env bash
set -uo pipefail

source_dir=/tmp/audit-work/94-skjkasdkd/source
definition=/tmp/audit-work/94-skjkasdkd/build/semantic-kompiled

echo "PYTHON_COMMAND: python3 -c 'print(False and (1 % 0))'"
python3 -c 'print(False and (1 % 0))'
python_status=$?
echo "PYTHON_EXIT: $python_status"

echo "KRUN_COMMAND: krun eager-and-witness.mpy --definition $definition -cARGS=listVal()"
k_output=$(krun "$source_dir/eager-and-witness.mpy" \
  --definition "$definition" \
  '-cARGS=listVal()' 2>&1)
k_status=$?
printf '%s\n' "$k_output"
echo "KRUN_EXIT: $k_status"

if [[ "$python_status" -eq 0 && "$k_output" == *"result ( boolVal ( false ) )"* ]]; then
  echo "SEMANTIC_MATCH: PASS"
  exit 0
fi

echo "SEMANTIC_MATCH: FAIL (expected out-of-program witness)"
exit 1
