#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: capture.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift

{
  printf 'UTC: '
  date -u '+%Y-%m-%dT%H:%M:%SZ'
  printf 'CWD: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log"

set +e
"$@" >> "$log" 2>&1
status=$?
set -e

printf 'EXIT_STATUS: %d\n' "$status" >> "$log"
exit "$status"
