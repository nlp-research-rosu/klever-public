#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG_FILE COMMAND [ARG ...]" >&2
  exit 2
fi

log_file=$1
shift

{
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf '[exit_status] %d\n' "$command_status"
  exit "$command_status"
} 2>&1 | tee "$log_file"

exit "${PIPESTATUS[0]}"
