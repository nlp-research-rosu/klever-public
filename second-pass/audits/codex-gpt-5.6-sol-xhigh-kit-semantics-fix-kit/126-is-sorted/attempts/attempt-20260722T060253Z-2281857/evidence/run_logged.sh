#!/usr/bin/env bash
set +e

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
} > "$log"

"$@" >> "$log" 2>&1
status=$?

printf 'EXIT_STATUS: %d\n' "$status" >> "$log"
exit "$status"
