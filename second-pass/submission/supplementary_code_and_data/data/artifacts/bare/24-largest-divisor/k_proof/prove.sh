#!/usr/bin/env bash
set -euo pipefail

# Recreate the translator artifact and both backends from source.
python3 py2mpy.py solution.py > solution.mpy
kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX

# Exercise both a composite input from the prompt and a prime input.  krun
# returns a final configuration even for a stuck program, so check the result
# cell as well as the process status.
check_krun() {
  local input_number="$1"
  local expected_result="$2"
  local run_output
  run_output="$(
    krun solution.mpy \
      -cARG="${input_number}" \
      --definition semantic-kompiled \
      --output pretty
  )"
  printf '%s\n' "${run_output}"
  if ! rg -Uq "<result>[[:space:]]+${expected_result}[[:space:]]+</result>" <<<"${run_output}"; then
    printf 'krun result check failed for n=%s (expected %s)\n' \
      "${input_number}" "${expected_result}" >&2
    return 1
  fi
}

check_krun 15 5
check_krun 101 1

# The Haskell backend symbolically proves every claim in spec.k.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty
