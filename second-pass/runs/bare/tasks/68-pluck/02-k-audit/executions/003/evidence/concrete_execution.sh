#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/68-pluck-audit
definition="$scratch/concrete-audit-kompiled"
program="$scratch/solution.mpy"

run_case() {
  local label=$1
  local args=$2
  local expected=$3
  echo "\$ krun solution.mpy --definition concrete-audit-kompiled -cARGS='$args'"
  local output
  output=$(krun "$program" --definition "$definition" -cARGS="$args" 2>&1)
  local status=$?
  printf '%s\n' "$output"
  echo "$label krun exit=$status"
  if (( status != 0 )); then
    return "$status"
  fi
  grep -Fq "    $expected" <<<"$output"
  local check_status=$?
  echo "$label expected-result-check exit=$check_status expected=$expected"
  return "$check_status"
}

overall=0
run_case example-1 'VList(4, 2, 3)' 'VList ( 2 , 1 , .Ints )' || overall=1
run_case empty 'VList()' 'VList ( .Ints )' || overall=1
run_case single-even 'VList(0)' 'VList ( 0 , 0 , .Ints )' || overall=1
run_case single-odd 'VList(1)' 'VList ( .Ints )' || overall=1
run_case duplicate-minimum 'VList(4, 2, 2)' 'VList ( 2 , 1 , .Ints )' || overall=1
run_case minimum-at-end 'VList(8, 6, 4, 2)' 'VList ( 2 , 3 , .Ints )' || overall=1
run_case large-value 'VList(1000000000000, 3, 2)' 'VList ( 2 , 2 , .Ints )' || overall=1
echo "concrete execution aggregate exit=$overall"
exit "$overall"
