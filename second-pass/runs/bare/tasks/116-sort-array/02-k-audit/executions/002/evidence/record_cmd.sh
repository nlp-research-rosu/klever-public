#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: record_cmd.sh LOG COMMAND [ARG ...]" >&2
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
  printf '\nEXIT_STATUS: %d\n' "$command_status"
} >"$log_path" 2>&1

exit "$command_status"
