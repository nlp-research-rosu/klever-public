#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/160-do-algebra/candidate
definition=/tmp/audit-work/160-do-algebra/concrete-kompiled
overall=0

run_normal() {
  local name="$1"
  local ops="$2"
  local operands="$3"
  local expected="$4"
  local output
  local status
  printf 'CASE: %s expected_python=%s\n' "$name" "$expected"
  printf 'COMMAND: krun solution.mpy --definition %q -cOPS=%q -cOPERANDS=%q\n' \
    "$definition" "$ops" "$operands"
  output="$(krun solution.mpy --definition "$definition" -cOPS="$ops" -cOPERANDS="$operands" 2>&1)"
  status=$?
  printf '%s\n' "$output"
  printf 'EXIT: %d\n' "$status"
  if [[ "$status" -ne 0 ]] || ! grep -Fq "answer ( $expected )" <<<"$output"; then
    overall=1
  fi
}

cd "$work" || exit 125

run_normal \
  prompt-example \
  'ops(Op("+", Op("*", Op("-", .Ops))))' \
  'ints(Num(2, Num(3, Num(4, Num(5, .Ints)))))' \
  9
run_normal \
  minimum-subtraction \
  'ops(Op("-", .Ops))' \
  'ints(Num(0, Num(1, .Ints)))' \
  -1
run_normal \
  zero-to-zero-power \
  'ops(Op("**", .Ops))' \
  'ints(Num(0, Num(0, .Ints)))' \
  1
run_normal \
  right-associative-power \
  'ops(Op("**", Op("**", .Ops)))' \
  'ints(Num(2, Num(3, Num(2, .Ints))))' \
  512
run_normal \
  left-associative-floor \
  'ops(Op("//", Op("//", .Ops)))' \
  'ints(Num(20, Num(3, Num(2, .Ints))))' \
  3

printf 'CASE: division-by-zero expected_python=ZeroDivisionError\n'
printf 'COMMAND: krun solution.mpy --definition %q -cOPS=%q -cOPERANDS=%q\n' \
  "$definition" 'ops(Op("//", .Ops))' 'ints(Num(1, Num(0, .Ints)))'
division_output="$(
  krun solution.mpy --definition "$definition" \
    -cOPS='ops(Op("//", .Ops))' \
    -cOPERANDS='ints(Num(1, Num(0, .Ints)))' 2>&1
)"
division_status=$?
printf '%s\n' "$division_output"
printf 'EXIT: %d\n' "$division_status"
if [[ "$division_status" -eq 0 ]] || ! grep -Fq 'parseMul' <<<"$division_output"; then
  overall=1
fi

printf 'COMMAND: python3 /audit-output/evidence/differential_test.py\n'
python3 /audit-output/evidence/differential_test.py
python_status=$?
printf 'EXIT: %d\n' "$python_status"
if [[ "$python_status" -ne 0 ]]; then
  overall=1
fi

exit "$overall"
