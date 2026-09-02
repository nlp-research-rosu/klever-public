#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_file"

"$@" >> "$log_file" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status" >> "$log_file"
exit "$status"
