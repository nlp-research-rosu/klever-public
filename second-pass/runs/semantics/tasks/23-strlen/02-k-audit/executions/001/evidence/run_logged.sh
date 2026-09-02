#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

logfile=$1
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
} >"$logfile" 2>&1

exit "$status"
