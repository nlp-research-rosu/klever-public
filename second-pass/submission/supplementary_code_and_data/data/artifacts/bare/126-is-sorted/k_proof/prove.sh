#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
kompile semantic.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX

run_expect() {
  local list_value="$1"
  local expected_bool="$2"
  local actual_output
  actual_output="$(krun solution.mpy --definition semantic-kompiled -cARGS="$list_value")"
  printf '%s\n' "$actual_output"
  printf '%s\n' "$actual_output" | rg -q "BoolVal \\( $expected_bool \\)"
}

# The eight examples in prompt.py, plus the empty-list boundary case.
run_expect 'PyList(Cons(5, Nil))' true
run_expect 'PyList(Cons(1, Cons(2, Cons(3, Cons(4, Cons(5, Nil))))))' true
run_expect 'PyList(Cons(1, Cons(3, Cons(2, Cons(4, Cons(5, Nil))))))' false
run_expect 'PyList(Cons(1, Cons(2, Cons(3, Cons(4, Cons(5, Cons(6, Nil)))))))' true
run_expect 'PyList(Cons(1, Cons(2, Cons(3, Cons(4, Cons(5, Cons(6, Cons(7, Nil))))))))' true
run_expect 'PyList(Cons(1, Cons(3, Cons(2, Cons(4, Cons(5, Cons(6, Cons(7, Nil))))))))' false
run_expect 'PyList(Cons(1, Cons(2, Cons(2, Cons(3, Cons(3, Cons(4, Nil)))))))' true
run_expect 'PyList(Cons(1, Cons(2, Cons(2, Cons(2, Cons(3, Cons(4, Nil)))))))' false
run_expect 'PyList(Nil)' true

# Required positive target: this must print #Top and exit zero.
kprove spec.k --definition semantic-kompiled --spec-module SPEC

# Negative validation: weakening <= 2 to <= 3 must be rejected on [2, 2, 2].
if kprove mutation-spec.k --definition semantic-kompiled --spec-module MUTATION-SPEC; then
  printf '%s\n' 'error: the expected-failure mutation was incorrectly proved' >&2
  exit 1
fi
