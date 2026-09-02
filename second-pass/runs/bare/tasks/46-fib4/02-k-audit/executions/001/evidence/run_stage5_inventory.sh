#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/46-fib4

printf 'AUDIT STAGE 5: numbered source and mechanical declaration inventory\n'
run sha256sum \
  "$scratch/solution.py" \
  "$scratch/solution.mpy" \
  "$scratch/semantic.k" \
  "$scratch/verification.k" \
  "$scratch/spec.k"
run nl -ba "$scratch/solution.mpy"
run nl -ba "$scratch/semantic.k"
run nl -ba "$scratch/verification.k"
run nl -ba "$scratch/spec.k"
run rg -n \
  '^[[:space:]]*(requires|module|imports|syntax|configuration|rule|claim)|\[(function|total|functional|simplification|concrete|priority|owise|circularity)' \
  "$scratch/semantic.k" "$scratch/verification.k" "$scratch/spec.k"
