#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  printf 'usage: %s LOGFILE COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

logfile=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$logfile"

"$@" >>"$logfile" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status" >>"$logfile"
exit "$status"
