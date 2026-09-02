#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --backend haskell \
  --syntax-module FIBFIB-SYNTAX \
  --main-module FIBFIB

run_case() {
  local n="$1"
  local expected="$2"
  local output
  local actual

  output="$(krun solution.mpy -cN="$n")"
  actual="$(printf '%s\n' "$output" | sed -n '/<result>/ { n; s/[[:space:]]//g; p; }')"
  printf 'krun fibfib(%s) => %s\n' "$n" "$actual"
  test "$actual" = "$expected"
}

run_case 0 0
run_case 1 0
run_case 2 1
run_case 5 4
run_case 8 24
run_case 10 81

proof_output="$(
  kprove spec.k \
    --definition semantic-kompiled \
    --spec-module FIBFIB-SPEC \
    -w none
)"
printf '%s\n' "$proof_output"
printf '%s\n' "$proof_output" | grep -qx '#Top'
