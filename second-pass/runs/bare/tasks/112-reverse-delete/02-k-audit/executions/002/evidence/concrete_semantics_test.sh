#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/112-reverse-delete
definition="$scratch/audit-semantic-llvm-kompiled"
program="$scratch/solution.mpy"
failures=0

run_case() {
  local label=$1
  local s_token=$2
  local c_token=$3
  local expected=$4
  local output
  local status

  set +e
  output=$(krun "$program" --definition "$definition" -cS="$s_token" -cC="$c_token" 2>&1)
  status=$?
  set -e
  printf '\nCASE %s\n' "$label"
  printf 'COMMAND: krun %q --definition %q -cS=%q -cC=%q\n' \
    "$program" "$definition" "$s_token" "$c_token"
  printf 'PYTHON-ORACLE: %s\n' "$expected"
  printf 'KRUN-EXIT: %d\n%s\n' "$status" "$output"
  if (( status != 0 )) || ! grep -Fq "$expected" <<<"$output"; then
    printf 'CASE-RESULT: MISMATCH\n'
    failures=$((failures + 1))
  else
    printf 'CASE-RESULT: MATCH\n'
  fi
}

run_case prompt-1 '"abcde"' '"ae"' \
  'tupleVal ( strVal ( "bcd" ) , boolVal ( false ) )'
run_case both-empty '""' '""' \
  'tupleVal ( strVal ( "" ) , boolVal ( true ) )'
run_case all-deleted '"aaaa"' '"a"' \
  'tupleVal ( strVal ( "" ) , boolVal ( true ) )'
run_case single-kept '"x"' '""' \
  'tupleVal ( strVal ( "x" ) , boolVal ( true ) )'
run_case mixed-branches '"abac"' '"a"' \
  'tupleVal ( strVal ( "bc" ) , boolVal ( false ) )'
run_case unicode-non-bmp '"😀a😀"' '"a"' \
  'tupleVal ( strVal ( "😀😀" ) , boolVal ( true ) )'
run_case unicode-shared-utf8-byte '"😀"' '"ð"' \
  'tupleVal ( strVal ( "\xf0\x9f\x98\x80" ) , boolVal ( true ) )'

printf '\nTOTAL-FAILURES: %d\n' "$failures"
exit "$failures"
