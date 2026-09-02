#!/usr/bin/env bash
set -euo pipefail
trap 'rc=$?; echo "EXIT_STATUS=$rc"' EXIT

definition=/tmp/audit-work/11-string-xor/build/semantic-kompiled
program=/tmp/audit-work/11-string-xor/source/solution.mpy

run_case() {
  local label=$1
  local args=$2
  local expected=$3
  local expected_k=$4
  local output

  echo "CASE=$label"
  echo "ARGS=$args"
  echo "PYTHON_EXPECTED=$expected"
  echo "COMMAND: krun $program --definition $definition -cARGS=$args --output pretty"
  output=$(krun "$program" --definition "$definition" -cARGS="$args" --output pretty)
  printf '%s\n' "$output"
  grep -F "$expected_k" <<<"$output" > /dev/null
  echo 'K_RESULT_MATCH=true'
}

echo 'COMMAND: bash /audit-output/evidence/03_concrete.sh'
run_case empty_empty \
  'Args(str(empty),str(empty))' \
  '' \
  'returned ( str ( empty ) )'
run_case empty_one \
  'Args(str(empty),str(cons(true,empty)))' \
  '' \
  'returned ( str ( empty ) )'
run_case one_empty \
  'Args(str(cons(true,empty)),str(empty))' \
  '' \
  'returned ( str ( empty ) )'
run_case zero_zero \
  'Args(str(cons(false,empty)),str(cons(false,empty)))' \
  '0' \
  'returned ( str ( cons ( false , empty ) ) )'
run_case one_one \
  'Args(str(cons(true,empty)),str(cons(true,empty)))' \
  '0' \
  'returned ( str ( cons ( false , empty ) ) )'
run_case zero_one \
  'Args(str(cons(false,empty)),str(cons(true,empty)))' \
  '1' \
  'returned ( str ( cons ( true , empty ) ) )'
run_case one_zero \
  'Args(str(cons(true,empty)),str(cons(false,empty)))' \
  '1' \
  'returned ( str ( cons ( true , empty ) ) )'
run_case documented \
  'Args(str(cons(false,cons(true,cons(false,empty)))),str(cons(true,cons(true,cons(false,empty)))))' \
  '100' \
  'returned ( str ( cons ( true , cons ( false , cons ( false , empty ) ) ) ) )'
run_case left_longer \
  'Args(str(cons(false,cons(true,cons(false,cons(true,empty))))),str(cons(true,cons(true,empty))))' \
  '10' \
  'returned ( str ( cons ( true , cons ( false , empty ) ) ) )'
run_case right_longer \
  'Args(str(cons(true,cons(true,empty))),str(cons(false,cons(true,cons(false,cons(true,empty))))))' \
  '10' \
  'returned ( str ( cons ( true , cons ( false , empty ) ) ) )'
run_case symbolic_segment_documented \
  'Args(str(segment(3,seed(2))),str(segment(3,seed(3))))' \
  '100' \
  'returned ( str ( cons ( true , cons ( false , cons ( false , empty ) ) ) ) )'
run_case symbolic_segment_unequal \
  'Args(str(segment(4,seed(10))),str(segment(2,seed(3))))' \
  '10' \
  'returned ( str ( cons ( true , cons ( false , empty ) ) ) )'
