#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the submitted constructor program with the fixed translator.
python3 py2mpy.py solution.py > solution.mpy

# Compile the semantics and its exact solution-program wrapper for both krun
# and kprove.  The Haskell backend is the symbolic proof backend.
kompile verification.k \
  --backend haskell \
  --main-module ANY-INT-VERIFICATION \
  --syntax-module ANY-INT-VERIFICATION \
  -o verification-kompiled

# Prove that the constructor tree generated above is byte-for-byte equal after
# parsing/macro expansion to the tree used by all verification claims.
actual_program="$({
  kast -d verification-kompiled \
    -m ANY-INT-VERIFICATION -s Program \
    --expand-macros -o kore solution.mpy
})"
verified_program="$({
  kast -d verification-kompiled \
    -m ANY-INT-VERIFICATION -s Program \
    --expand-macros -o kore -e solutionProgram
})"
test "$actual_program" = "$verified_program"

run_case() {
  local term="$1"
  local expected="$2"
  local output
  output="$(krun -d verification-kompiled -cPGM="$term")"
  printf '%s\n' "$output"
  grep -Fq "boolVal ( $expected )" <<<"$output"
}

# Exercise every example in prompt.py through the K semantics.
run_case 'RunAnyInt(intVal(5), intVal(2), intVal(7))' true
run_case 'RunAnyInt(intVal(3), intVal(2), intVal(2))' false
run_case 'RunAnyInt(intVal(3), intVal(-2), intVal(1))' true
run_case 'RunAnyInt(floatVal(3.6), floatVal(-2.2), intVal(2))' false

# Prove all seven exhaustive symbolic claims in spec.k.  Success prints #Top.
kprove spec.k \
  -d verification-kompiled \
  --spec-module ANY-INT-SPEC
