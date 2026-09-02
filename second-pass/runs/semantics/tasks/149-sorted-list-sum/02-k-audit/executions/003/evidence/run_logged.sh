#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  printf 'usage: %s LABEL COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

label=$1
shift
log="/audit-output/evidence/${label}.log"

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  exit "$status"
} 2>&1 | tee "$log"

exit "${PIPESTATUS[0]}"
