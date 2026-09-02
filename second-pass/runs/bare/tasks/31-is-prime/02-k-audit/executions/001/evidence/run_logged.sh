#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

logfile=$1
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$logfile"

"$@" >>"$logfile" 2>&1
status=$?

printf 'EXIT_STATUS: %d\n' "$status" >>"$logfile"
exit "$status"
