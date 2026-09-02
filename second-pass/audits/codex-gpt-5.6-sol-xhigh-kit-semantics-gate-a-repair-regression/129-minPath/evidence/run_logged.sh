#!/usr/bin/env bash
set +e

if (( $# < 2 )); then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'CWD: %q\n' "$PWD"
  "$@"
  command_status=$?
  printf '\nEXIT_STATUS: %d\n' "$command_status"
} >"$log_file" 2>&1

exit "$command_status"
