#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log"

set +e
"$@" 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}
set -e

printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$log"
exit "$status"
