#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/candidate-fresh
definition="${CONCRETE_DEFINITION:-$work/concrete-kompiled}"
program="$work/solution.mpy"

run_case() {
  local label="$1"
  local args_term="$2"
  local py_args="$3"

  printf '\nCASE: %s\n' "$label"
  printf 'PYTHON_ARGS: %s\n' "$py_args"
  PYTHONPATH="$work:/tmp/audit-work/reference" python3 -c \
    "import ast, canonical, solution; a=ast.literal_eval('$py_args'); print('canonical=', canonical.triangle_area(*a)); print('generated=', solution.triangle_area(*a))"
  printf 'COMMAND: krun %q -cARGS=%q --definition %q --output pretty\n' \
    "$program" "$args_term" "$definition"
  krun "$program" -cARGS="$args_term" --definition "$definition" --output pretty
  local status=$?
  printf 'KRUN_EXIT_STATUS: %s\n' "$status"
}

run_case valid_example 'Args(VInt(3), VInt(4), VInt(5))' '(3,4,5)'
run_case invalid_first_guard 'Args(VInt(1), VInt(2), VInt(10))' '(1,2,10)'
run_case invalid_second_guard 'Args(VInt(2), VInt(5), VInt(3))' '(2,5,3)'
run_case invalid_third_guard 'Args(VInt(5), VInt(2), VInt(3))' '(5,2,3)'
run_case zero_boundary 'Args(VInt(0), VInt(0), VInt(0))' '(0,0,0)'
run_case just_valid_integer 'Args(VInt(2), VInt(2), VInt(1))' '(2,2,1)'
run_case irrational_area 'Args(VInt(2), VInt(2), VInt(2))' '(2,2,2)'
run_case negative_length 'Args(VInt(-1), VInt(2), VInt(2))' '(-1,2,2)'
run_case valid_float_sides 'Args(VFloat(3.0), VFloat(4.0), VFloat(5.0))' '(3.0,4.0,5.0)'

exit 0
