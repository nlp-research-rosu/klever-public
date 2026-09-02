#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

logfile=$1
shift

{
  printf 'cwd: %q\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
  printf 'started_utc: %(%Y-%m-%dT%H:%M:%SZ)T\n' -1
} > "$logfile"

"$@" > >(tee -a "$logfile") 2> >(tee -a "$logfile" >&2)
status=$?

{
  printf '\nexit_status: %d\n' "$status"
  printf 'finished_utc: %(%Y-%m-%dT%H:%M:%SZ)T\n' -1
} >> "$logfile"

exit "$status"
