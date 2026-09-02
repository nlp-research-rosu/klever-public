#!/usr/bin/env bash
set -o pipefail

if [[ $# -lt 2 ]]; then
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

"$@" > >(tee -a "$logfile") 2> >(tee -a "$logfile" >&2)
status=$?
printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$logfile"
exit "$status"
