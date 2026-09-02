#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

logfile=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$logfile"

set +e
"$@" >> "$logfile" 2>&1
status=$?
set -e

printf 'EXIT_STATUS: %d\n' "$status" >> "$logfile"
printf '%s\n' "$status"
exit "$status"
