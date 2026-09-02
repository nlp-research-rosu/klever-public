#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/137-compare-one-audit
definition="$work/concrete-kompiled"

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/concrete_python_oracle.py'
python3 /audit-output/evidence/concrete_python_oracle.py
oracle_status=$?
printf 'PYTHON ORACLE EXIT: %s\n' "$oracle_status"
(( oracle_status == 0 )) || exit "$oracle_status"

run_k_case() {
  case_id=$1
  a=$2
  b=$3
  printf 'COMMAND [%s]: timeout --signal=TERM --kill-after=2 12 krun solution.mpy --definition concrete-kompiled -cA=%s -cB=%s --output pretty\n' \
    "$case_id" "$a" "$b"
  timeout --signal=TERM --kill-after=2 12 \
    krun "$work/solution.mpy" \
      --definition "$definition" \
      "-cA=$a" \
      "-cB=$b" \
      --output pretty \
    | sed -n '/<k>/,/<\/k>/p; /<result>/,/<\/result>/p'
  statuses=("${PIPESTATUS[@]}")
  printf 'KRUN %s EXIT: %s (sed=%s)\n' "$case_id" "${statuses[0]}" "${statuses[1]}"
}

run_k_case example_float 'pyInt(1)' 'pyFloat(25,10)'
run_k_case example_comma 'pyInt(1)' 'pyStr("2,3")'
run_k_case example_strings 'pyStr("5,1")' 'pyStr("6")'
run_k_case example_equal 'pyStr("1")' 'pyInt(1)'
run_k_case zero_equal 'pyFloat(0,1)' 'pyStr("0,0")'
run_k_case negative_decimal 'pyStr("-0,5")' 'pyInt(0)'
run_k_case rational_equal 'pyFloat(1,10)' 'pyFloat(10,100)'
run_k_case binary64_int_rounding 'pyInt(9007199254740993)' 'pyInt(9007199254740992)'
run_k_case binary64_string_rounding 'pyStr("9007199254740993")' 'pyInt(9007199254740992)'

printf '%s\n' 'STAGE3_CONCRETE_NORMAL_AND_ROUNDING_CASES_COMPLETE'
