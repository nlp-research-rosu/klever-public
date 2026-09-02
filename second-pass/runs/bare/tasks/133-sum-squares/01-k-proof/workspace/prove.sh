#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --backend llvm \
  --syntax-module MPY-SYNTAX \
  --main-module MPY

run_case() {
  local expected="$1"
  local args="$2"
  local output
  local k_cell

  output="$(krun solution.mpy --definition semantic-kompiled -cARGS="$args")"
  printf '%s\n' "$output"
  k_cell="$(printf '%s\n' "$output" | sed -n '/<k>/,/<\/k>/p' | tr -d '[:space:]')"
  test "$k_cell" = "<k>intVal($expected)~>.K</k>"
}

run_case 14 'listVal(cons(intVal(1), cons(intVal(2), cons(intVal(3), nil))))'
run_case 98 'listVal(cons(intVal(1), cons(intVal(4), cons(intVal(9), nil))))'
run_case 84 'listVal(cons(intVal(1), cons(intVal(3), cons(intVal(5), cons(intVal(7), nil)))))'
run_case 29 'listVal(cons(ratVal(14, ten), cons(ratVal(42, ten), cons(intVal(0), nil))))'
run_case 6 'listVal(cons(ratVal(-24, ten), cons(intVal(1), cons(intVal(1), nil))))'

kompile verification.k \
  --backend haskell \
  --syntax-module MPY-SYNTAX \
  --main-module VERIFICATION

proof_output="$(kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC)"
printf '%s\n' "$proof_output"
test "$(printf '%s\n' "$proof_output" | tr -d '[:space:]')" = '#Top'
