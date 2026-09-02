#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit_status] %d\n' "$status"
  return "$status"
}

printf 'Audit stage 5: machine inventory supporting the exhaustive static review\n'
run rg -n '^\s*syntax ' /candidate/semantic.k /candidate/verification.k
run rg -n '^\s*rule ' /candidate/semantic.k /candidate/verification.k
run rg -n '\[(function|total|functional|simplification|concrete|owise|priority)' \
  /candidate/semantic.k /candidate/verification.k
run rg -c '^\s*rule ' /candidate/semantic.k /candidate/verification.k
run rg -n 'Module|FuncDef|If|Assign|Return|Int|Float|Name|Call|UnaryOp|BinOp|Compare|CmpOp' \
  /candidate/solution.mpy
