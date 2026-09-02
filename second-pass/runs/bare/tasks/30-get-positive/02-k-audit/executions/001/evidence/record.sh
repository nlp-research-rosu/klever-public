#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 64
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
