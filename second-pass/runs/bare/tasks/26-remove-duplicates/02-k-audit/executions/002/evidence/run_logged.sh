#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift

: > "$log"
{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee -a "$log"

"$@" 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$log"
exit "$status"
