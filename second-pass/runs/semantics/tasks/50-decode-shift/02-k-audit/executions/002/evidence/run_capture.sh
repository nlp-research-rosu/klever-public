#!/usr/bin/env bash
set -o pipefail

if (( $# < 2 )); then
  echo "usage: run_capture.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log"

"$@" >>"$log" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status" >>"$log"
exit "$status"
