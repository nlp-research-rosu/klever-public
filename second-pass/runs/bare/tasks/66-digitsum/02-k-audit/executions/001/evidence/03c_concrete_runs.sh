#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run_case() {
  input=$1
  expected_candidate=$2
  config_arg="-cINPUT=\"$input\""
  printf '$ krun solution.mpy --definition audit-concrete-llvm-kompiled %q --output pretty\n' "$config_arg"
  output=$(krun solution.mpy \
    --definition audit-concrete-llvm-kompiled \
    "$config_arg" \
    --output pretty)
  status=$?
  printf '%s\n' "$output"
  printf '[exit %d]\n' "$status"
  actual=$(printf '%s\n' "$output" \
    | rg -o 'intVal \( -?[0-9]+ \)' \
    | rg -o -- '-?[0-9]+' \
    | head -1)
  if [[ "$actual" == "$expected_candidate" ]]; then
    printf 'COMPARE candidate_python=%s k_result=%s MATCH\n' \
      "$expected_candidate" "$actual"
  else
    printf 'COMPARE candidate_python=%s k_result=%s MISMATCH\n' \
      "$expected_candidate" "${actual:-<missing>}"
  fi
}

cd /tmp/audit-work/reconstruction || exit 125
run python3 /audit-output/evidence/concrete_case_oracles.py
run_case "" 0
run_case "abAB" 131
run_case "abcCd" 67
run_case "helloE" 69
run_case "woArBld" 131
run_case "aAaaaXa" 153
run_case "@" 0
run_case "A" 65
run_case "Z" 90
run_case "[" 0
run_case '`' 0
run_case "a" 0
run_case "A@Z[" 155
run_case "É" 0
run_case "Ω" 0
run_case "𐐀" 0
run_case "aÉZΩ" 90
