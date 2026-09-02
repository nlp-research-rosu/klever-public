#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy
kompile semantic.k \
  --backend haskell \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX

run_case() {
  local input="$1"
  local expected="$2"
  local result

  result="$(krun solution.mpy -cINPUT="$input" --output pretty)"
  grep -Fq "pyBool ( $expected )" <<<"$result"
  printf 'krun %-48s => %s\n' "$input" "$expected"
}

# The five prompt examples, followed by two distinct-position edge cases.
run_case '1 :: 3 :: 5 :: 0 :: .ISeq' false
run_case '1 :: 3 :: -2 :: 1 :: .ISeq' false
run_case '1 :: 2 :: 3 :: 7 :: .ISeq' false
run_case '2 :: 4 :: -5 :: 3 :: 5 :: 7 :: .ISeq' true
run_case '1 :: .ISeq' false
run_case '0 :: 0 :: .ISeq' true
run_case '0 :: .ISeq' false

# This is the required positive target proof.  Success prints #Top.
kprove spec.k --definition semantic-kompiled --spec-module SPEC
