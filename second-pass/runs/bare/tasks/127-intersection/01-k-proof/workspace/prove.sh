#!/usr/bin/env bash
set -euo pipefail

# Regenerate the constructor term with the fixed front-end.
python3 py2mpy.py solution.py > solution.mpy

# Build the executable semantics and exercise all examples from prompt.py.
kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition semantic-kompiled

run_and_expect() {
  local interval1="$1"
  local interval2="$2"
  local expected="$3"
  local output

  output="$(krun solution.mpy \
    --definition semantic-kompiled \
    -cINTERVAL1="$interval1" \
    -cINTERVAL2="$interval2" \
    --output pretty)"
  printf '%s\n' "$output"
  grep -Fq "strVal ( \"$expected\" )" <<<"$output"
}

run_and_expect 'TupleExpr(Int(1),Int(2))' \
               'TupleExpr(Int(2),Int(3))' 'NO'
run_and_expect 'TupleExpr(Int(-1),Int(1))' \
               'TupleExpr(Int(0),Int(4))' 'NO'
run_and_expect 'TupleExpr(Int(-3),Int(-1))' \
               'TupleExpr(Int(-5),Int(5))' 'YES'

# First prove the inductive trial-division loop lemma without assuming it.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition loop-kompiled
kprove spec.k \
  --definition loop-kompiled \
  --spec-module LOOP-CORRECTNESS-SPEC \
  --output pretty

# Then use that proved lemma to prove the four exhaustive interval-order cases.
kompile verification.k \
  --main-module VERIFICATION-WITH-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty
