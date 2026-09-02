#!/usr/bin/env bash
set -euo pipefail

# Recreate the constructor program with the fixed supplied translator.
python3 py2mpy.py solution.py > solution.mpy

# Compile and concretely execute the handwritten operational semantics.
kompile semantic.k --backend haskell \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX

run_case() {
  local a="$1"
  local b="$2"
  local expected="$3"
  local actual
  actual="$(
    krun solution.mpy -cA="$a" -cB="$b" \
      --definition semantic-kompiled \
      | sed -n '/<result>/{n;s/ //gp;}'
  )"
  test "$actual" = "$expected"
  printf 'krun multiply(%s, %s) = %s\n' "$a" "$b" "$actual"
}

run_case 148 412 16
run_case 19 28 72
run_case 2020 1851 0
run_case 14 -15 20
run_case -14 15 20
run_case -14 -15 20

# Compile the proof extension and prove its universal all-integers claim.
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX
kprove spec.k --definition verification-kompiled --spec-module SPEC \
  | tee kprove.out
grep -qx '#Top' kprove.out
