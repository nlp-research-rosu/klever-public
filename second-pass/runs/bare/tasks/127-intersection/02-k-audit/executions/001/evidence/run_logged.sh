#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  printf 'usage: %s LOGFILE COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_file="$1"
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee "$log_file"

"$@" 2>&1 | tee -a "$log_file"
command_status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %d\n' "$command_status" | tee -a "$log_file"
exit "$command_status"
