#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: run-logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'OUTPUT-BEGIN\n'
  "$@" 2>&1
  command_status=$?
  printf 'OUTPUT-END\n'
  printf 'EXIT-STATUS: %d\n' "$command_status"
  exit "$command_status"
} | tee "$log_file"

exit "${PIPESTATUS[0]}"
