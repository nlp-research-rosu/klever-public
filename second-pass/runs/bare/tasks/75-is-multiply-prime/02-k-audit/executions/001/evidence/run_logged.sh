#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee "$log"

set +e
"$@" 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}
set -e

printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$log"
exit "$status"
