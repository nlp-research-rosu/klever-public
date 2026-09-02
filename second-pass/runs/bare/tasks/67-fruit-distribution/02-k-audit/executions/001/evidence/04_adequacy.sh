#!/usr/bin/env bash
set -u

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

run python3 /audit-output/evidence/04_adequacy_witnesses.py
run krun example-abstract.mpy \
  --definition audit-verification-kompiled \
  --output pretty
run krun example-concrete-1.mpy \
  --definition audit-verification-kompiled \
  --output pretty
run cmp --silent source.kast alias.kast
