#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 2
fi

logfile=$1
shift

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$logfile"

"$@" >> "$logfile" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status" >> "$logfile"
exit "$status"
