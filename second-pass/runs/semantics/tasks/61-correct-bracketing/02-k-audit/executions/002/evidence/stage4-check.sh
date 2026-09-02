#!/usr/bin/env bash
set -u

cd /tmp/audit-work/proof || exit 90

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  return "$status"
}

run rg -n '^[[:space:]]*claim|\[label\(' spec.k || exit $?
run python3 /audit-output/evidence/pinning_and_witnesses.py || exit $?
