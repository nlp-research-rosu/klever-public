#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

logfile=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
} >"$logfile"

"$@" >>"$logfile" 2>&1
status=$?

printf 'EXIT_STATUS: %d\n' "$status" >>"$logfile"
exit "$status"
