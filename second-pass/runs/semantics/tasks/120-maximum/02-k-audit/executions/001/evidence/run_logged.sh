#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOG_PATH COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKING_DIRECTORY: %s\n' "$PWD"
  printf '%s\n' 'OUTPUT_BEGIN'
} >"$log_path"

"$@" >>"$log_path" 2>&1
status=$?

{
  printf '%s\n' 'OUTPUT_END'
  printf 'EXIT_STATUS: %d\n' "$status"
} >>"$log_path"

exit "$status"
