#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
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

set +e
"$@" >> "$log" 2>&1
status=$?
set -e

printf 'EXIT_STATUS: %d\n' "$status" >> "$log"
sed -n '1,400p' "$log"
exit "$status"
