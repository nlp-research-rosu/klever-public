#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run nl -ba /candidate/semantic.k
run nl -ba /candidate/verification.k
run nl -ba /candidate/spec.k
run nl -ba /candidate/solution.mpy
run nl -ba /candidate/solution.py
run rg -n \
  'syntax|rule|claim|configuration|\[(function|total|functional|simplification|priority|anywhere|macro|opaque|concrete)' \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k
