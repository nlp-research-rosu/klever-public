#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log=$1
shift

: > "$log"
{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee -a "$log"

set -o pipefail
"$@" 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %s\n' "$status" | tee -a "$log"
exit "$status"
