#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  printf 'usage: %s LOGFILE COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_file="$1"
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_file"

"$@" > >(tee -a "$log_file") 2> >(tee -a "$log_file" >&2)
status=$?

printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$log_file"
exit "$status"
