#!/usr/bin/env bash
set -u

log_file=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
} >"$log_file" 2>&1

exit "$status"
