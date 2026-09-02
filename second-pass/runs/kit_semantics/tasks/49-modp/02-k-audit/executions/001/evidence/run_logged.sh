#!/usr/bin/env bash

set +e

if (( $# < 2 )); then
  echo "usage: $0 LOG_PATH COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
} >"$log_path" 2>&1

exit "$status"
