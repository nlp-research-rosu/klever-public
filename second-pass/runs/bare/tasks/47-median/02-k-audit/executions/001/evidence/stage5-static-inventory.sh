#!/usr/bin/env bash
set +e

record() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  return 0
}

record python3 /audit-output/evidence/inventory_k.py
record rg -n \
  'simplification|anywhere|priority|owise|opaque|trusted|functional|total|function' \
  /tmp/audit-work/47-median/candidate-src/semantic.k \
  /tmp/audit-work/47-median/candidate-src/verification.k
record nl -ba /tmp/audit-work/47-median/candidate-src/semantic.k
record nl -ba /tmp/audit-work/47-median/candidate-src/verification.k
