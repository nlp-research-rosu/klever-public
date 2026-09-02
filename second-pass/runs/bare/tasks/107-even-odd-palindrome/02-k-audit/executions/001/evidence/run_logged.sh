#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf '%s\n' '--- OUTPUT ---'
} >"$log_path"

"$@" >>"$log_path" 2>&1
status=$?

{
  printf '%s\n' '--- END OUTPUT ---'
  printf 'EXIT_STATUS: %d\n' "$status"
} >>"$log_path"

exit "$status"
