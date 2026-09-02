#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/candidate-clean
definition="$scratch/audit-semantic-kompiled"
program="$scratch/solution.mpy"

run_case() {
  local label=$1
  local python_list=$2
  local k_args=$3

  printf 'CASE: %s\n' "$label"
  printf 'PYTHON_COMMAND: solution.skjkasdkd(%s)\n' "$python_list"
  (
    cd "$scratch" || exit 1
    python3 - "$python_list" <<'PY'
import ast
import sys
import solution

values = ast.literal_eval(sys.argv[1])
print(f"PYTHON_RESULT: {solution.skjkasdkd(values)}")
PY
  )
  local python_status=$?
  printf 'PYTHON_EXIT_STATUS: %d\n' "$python_status"

  printf 'KRUN_COMMAND: krun %q --definition %q -cARGS=%q\n' \
    "$program" "$definition" "$k_args"
  krun "$program" --definition "$definition" -cARGS="$k_args"
  local krun_status=$?
  printf 'KRUN_EXIT_STATUS: %d\n\n' "$krun_status"

  if (( python_status != 0 || krun_status != 0 )); then
    return 1
  fi
}

run_case empty '[]' 'listVal()' || exit $?
run_case one_not_prime '[1]' 'listVal(intVal(1))' || exit $?
run_case smallest_prime '[2]' 'listVal(intVal(2))' || exit $?
run_case composites_only '[4, 6, 8, 9]' \
  'listVal(intVal(4), intVal(6), intVal(8), intVal(9))' || exit $?
run_case negative_and_prime '[-3, 11]' \
  'listVal(intVal(-3), intVal(11))' || exit $?
run_case repeated_primes '[7, 7]' \
  'listVal(intVal(7), intVal(7))' || exit $?
run_case prompt_boundary '[0, 8, 1, 2, 1, 7]' \
  'listVal(intVal(0), intVal(8), intVal(1), intVal(2), intVal(1), intVal(7))' || exit $?
run_case multi_digit_prime '[181, 32, 109]' \
  'listVal(intVal(181), intVal(32), intVal(109))' || exit $?
run_case larger_prime '[104729]' \
  'listVal(intVal(104729))' || exit $?
