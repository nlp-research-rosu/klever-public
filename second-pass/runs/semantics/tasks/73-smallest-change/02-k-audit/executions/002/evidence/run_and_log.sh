#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: run_and_log.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf 'EXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
} 2>&1 | tee "$log_path"

exit "${PIPESTATUS[0]}"
