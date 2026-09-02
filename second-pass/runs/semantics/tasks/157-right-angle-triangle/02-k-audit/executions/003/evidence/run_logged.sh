#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

logfile="$1"
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$logfile"

"$@" >> "$logfile" 2>&1
status=$?

printf 'EXIT STATUS: %d\n' "$status" >> "$logfile"
exit "$status"
