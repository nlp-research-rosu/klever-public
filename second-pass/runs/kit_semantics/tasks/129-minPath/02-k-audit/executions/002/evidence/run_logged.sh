#!/usr/bin/env bash
set -o pipefail

if (( $# < 2 )); then
  echo "usage: run_logged.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf 'EXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
} >"$log_file" 2>&1
