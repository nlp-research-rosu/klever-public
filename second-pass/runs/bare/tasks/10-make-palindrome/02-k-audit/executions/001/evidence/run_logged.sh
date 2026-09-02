#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log=$1
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf 'EXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
} 2>&1 | tee "$log"

exit "${PIPESTATUS[0]}"
