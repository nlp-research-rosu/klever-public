#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the exact translator artifact used by both execution and proof.
python3 py2mpy.py solution.py > solution.mpy

# verification.k imports semantic.k and the translated-program constant.
# kprove requires the Haskell backend in this K distribution.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# At depth one, both inputs have loaded their Module into the function map.
# Equality of the canonical KORE states ties solutionProgram to solution.mpy.
cmp \
  <(krun solution.mpy --definition verification-kompiled --depth 1 \
      -cARGS='intVal(0)' --output kore) \
  <(krun solution-token.mpy --definition verification-kompiled --depth 1 \
      -cARGS='intVal(0)' --output kore)

# Exercise all three examples from prompt.py with contract-typed K values.
example1="$(krun solution.mpy --definition verification-kompiled \
  -cARGS='gridVal(rowVal(0,0,1,0),rowVal(0,1,0,0),rowVal(1,1,1,1)),intVal(1)')"
printf '%s\n' "$example1"
grep -Fq 'intVal ( 6 )' <<< "$example1"

example2="$(krun solution.mpy --definition verification-kompiled \
  -cARGS='gridVal(rowVal(0,0,1,1),rowVal(0,0,0,0),rowVal(1,1,1,1),rowVal(0,1,1,1)),intVal(2)')"
printf '%s\n' "$example2"
grep -Fq 'intVal ( 5 )' <<< "$example2"

example3="$(krun solution.mpy --definition verification-kompiled \
  -cARGS='gridVal(rowVal(0,0,0),rowVal(0,0,0)),intVal(5)')"
printf '%s\n' "$example3"
grep -Fq 'intVal ( 0 )' <<< "$example3"

# This is the positive target-proof command.  It proves every claim in SPEC.
kprove spec.k --definition verification-kompiled --spec-module SPEC
