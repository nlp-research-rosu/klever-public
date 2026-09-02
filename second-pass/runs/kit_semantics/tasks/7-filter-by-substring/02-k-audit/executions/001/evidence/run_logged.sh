#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG_FILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_file"

set +e
"$@" >> "$log_file" 2>&1
status=$?
set -e

printf '\nEXIT_STATUS: %d\n' "$status" >> "$log_file"
exit "$status"
