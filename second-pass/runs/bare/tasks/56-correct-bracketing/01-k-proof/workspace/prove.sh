#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recheck that the committed constructor tree is exactly the translator output.
generated_mpy="$(mktemp ./solution-regenerated.XXXXXX.mpy)"
trap 'rm -f "$generated_mpy"' EXIT
python3 py2mpy.py solution.py > "$generated_mpy"
cmp solution.mpy "$generated_mpy"

# Compile the executable definition and exercise normal completion, empty
# input, nested input, and early rejection through the real solution.mpy term.
kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition llvm-kompiled

run_case() {
  local input="$1"
  local expected="$2"
  local output
  output="$(krun solution.mpy --definition llvm-kompiled -cINPUT="$input")"
  grep -Fq "result ( BVal ( $expected ) )" <<< "$output"
}

run_case '""' true
run_case '"<"' false
run_case '"<>"' true
run_case '"<<><>>"' true
run_case '"><<>"' false

# Compile the symbolic definition and prove every claim in spec.k.  Success is
# reported by kprove as #Top and a zero exit status.
kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition haskell-kompiled

kprove spec.k \
  --definition haskell-kompiled \
  --spec-module SPEC
