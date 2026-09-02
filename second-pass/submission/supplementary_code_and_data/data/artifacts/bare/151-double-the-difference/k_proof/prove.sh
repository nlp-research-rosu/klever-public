#!/usr/bin/env bash
set -euo pipefail

# Recreate the constructor program from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Compile the executable semantics used for concrete runs.
kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX

run_case() {
  local expected="$1"
  local input="$2"
  local output

  output="$(
    krun solution.mpy \
      --definition semantic-kompiled \
      -cINPUT="$input"
  )"
  printf '%s\n' "$output"
  printf '%s\n' "$output" | grep -Fq "pyInt ( $expected )"
}

# The four examples from prompt.py, followed by empty and mixed-value cases.
run_case 10 'pyList(intCons(1,intCons(3,intCons(2,intCons(0,nil)))))'
run_case 0  'pyList(intCons(-1,intCons(-2,intCons(0,nil))))'
run_case 81 'pyList(intCons(9,intCons(-2,nil)))'
run_case 0  'pyList(intCons(0,nil))'
run_case 0  'pyList(nil)'
run_case 10 'pyList(floatCons(1.5,boolCons(true,listCons(intCons(7,nil),intCons(3,nil)))))'

# Add the mathematical specification and its evaluator to the proof definition.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# This is the required positive target proof.  Success prints #Top and exits 0.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
