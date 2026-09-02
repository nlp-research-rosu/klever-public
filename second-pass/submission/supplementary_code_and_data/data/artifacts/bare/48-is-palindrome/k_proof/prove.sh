#!/usr/bin/env bash
set -euo pipefail

# Recreate the constructor term from the submitted Python implementation.
python3 py2mpy.py solution.py > solution.mpy

# VERIFICATION imports SEMANTIC, so this compiles both executable semantics and
# the mathematical palindrome predicate into the Haskell proof backend.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell

expect_krun() {
  local k_string="$1"
  local expected="$2"
  local output

  output="$(krun solution.mpy \
    --definition verification-kompiled \
    -cFUNCTION='"is_palindrome"' \
    -cARG="$k_string")"
  printf '%s\n' "$output"
  [[ "$output" == *"PyBool ( $expected )"* ]]
}

# The four examples in prompt.py.
expect_krun '""' true
expect_krun '"aba"' true
expect_krun '"aaaaa"' true
expect_krun '"zbcd"' false

# Sole positive target proof: universally quantified over S:String.
kprove spec.k --definition verification-kompiled
