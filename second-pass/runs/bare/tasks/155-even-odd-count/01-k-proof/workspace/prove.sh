#!/usr/bin/env bash
set -euo pipefail

# Recreate the constructor term using the fixed supplied translator.
python3 py2mpy.py solution.py > solution.mpy

# The enriched definition imports the operational semantics and the independent
# recursive digit-count model used by the proof.
kompile definition.k \
  --backend haskell \
  --main-module DEFINITION \
  --syntax-module MPY-SYNTAX

check_case() {
  local input="$1"
  local expected_pair="$2"
  local output
  output="$(krun solution.mpy --definition definition-kompiled -cNUM="$input")"
  printf '%s\n' "$output"
  grep -Fq "$expected_pair" <<<"$output"
}

# Prompt examples, the zero boundary, and larger positive/negative executions.
check_case -12 'pairVal ( intVal ( 1 ) , intVal ( 1 ) )'
check_case 123 'pairVal ( intVal ( 1 ) , intVal ( 2 ) )'
check_case 0 'pairVal ( intVal ( 0 ) , intVal ( 0 ) )'
check_case -78 'pairVal ( intVal ( 1 ) , intVal ( 1 ) )'
check_case 346211 'pairVal ( intVal ( 3 ) , intVal ( 3 ) )'

# Proves both the generalized loop invariant and the end-to-end all-Int claim.
kprove spec.k \
  --definition definition-kompiled \
  --spec-module SPEC \
  --output pretty
