#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: run-evidence.sh LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log"

"$@" > >(tee -a "$log") 2> >(tee -a "$log" >&2)
status=$?
printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$log"
exit "$status"
