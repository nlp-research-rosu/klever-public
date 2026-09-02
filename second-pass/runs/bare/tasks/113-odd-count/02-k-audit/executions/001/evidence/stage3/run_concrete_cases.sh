#!/usr/bin/env bash
set -u

definition=/tmp/audit-work/build/semantic-kompiled
program=/tmp/audit-work/source/solution.mpy
evidence=/audit-output/evidence/stage3

run_case() {
  local name=$1
  local input=$2
  local log="$evidence/krun-$name.log"
  {
    printf '$ krun %q --definition %q --output pretty -cINPUT=%q\n' \
      "$program" "$definition" "$input"
    krun "$program" \
      --definition "$definition" \
      --output pretty \
      -cINPUT="$input"
    status=$?
    echo "exit: $status"
    return "$status"
  } >"$log" 2>&1
}

run_case empty-list \
  'pyList(noValues)'
run_case empty-string \
  'pyList(value(pyString(inputDigits(noDigits)), noValues))'
run_case prompt-one \
  'pyList(value(pyString(inputDigits(digit(oddDigit, digit(evenDigit, digit(oddDigit, digit(evenDigit, digit(oddDigit, digit(evenDigit, digit(oddDigit, noDigits))))))))), noValues))'
run_case parity-boundaries \
  'pyList(value(pyString(inputDigits(digit(evenDigit, digit(evenDigit, digit(evenDigit, digit(evenDigit, digit(evenDigit, noDigits))))))), value(pyString(inputDigits(digit(oddDigit, digit(oddDigit, digit(oddDigit, digit(oddDigit, digit(oddDigit, noDigits))))))), noValues)))'
