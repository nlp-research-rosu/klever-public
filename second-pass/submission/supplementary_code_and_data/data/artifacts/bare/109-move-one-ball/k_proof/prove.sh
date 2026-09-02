#!/usr/bin/env bash
set -euo pipefail

# Recreate the exact constructor input consumed by the K definition.
python3 py2mpy.py solution.py > solution.mpy

# LLVM-backed concrete executions.
kompile semantic.k \
  --backend llvm \
  --main-module HUMAN-EVAL \
  --syntax-module HUMAN-EVAL-SYNTAX \
  --output-definition semantic-llvm-kompiled

run_case() {
  local input=$1
  local expected=$2
  local output
  output=$(krun solution.mpy \
    --definition semantic-llvm-kompiled \
    -cINPUT="$input")
  printf '%s\n' "$output"
  grep -Fq "bVal ( $expected )" <<<"$output"
}

run_case '.IList' true
run_case '3 :: 4 :: 5 :: 1 :: 2 :: .IList' true
run_case '3 :: 5 :: 4 :: 1 :: 2 :: .IList' false
run_case '2 :: 1 :: 3 :: .IList' false

# Haskell-backed symbolic proof. This proves every claim in spec.k.
kompile semantic.k \
  --backend haskell \
  --main-module HUMAN-EVAL \
  --syntax-module HUMAN-EVAL-SYNTAX \
  --output-definition semantic-haskell-kompiled

kprove spec.k \
  --definition semantic-haskell-kompiled \
  --spec-module HUMAN-EVAL-SPEC
