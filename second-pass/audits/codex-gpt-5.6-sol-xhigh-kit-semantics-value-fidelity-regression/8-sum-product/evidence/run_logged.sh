#!/usr/bin/env bash
set -uo pipefail

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
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$logfile"

"$@" > >(tee -a "$logfile") 2> >(tee -a "$logfile" >&2)
status=$?

{
  printf '\nEXIT_STATUS: %d\n' "$status"
  printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$logfile"

exit "$status"
