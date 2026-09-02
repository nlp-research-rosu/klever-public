#!/usr/bin/env bash
set -euo pipefail

definition=${1:?LLVM definition path is required}
program=${2:?solution.mpy path is required}

run_case() {
  local label=$1
  local k_input=$2
  local json_input=$3
  local expected=$4
  local k_output

  printf 'CASE: %s\n' "$label"
  printf 'COMMAND: krun %q --definition %q -cINPUT=%q\n' \
    "$program" "$definition" "$k_input"
  k_output=$(krun "$program" --definition "$definition" -cINPUT="$k_input")
  printf '%s\n' "$k_output"
  printf 'COMMAND: %q %q\n' \
    /audit-output/evidence/concrete_case_oracle.py "$json_input"
  /audit-output/evidence/concrete_case_oracle.py "$json_input"
  if ! grep -Fq "bVal ( $expected )" <<< "$k_output"; then
    printf 'ERROR: expected bVal ( %s )\n' "$expected" >&2
    return 1
  fi
  printf 'EXPECTED K RESULT: %s\n' "$expected"
}

run_case empty '.IList' '[]' true
run_case singleton '7 :: .IList' '[7]' true
run_case sorted '1 :: 2 :: 3 :: .IList' '[1,2,3]' true
run_case one_drop_rotation '3 :: 1 :: 2 :: .IList' '[3,1,2]' true
run_case two_drops '2 :: 1 :: 3 :: .IList' '[2,1,3]' false
run_case documented_true '3 :: 4 :: 5 :: 1 :: 2 :: .IList' '[3,4,5,1,2]' true
run_case documented_false '3 :: 5 :: 4 :: 1 :: 2 :: .IList' '[3,5,4,1,2]' false
run_case negative_boundary '-3 :: -1 :: 2 :: -10 :: .IList' '[-3,-1,2,-10]' true
