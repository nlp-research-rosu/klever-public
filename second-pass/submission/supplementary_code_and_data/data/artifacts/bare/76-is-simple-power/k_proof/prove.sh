#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

mkdir -p build

kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  -o build/semantic-kompiled

check_case() {
  local case_x="$1"
  local case_n="$2"
  local expected="$3"
  local run_output

  run_output="$(
    krun solution.mpy \
      -cX="$case_x" \
      -cN="$case_n" \
      --definition build/semantic-kompiled
  )"
  printf '%s\n' "$run_output"
  printf '%s\n' "$run_output" \
    | rg -q -U "<result>[[:space:]]*${expected}[[:space:]]*</result>"
}

check_case 1 4 true
check_case 2 2 true
check_case 8 2 true
check_case 3 2 false
check_case 3 1 false
check_case 5 3 false

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  -o build/verification-kompiled

kprove spec.k --definition build/verification-kompiled
