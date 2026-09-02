#!/usr/bin/env bash
set -euo pipefail

# Recreate the translated constructor tree and the Haskell backend definition.
python3 py2mpy.py solution.py > solution.mpy
kompile semantic.k --backend haskell \
  --main-module SEMANTIC --syntax-module SEMANTIC-SYNTAX

# Sanity-check the Python implementation independently.
python3 - <<'PY'
from solution import fib4

expected = [0, 0, 2, 0, 2, 4, 8, 14, 28, 54, 104, 200]
assert [fib4(n) for n in range(len(expected))] == expected
PY

# Exercise all prompt examples through the K semantics and check their result.
run_and_check() {
  local n="$1"
  local expected="$2"
  local output
  output="$(krun solution.mpy -cARG="$n")"
  printf '%s\n' "$output"
  grep -Fq "result ( $expected )" <<<"$output"
}

run_and_check 5 4
run_and_check 6 8
run_and_check 7 14

# Prove every claim: the spec-model link, four base cases, symbolic
# initialization for n >= 4, the circular all-n loop invariant, and the
# prompt's fib4(7) example.
kprove spec.k --definition semantic-kompiled --spec-module SPEC
