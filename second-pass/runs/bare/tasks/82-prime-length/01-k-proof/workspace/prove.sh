#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Rebuild the translator output from the implementation.
python3 py2mpy.py solution.py > solution.mpy

# Compile the operational semantics and exercise both prompt examples and
# boundary cases.  Each run is checked against the expected final K value.
kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX

check_krun() {
  local arg="$1"
  local expected="$2"
  local output
  output="$(krun solution.mpy --definition semantic-kompiled -cARG="$arg")"
  printf '%s\n' "$output"
  if ! grep -Fq "VBool ( $expected )" <<<"$output"; then
    printf 'krun result mismatch for %s (expected %s)\n' "$arg" "$expected" >&2
    return 1
  fi
}

check_krun 'VStr("Hello")' true
check_krun 'VStr("abcdcba")' true
check_krun 'VStr("kittens")' true
check_krun 'VStr("orange")' false
check_krun 'VStr("")' false
check_krun 'VStr("a")' false
check_krun 'VStr("ab")' true
check_krun 'VStr("abc")' true
check_krun 'VStr("abcdefgh")' false

# Compile the contract predicate with the semantics, then prove the single
# symbolic claim in spec.k.  That claim quantifies over every K String.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# Confirm that the exact translated file and the program proved in spec.k are
# the same term after parsing and macro expansion.
kast solution.mpy \
  --definition verification-kompiled \
  --expand-macros \
  --output kore > solution.kore
kast \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Program \
  --expression solutionProgram \
  --expand-macros \
  --output kore > specified-solution.kore
cmp solution.kore specified-solution.kore

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
