#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
} >"$log" 2>&1

exit "$status"
