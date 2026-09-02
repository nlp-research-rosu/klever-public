#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: run-capture.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_file="$1"
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_file"

set +e
"$@" >> "$log_file" 2>&1
command_status=$?
set -e

printf '\nEXIT_STATUS: %d\n' "$command_status" >> "$log_file"
cat "$log_file"
exit "$command_status"
