#!/usr/bin/env bash
set -u

log_file=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee "$log_file"

"$@" 2>&1 | tee -a "$log_file"
command_status=${PIPESTATUS[0]}

printf 'EXIT_STATUS: %s\n' "$command_status" | tee -a "$log_file"
exit "$command_status"
