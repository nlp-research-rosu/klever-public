#!/usr/bin/env bash
set -euo pipefail

# Recreate the translated program from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Compile the semantics together with its mathematical verification helpers.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# Exercise the translated term under the K semantics.  The comparison strips
# only layout whitespace from the isolated <result> cell.
check_case() {
  local n="$1"
  local expected="$2"
  local actual
  actual="$(
    krun solution.mpy --definition verification-kompiled -cN="$n" \
      | sed -n '/<result>/,/<\/result>/p' \
      | tr -d '[:space:]'
  )"
  test "$actual" = "<result>Bool($expected)</result>"
  printf 'krun is_prime(%s) = %s\n' "$n" "$expected"
}

check_case 6 false
check_case 101 true
check_case 11 true
check_case 13441 true
check_case 61 true
check_case 4 false
check_case 1 false
check_case 2 true
check_case 49 false

# This single positive target command proves every claim in SPEC.  Capture and
# check stdout as well as relying on kprove's exit status.
proof_output="$(
  kprove \
    --definition verification-kompiled \
    --spec-module SPEC \
    spec.k
)"
printf '%s\n' "$proof_output"
test "$proof_output" = "#Top"
