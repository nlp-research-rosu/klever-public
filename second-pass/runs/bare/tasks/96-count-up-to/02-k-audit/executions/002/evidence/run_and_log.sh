#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee "$log"

"$@" 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$log"
exit "$status"
